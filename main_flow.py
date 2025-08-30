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

    def __init__(self):
        super().__init__()
        self.agents = crowd_wisdom_agents
        logger.info("CrowdWisdomTradingFlow initialized")

    @start()
    def initiate_data_collection(self) -> dict:
        logger.info("🚀 Starting CrowdWisdom Trading AI Agent Flow")
        logger.info(f"Flow ID: {self.state.id}")
        self.state.current_phase = "data_collection"

        scraping_tasks = []

        for site_config in Config.TARGET_SITES:
            site_url = f"{site_config['base_url']}{site_config['markets_endpoint']}"

            task_description = f"""
            Scrape prediction market data from {site_config['name']}.

            Target URL: {site_url}
            Site Name: {site_config['name']}

            Instructions:
            1. Navigate to the URL and extract all available prediction markets/products
            2. Focus on extracting market titles, current prices/odds, categories, and any volume data
            3. Return the data in the specified JSON format
            4. If the site is inaccessible or returns errors, document the error but continue
            5. Aim to collect at least 10-20 markets if available

            Use the appropriate scraping tool based on the site's requirements.
            """

            scraping_task = Task(
                description=task_description,
                agent=self.agents.data_collector_agent(),
                expected_output="JSON formatted prediction market data with products array",
                guardrail=GUARDRAILS["validate_scraped_data"]
            )

            scraping_tasks.append({
                "site": site_config['name'],
                "task": scraping_task,
                "url": site_url
            })

        return {
            "scraping_tasks": scraping_tasks,
            "total_sites": len(Config.TARGET_SITES),
            "phase": "data_collection_initiated"
        }

    @listen(initiate_data_collection)
    def execute_data_collection(self, collection_config: dict) -> dict:
        logger.info("📊 Executing data collection from prediction market sites")

        scraped_results = []
        errors = []

        for task_info in collection_config["scraping_tasks"]:
            site_name = task_info["site"]
            task = task_info["task"]

            try:
                logger.info(f"Scraping data from {site_name}")
                site_crew = Crew(
                    agents=[self.agents.data_collector_agent()],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=True
                )
                result = site_crew.kickoff()

                if result:
                    try:
                        if hasattr(result, 'raw'):
                            result_data = json.loads(result.raw) if isinstance(result.raw, str) else result.raw
                        else:
                            result_data = json.loads(str(result)) if isinstance(result, str) else result

                        scraped_results.append({
                            "site": site_name,
                            "data": result_data,
                            "success": True,
                            "products_count": len(result_data.get('products', [])) if isinstance(result_data, dict) else 0
                        })

                    except (json.JSONDecodeError, AttributeError) as e:
                        logger.warning(f"Failed to parse result from {site_name}: {str(e)}")
                        scraped_results.append({
                            "site": site_name,
                            "data": {"products": [], "error": f"Parse error: {str(e)}"},
                            "success": False,
                            "products_count": 0
                        })

            except Exception as e:
                logger.error(f"Error scraping {site_name}: {str(e)}")
                errors.append({
                    "site": site_name,
                    "error": str(e),
                    "phase": "data_collection"
                })

        self.state.scraped_data = scraped_results
        self.state.scraping_errors = errors
        self.state.total_products_collected = sum(r["products_count"] for r in scraped_results)

        logger.info(f"Data collection completed: {self.state.total_products_collected} total products collected")

        return {
            "scraped_results": scraped_results,
            "total_products": self.state.total_products_collected,
            "errors": errors,
            "success_rate": len([r for r in scraped_results if r["success"]]) / len(scraped_results) if scraped_results else 0
        }

    @router(execute_data_collection)
    def route_to_matching(self, collection_results: dict) -> str:
        if collection_results["total_products"] > 0:
            logger.info("✅ Data collection successful, proceeding to product matching")
            return "product_matching"
        else:
            logger.warning("❌ No products collected, proceeding to error handling")
            return "handle_collection_failure"

    @listen("product_matching")
    def execute_product_matching(self) -> dict:
        logger.info("🔍 Executing product matching analysis")
        self.state.current_phase = "product_matching"

        all_products = []
        for result in self.state.scraped_data:
            if result["success"] and "data" in result:
                products = result["data"].get("products", [])
                for product in products:
                    product["source_site"] = result["site"]
                    all_products.append(product)

        if not all_products:
            logger.warning("No products available for matching")
            return {"error": "No products to match", "matched_products": []}

        matching_task = Task(
            description=f"""
            Analyze the collected prediction market data to identify and group similar markets across different platforms.

            You have {len(all_products)} total products from {len(self.state.scraped_data)} different sites.

            Data to analyze:
            {json.dumps(all_products, indent=2)}

            Your task:
            1. Compare products across different sites to find markets that refer to the same underlying event
            2. Group similar/identical markets together
            3. Calculate confidence scores for your matches (0.0 to 1.0)
            4. Analyze price differences across sites for the same markets
            5. Create unified titles for matched product groups

            Focus on finding markets that are clearly about the same event, outcome, or prediction.
            Be conservative with matches - only group together if you're confident they match.
            """,
            agent=self.agents.product_matcher_agent(),
            expected_output="JSON with matched product groups, confidence scores, and analysis summary",
            guardrail=GUARDRAILS["validate_product_matching"]
        )

        try:
            matching_crew = Crew(
                agents=[self.agents.product_matcher_agent()],
                tasks=[matching_task],
                process=Process.sequential,
                verbose=True
            )
            result = matching_crew.kickoff()

            if result:
                if hasattr(result, "raw"):
                    matching_data = json.loads(result.raw) if isinstance(result.raw, str) else result.raw
                else:
                    matching_data = json.loads(str(result)) if isinstance(result, str) else result

                self.state.matched_products = matching_data.get("matched_products", [])
                self.state.unique_products_count = matching_data.get("total_unique_products", 0)
                self.state.matching_confidence = sum(
                    p.get("match_confidence", 0.5) for p in self.state.matched_products
                ) / len(self.state.matched_products) if self.state.matched_products else 0.0

                logger.info(f"Product matching completed: {self.state.unique_products_count} unique product groups identified")

                return {
                    "matched_products": self.state.matched_products,
                    "unique_count": self.state.unique_products_count,
                    "average_confidence": self.state.matching_confidence,
                    "success": True
                }

        except Exception as e:
            logger.error(f"Error in product matching: {str(e)}")
            self.state.errors_encountered.append({
                "phase": "product_matching",
                "error": str(e)
            })

        return {"error": "Product matching failed", "matched_products": []}

    @listen(execute_product_matching)
    def generate_final_csv(self, matching_results: dict) -> dict:
        logger.info("📊 Generating final CSV output")
        self.state.current_phase = "csv_generation"

        if not matching_results.get("success") or not self.state.matched_products:
            logger.warning("No matched products available for CSV generation")
            return {"error": "No data available for CSV generation"}

        csv_task = Task(
            description=f"""
            Create a comprehensive CSV file from the matched prediction market data.

            Matched Products Data:
            {json.dumps(self.state.matched_products, indent=2)}

            Requirements:
            1. Create a CSV with columns:
               - unified_title, category, polymarket_price, kalshi_price,
                 other_site_price, price_difference, sites_available,
                 confidence_level, volume_info, last_updated
            2. Include headers
            3. Handle missing data with "N/A"
            4. Proper CSV escaping
            5. Provide summary of data process

            Start response with CSV content.
            """,
            agent=self.agents.data_organizer_agent(),
            expected_output="Complete CSV content with headers and rows, plus summary",
            guardrail=GUARDRAILS["validate_csv_output"]
        )
        try:
            csv_crew = Crew(
                agents=[self.agents.data_organizer_agent()],
                tasks=[csv_task],
                process=Process.sequential,
                verbose=True
            )
            result = csv_crew.kickoff()

            if result:
                csv_content = result.raw if hasattr(result, "raw") else str(result)
                csv_file_path = Config.CSV_OUTPUT_PATH
                try:
                    with open(csv_file_path, "w", encoding="utf-8") as f:
                        f.write(csv_content)

                    logger.info(f"CSV file saved to: {csv_file_path}")

                    self.state.csv_content = csv_content
                    self.state.csv_file_path = str(csv_file_path)
                    self.state.flow_success = True

                    summary = {
                        "total_sites_scraped": len(Config.TARGET_SITES),
                        "successful_scrapes": len([r for r in self.state.scraped_data if r["success"]]),
                        "total_products_collected": self.state.total_products_collected,
                        "unique_products_identified": self.state.unique_products_count,
                        "average_matching_confidence": round(self.state.matching_confidence, 3),
                        "csv_file_path": str(csv_file_path),
                        "csv_rows_generated": len(csv_content.split("\n")) - 1,
                        "timestamp": datetime.now().isoformat(),
                        "errors": self.state.errors_encountered
                    }
                    self.state.final_summary = summary

                    return {
                        "csv_generated": True,
                        "file_path": str(csv_file_path),
                        "summary": summary,
                        "success": True
                    }

                except IOError as e:
                    logger.error(f"Failed to save CSV file: {str(e)}")
                    return {"error": f"Failed to save CSV: {str(e)}"}

        except Exception as e:
            logger.error(f"Error generating CSV: {str(e)}")
            self.state.errors_encountered.append({
                "phase": "csv_generation",
                "error": str(e)
            })

        return {"error": "CSV generation failed"}

    @listen("handle_collection_failure")
    def handle_collection_failure(self) -> dict:
        logger.warning("🚨 Handling data collection failure")

        error_csv = """unified_title,category,polymarket_price,kalshi_price,other_site_price,price_difference,sites_available,confidence_level,volume_info,last_updated
\"No data collected - See error log\",\"Error\",\"N/A\",\"N/A\",\"N/A\",\"N/A\",\"None\",\"0.0\",\"N/A\",\"{}\"""".format(datetime.now().isoformat())

        try:
            with open(Config.CSV_OUTPUT_PATH, "w", encoding="utf-8") as f:
                f.write(error_csv)
            logger.info(f"Error CSV saved to: {Config.CSV_OUTPUT_PATH}")
        except IOError as e:
            logger.error(f"Failed to save error CSV: {str(e)}")

        self.state.csv_content = error_csv
        self.state.csv_file_path = str(Config.CSV_OUTPUT_PATH)
        self.state.flow_success = False

        return {
            "error_handled": True,
            "csv_generated": True,
            "file_path": str(Config.CSV_OUTPUT_PATH),
            "success": False
        }


def run_crowdwisdom_flow():
    logger.info("🎯 Initializing CrowdWisdom Trading AI Agent")
    flow = CrowdWisdomTradingFlow()
    try:
        logger.info("▶️ Starting flow execution")
        final_result = flow.kickoff()
        logger.info("✅ Flow execution completed")
        logger.info(f"Final Summary: {flow.state.final_summary}")
        if flow.state.flow_success:
            logger.info(f"🎉 SUCCESS: CSV file generated at {flow.state.csv_file_path}")
        else:
            logger.warning("⚠️ Flow completed with errors - check logs and output CSV")
        return flow.state
    except Exception as e:
        logger.error(f"❌ Flow execution failed: {str(e)}")
        raise e


if __name__ == "__main__":
    final_state = run_crowdwisdom_flow()
    print(f"\n🏁 Flow completed. Final state: {final_state.flow_success}")
