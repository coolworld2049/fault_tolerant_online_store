import logging
import sys

import uvicorn
from loguru import logger

from app.settings import settings

if __name__ == "__main__":
    logger.remove()
    uvicorn.run(
        "app.application:create_fastapi_app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKER_NUMBER,
        reload=settings.RELOAD,
        factory=True,
    )
