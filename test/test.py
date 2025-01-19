import unittest
from unittest.mock import patch, MagicMock
import src.main as main  # Import the main module
import matplotlib.pyplot as plt

class TestMain(unittest.TestCase):
    @patch('src.main.generate_dataset')
    @patch('src.main.LoginChecker')
    @patch('src.main.run_experiment')
    def test_main_runs_experiments_and_generates_plots(self, mock_run_experiment, mock_login_checker, mock_generate_dataset):
        """
        Test that main() runs experiments for different dataset sizes and search types,
        and that it generates the plots correctly.
        """
        # Mock the dataset and LoginChecker
        mock_dataset = [1, 2, 3]
        mock_generate_dataset.return_value = mock_dataset
        mock_login_checker_instance = MagicMock()
        mock_login_checker.return_value = mock_login_checker_instance

        # Mock the run_experiment function to return a fixed time
        mock_run_experiment.return_value = 0.1

        # Call the main function (it will use the mocked objects)
        main.main()

        # Assert that generate_dataset was called with the correct dataset sizes
        expected_dataset_sizes = [1000, 5000, 10000, 50000, 100000]
        for size in expected_dataset_sizes:
            mock_generate_dataset.assert_any_call(size)

        # Assert that LoginChecker was called with the correct arguments
        for size in expected_dataset_sizes:
            mock_login_checker.assert_any_call(dataset=mock_dataset, capacity=size, error_rate=0.01)

        # Assert that run_experiment was called the correct number of times
        expected_search_types = ['linear', 'binary', 'hash', 'bloom', 'cuckoo']
        self.assertEqual(mock_run_experiment.call_count, len(expected_dataset_sizes) * len(expected_search_types))

        # Assert that run_experiment was called with the correct arguments
        for search_type in expected_search_types:
            for size in expected_dataset_sizes:
                mock_run_experiment.assert_any_call(mock_login_checker_instance, mock_dataset, 1000, search_type)

    @patch('src.main.plt')
    def test_main_generates_plots(self, mock_plt):
        """
        Test that main() generates the plots correctly (using mocking).
        """
        # Configure mock dataset and results (replace with your actual expected data)
        mock_dataset_sizes = [1000, 5000]
        mock_results = {
            'linear': [0.1, 0.2],
            'binary': [0.01, 0.02],
            'hash': [0.001, 0.002],
            'bloom': [0.005, 0.006],
            'cuckoo': [0.002, 0.003],
        }

        # Mock the necessary functions to return the configured data
        with patch('src.main.generate_dataset', return_value=[]), \
             patch('src.main.LoginChecker', return_value=MagicMock()), \
             patch('src.main.run_experiment', side_effect=[0.1, 0.2, 0.01, 0.02, 0.001, 0.002, 0.005, 0.006, 0.002, 0.003]):

            # Run the main function
            main.main()

            # Assert that the plot functions were called correctly
            self.assertEqual(mock_plt.figure.call_count, 6)  # 1 combined plot + 5 individual plots
            self.assertEqual(mock_plt.plot.call_count, 10)  # 5 individual plots + 5 lines on combined plot
            self.assertEqual(mock_plt.xlabel.call_count, 6)
            self.assertEqual(mock_plt.ylabel.call_count, 6)
            self.assertEqual(mock_plt.title.call_count, 6)
            self.assertEqual(mock_plt.legend.call_count, 6)
            self.assertEqual(mock_plt.grid.call_count, 6)
            self.assertEqual(mock_plt.savefig.call_count, 6)  # 5 individual + 1 combined
            self.assertEqual(mock_plt.close.call_count, 5)  # Close individual plots
            mock_plt.show.assert_called_once()

            # Assert that savefig was called with the correct filenames
            mock_plt.savefig.assert_any_call("linear_runtime.png")
            mock_plt.savefig.assert_any_call("binary_runtime.png")
            mock_plt.savefig.assert_any_call("hash_runtime.png")
            mock_plt.savefig.assert_any_call("bloom_runtime.png")
            mock_plt.savefig.assert_any_call("cuckoo_runtime.png")
            mock_plt.savefig.assert_any_call("combined_runtime_comparison.png")

if __name__ == '__main__':
    unittest.main()