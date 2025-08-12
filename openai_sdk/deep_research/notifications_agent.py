

# Setup Push notification
import os
from agents import Agent, function_tool
import requests


def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )
    
@function_tool
def send_push_notification(message : str):
    push(message)
    return {"status": "success"}

# Agent to send the HTML formatted email
instructions = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provieded with a detailed report. You should use your tool to send one push notification, providing the report
converted into clean, well presented HTML with an appropriate subject line."""

notification_agent = Agent(
    name="notification_agent",
    tools=[send_push_notification],
    instructions=instructions,
    model="gpt-4o-mini",
)