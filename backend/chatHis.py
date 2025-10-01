import json
import os
from datetime import datetime

HISTORY_FILE = 'chat_history.json' #First I Created an Empty JSon file to Store the conversations history, why Json beacuse it allows us to store data in the form of objects

def load_history():  #Then I will load the chat history from JSON file
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history): # AFter loading i will save the chat history to JSON file
    # I willl keep only last 10 entries
    if len(history) > 10:
        history = history[-10:]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_entry(q, a, source="unknown"): # If the conversation starts, I will add a new question-answer pair to history
    history = load_history()
    entry = {
        "question": q,
        "answer": a,
        "timestamp": datetime.now().isoformat(),
        "source": source  # This helps me to track the response source, which ? either knowledge base or LLm
    }
    history.append(entry)
    save_history(history)
    return history

def clear_history(): # Logic to clear all chat history -- How ? - very simple, empty the JSON File HAHA...
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f, indent=2)
        return True
    except Exception as e:
        print(f" OOPS ... Error clearing history: {e}")
        return False

def get_history_count(): # Get the total number of history entries - I dont know why this needs, but trust me it helps....
    history = load_history()
    return len(history)
    return history