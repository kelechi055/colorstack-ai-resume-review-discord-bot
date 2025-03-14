import logging
import os
import sys
from ai_resume_review_bot import start_bot
from config import DISCORD_TOKEN


# Configure logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Run the bot
if __name__ == "__main__":
    logger.info("Starting Resume Review Discord Bot")
    try:
        logger.info("Connecting to Discord...")
        start_bot(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
        # If running on Heroku, exit with error code to trigger restart
        sys.exit(1)