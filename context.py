"""
late injection: a small block appended just before we send.

It goes to the end of the message list so the prefix in front of it stays cached. (maintain prefix cache)
"""

import subprocess
from datetime import datetime

def git_branch():
    # subprocess.run() will execute this in terminal
    result = subprocess.run(
        "git branch --show-current", shell=True,
        capture_output=True, text=True
    )
    return result.stdout.strip() or "(detached)"

def reminder():
    """The block appended to the messages on every turn."""
    return {
        "role": "user",
        "content": (
            "<env>\n"
            f"time: {datetime.now():%Y-%m-%d %H:%M}\n"
            f"git branch: {git_branch()}\n"
            "</env>"
        )
    }