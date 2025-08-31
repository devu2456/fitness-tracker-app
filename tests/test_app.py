import unittest
from src.app import FitnessTrackerApp
import tkinter as tk

class TestFitnessTracker(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = FitnessTrackerApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_add_workout(self):
        self.app.workouts.append({"workout": "Running", "duration": 30})
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0]["workout"], "Running")
        self.assertEqual(self.app.workouts[0]["duration"], 30)

if __name__ == "__main__":
    unittest.main()