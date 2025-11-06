"""
Worker initializer for setting up background workers
"""
import asyncio
import logging
from utils.worker_scheduler import worker_scheduler

logger = logging.getLogger(__name__)


async def initialize_workers() -> None:
    """
    Initialize and add all workers to the scheduler
    
    This function registers all background workers with their
    respective execution intervals.
    """
    try:
        # Example: Add image cleanup worker - runs every hour
        # await worker_scheduler.add_task(
        #     name="image_cleanup",
        #     func=image_cleanup_worker.cleanup_unused_images,
        #     interval=3600
        # )
        
        # Example: Add billing manager - runs every 6 hours
        # await worker_scheduler.add_task(
        #     name="billing_manager",
        #     func=run_billing_manager,
        #     interval=21600
        # )
        
        # Example: Add project deployment manager - runs every 10 seconds
        # await worker_scheduler.add_task(
        #     name="project_deployment",
        #     func=project_manager.start,
        #     interval=10
        # )
        
        logger.info("Workers initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing workers: {e}", exc_info=True)


async def start_workers() -> None:
    """Start all registered workers"""
    try:
        await worker_scheduler.start()
        await initialize_workers()
        logger.info("All workers started")
    except Exception as e:
        logger.error(f"Error starting workers: {e}", exc_info=True)


async def stop_workers() -> None:
    """Stop all workers"""
    try:
        await worker_scheduler.stop()
        logger.info("All workers stopped")
    except Exception as e:
        logger.error(f"Error stopping workers: {e}", exc_info=True)

