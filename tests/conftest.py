import sys
from unittest.mock import MagicMock

# Mock tkinter globally for all tests
mock_tk = MagicMock()
sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.ttk'] = mock_tk
sys.modules['tkinter.messagebox'] = mock_tk