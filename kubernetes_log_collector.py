#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Define a constant for the log rotation size (e.g., 10MB)
LOG_ROTATION_BYTES = 10 * 1024 * 1024
LOG_BACKUP_COUNT = 5

class KubernetesLogCollector:
    """
    A class to collect logs from specified pods in a Kubernetes namespace.
    """

    def __init__(self, **kwargs):
        """
        Initializes the log collector with configuration from command-line arguments.
        """
        self.namespace = kwargs.get('namespace')
        self.selector = kwargs.get('selector')
        self.output_dir = Path(kwargs.get('output_dir'))
        self.kubeconfig = kwargs.get('kubeconfig')
        self.container = kwargs.get('container')
        self.since = kwargs.get('since')
        self.tail = kwargs.get('tail')
        self.follow = kwargs.get('follow')
        self.previous = kwargs.get('previous')
        self.api_client = None
        self.core_v1_api = None
        self.active_handlers =

    def _setup_kubernetes_client(self):
        """
        Sets up the Kubernetes API client, trying in-cluster config first,
        then falling back to kubeconfig.
        """
        try:
            config.load_incluster_config()
            print("INFO: Authenticated using in-cluster service account.")
        except config.ConfigException:
            try:
                config.load_kube_config(config_file=self.kubeconfig)
                print("INFO: Authenticated using kubeconfig file.")
            except config.ConfigException as e:
                print(f"ERROR: Could not authenticate with Kubernetes. {e}", file=sys.stderr)
                sys.exit(1)
        
        self.api_client = client.ApiClient()
        self.core_v1_api = client.CoreV1Api(self.api_client)

    def _validate_cluster_connection(self):
        """
        Performs a lightweight API call to validate the connection to the cluster.
        """
        try:
            self.core_v1_api.get_api_resources()
            print("INFO: Successfully connected to the Kubernetes API server.")
        except ApiException as e:
            print(f"ERROR: Failed to connect to Kubernetes API server. Status: {e.status}, Reason: {e.reason}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: An unexpected error occurred while validating cluster connection: {e}", file=sys.stderr)
            sys.exit(1)

    def _validate_output_directory(self):
        """
        Validates that the output directory exists and is writable.
        Attempts to create it if it does not exist.
        """
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            # Test writability by creating a temporary file
            test_file = self.output_dir / ".k8slogtest"
            test_file.touch()
            test_file.unlink()
            print(f"INFO: Output directory '{self.output_dir}' is valid and writable.")
        except OSError as e:
            print(f"ERROR: Output directory '{self.output_dir}' is not writable or could not be created: {e}", file=sys.stderr)
            sys.exit(1)

    def _find_target_pods(self):
        """
        Finds pods matching the label selector in the specified namespace.
        Validates that the namespace exists and that at least one pod is found.
        """
        try:
            # 1. Check if namespace exists
            self.core_v1_api.read_namespace(name=self.namespace)
        except ApiException as e:
            if e.status == 404:
                print(f"ERROR: Namespace '{self.namespace}' not found.", file=sys.stderr)
            else:
                print(f"ERROR: Could not access namespace '{self.namespace}'. Status: {e.status}, Reason: {e.reason}", file=sys.stderr)
            sys.exit(1)

        try:
            # 2. Find pods by label selector
            pod_list = self.core_v1_api.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=self.selector
            )
            if not pod_list.items:
                print(f"INFO: No pods found matching selector '{self.selector}' in namespace '{self.namespace}'. Exiting.")
                sys.exit(0)
            
            print(f"INFO: Found {len(pod_list.items)} pod(s) matching selector '{self.selector}'.")
            return pod_list.items
        except ApiException as e:
            print(f"ERROR: Could not list pods. Status: {e.status}, Reason: {e.reason}", file=sys.stderr)
            sys.exit(1)
            
    def _get_output_path(self, pod_name, container_name, is_previous=False):
        """
        Constructs the full, timestamped path for a log file.
        """
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        suffix = "_previous" if is_previous else ""
        filename = f"{container_name}{suffix}_{timestamp}.log"
        
        path = self.output_dir / self.namespace / pod_name
        path.mkdir(parents=True, exist_ok=True)
        return path / filename

    def _fetch_and_store_logs(self, pod, container):
        """
        Fetches logs for a single container and stores them.
        Handles both batch and streaming modes.
        """
        pod_name = pod.metadata.name
        container_name = container.name

        print(f"INFO: Processing container '{container_name}' in pod '{pod_name}'...")

        if self.follow:
            self._stream_logs_with_rotation(pod_name, container_name)
        else:
            self._batch_fetch_logs(pod_name, container_name)
            if self.previous:
                self._batch_fetch_logs(pod_name, container_name, is_previous=True)

    def _batch_fetch_logs(self, pod_name, container_name, is_previous=False):
        """
        Performs a one-time fetch of logs for a container.
        """
        output_path = self._get_output_path(pod_name, container_name, is_previous)
        log_type = "previous" if is_previous else "current"
        
        try:
            logs = self.core_v1_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.namespace,
                container=container_name,
                previous=is_previous,
                since_seconds=self._parse_since(),
                tail_lines=self.tail,
                _preload_content=True  # Batch mode, load all content
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(logs)
            print(f"  -> Saved {log_type} logs to '{output_path}'")
        except ApiException as e:
            if is_previous and e.status == 400:
                # This is expected if a container has never restarted.
                print(f"  -> INFO: No previous container instance found for '{container_name}'.")
            else:
                print(f"  -> ERROR: Failed to fetch {log_type} logs for '{container_name}'. Status: {e.status}, Reason: {e.reason}", file=sys.stderr)

    def _stream_logs_with_rotation(self, pod_name, container_name):
        """
        Streams logs in real-time and uses RotatingFileHandler for storage.
        """
        output_path = self._get_output_path(pod_name, container_name)
        
        # Setup a dedicated logger for this stream
        logger_name = f"k8s.{self.namespace}.{pod_name}.{container_name}"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        # Prevent propagation to root logger to avoid duplicate console output
        logger.propagate = False
        
        # Use RotatingFileHandler for automatic rotation by size
        handler = RotatingFileHandler(
            output_path,
            maxBytes=LOG_ROTATION_BYTES,
            backupCount=LOG_BACKUP_COUNT
        )
        # Use a simple formatter that just outputs the message
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        self.active_handlers.append(handler)
        
        print(f"  -> Streaming logs to '{output_path}' (rotation at {LOG_ROTATION_BYTES / 1024**2:.1f} MB)...")
        
        try:
            log_stream = self.core_v1_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.namespace,
                container=container_name,
                follow=True,
                tail_lines=self.tail,
                _preload_content=False  # Crucial for streaming
            )
            
            for line in log_stream.stream():
                logger.info(line.decode('utf-8').strip())
        
        except ApiException as e:
            print(f"  -> ERROR: API error while streaming logs for '{container_name}'. Status: {e.status}, Reason: {e.reason}", file=sys.stderr)
        finally:
            log_stream.release_conn()

    def _parse_since(self):
        """
        Converts a time duration string (e.g., 1h, 10m, 30s) to seconds.
        Returns None if self.since is not set.
        """
        if not self.since:
            return None
        
        total_seconds = 0
        self.since = self.since.lower()
        
        if 'h' in self.since:
            total_seconds += int(self.since.split('h')) * 3600
        if 'm' in self.since:
            total_seconds += int(self.since.split('m').split('h')[-1]) * 60
        if 's' in self.since:
            total_seconds += int(self.since.split('s').split('m')[-1])
            
        return total_seconds if total_seconds > 0 else None

    def run(self):
        """
        Main execution method to orchestrate the log collection process.
        """
        try:
            self._validate_output_directory()
            self._setup_kubernetes_client()
            self._validate_cluster_connection()
            
            target_pods = self._find_target_pods()
            
            for pod in target_pods:
                containers = pod.spec.containers
                if self.container:
                    # Filter for the specified container
                    containers = [c for c in containers if c.name == self.container]
                    if not containers:
                        print(f"WARNING: Container '{self.container}' not found in pod '{pod.metadata.name}'. Skipping pod.", file=sys.stderr)
                        continue
                
                for container in containers:
                    self._fetch_and_store_logs(pod, container)
            
            if self.follow:
                print("\nINFO: Streaming logs. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1) # Keep the main thread alive while streams run

        except KeyboardInterrupt:
            print("\nINFO: Shutdown signal received, cleaning up...")
        finally:
            print("INFO: Closing all open file handlers and connections.")
            for handler in self.active_handlers:
                handler.close()
            if self.api_client:
                self.api_client.close()
            sys.exit(0)

def main():
    """
    Parses command-line arguments and runs the log collector.
    """
    parser = argparse.ArgumentParser(
        description="A robust script to collect logs from Kubernetes pods."
    )
    
    # Required arguments
    parser.add_argument('--namespace', required=True, help="The Kubernetes namespace to operate in.")
    parser.add_argument('--selector', required=True, help="Kubernetes label selector (e.g., 'app=my-api,env=production').")
    parser.add_argument('--output-dir', required=True, help="The local or shared directory to store log files.")
    
    # Optional arguments
    parser.add_argument('--kubeconfig', help="Path to the Kubernetes configuration file. Defaults to standard locations.")
    parser.add_argument('--container', help="Specify a single container name to collect logs from. If omitted, collects from all containers.")
    parser.add_argument('--since', help="A time duration string (e.g., 1h, 10m, 30s) to fetch logs from the recent past.")
    parser.add_argument('--tail', type=int, help="Fetch only the last N lines of logs.")
    
    # Boolean flags
    parser.add_argument('--follow', action='store_true', help="Stream logs in real-time until manually terminated.")
    parser.add_argument('--previous', action='store_true', help="Collect logs from previously terminated containers (due to crashes or restarts).")
    
    args = parser.parse_args()
    
    collector = KubernetesLogCollector(**vars(args))
    collector.run()

if __name__ == "__main__":
    main()
