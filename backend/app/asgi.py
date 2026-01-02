import sys
import asyncio
import logging

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


logging.basicConfig(level=logging.INFO)


from app.entrypoints.api.app_factory import create_app

app = create_app()