import asyncio
import time
import threading
import schedule  # type: ignore[import-untyped]
from typing import Callable, Awaitable, Coroutine, Any

def run_async_job(async_func: Callable[[], Any]) -> None:
    """Ejecuta una función async en el event loop de asyncio"""
    asyncio.run(async_func())

def run_continuously(interval: int = 1) -> tuple[threading.Event, threading.Thread]:
    """Ejecuta `schedule.run_pending()` en segundo plano sin bloquear FastAPI"""
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        def __init__(self) -> None:
            super().__init__(daemon=True)

        def run(self) -> None:
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run, continuous_thread