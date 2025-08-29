#!/usr/bin/env python3
"""
CrowdWisdomTrading AI Agent - Main Execution Script
"""
import sys
import os
from pathlib import Path
from config import Config, logger, setup_logging
from main_flow import run_crowdwisdom_flow
from llm_integration import mistral_integration

def print_banner():
    print("CrowdWisdomTrading AI Agent\n")

def check_prerequisites():
    logger.info("Checking prerequisites...")
    if not Config.MISTRAL_API_KEY:
        print("MISTRAL_API_KEY missing in .env file")
        return False
    return True

def display_results(final_state):
    print("\nExecution Results")
    if final_state.flow_success:
        print("✅ STATUS: SUCCESS")
        print(f"\nFiles:\n- CSV: {final_state.csv_file_path}\n- Log: {Config.OUTPUT_DIR / 'crowdwisdom_trading.log'}")
    else:
        print("⚠️ STATUS: ISSUES ENCOUNTERED")
        for error in final_state.errors_encountered:
            print(f"- {error.get('phase', 'Unknown')}: {error.get('error', 'Unknown error')}")

def main():
    print_banner()
    setup_logging()
    if not check_prerequisites():
        sys.exit(1)
    final_state = run_crowdwisdom_flow()
    display_results(final_state)
    sys.exit(0 if final_state.flow_success else 1)

if __name__ == "__main__":
    main()
