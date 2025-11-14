import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    print("오류: GOOGLE_API_KEY가 .env 파일에 없습니다.")
    exit()

retry_config=types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

llm = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)

# --- 병렬 실행될 에이전트 3개 ---
tech_researcher = Agent(
    name="TechResearcher", model=llm,
    instruction="Research the latest AI/ML trends. Keep the report very concise (100 words).",
    tools=[google_search], output_key="tech_research",
)

health_researcher = Agent(
    name="HealthResearcher", model=llm,
    instruction="Research recent medical breakthroughs. Keep the report concise (100 words).",
    tools=[google_search], output_key="health_research",
)

finance_researcher = Agent(
    name="FinanceResearcher", model=llm,
    instruction="Research current fintech trends. Keep the report concise (100 words).",
    tools=[google_search], output_key="finance_research",
)

# --- 병렬 실행 후 결과를 취합할 에이전트 ---
aggregator_agent = Agent(
    name="AggregatorAgent",
    model=llm,
    instruction="""Combine these three research findings into a single executive summary:
    Technology Trends: {tech_research}
    Health Breakthroughs: {health_research}
    Finance Innovations: {finance_research}
    Your summary should highlight common themes. The final summary should be around 200 words.""",
    output_key="executive_summary",
)

# 1. 병렬 에이전트 (3개 리서치 동시 실행)
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[tech_researcher, health_researcher, finance_researcher],
)

# 2. 순차 에이전트 (병렬 실행 -> 취합 실행)
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_research_team, aggregator_agent],
)

async def main():
    print("--- 3. 병렬 워크플로우 (Section 4) 실행 ---")
    runner = InMemoryRunner(agent=root_agent, app_name="agents")
    response = await runner.run_debug(
        "Run the daily executive briefing on Tech, Health, and Finance"
    )
    print(f"\n--- 최종 결과 (executive_summary) ---\n{response}")
    print("--- 실행 완료 ---")

if __name__ == "__main__":
    asyncio.run(main())