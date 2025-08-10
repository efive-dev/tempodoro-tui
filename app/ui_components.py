from textual.widgets import Static, Input, Button, Label, DataTable
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.app import ComposeResult

def build_ui() -> ComposeResult:
    yield Static("Pomodoro TUI - Press 'ctrl + q' to quit", classes="title")
    with Horizontal():
        with Vertical(id="controls"):
            yield Static("Pomodoro TUI", classes="title")
            yield Label("Messages:")
            yield Static("", id="messages")
            yield Label("Login")
            yield Input(placeholder="username", id="username")
            yield Input(password=True, placeholder="password", id="password")
            yield Button("Login", id="login_btn")
            yield Label("Session settings", id="settings_label")
            yield Input(value="25", id="session_duration")
            yield Input(value="5", id="break_duration")
            with Horizontal():
                yield Button("Start Session", id="start_btn")
                yield Button("Stop Session", id="stop_btn", disabled=True)
                yield Button("Complete Session", id="complete_btn", disabled=True)
            yield Label("Status:")
            yield Static("Not started", id="status")
            yield Static("00:00", id="timer", classes="big-timer")
            yield Button("Refresh History", id="history_btn")
            
        with VerticalScroll(id="history_panel"):
            yield Static("History", classes="title")
            history_table = DataTable(id="history_table")
            history_table.add_columns("id", "startedAt", "sessionMinutes", "breakMinutes", "status")
            yield history_table
            yield Input(placeholder="Session ID to delete", id="delete_session_id")
            yield Button("Delete Session", id="delete_btn")


