from fastapi import FastAPI

from sqlalchemy.orm import sessionmaker
from database.db import sync_engine
from database.models import requests_table

app = FastAPI(title="TestWork")

Session = sessionmaker(bind=sync_engine)
session = Session()

@app.get("/logs")
async def get_logs():
    logs = session.query(requests_table).all()
    logs_list = [{"id": log.id, "id_user": log.id_user, "command_bot": log.command_bot, "date_time": log.date_time, "message_bot": log.message_bot} for log in logs]
    return logs_list

@app.get("/logs/{user_id}")
async def get_logs_by_user(user_id: int):
    logs = session.query(requests_table).filter_by(id_user=user_id).all()
    logs_list = [{"id": log.id, "id_user": log.id_user, "command_bot": log.command_bot, "date_time": log.date_time, "message_bot": log.message_bot} for log in logs]
    return logs_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


