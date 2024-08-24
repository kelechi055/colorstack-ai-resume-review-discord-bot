import random

import logging
from ai_resume_review_bot import start_bot
from config import DISCORD_TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Run the bot
if __name__ == "__main__":
    start_bot(DISCORD_TOKEN)