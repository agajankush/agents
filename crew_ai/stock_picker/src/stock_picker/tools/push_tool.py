from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests

class PushNotificationInput(BaseModel):
    """A message to send to the user"""
    message: str = Field(..., description="The message to send to the user")

class PushNotificationTool(BaseTool):
    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotificationInput

    def _run(self, message: str) -> str:
        pusover_user = os.getenv("PUSHOVER_USER")
        pusover_token = os.getenv("PUSHOVER_TOKEN")
        pusover_url = "https://api.pushover.net/1/messages.json"
        payload = {
            "user": pusover_user,
            "token": pusover_token,
            "message": message
        }
        requests.post(pusover_url, data=payload)
        return '{"notification": "ok"}'
