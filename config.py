import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

MODERATION_GROUP_ID = int(os.getenv("MODERATION_GROUP_ID"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")