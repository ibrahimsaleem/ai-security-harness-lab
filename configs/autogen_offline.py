# Offline AutoGen check using the replay model client (no API calls).
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.replay import ReplayChatCompletionClient

async def main():
    agent = AssistantAgent("triage", model_client=ReplayChatCompletionClient(["Finding confirmed: SQLi in db.py"]))
    r = await agent.run(task="Triage lab-sqli-string-format")
    assert "SQLi" in r.messages[-1].content
    print("autogen offline OK:", r.messages[-1].content)
asyncio.run(main())
