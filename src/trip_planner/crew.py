from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from trip_planner.tools.browser_tools import scrape_and_summarize_website
from trip_planner.tools.calculator_tools import calculate
from trip_planner.tools.search_tools import search_internet

load_dotenv()


@CrewBase
class TripCrew:
    """여행 플래너 Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.origin = None
        self.cities = None
        self.date_range = None
        self.interests = None

    @agent
    def city_selector(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selector'],
            tools=[search_internet, scrape_and_summarize_website],
            verbose=True
        )

    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'],
            tools=[search_internet, scrape_and_summarize_website],
            verbose=True
        )

    @agent
    def travel_concierge(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_concierge'],
            tools=[search_internet, scrape_and_summarize_website, calculate],
            verbose=True
        )

    @task
    def identify_city(self) -> Task:
        return Task(
            config=self.tasks_config['identify_city'],
            agent=self.city_selector()
        )

    @task
    def gather_city_info(self) -> Task:
        return Task(
            config=self.tasks_config['gather_city_info'],
            agent=self.local_expert()
        )

    @task
    def create_itinerary(self) -> Task:
        return Task(
            config=self.tasks_config['create_itinerary'],
            agent=self.travel_concierge()
        )

    @crew
    def crew(self) -> Crew:
        """여행 플래너 Crew를 생성합니다"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
