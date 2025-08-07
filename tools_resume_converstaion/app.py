from dotenv import load_dotenv
import json
from openai import OpenAI
import os
import requests
from pypdf import PdfReader
import gradio as gr

load_dotenv(override=True)

# Push notification Setup
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"
def push(message):
    print(f"Push: {message}")
    payload = {
        "user": pushover_user, 
        "token": pushover_token, 
        "message": message
    }
    requests.post(pushover_url, data=payload)

# Tool 1
def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": True}

# Tool 2
def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": True}

def record_recruiter_question(inquiry):
    push(f"Job Description: {inquiry}")
    return {"recorded": True}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "Email address of the user"
            },
            "name": {
                "type": "string",
                "description": "Name of the user"
            },
            "notes": {
                "type": "string",
                "description": "Additional notes provided by the user"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that was asked"
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

record_recruiter_question_json = {
    "name": "record_recruiter_question",
    "description": "Use this tool to record if a recuiter sends in a job desciription or inquiry",
    "parameters": {
        "type": "object",
        "properties": {
            "inquiry": {
                "type": "string",
                "description": "The job description or inquiry from the recruiter"
            }
        },
        "required": ["inquiry"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
         {"type": "function", "function": record_unknown_question_json},
         {"type": "function", "function": record_recruiter_question_json}]

class Conversation:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Ashutosh Gajankush"
        render = PdfReader("data/resume/Ashutosh_Gajankush.pdf")
        self.resume = ""
        for page in render.pages:
            text = page.extract_text()
            if text:
                self.resume += text
        with open("data/resume/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        

    def handle_tool_calls(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = tool_call.function.arguments
            if tool_name == "record_user_details":
                result = record_user_details(**json.loads(tool_args))
            elif tool_name == "record_unknown_question":
                result = record_unknown_question(**json.loads(tool_args))
            elif tool_name == "record_recruiter_question":
                result = record_recruiter_question(**json.loads(tool_args))
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results
        
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. \
If you suspect the user is a recruiter, use the record_recruiter_question tool to record the job description or inquiry they send in."

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools
            )
            finish_reason = response.choices[0].finish_reason
            
            if finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                tool_results = self.handle_tool_calls(tool_calls)
                messages.append(message)
                messages.extend(tool_results)
            else:
                done = True
        return response.choices[0].message.content

if __name__ == "__main__":
    conversation = Conversation()
    gr.ChatInterface(
        conversation.chat,
        title="Ashutosh Gajankush - Resume Chat",
        type="messages",
        description="Chat with Ashutosh Gajankush's resume. Ask questions about his background, skills, and experience.",
        theme="compact"
    ).launch()



