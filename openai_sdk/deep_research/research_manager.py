
import asyncio
from agents import Runner, gen_trace_id, trace

from planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from assistant_agent import search_agent
from researcher_agent import writer_agent, ReportData
from notifications_agent import notification_agent

class ResearchManager:
    
    async def run(self,query: str):
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."
            await self.send_notification(report)
            yield "Email sent, research complete"
            yield report.markdown_report
        
    # Create Plan
    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Uses the planner agent to plan which searched to run for the query """
        print("Planning searches...")
        result = await Runner.run(planner_agent, f"Query: {query}")
        print(f"Will perform {len(result.final_output.searches)} searches.")
        return result.final_output

    # Perform Individual searches helper function
    async def search(self, item: WebSearchItem) -> str | None:
        """ Uses the search agent to perform a single search """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(search_agent, input)
        return str(result.final_output)
        
    # perform searches in parallel
    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Uses the search agent to perform the searches in the search plan """
        print("Performing searches...")
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = await asyncio.gather(*tasks)
        print("Finished searching")
        return results

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Uses the writer agent to write the report based on the query and search results """
        print("Thinking about the report...")
        input = f"Original Query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input)
        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def send_notification(self, report: ReportData):
        """ Uses the notification agent to send a notification with the report """
        result = await Runner.run(notification_agent, report.markdown_report)
        print("Notification sent")
        return report