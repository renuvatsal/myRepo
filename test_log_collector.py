import unittest
import os
import shutil
import sys
from unittest.mock import patch, MagicMock, mock_open, call
from kubernetes.client.rest import ApiException

# Add the directory of log_collector.py to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from log_collector import KubernetesLogCollector

class MockV1Pod:
    """A mock V1Pod object for testing."""
    def __init__(self, name, containers):
        self.metadata = MagicMock()
        self.metadata.name = name
        self.spec = MagicMock()
        self.spec.containers = [self._create_container(c) for c in containers]

    def _create_container(self, name):
        container = MagicMock()
        container.name = name
        return container

class MockV1PodList:
    """A mock V1PodList object for testing."""
    def __init__(self, pods):
        self.items = pods

class TestKubernetesLogCollector(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory for test outputs."""
        self.test_output_dir = "temp_test_logs"
        # Start with a clean directory
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        self.mock_pods = [
            MockV1Pod("pod-alpha-123", ["frontend", "redis"]),
            MockV1Pod("pod-beta-456", ["backend"])
        ]

    def tearDown(self):
        """Clean up the temporary directory after tests."""
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

    @patch('log_collector.client')
    @patch('log_collector.config')
    def test_batch_collection_all_containers(self, mock_k8s_config, mock_k8s_client):
        """
        Test batch log collection for all containers in found pods.
        """
        # --- Mock Kubernetes API ---
        mock_core_v1_api = MagicMock()
        mock_k8s_client.CoreV1Api.return_value = mock_core_v1_api
        mock_core_v1_api.list_namespaced_pod.return_value = MockV1PodList(self.mock_pods)
        
        # Mock log reading to return a simple string for batch mode
        mock_core_v1_api.read_namespaced_pod_log.return_value = "This is a log line.\n"

        # --- Run the collector ---
        collector = KubernetesLogCollector(
            kubeconfig=None, namespace="test-ns", selector="app=test",
            output_dir=self.test_output_dir, container=None,
            since=None, tail=None, follow=False, previous=False
        )
        collector.run()

        # --- Assertions ---
        # Verify it tried to fetch logs for all 3 containers
        self.assertEqual(mock_core_v1_api.read_namespaced_pod_log.call_count, 3)
        
        # Check that log files were created
        pod1_dir = os.path.join(self.test_output_dir, "test-ns", "pod-alpha-123")
        pod2_dir = os.path.join(self.test_output_dir, "test-ns", "pod-beta-456")
        
        self.assertTrue(os.path.isdir(pod1_dir))
        self.assertTrue(os.path.isdir(pod2_dir))
        
        # Check that 2 files were created for pod1 and 1 for pod2
        self.assertEqual(len(os.listdir(pod1_dir)), 2)
        self.assertEqual(len(os.listdir(pod2_dir)), 1)


    @patch('log_collector.client')
    @patch('log_collector.config')
    def test_previous_flag_collection(self, mock_k8s_config, mock_k8s_client):
        """
        Test that --previous flag correctly fetches current and previous logs.
        """
        mock_core_v1_api = MagicMock()
        mock_k8s_client.CoreV1Api.return_value = mock_core_v1_api
        mock_core_v1_api.list_namespaced_pod.return_value = MockV1PodList([self.mock_pods[0]]) # Just one pod

        # Simulate getting current logs, then previous logs
        def log_side_effect(*args, **kwargs):
            if kwargs.get('previous'):
                return "This is a PREVIOUS log line.\n"
            return "This is a CURRENT log line.\n"
        
        mock_core_v1_api.read_namespaced_pod_log.side_effect = log_side_effect

        collector = KubernetesLogCollector(
            kubeconfig=None, namespace="test-ns", selector="app=test",
            output_dir=self.test_output_dir, container="frontend",
            since=None, tail=None, follow=False, previous=True
        )
        collector.run()

        # --- Assertions ---
        # Called once for current, once for previous
        self.assertEqual(mock_core_v1_api.read_namespaced_pod_log.call_count, 2)
        
        pod_dir = os.path.join(self.test_output_dir, "test-ns", "pod-alpha-123")
        files = os.listdir(pod_dir)
        self.assertEqual(len(files), 2) # One current, one previous

        has_current = any("frontend_" in f and "previous" not in f for f in files)
        has_previous = any("frontend_previous_" in f for f in files)
        self.assertTrue(has_current)
        self.assertTrue(has_previous)

    @patch('log_collector.threading.Thread') # Mock threads to run sequentially
    @patch('log_collector.client')
    @patch('log_collector.config')
    def test_streaming_collection(self, mock_k8s_config, mock_k8s_client, mock_thread):
        """
        Test streaming log collection.
        """
        # --- Mock Kubernetes API for streaming ---
        mock_core_v1_api = MagicMock()
        mock_k8s_client.CoreV1Api.return_value = mock_core_v1_api
        mock_core_v1_api.list_namespaced_pod.return_value = MockV1PodList([self.mock_pods[1]]) # Just backend pod

        # For streaming, the client returns an iterable of byte strings
        mock_stream = MagicMock()
        mock_stream.__iter__.return_value = [b'Streaming line 1\n', b'Streaming line 2\n']
        mock_core_v1_api.read_namespaced_pod_log.return_value = mock_stream
        
        # Make threads run the target function immediately instead of in parallel
        def run_thread_sequentially(target, args):
            target(*args)
            return MagicMock() # Return a mock thread object
        mock_thread.side_effect = run_thread_sequentially

        collector = KubernetesLogCollector(
            kubeconfig=None, namespace="test-ns", selector="app=test",
            output_dir=self.test_output_dir, container=None,
            since=None, tail=None, follow=True, previous=False
        )
        collector.run()

        # --- Assertions ---
        mock_core_v1_api.read_namespaced_pod_log.assert_called_once()
        
        pod_dir = os.path.join(self.test_output_dir, "test-ns", "pod-beta-456")
        files = os.listdir(pod_dir)
        self.assertEqual(len(files), 1)

        with open(os.path.join(pod_dir, files[0]), 'r') as f:
            content = f.read()
            self.assertEqual(content, "Streaming line 1\nStreaming line 2\n")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
