import aiohttp

BASE_URL = "http://localhost:8080"

async def login_api(username: str, password: str) -> str:
    async with aiohttp.ClientSession() as sess:
        async with sess.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password}) as resp:
            if resp.status != 200:
                raise Exception(f"Login failed: {await resp.text()}")
            data = await resp.json()
            return data.get("token")

async def start_session_api(token: str, session_duration: int, break_duration: int) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as sess:
        async with sess.post(f"{BASE_URL}/api/pomodoro/start", json={"sessionDuration": session_duration, "breakDuration": break_duration}, headers=headers) as resp:
            if resp.status not in (200, 201):
                raise Exception(f"Failed to start session: {await resp.text()}")
            return await resp.json()

async def stop_session_api(token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as sess:
        async with sess.patch(f"{BASE_URL}/api/pomodoro/stop", headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to stop session: {await resp.text()}")
            return await resp.json()

async def complete_session_api(token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as sess:
        async with sess.patch(f"{BASE_URL}/api/pomodoro/complete", headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to complete session: {await resp.text()}")
            return await resp.json()

async def fetch_history_api(token: str) -> list:
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as sess:
        async with sess.get(f"{BASE_URL}/api/pomodoro/history", headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to fetch history: {await resp.text()}")
            return await resp.json()

async def delete_session_api(token: str, session_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as sess:
        async with sess.delete(f"{BASE_URL}/api/pomodoro/{session_id}", headers=headers) as resp:
            if resp.status != 204:
                raise Exception(f"Failed to delete session: {await resp.text()}")
