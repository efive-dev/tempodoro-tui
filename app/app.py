import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from tzlocal import get_localzone
from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button, Label, DataTable
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive

from .api import login_api, start_session_api, stop_session_api, complete_session_api, fetch_history_api, delete_session_api
from .ui_components import build_ui
from .timer import TimerLoop
from .utils import show_temporary_message


class PomodoroApp(App):
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [("q", "quit", "Quit")]

    token = None
    current_phase = reactive(None)
    phase_start_time = reactive(None)
    phase_duration_minutes = reactive(0)
    timer_task = None
    status_text = reactive("Not started")
    timer_display = reactive("00:00")
    local_tz = None

    def compose(self) -> ComposeResult:
        return build_ui()

    CSS_PATH = "./../public/styles.css"

    async def on_mount(self):
        try:
            self.local_tz = get_localzone()
        except Exception:
            self.local_tz = ZoneInfo("UTC")
        self._hide_app_section()

    def _hide_app_section(self):
        for wid in ["#settings_label", "#session_duration", "#break_duration", "#start_btn", "#stop_btn", "#complete_btn", "#status", "#timer"]:
            self.query_one(wid).display = False

    def _show_app_section(self):
        for wid in ["#settings_label", "#session_duration", "#break_duration", "#start_btn", "#stop_btn", "#complete_btn", "#status", "#timer"]:
            self.query_one(wid).display = True

    def show_message(self, msg: str, seconds: float = 4.0):
        messages = self.query_one("#messages", Static)
        show_temporary_message(self, messages, msg, seconds)

    async def action_quit(self):
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
        self.exit()

    async def on_button_pressed(self, event: Button.Pressed):
        bid = event.button.id
        if bid == "login_btn":
            await self.handle_login()
        elif bid == "start_btn":
            await self.handle_start_session()
        elif bid == "stop_btn":
            await self.handle_stop_session()
        elif bid == "complete_btn":
            await self.handle_complete_session()
        elif bid == "history_btn":
            await self.fetch_history()
        elif bid == "delete_btn":
            await self.handle_delete_session()


    async def handle_login(self):
        username = self.query_one("#username", Input).value.strip()
        password = self.query_one("#password", Input).value.strip()
        if not username or not password:
            self.show_message("Enter username and password")
            return
        try:
            self.token = await login_api(username, password)
            if not self.token:
                raise Exception("No token returned")
            self._show_app_section()
            self.show_message("Logged in")
            await self.fetch_history()
        except Exception as e:
            self.show_message(str(e))

    async def handle_start_session(self):
        try:
            session_duration = int(self.query_one("#session_duration", Input).value or 25)
            break_duration = int(self.query_one("#break_duration", Input).value or 5)
            session = await start_session_api(self.token, session_duration, break_duration)
            started_at = session.get("startedAt")
            if started_at:
                phase_start = datetime.fromisoformat(started_at.replace("Z", "+00:00")).astimezone(self.local_tz)
            else:
                phase_start = datetime.now(self.local_tz)
            self.current_phase = "session"
            self.phase_start_time = phase_start
            self.phase_duration_minutes = session_duration
            self.status_text = session.get("status", "running")
            self.query_one("#status", Static).update(f"Status: {self.status_text}")
            self.query_one("#stop_btn", Button).disabled = False
            self.query_one("#complete_btn", Button).disabled = False

            if self.timer_task and not self.timer_task.done():
                self.timer_task.cancel()
            self.timer_task = asyncio.create_task(
                TimerLoop(self).run()
            )
        except Exception as e:
            self.show_message(str(e))

    async def handle_stop_session(self):
        try:
            session = await stop_session_api(self.token)
            self.status_text = session.get("status", "stopped")
            self.query_one("#status", Static).update(f"Status: {self.status_text}")
            await self.reset_timer()
            await self.fetch_history()
        except Exception as e:
            self.show_message(str(e))

    async def handle_complete_session(self):
        try:
            session = await complete_session_api(self.token)
            self.status_text = session.get("status", "completed")
            self.query_one("#status", Static).update(f"Status: {self.status_text}")
            await self.reset_timer()
            await self.fetch_history()
        except Exception as e:
            self.show_message(str(e))

    async def reset_timer(self):
        self.timer_display = "00:00"
        self.query_one("#timer", Static).update(self.timer_display)
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
        self.current_phase = None
        self.phase_start_time = None
        self.phase_duration_minutes = 0
        self.query_one("#stop_btn", Button).disabled = True
        self.query_one("#complete_btn", Button).disabled = True

    async def fetch_history(self):
        if not self.token:
            return
        try:
            history = await fetch_history_api(self.token)
            history_table = self.query_one("#history_table", DataTable)
            history_table.clear(columns=False)
            for item in history:
                history_table.add_row(
                    str(item.get("id", "-")),
                    item.get("startedAt", "-"),
                    str(item.get("sessionDuration", "-")),
                    str(item.get("breakDuration", "-")),
                    item.get("status", "-"),
                )
        except Exception as e:
            self.show_message(str(e))

    async def handle_delete_session(self):
        session_id_str = self.query_one("#delete_session_id", Input).value.strip()
        if not session_id_str.isdigit():
            self.show_message("Please enter a valid numeric session ID")
            return

        session_id = int(session_id_str)
        try:
            await delete_session_api(self.token, session_id)
            self.show_message(f"Session {session_id} deleted")

            if self.current_phase is not None:
                await self.reset_timer()

            await self.fetch_history()
        except Exception as e:
            self.show_message(str(e))




