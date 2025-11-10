import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
import datetime
import src.app as app_module

# Patch tkinter before importing your app
with patch.dict("sys.modules", {
    "tkinter": MagicMock(),
    "tkinter.ttk": MagicMock(),
    "tkinter.messagebox": MagicMock(),
    "tkinter.simpledialog": MagicMock(),
}):
    import src.app as app_module
    from src.app import FitnessTrackerApp


class TestFitnessTracker(unittest.TestCase):
    def setUp(self):
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
        # Reset messagebox mocks before each test
        app_module.messagebox.showinfo.reset_mock()
        app_module.messagebox.showerror.reset_mock()



    def test_add_workout_invalid_duration(self):
        self.app.workout_entry.get.return_value = "Running"
        self.app.duration_entry.get.return_value = "abc"
        self.app.category_var.get.return_value = "Cardio"
        self.app.date_entry.get.return_value = "2025-09-04"
        self.app.add_workout()
        app_module.messagebox.showerror.assert_called()
        self.assertEqual(len(self.app.workouts), 0)

    def test_add_workout_missing_fields(self):
        self.app.workout_entry.get.return_value = ""
        self.app.duration_entry.get.return_value = ""
        self.app.category_var.get.return_value = ""
        self.app.date_entry.get.return_value = ""
        self.app.add_workout()
        app_module.messagebox.showerror.assert_called()
        self.assertEqual(len(self.app.workouts), 0)

    def test_view_workouts_nonempty(self):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        self.app.view_workouts()
        self.assertTrue(app_module.messagebox.showinfo.called)
        args, kwargs = app_module.messagebox.showinfo.call_args
        self.assertEqual(args[0], "Workouts")
        self.assertIn("Running", args[1])

    def test_view_workouts_empty(self):
        self.app.workouts = []
        self.app.view_workouts()
        app_module.messagebox.showinfo.assert_called_with("Workouts", "No workouts logged yet.")

    @patch("tkinter.simpledialog.askinteger")
    def test_delete_workout_valid(self, mock_ask):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        app_module.simpledialog.askinteger.return_value = 1
        self.app.delete_workout()
        self.assertEqual(len(self.app.workouts), 0)
        app_module.messagebox.showinfo.assert_called()
        app_module.messagebox.showerror.assert_not_called()

    @patch("tkinter.simpledialog.askinteger")
    def test_delete_workout_invalid(self, mock_ask):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        app_module.simpledialog.askinteger.return_value = 2
        self.app.delete_workout()
        app_module.messagebox.showerror.assert_called()
        self.assertEqual(len(self.app.workouts), 1)

    def test_delete_workout_empty(self):
        self.app.workouts = []
        self.app.delete_workout()
        app_module.messagebox.showinfo.assert_called_with("Delete", "No workouts to delete.")

    def test_show_stats_empty(self):
        self.app.workouts = []
        self.app.show_stats()
        app_module.messagebox.showinfo.assert_called_with("Statistics", "No workouts to show stats.")

    def test_show_stats_nonempty(self):
        self.app.workouts = [
            {"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"},
            {"workout": "Yoga", "duration": 60, "category": "Flexibility", "date": "2025-09-03"}
        ]
        self.app.show_stats()
        self.assertTrue(app_module.messagebox.showinfo.called)
        args, kwargs = app_module.messagebox.showinfo.call_args
        self.assertEqual(args[0], "Statistics")
        self.assertIn("Total Workouts: 2", args[1])

    @patch("builtins.open", new_callable=mock_open)
    def test_save_workouts_success(self, mock_file):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        self.app.save_workouts()
        app_module.messagebox.showinfo.assert_called_with("Save", "Workouts saved successfully.")

    @patch("builtins.open", side_effect=Exception("fail"))
    def test_save_workouts_failure(self, mock_file):
        self.app.workouts = [{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]
        self.app.save_workouts()
        app_module.messagebox.showerror.assert_called()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"workout": "Running", "duration": 30, "category": "Cardio", "date": "2025-09-04"}]')
    def test_load_workouts_success(self, mock_file, mock_exists):
        self.app.load_workouts()
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0]["workout"], "Running")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=Exception("fail"))
    def test_load_workouts_failure(self, mock_file, mock_exists):
        self.app.load_workouts()
        app_module.messagebox.showerror.assert_called()


if __name__ == "__main__":
    unittest.main()