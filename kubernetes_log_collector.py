import sys
import getopt
import os
import time
import signal
import threading
from datetime import datetime
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class KubernetesLogCollector:
    """
    Collects logs from specified pods in a Kubernetes namespace.
    """
    def __init__(self, kubeconfig, namespace, selector, output_dir, container, since, tail, follow, previous):
        """
        Initializes the KubernetesLogCollector.
        """
        self.kubeconfig = kubeconfig
        self.namespace = namespace
        self.selector = selector
        self.output_dir = output_dir
        self.target_container = container
        self.since_seconds = self._parse_since(since) if since else None
        self.tail_lines = tail
        self.follow = follow
        self.previous = previous
        self.api_client = self._get_api_client()
        self.core_v1 = client.CoreV1Api(self.api_client)
        self.active_handlers = {}
        # Use a lock for thread-safe access to active_handlers
        self.handler_lock = threading.Lock()
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _parse_since(self, since_str):
        """Converts a duration string (e.g., 10s, 5m, 1h) to seconds."""
        try:
            val = int(since_str[:-1])
            unit = since_str[-1].lower()
            if unit == 's':
                return val
            elif unit == 'm':
                return val * 60
            elif unit == 'h':
                return val * 3600
            else:
                print(f"Error: Invalid time unit in --since '{since_str}'. Use 's', 'm', or 'h'.", file=sys.stderr)
                sys.exit(1)
        except (ValueError, IndexError):
            print(f"Error: Invalid format for --since '{since_str}'. Use format like '10s', '5m', '1h'.", file=sys.stderr)
            sys.exit(1)

    def _get_api_client(self):
        """Initializes and returns a Kubernetes API client."""
        try:
            if self.kubeconfig:
                config.load_kube_config(config_file=self.kubeconfig)
            else:
                config.load_kube_config()
            return client.ApiClient()
        except config.ConfigException as e:
            print(f"Error: Could not configure Kubernetes client. {e}", file=sys.stderr)
            sys.exit(1)

    def _validate_inputs(self):
        """Validates inputs and environment."""
        print("1. Validating inputs...")
        try:
            self.core_v1.read_namespace(name=self.namespace)
            print(f"   - Namespace '{self.namespace}' found.")
        except ApiException as e:
            if e.status == 404:
                print(f"Error: Namespace '{self.namespace}' not found.", file=sys.stderr)
            else:
                print(f"Error connecting to Kubernetes API: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir, exist_ok=True)
            if not os.access(self.output_dir, os.W_OK):
                print(f"Error: Output directory '{self.output_dir}' is not writable.", file=sys.stderr)
                sys.exit(1)
            print(f"   - Output directory '{self.output_dir}' is valid and writable.")
        except OSError as e:
            print(f"Error creating or accessing output directory '{self.output_dir}': {e}", file=sys.stderr)
            sys.exit(1)
        print("   - Validation successful.")

    def _find_pods(self):
        """Finds pods based on the label selector."""
        print(f"\n2. Searching for pods with selector '{self.selector}' in namespace '{self.namespace}'...")
        try:
            pods = self.core_v1.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=self.selector
            )
            if not pods.items:
                print("   - No pods found matching the selector. Exiting gracefully.")
                sys.exit(0)
            print(f"   - Found {len(pods.items)} pod(s).")
            return pods.items
        except ApiException as e:
            print(f"Error fetching pods: {e}", file=sys.stderr)
            sys.exit(1)

    def _get_output_path(self, pod_name, container_name, is_previous=False):
        """Creates the directory structure and returns the full log file path."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        suffix = "_previous" if is_previous else ""
        filename = f"{container_name}{suffix}_{timestamp}.log"
        log_dir = os.path.join(self.output_dir, self.namespace, pod_name)
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, filename)

    def _batch_fetch_logs(self, pod_name, container_name, is_previous=False):
        """Performs a one-time fetch of logs for a container."""
        log_file_path = self._get_output_path(pod_name, container_name, is_previous)
        log_type = "previous" if is_previous else "current"
        print(f"   - Fetching {log_type} logs for {pod_name}/{container_name}...")

        try:
            logs_str = self.core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.namespace,
                container=container_name,
                previous=is_previous,
                since_seconds=self.since_seconds,
                tail_lines=self.tail_lines,
                _preload_content=True  # For batch, get content as a string
            )
            with open(log_file_path, 'w', encoding='utf-8') as f:
                f.write(logs_str)
            print(f"     - Saved to {log_file_path}")
        except ApiException as e:
            if is_previous and e.status == 400:
                print(f"     - INFO: No previous container instance found for '{container_name}'. Skipping.")
            else:
                print(f"     - ERROR fetching logs for {pod_name}/{container_name}: {e.reason}", file=sys.stderr)
        except Exception as e:
            print(f"     - An unexpected error occurred for {pod_name}/{container_name}: {e}", file=sys.stderr)

    def _stream_logs(self, pod_name, container_name):
        """Streams logs in real-time for a single container."""
        log_file_path = self._get_output_path(pod_name, container_name)
        print(f"   - Streaming logs for {pod_name}/{container_name} to {log_file_path}...")
        log_stream = None
        try:
            log_stream = self.core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.namespace,
                container=container_name,
                follow=True,
                since_seconds=self.since_seconds,
                tail_lines=self.tail_lines,
                _preload_content=False  # Must be False for streaming
            )
            with open(log_file_path, 'w', encoding='utf-8') as f:
                with self.handler_lock:
                    self.active_handlers[log_file_path] = f
                
                for line in log_stream:
                    f.write(line.decode('utf-8', errors='ignore'))
                    f.flush()

        except ApiException as e:
            print(f"   - ERROR streaming logs for {pod_name}/{container_name}: {e.reason}", file=sys.stderr)
        except Exception as e:
            # This can happen if the thread is interrupted during shutdown
            if not isinstance(e, KeyboardInterrupt):
                print(f"   - An unexpected error occurred while streaming {pod_name}/{container_name}: {e}", file=sys.stderr)
        finally:
            with self.handler_lock:
                if log_file_path in self.active_handlers:
                    self.active_handlers[log_file_path].close()
                    del self.active_handlers[log_file_path]
            if log_stream:
                log_stream.release_conn()
            print(f"   - Stream ended for {pod_name}/{container_name}.")

    def _handle_shutdown(self, signum, frame):
        """Gracefully shuts down on SIGINT/SIGTERM."""
        print("\nShutdown signal received. Closing all log files...")
        with self.handler_lock:
            for path, handler in self.active_handlers.items():
                print(f"   - Closing {path}")
                handler.close()
            self.active_handlers.clear()
        print("Shutdown complete.")
        sys.exit(0)

    def run(self):
        """Main execution method."""
        self._validate_inputs()
        pods = self._find_pods()
        threads = []

        print("\n3. Starting log collection...")
        for pod in pods:
            pod_name = pod.metadata.name
            print(f"\nProcessing pod: {pod_name}")
            
            containers_to_process = pod.spec.containers
            if self.target_container:
                filtered_containers = [c for c in containers_to_process if c.name == self.target_container]
                if not filtered_containers:
                    print(f"   - Warning: Specified container '{self.target_container}' not found in pod '{pod_name}'. Skipping.")
                    continue
                containers_to_process = filtered_containers
            
            for container in containers_to_process:
                if self.follow:
                    if self.previous:
                        print("   - Warning: --previous flag is ignored when --follow is used.")
                    thread = threading.Thread(target=self._stream_logs, args=(pod_name, container.name))
                    threads.append(thread)
                    thread.start()
                else:
                    self._batch_fetch_logs(pod_name, container.name, is_previous=False)
                    if self.previous:
                        self._batch_fetch_logs(pod_name, container.name, is_previous=True)
        
        if self.follow:
            print("\nAll log streams started. Press Ctrl+C to stop.")
            try:
                for t in threads:
                    t.join()
            except KeyboardInterrupt:
                self._handle_shutdown(None, None)

        print("\nLog collection process finished.")

def parse_args(argv):
    """Parses command-line arguments using getopt."""
    kubeconfig = None
    namespace = None
    selector = None
    output_dir = None
    container = None
    since = None
    tail = None
    follow = False
    previous = False

    short_opts = "n:s:o:c:"
    long_opts = [
        "kubeconfig=", "namespace=", "selector=", "output-dir=", 
        "container=", "since=", "tail=", "follow", "previous"
    ]
    
    help_str = (
        "Usage: python log_collector.py --namespace <ns> --selector <sel> --output-dir <dir> [options]\n\n"
        "Required:\n"
        "  --namespace/-n   Kubernetes namespace\n"
        "  --selector/-s    Label selector (e.g., 'app=my-api')\n"
        "  --output-dir/-o  Output directory for logs\n\n"
        "Optional:\n"
        "  --kubeconfig     Path to kubeconfig file (defaults to standard locations)\n"
        "  --container/-c   Specific container name to collect from\n"
        "  --since          Fetch logs since a duration (e.g., 10s, 5m, 1h)\n"
        "  --tail           Fetch the last N lines of logs\n"
        "  --follow         Stream logs in real-time\n"
        "  --previous       Fetch logs from previous, terminated containers\n"
    )

    try:
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError as e:
        print(f"Argument Error: {e}\n\n{help_str}", file=sys.stderr)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--kubeconfig':
            kubeconfig = arg
        elif opt in ("-n", "--namespace"):
            namespace = arg
        elif opt in ("-s", "--selector"):
            selector = arg
        elif opt in ("-o", "--output-dir"):
            output_dir = arg
        elif opt in ("-c", "--container"):
            container = arg
        elif opt == '--since':
            since = arg
        elif opt == '--tail':
            try:
                tail = int(arg)
            except ValueError:
                print("Error: --tail argument must be an integer.", file=sys.stderr)
                sys.exit(2)
        elif opt == '--follow':
            follow = True
        elif opt == '--previous':
            previous = True

    if not all([namespace, selector, output_dir]):
        print(f"Missing one or more required arguments.\n\n{help_str}", file=sys.stderr)
        sys.exit(2)

    return kubeconfig, namespace, selector, output_dir, container, since, tail, follow, previous

if __name__ == "__main__":
    try:
        kubeconfig, namespace, selector, output_dir, container, since, tail, follow, previous = parse_args(sys.argv[1:])
        collector = KubernetesLogCollector(
            kubeconfig=kubeconfig,
            namespace=namespace,
            selector=selector,
            output_dir=output_dir,
            container=container,
            since=since,
            tail=tail,
            follow=follow,
            previous=previous
        )
        collector.run()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")
        sys.exit(0)
