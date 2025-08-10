## TUI Client (Python)

The client app is a terminal-based interactive Pomodoro tool built with:

- **Python 3.10+**
- **Textual** library for TUI components.
- **aiohttp** for async HTTP requests.

It is meant to be used as a frontend for [tempodoro](https://github.com/efive-dev/tempodoro).

### Features

- Login with username/password to get a JWT token.
- Start a Pomodoro session with configurable session and break durations.
- Stop or complete ongoing Pomodoro sessions.
- View session history in a table.
- Delete a selected session via a button (calls DELETE endpoint).
- Timer display with countdown for session and break periods.

### How to run
0. Register a user

The backend can be found at [tempodoro](https://github.com/efive-dev/tempodoro).
Once you have the backend running register a user using the following request:
```bash
curl -X POST http://localhost:8080/auth/register   -H "Content-Type: application/json"   -d '{"username": "your_username", "password": "your_password"}'
```

1. Clone the repository

```bash
git clone https://github.com/efive-dev/tempodoro-tui.git
cd tempodoro-tui
```

2. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the TUI client:

```bash
python __main__.py
```
