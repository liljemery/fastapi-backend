"""
Base worker class for background task processing
"""
import asyncio
import logging
from typing import Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseWorker(ABC):
    """
    Base class for background workers
    
    Provides common functionality for worker lifecycle management,
    error handling, and status monitoring.
    """
    
    def __init__(self, name: str) -> None:
        """
        Initialize base worker
        
        Args:
            name: Worker name
        """
        self.name = name
        self.running: bool = False
        self.logger = logging.getLogger(f"worker.{name}")
    
    @abstractmethod
    async def process(self) -> None:
        """
        Main processing method to be implemented by subclasses
        
        This method contains the core logic for the worker.
        """
        pass
    
    async def start(self) -> None:
        """
        Start the worker
        
        Begins the worker's processing loop.
        """
        if self.running:
            self.logger.warning(f"{self.name} is already running")
            return
        
        self.running = True
        self.logger.info(f"{self.name} started")
        
        try:
            await self.process()
        except Exception as e:
            self.logger.error(f"Error in {self.name}: {e}", exc_info=True)
        finally:
            self.running = False
            self.logger.info(f"{self.name} stopped")
    
    async def stop(self) -> None:
        """
        Stop the worker
        
        Gracefully stops the worker's processing loop.
        """
        self.running = False
        self.logger.info(f"{self.name} stopping...")
    
    def get_status(self) -> dict:
        """
        Get worker status
        
        Returns:
            Dictionary with worker status information
        """
        return {
            "name": self.name,
            "running": self.running
        }


class IntervalWorker(BaseWorker):
    """
    Worker that runs at regular intervals
    """
    
    def __init__(self, name: str, interval: int = 60) -> None:
        """
        Initialize interval worker
        
        Args:
            name: Worker name
            interval: Execution interval in seconds
        """
        super().__init__(name)
        self.interval = interval
    
    async def process(self) -> None:
        """Process loop with interval delays"""
        while self.running:
            try:
                await self.execute()
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                self.logger.info(f"{self.name} cancelled")
                break
            except Exception as e:
                self.logger.error(f"Error in {self.name} execution: {e}", exc_info=True)
                await asyncio.sleep(self.interval)
    
    @abstractmethod
    async def execute(self) -> None:
        """
        Execute method to be implemented by subclasses
        
        This method is called at each interval.
        """
        pass

