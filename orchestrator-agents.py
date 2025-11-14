import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search
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

# 1. Research Agent (팀원)
research_agent = Agent(
    name="ResearchAgent",
    model=llm,
    instruction="""You are a specialized research agent. Your only job is to use the
    google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
    tools=[google_search],
    output_key="research_findings",
)

# 2. Summarizer Agent (팀원)
summarizer_agent = Agent(
    name="SummarizerAgent",
    model=llm,
    instruction="""Read the provided research findings: {research_findings}
    Create a concise summary as a bulleted list with 3-5 key points.""",
    output_key="final_summary",
)

# 3. Root Coordinator (팀장)
root_agent = Agent(
    name="ResearchCoordinator",
    model=llm,
    instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
    1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
    2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
    3. Finally, present the final summary clearly to the user as your response.""",
    tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
)

async def main():
    print("--- 1. LLM 오케스트레이터 (Section 2) 실행 ---")
    runner = InMemoryRunner(agent=root_agent, app_name="agents")
    response = await runner.run_debug(
        "What are the latest advancements in quantum computing and what do they mean for AI?"
    )
    print("--- 실행 완료 ---")
    # 최종 응답은 response 변수에 저장되지만, run_debug는 과정을 모두 출력합니다.

if __name__ == "__main__":
    asyncio.run(main())