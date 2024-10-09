from sqlalchemy import insert
from datetime import datetime
from database.models import metadata_obj, requests_table
from database.db import sync_engine

# Function to create tables
def create_tables():
    metadata_obj.create_all(sync_engine)

async def insert_request(user_id, command, response):
    with sync_engine.connect() as conn:
        # Insert a new log entry into the requests_table
        stmt = insert(requests_table).values(
            [
                {"id_user": user_id, "command_bot": command, "date_time": datetime.now(), "message_bot": response}
            ]
        )
        conn.execute(stmt)
        conn.commit()

    return "Запрос выполнен успешно."