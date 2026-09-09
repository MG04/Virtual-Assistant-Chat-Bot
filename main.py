#!/usr/bin/env python3
"""Project Entrypoint for the Virtual Personal Assistant.

Run with:
    python main.py
"""

import sys
from pathlib import Path

# Ensure root directory is in sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if __name__ == '__main__':
    from src.main import root
    root.mainloop()
