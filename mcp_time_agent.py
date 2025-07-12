import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from agents.run_context import RunContextWrapper


load_dotenv()

async def execute_agent():
    run_context = RunContextWrapper(context=None)
    async with MCPServerStdio(
        cache_tools_list=True,
        params={
          "command": "uvx",
          "args": ["mcp-server-time", "--local-timezone", "America/New_York"],
        }
    ) as server:

        agent=Agent(
            name="Assistant",
            instructions="Use the tools to achieve the tasks.",
            mcp_servers=[server]
        )
        tools = await server.list_tools(run_context, agent)

        result = await Runner.run(agent, "What time is it in New York?")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(execute_agent())