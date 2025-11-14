import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
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

# 1. Outline Agent
outline_agent = Agent(
    name="OutlineAgent",
    model=llm,
    instruction="""Create a blog outline for the given topic with:
    1. A catchy headline
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each
    4. A concluding thought""",
    output_key="blog_outline",
)

# 2. Writer Agent
writer_agent = Agent(
    name="WriterAgent",
    model=llm,
    instruction="""Following this outline strictly: {blog_outline}
    Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
    output_key="blog_draft",
)

# 3. Editor Agent
editor_agent = Agent(
    name="EditorAgent",
    model=llm,
    instruction="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
    output_key="final_blog",
)

# 4. Sequential Agent (작업 파이프라인)
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)

async def main():
    print("--- 2. 순차 워크플로우 (Section 3) 실행 ---")
    runner = InMemoryRunner(agent=root_agent, app_name="agents")
    response = await runner.run_debug(
        "Write a blog post about the benefits of multi-agent systems for software developers"
    )
    print(f"\n--- 최종 결과 (final_blog) ---\n{response}")
    print("--- 실행 완료 ---")

if __name__ == "__main__":
    asyncio.run(main())