import asyncio
from datetime import datetime
from textual.widgets import Static, Input

class TimerLoop:
    def __init__(self, app):
        self.app = app

    async def run(self):
        try:
            while True:
                if not self.app.phase_start_time or not self.app.phase_duration_minutes:
                    self.app.query_one("#timer", Static).update("00:00")
                    await asyncio.sleep(1)
                    continue
                now = datetime.now(self.app.local_tz)
                elapsed = (now - self.app.phase_start_time).total_seconds()
                total = int(self.app.phase_duration_minutes * 60)
                remaining = max(total - int(elapsed), 0)
                minutes, seconds = divmod(remaining, 60)
                self.app.timer_display = f"{minutes:02d}:{seconds:02d}"
                self.app.query_one("#timer", Static).update(self.app.timer_display)

                if remaining <= 0:
                    if self.app.current_phase == "session":
                        self.app.current_phase = "break"
                        self.app.phase_start_time = datetime.now(self.app.local_tz)
                        self.app.phase_duration_minutes = int(self.app.query_one("#break_duration", Input).value or 5)
                        self.app.query_one("#status", Static).update("Status: Break started")
                        continue
                    elif self.app.current_phase == "break":
                        self.app.query_one("#status", Static).update("Status: Break ended, completing session...")
                        try:
                            await self.app.handle_complete_session()
                        except Exception as e:
                            self.app.show_message(f"Warning: {e}")
                        break
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

