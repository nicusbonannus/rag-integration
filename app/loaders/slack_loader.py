import os
import time

from slack_sdk import WebClient
from haystack import Document
from dotenv import load_dotenv

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_NAME = "general"

client = WebClient(token=SLACK_TOKEN)

def get_channel_id(channel_name: str) -> str:
    response = client.conversations_list()
    channels = response.get("channels", [])
    for channel in channels:
        if channel["name"] == channel_name:
            return channel["id"]
    raise ValueError(f"Channel '{channel_name}' not found")

def get_user_name(user_id: str, user_cache: dict) -> str:
    if user_id in user_cache:
        return user_cache[user_id]
    try:
        response = client.users_info(user=user_id)
        user_info = response.get("user", {})
        name = user_info.get("real_name") or user_info.get("profile", {}).get("display_name") or user_id
        user_cache[user_id] = name
        return name
    except Exception:
        return user_id

def load_slack_messages():
    channel_id = get_channel_id(CHANNEL_NAME)
    messages = []
    cursor = None
    i = 1

    for _ in range(15):
        print(f"Round number: {i}")
        response = client.conversations_history(channel=channel_id, cursor=cursor, limit=15)
        messages.extend(response.get("messages", []))
        cursor = response.get("response_metadata", {}).get("next_cursor")
        time.sleep(61) #every one minute, we have 15 rows maximum
        i += 1
        if not cursor:
            break

    user_cache = {}
    documents = []
    for msg in messages:
        if "subtype" in msg:
            continue
        content = msg.get("text", "")
        ts = msg.get("ts")
        user_id = msg.get("user", "unknown")
        author = get_user_name(user_id, user_cache)
        documents.append(Document(content=content,
                                  meta={"channel": CHANNEL_NAME, "user_id": user_id, "author": author,
                                        "timestamp": ts}))

    return documents
