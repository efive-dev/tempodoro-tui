import asyncio
from textual.widgets import Static

def show_temporary_message(app, widget: Static, msg: str, seconds: float = 4.0):
    widget.update(msg)
    async def clear_msg():
        await asyncio.sleep(seconds)
        widget.update("")
    asyncio.create_task(clear_msg())

