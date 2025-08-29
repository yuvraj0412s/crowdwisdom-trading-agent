"""
CrewAI Agents for CrowdWisdomTrading AI Agent
Implements the three main agents for the data pipeline
"""

from crewai import Agent
from tools import SCRAPING_TOOLS
from llm_integration import mistral_integration
from config import Config, logger

class CrowdWisdomAgents:
    """
    Factory class for creating CrewAI agents
    """
    def __init__(self):
        self.llm = mistral_integration.get_crewai_llm()
        logger.info("CrowdWisdom agents initialized with Mistral LLM")

    def data_collector_agent(self):
        """
        Agent 1: Data Collector - Responsible for scraping data
        """
        return Agent(
            role="Senior Data Collection Specialist",
            goal="Scrape prediction market data from multiple gambling/prediction websites efficiently and accurately",
            backstory="You are an expert data collection specialist with deep knowledge of web scraping techniques. You ensure collected data is structured and accurate.",
            tools=SCRAPING_TOOLS,
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300,
            system_template="""
You are a professional data collector specializing in prediction market data.
Your responsibilities:
1. Visit the specified websites and extract product/market information
2. Structure the data in a consistent JSON format
3. Ensure data quality and completeness
4. Handle errors gracefully
Return data in:
{
    "site": "website_name", "url": "scraped_url", "products_count": number,
    "products": [{...}], "timestamp": timestamp
}
If you encounter errors, still return a JSON structure with an error field and empty products array.
"""
        )

    def product_matcher_agent(self):
        """
        Agent 2: Product Matcher - Identify and match similar products
        """
        return Agent(
            role="Senior Market Analysis Specialist",
            goal="Analyze and identify similar prediction markets across different platforms, creating unified product groups",
            backstory="You are a market analysis specialist able to match equivalent markets across platforms like Polymarket, Kalshi, etc.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=4,
            max_execution_time=600,
            system_template="""
You are a market analysis expert specializing in cross-platform prediction market comparison.
Your responsibilities:
1. Analyze market data from multiple websites
2. Identify markets referring to the same event/outcome
3. Group similar/identical markets
4. Assess confidence
Return data in:
{
    "matched_products": [
        {
            "unified_title": "standardized_name",
            "products": [{...}],
            "match_confidence": 0.85,
            "sites": ["site1", "site2"],
            "price_analysis": {"site1_price": "...", "site2_price": "...", "price_difference": "..."}
        }
    ],
    "total_unique_products": number,
    "analysis_summary": "..."
}
Be conservative with matches.
"""
        )

    def data_organizer_agent(self):
        """
        Agent 3: Data Re-arranger/CSV Generator
        """
        return Agent(
            role="Senior Data Organization Specialist",
            goal="Transform matched prediction market data into a clean, organized CSV format for analysis and reporting",
            backstory="You create structured datasets for business analysis from complex, multi-source data.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300,
            system_template="""
You are a data organization expert specializing in business-ready datasets.
Organize matched product data into a comprehensive CSV.
Required columns:
- unified_title, category, polymarket_price, kalshi_price, other_site_price, price_difference,
  sites_available, confidence_level, volume_info, last_updated
Format: comma-separated, include header row, consistent date/time, handle missing data "N/A".
Always start with the actual CSV data.
"""
        )

    def get_all_agents(self):
        return [
            self.data_collector_agent(),
            self.product_matcher_agent(),
            self.data_organizer_agent()
        ]

crowd_wisdom_agents = CrowdWisdomAgents()
