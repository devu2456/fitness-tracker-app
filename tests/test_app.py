import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
import datetime

# Patch tkinter before importing your app
with patch.dict("sys.modules", {
    "tkinter": MagicMock(),
    "tkinter.ttk": MagicMock(),
    "tkinter.messagebox": MagicMock(),
    "tkinter.simpledialog": MagicMock(),
}):
    from src.app import FitnessTrackerApp


class TestFitnessTracker(unittest.TestCase):
    def setUp(self):
        # root is now just a MagicMock, no real window created
        self.root = MagicMock()
        self.app = FitnessTrackerApp(self.root)
        self.app.workout_entry.get = MagicMock()
        self.app.duration_entry.get = MagicMock()
        self.app.category_var.get = MagicMock()
        self.app.date_entry.get = MagicMock()
        self.app.workout_entry.delete = MagicMock()
        self.app.duration_entry.delete = MagicMock()
        self.app.date_entry.delete = MagicMock()
        self.app.date_entry.insert = MagicMock()
        self.app.data_file = "test_workouts.json"

    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    def test_add_workout_valid(self, mock_info, mock_error):
        self.app.workout_entry.get.return_value = "Running"
        self.app.duration_entry.get.return_value = "30"
        self.app.category_var.get.return_value = "Cardio"
        self.app.date_entry.get.return_value = "2025-09-04"
        self.app.add_workout()
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0]["workout"], "Running")
        mock_info.assert_called()
        mock_error.assert_not_called()

    @patch("tkinter.messagebox.showerror")
    def test_add_workout_invalid_duration(self, mock_error):
        self.app.workout_entry.get.return_value = "Running"
        self.app.duration_entry.get.return_value = "abc"
        self.app.category_var.get.return_value = "Cardio"
        self.app.date_entry.get.return_value = "2025-09-04"
        self.app.add_workout()
        mock_error.assert_called()
        self.assertEqual(len(self.app.workouts), 0)

    @patch("tkinter.messagebox.showerror")
    def test_add_workout_missing_fields(self, mock_error):
        self.app.workout_entry.get.return_value = ""
        self.app.duration_entry.get.return_value = ""
        self.app.category_var.get.return_value = ""
        self.app.date_entry.get.return_value = ""
        self.app.add_workout()
        mock_error.assert_called()
        self.assertEqual(len(self.app.workouts), 0)

    @patch("tkinter.messagebox.showinfo")
    def test_view_workouts_empty(self, mock_info):
        self.app.workouts = []
        self.app.view_workouts()
        mock_info.assert_called_with("Workouts", "No workouts logged yet.")

    @patch("tkinter.messagebox.showinfo")
    def test_view_workouts_nonempty(self, mock_info):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        self.app.view_workouts()
        self.assertTrue(mock_info.called)

    @patch("tkinter.simpledialog.askinteger")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    def test_delete_workout_valid(self, mock_error, mock_info, mock_ask):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        mock_ask.return_value = 1
        self.app.delete_workout()
        self.assertEqual(len(self.app.workouts), 0)
        mock_info.assert_called()
        mock_error.assert_not_called()

    @patch("tkinter.simpledialog.askinteger")
    @patch("tkinter.messagebox.showerror")
    def test_delete_workout_invalid(self, mock_error, mock_ask):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        mock_ask.return_value = 2
        self.app.delete_workout()
        mock_error.assert_called()
        self.assertEqual(len(self.app.workouts), 1)

    @patch("tkinter.messagebox.showinfo")
    def test_delete_workout_empty(self, mock_info):
        self.app.workouts = []
        self.app.delete_workout()
        mock_info.assert_called_with("Delete", "No workouts to delete.")

    @patch("tkinter.messagebox.showinfo")
    def test_show_stats_empty(self, mock_info):
        self.app.workouts = []
        self.app.show_stats()
        mock_info.assert_called_with("Statistics", "No workouts to show stats.")

    @patch("tkinter.messagebox.showinfo")
    def test_show_stats_nonempty(self, mock_info):
        self.app.workouts = [
            {"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"},
            {"workout": "Yoga", "duration": 60, "category": "Flexibility", "date": "2025-09-03"}
        ]
        self.app.show_stats()
        self.assertTrue(mock_info.called)

    @patch("builtins.open", new_callable=mock_open)
    @patch("tkinter.messagebox.showinfo")
    def test_save_workouts_success(self, mock_info, mock_file):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        self.app.save_workouts()
        mock_info.assert_called_with("Save", "Workouts saved successfully.")

    @patch("builtins.open", side_effect=Exception("fail"))
    @patch("tkinter.messagebox.showerror")
    def test_save_workouts_failure(self, mock_error, mock_file):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        self.app.save_workouts()
        mock_error.assert_called()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]')
    def test_load_workouts_success(self, mock_file, mock_exists):
        self.app.load_workouts()
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0]["workout"], "Running")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=Exception("fail"))
    @patch("tkinter.messagebox.showerror")
    def test_load_workouts_failure(self, mock_error, mock_file, mock_exists):
        self.app.load_workouts()
        mock_error.assert_called()


if __name__ == "__main__":
    unittest.main()