# test_agent.py
import asyncio
from agent import run_compliance_agent

async def main():
    text = """
    We use a local LLM to generate financial reports.
    No audit logs exist.
    No human approval before sending to clients.
    Sensitive data stored in shared cloud folders.
    """
    result = await run_compliance_agent(text)
    print(result)

asyncio.run(main())
