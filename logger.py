import os
import csv
from datetime import datetime

def log_chat(session_id: str, query: str, bot_response: str, is_crisis: bool):
    """
    Logs a single chat interaction into chat_log.csv.

    Args:
        session_id (str): Unique identifier for the user session.
        query (str): The user's input message.
        bot_response (str): The chatbot's response.
        is_crisis (bool): True if the input contained crisis-related keywords.
    """
    log_file = "chat_log.csv"
    file_exists = os.path.isfile(log_file)

    # Open in append mode and write data
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header row if file is new
        if not file_exists:
            writer.writerow(["timestamp", "session_id", "user_query", "bot_response", "is_crisis"])

        # Record the interaction
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, session_id, query, bot_response, is_crisis])
