from asyncio import Queue
from typing import Dict
from fastapi import BackgroundTasks
import json
from datetime import datetime, UTC

# Global event queue for book updates
book_updates: Dict[str, Queue] = {}

async def get_book_update_queue(client_id: str) -> Queue:
    if client_id not in book_updates:
        book_updates[client_id] = Queue()
    return book_updates[client_id]

async def remove_client(client_id: str, background_tasks: BackgroundTasks):
    if client_id in book_updates:
        del book_updates[client_id]

async def send_book_update(event_type: str, book_id: int, book_data: dict = None):
    if book_data:
        # Remove SQLAlchemy state from the dictionary
        cleaned_data = {k: v for k, v in book_data.items() 
                       if not k.startswith('_') and k != 'metadata'}
    else:
        cleaned_data = None

    message = {
        "event": event_type,
        "book_id": book_id,
        "data": cleaned_data,
        "timestamp": datetime.now(UTC).isoformat()
    }
    
    for queue in book_updates.values():
        try:
            await queue.put(message)
        except Exception:
            continue