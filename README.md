## How to run?
```bash
$env:UV_ENV_FILE = ".env" # set env variables
uv run agent.py # start agent
```

## Example prompt to solve wordle
Use ego-browser to play today Wordle in the browser. Do not fetch the answer from any API. You might see advertisements, login prompt before reaching the actual wordle space, close or skip all.
Enter each letter with page.click() on the on-screen keyboard, passing a short label.
Pause 1 second between clicks. When finished, keep page p1 open.