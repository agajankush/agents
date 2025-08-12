

from agents import Agent, ModelSettings, WebSearchTool


instructions = "You are a research assistant. Given a search term, you search the web for that term and \
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 \
words. Capture the main points. Write succintly, no need to have complete sentences or good \
grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the \
essence and ignore any fluff. Do not include any additional commentary other than the summary itself."

search_agent = Agent(
    name="Search agent",
    instructions=instructions,
    tools=[WebSearchTool(search_context_size="low")], # size here determines the context of the search results the more the expensive
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required") # Required means that we will always use the tool when available
)