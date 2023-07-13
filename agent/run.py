import asyncio
import datetime

from typing import List, Dict
from config import check_openai_api_key
from agent.research_agent import ResearchAgent



async def run_agent(task, report_type, agent):
    check_openai_api_key()

    start_time = datetime.datetime.now()


    assistant = ResearchAgent(task, agent)
    await assistant.conduct_research()

    report = await assistant.write_report(report_type)

    
    end_time = datetime.datetime.now()

    print(f"Time taken to complete research: {end_time - start_time}")
    print(f"Report: {report}")
    return report
