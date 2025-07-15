import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from agents.run_context import RunContextWrapper
from agents import set_default_openai_client, set_tracing_disabled, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv()


model=OpenAIChatCompletionsModel(model="qwen3:8b", 
                                openai_client=AsyncOpenAI(base_url="http://localhost:11434/v1"))

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

        result = await Runner.run(agent, "search what labubu is")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(execute_agent())