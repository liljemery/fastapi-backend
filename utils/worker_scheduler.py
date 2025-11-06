"""
Worker scheduler for managing background tasks
"""
import asyncio
import logging
from typing import Dict, Callable, Optional, Any
from functools import wraps

logger = logging.getLogger(__name__)


class WorkerScheduler:
    """
    Centralized task scheduler for background workers
    
    Manages task lifecycle, interval-based execution,
    error isolation, and status monitoring.
    """
    
    def __init__(self) -> None:
        self.tasks: Dict[str, asyncio.Task] = {}
        self.running: bool = False
        self.intervals: Dict[str, int] = {}
    
    async def add_task(
        self,
        name: str,
        func: Callable,
        interval: int
    ) -> None:
        """
        Add recurring task to scheduler
        
        Args:
            name: Task name
            func: Async function to execute
            interval: Execution interval in seconds
        """
        if name in self.tasks:
            logger.warning(f"Task {name} already exists, removing old task")
            await self.remove_task(name)
        
        self.intervals[name] = interval
        
        async def task_wrapper() -> None:
            while self.running:
                try:
                    await func()
                    await asyncio.sleep(interval)
                except asyncio.CancelledError:
                    logger.info(f"Task {name} cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in task {name}: {e}", exc_info=True)
                    await asyncio.sleep(interval)
        
        self.tasks[name] = asyncio.create_task(task_wrapper())
        logger.info(f"Added task {name} with interval {interval}s")
    
    async def remove_task(self, name: str) -> None:
        """
        Remove task from scheduler
        
        Args:
            name: Task name
        """
        if name in self.tasks:
            task = self.tasks[name]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.tasks[name]
            del self.intervals[name]
            logger.info(f"Removed task {name}")
    
    async def start(self) -> None:
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        logger.info("Worker scheduler started")
    
    async def stop(self) -> None:
        """Stop the scheduler and all tasks"""
        self.running = False
        
        for name in list(self.tasks.keys()):
            await self.remove_task(name)
        
        logger.info("Worker scheduler stopped")
    
    def get_task_status(self) -> Dict[str, Any]:
        """
        Get status of all tasks
        
        Returns:
            Dictionary with task statuses
        """
        tasks_status: Dict[str, Any] = {}
        
        for name, task in self.tasks.items():
            tasks_status[name] = {
                "interval": self.intervals.get(name, 0),
                "done": task.done(),
                "cancelled": task.cancelled()
            }
        
        return {
            "running": self.running,
            "tasks": tasks_status
        }


# Global scheduler instance
worker_scheduler = WorkerScheduler()

