import subprocess


def bash(command: str) -> str:
    """The function to execute bash command"""
    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    result = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True)

    return result.stdout + result.stderr

def read_file(path: str) -> str:
    """Read a file and return its contents."""
    with open(path) as f:
        return f.read()

# a list of tools
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command and return its combined stdout and stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to run",
                    }
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read",
                    }
                },
                "required": ["path"],
            },
        },
    },
]

TOOLS = {"bash": bash, "read_file": read_file}