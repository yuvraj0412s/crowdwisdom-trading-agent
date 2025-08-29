# main_flow.py (truncated)
import json
from datetime import datetime
from pathlib import Path

from crewai.flow.flow import Flow, listen, start, router
from crewai import Crew, Task, Process
from pydantic import BaseModel

from config import Config, logger
from agents import crowd_wisdom_agents
from guardrails import GUARDRAILS

class CrowdWisdomState(BaseModel):
    scraped_data: list = []
    scraping_errors: list = []
    total_products_collected: int = 0
    matched_products: list = []
    matching_confidence: float = 0.0
    unique_products_count: int = 0
    csv_content: str = ""
    csv_file_path: str = ""
    final_summary: dict = {}
    current_phase: str = "initialization"
    errors_encountered: list = []
    flow_success: bool = False

class CrowdWisdomTradingFlow(Flow[CrowdWisdomState]):
    # See previous response for full implementation
    pass

def run_crowdwisdom_flow():
    flow = CrowdWisdomTradingFlow()
    final_state = flow.kickoff()
    return flow.state

if __name__ == "__main__":
    final_state = run_crowdwisdom_flow()
    print(f"\n🏁 Flow completed. Final state: {final_state.flow_success}")
