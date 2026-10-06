"""Worker process entry point.

Run with: python -m workers.main
Individual workers are registered here as they are implemented in later tickets.
"""

import asyncio
import signal

import structlog

from api.config import get_settings
from api.logging_config import configure_logging

logger = structlog.get_logger(__name__)


async def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    logger.info("workers.starting", env=settings.app_env)

    # Workers will be added here in P05-09 (ingestion), P05-11 (aggregation).
    # For now, keep the process alive so docker-compose health checks pass.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    def _stop(_: int, __: object) -> None:
        if not stop.done():
            stop.set_result(None)

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    logger.info("workers.ready", note="No workers registered yet — add them in P05-09")
    await stop
    logger.info("workers.shutdown")


if __name__ == "__main__":
    asyncio.run(main())
