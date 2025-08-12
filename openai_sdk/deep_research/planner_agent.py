

from agents import Agent
from pydantic import BaseModel, Field


no_of_searches = 3

instructions = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
    to perform to best answer the query. Output {no_of_searches} terms to query for."

# Pydantic models for Websearch
class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this seach is important to the query.")
    query: str = Field(description="The search term to use for the web search.")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
# Agent which will output the search terms to use
planner_agent = Agent(
    name="PlannerAgent",
    instructions=instructions,
    model="gpt-4o-mini",
    output_type=WebSearchPlan
)