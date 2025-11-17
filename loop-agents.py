import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
from google.genai import types

load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    print("오류: GOOGLE_API_KEY가 .env 파일에 없습니다.")
    exit()

retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

llm = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)


# --- 루프 탈출을 위한 Python 함수 ---
def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}


# 1. 초안 작성 (루프 시작 전 1회 실행)
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=llm,
    instruction="Based on the user's prompt, write the first draft of a short story (around 100-150 words).",
    output_key="current_story",
)

# --- 루프에서 반복 실행될 에이전트 2개 ---

# 2. 비평가 에이전트
critic_agent = Agent(
    name="CriticAgent",
    model=llm,
    instruction="""You are a constructive story critic. Review the story provided below.
    Story: {current_story}

    Evaluate the story's plot, characters, and pacing.
    - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
    output_key="critique",
)

# 3. 수정자 에이전트 (비평을 보고 'exit_loop'를 부를지, 스토리를 수정할지 결정)
refiner_agent = Agent(
    name="RefinerAgent",
    model=llm,
    instruction="""You are a story refiner. You have a story draft and critique.
    Story Draft: {current_story}
    Critique: {critique}

    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
    output_key="current_story",  # 수정된 스토리로 덮어쓰기
    tools=[FunctionTool(exit_loop)],  # exit_loop 함수를 도구로 제공
)

# 4. 루프 에이전트 (비평 -> 수정) 2회 반복
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,  # 최대 2번 반복 (무한 루프 방지)
)

# 5. 순차 에이전트 (초안 작성 -> 루프 시작)
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
)


async def main():
    print("--- 4. 루프 워크플로우 (Section 5) 실행 ---")
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug(
        "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map"
    )
    print("--- 실행 완료 ---")
    # 최종 결과는 루프가 끝난 후의 "current_story"입니다.


if __name__ == "__main__":
    asyncio.run(main())