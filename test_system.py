#!/usr/bin/env python3
"""
Test Script for CrowdWisdomTrading AI Agent
Tests basic functionality and configuration
"""
import sys
from config import Config, logger
from llm_integration import mistral_integration
from tools import SCRAPING_TOOLS
from agents import crowd_wisdom_agents
from guardrails import GUARDRAILS
from main_flow import CrowdWisdomTradingFlow

def main():
    print("System Test")
    assert Config.MISTRAL_API_KEY, "Missing Mistral API key"
    assert Config.OUTPUT_DIR.exists(), "Missing output directory"
    assert SCRAPING_TOOLS, "No scraping tools found"
    assert crowd_wisdom_agents.data_collector_agent(), "Data collector missing"
    assert GUARDRAILS['validate_scraped_data'], "Guardrails missing"
    assert CrowdWisdomTradingFlow(), "Flow creation failed"
    print("All tests passed.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
