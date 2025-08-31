import unittest
from unittest.mock import MagicMock, patch

# Patch tkinter before importing your app
with patch.dict("sys.modules", {
    "tkinter": MagicMock(),
    "tkinter.ttk": MagicMock(),
    "tkinter.messagebox": MagicMock(),
}):
    from src.app import FitnessTrackerApp


class TestFitnessTracker(unittest.TestCase):
    def setUp(self):
        # root is now just a MagicMock, no real window created
        self.root = MagicMock()
        self.app = FitnessTrackerApp(self.root)

    def test_add_workout(self):
        self.app.workouts.append({"workout": "Running", "duration": 30})
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0]["workout"], "Running")
        self.assertEqual(self.app.workouts[0]["duration"], 30)


if __name__ == "__main__":
    unittest.main()