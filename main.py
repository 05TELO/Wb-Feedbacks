import asyncio
import json
import logging
import schedule

from src.feedbacks import SKUManager
from src.config import load_config
from telegram import Bot


conf = load_config(".env")

token = conf.bot.token
chat_id = conf.bot.chat_id
file_path = conf.bot.path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=token)


async def send_message() -> None:
    manager = SKUManager(file_path)
    messages = manager.get_result()
    logger.info("Preparing to send messages")
    for message in messages:
        try:
            text = json.dumps(message, indent=4, ensure_ascii=False)
            logger.info(f"Sending message: {text}")
            await bot.send_message(chat_id=chat_id, text=text)
            await asyncio.sleep(5)
        except Exception as ex:
            logger.exception(ex)


async def main() -> None:
    schedule.every(conf.bot.resp_time).minutes.do(
        lambda: asyncio.ensure_future(send_message())
    )
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
