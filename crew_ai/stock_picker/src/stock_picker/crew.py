from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from stock_picker.tools.push_tool import PushNotificationTool
from crewai.memory import ShortTermMemory, LongTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class TrendingCompany(BaseModel):
    name: str = Field(..., description="The name of the trending company")
    ticker: str = Field(..., description="The ticker symbol of the trending company")
    reason: str = Field(..., description="The reason why this company is trending")

class TrendingCompanyList(BaseModel):
    companies: List[TrendingCompany] = Field(..., description="A list of trending companies")

class TrendingCompanyResearch(BaseModel):
    name: str = Field(..., description="The name of the trending company")
    market_position: str = Field(..., description="Current market position and competitive analysis")
    future_outlook: str = Field(..., description="Future outlook and growth prospects")
    investment_potential: str = Field(..., description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    research_list: List[TrendingCompanyResearch] = Field(..., description="Comprehensive research on call trending companies")
    
@CrewBase
class StockPicker():
    """StockPicker crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def trending_company_finder(self) -> Agent:
        """Trending company finder agent"""
        return Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()], memory=True)
    
    @agent
    def financial_researcher(self) -> Agent:
        """Financial researcher agent"""
        return Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()])
    
    @agent
    def stock_picker(self) -> Agent:
        """Stock picker agent"""
        return Agent(config=self.agents_config['stock_picker'], tools=[PushNotificationTool()], memory=True)
    
    @task
    def find_trending_companies(self) -> Task:
        """Find trending companies task"""
        return Task(config=self.tasks_config['find_trending_companies'], output_pydantic=TrendingCompanyList)
    
    @task
    def research_trending_companies(self) -> Task:
        """Research trending companies task"""
        return Task(config=self.tasks_config['research_trending_companies'], output_pydantic=TrendingCompanyResearchList)
    
    @task
    def pick_best_company(self) -> Task:
        """Pick best company task"""
        return Task(config=self.tasks_config['pick_best_company'])
    
    @crew
    def crew(self) -> Crew:
        manager = Agent(config=self.agents_config['manager'], verbose=True)
        """Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            manager_agent=manager,
            verbose=True,
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path='./memory/ltm.db'
                )
            ),
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": "text-embedding-3-small"
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
            entity_memory = EntityMemory(
                storage = RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config":{
                            "model": "text-embedding-3-small"
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )
    
