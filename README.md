# ACEestFitness and Gym - Fitness Tracker App

## Overview
This is a simple Tkinter-based fitness tracker application for logging workouts, viewing statistics, and managing your fitness data. The repository also includes unit tests for all major features and a sample GitHub Actions pipeline for CI.

## Setup & Running Locally

### Prerequisites
- Python 3.8+
- (macOS users) Ensure Python is installed with Tkinter support (`brew install python tcl-tk`)
- Recommended: Use a virtual environment

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/devu2456/fitness-tracker-app.git
   cd fitness-tracker-app
   ```
2. Create and activate a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application
1. Navigate to the `src` folder:
   ```sh
   cd src
   ```
2. Run the app:
   ```sh
   python app.py
   ```

## Running Tests Locally
1. From the project root, run:
   ```sh
   python -m unittest tests/test_app.py
   ```
   This will execute all unit tests and display results in the terminal.

## GitHub Actions Pipeline
- The repository includes a sample GitHub Actions workflow (`.github/workflows/python-app.yml`) that:
  - Sets up Python
  - Installs dependencies
  - Runs unit tests automatically on push and pull request events
- This ensures code quality and test coverage for every change.

## Contact
For issues or contributions, please open an issue or pull request on GitHub.