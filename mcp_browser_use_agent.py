import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from agents.run_context import RunContextWrapper
from agents import set_default_openai_client, set_tracing_disabled, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv()

external_client = AsyncOpenAI(
    base_url = 'https://api.moonshot.ai/v1',
    api_key =os.getenv("KIMI_API_KEY"),
)
model=OpenAIChatCompletionsModel(model="kimi-latest", openai_client=external_client)

async def execute_agent():
    run_context = RunContextWrapper(context=None)
    async with MCPServerStdio(
        cache_tools_list=True,
        params={
          "command": "npx",
          "args": ["@playwright/mcp@latest"],
        },
        client_session_timeout_seconds= 120,
    ) as server:

        agent=Agent(
            model=model,
            name="Assistant",
            instructions="Use browser and other tools to achieve the tasks.",
            mcp_servers=[server]
        )
        tools = await server.list_tools(run_context, agent)

        result = await Runner.run(agent, "go to sina.com and get me today's news headlines")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(execute_agent())