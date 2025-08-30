"""
Custom Web Scraping Tools for CrowdWisdomTrading AI Agent
"""

import json
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
from config import Config, logger
from typing import Type


class WebScrapingToolInput(BaseModel):
    url: str = Field(..., description="URL to scrape")
    site_name: str = Field(..., description="Name of the website")
    max_products: int = Field(default=50, description="Max products to scrape")


class PolygonMarketScraperTool(BaseTool):
    name: str = "PolygonMarketScraper"
    description: str = ("Scrapes prediction market data from Polymarket.com. Returns structured JSON.")

    args_schema: Type[WebScrapingToolInput] = WebScrapingToolInput

    def _run(self, url, site_name, max_products=50):
        try:
            logger.info(f"Starting scraping for {site_name} at {url}")

            chrome_options = Options()
            if Config.HEADLESS_BROWSER:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"--user-agent={Config.USER_AGENT}")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            try:
                driver.get(url)
                time.sleep(random.uniform(3, 7))
                products = []
                if site_name.lower() == "polymarket":
                    products = self._scrape_polymarket(driver, max_products)
                elif site_name.lower() == "kalshi":
                    products = self._scrape_kalshi(driver, max_products)
                else:
                    products = self._scrape_generic(driver, max_products)
                logger.info(f"Successfully scraped {len(products)} products from {site_name}")
                return json.dumps({
                    "site": site_name,
                    "url": url,
                    "products_count": len(products),
                    "products": products,
                    "timestamp": time.time()
                }, indent=2)
            finally:
                driver.quit()
        except Exception as e:
            logger.error(f"Error scraping {site_name}: {str(e)}")
            return json.dumps({
                "site": site_name,
                "url": url,
                "error": str(e),
                "products": [],
                "products_count": 0
            })

    def _scrape_polymarket(self, driver, max_products):
        products = []
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid*='market'], .market-card"))
            )
            market_selectors = [
                "[data-testid*='market']",
                ".market-card"
            ]
            market_elements = []
            for selector in market_selectors:
                market_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if market_elements:
                    break
            if not market_elements:
                market_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='button'], a[href*='market']")
            for i, element in enumerate(market_elements[:max_products]):
                try:
                    title = element.text
                    price_text = element.text
                    product = {
                        "title": title or f"Market {i+1}",
                        "price": price_text,
                        "category": "Unknown",
                        "volume": "",
                        "url": "",
                        "site": "polymarket",
                        "confidence_score": 0.8 if title and price_text else 0.5
                    }
                    products.append(product)
                except Exception as e:
                    logger.warning(f"Error extracting product {i}: {str(e)}")
                    continue
        except Exception as e:
            logger.error(f"Error scraping Polymarket: {str(e)}")
        return products

    def _scrape_kalshi(self, driver, max_products):
        products = []
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            market_selectors = [".market-item", ".event-card"]
            market_elements = []
            for selector in market_selectors:
                market_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if market_elements:
                    break
            if not market_elements:
                market_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='card']")
            for i, element in enumerate(market_elements[:max_products]):
                try:
                    title = element.text
                    price_text = element.text
                    product = {
                        "title": title or f"Kalshi Market {i+1}",
                        "price": price_text,
                        "category": "Prediction",
                        "volume": "",
                        "url": "",
                        "site": "kalshi",
                        "confidence_score": 0.7 if title else 0.4
                    }
                    products.append(product)
                except Exception:
                    continue
        except Exception as e:
            logger.error(f"Error scraping Kalshi: {str(e)}")
        return products

    def _scrape_generic(self, driver, max_products):
        products = []
        try:
            text_elements = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, p, span, div")
            potential_products = []
            for element in text_elements:
                text = element.text.strip()
                if len(text) > 10 and len(text) < 200:
                    potential_products.append(text)
            unique_products = list(set(potential_products))[:max_products]
            for i, title in enumerate(unique_products):
                product = {
                    "title": title,
                    "price": "Unknown",
                    "category": "General",
                    "volume": "",
                    "url": "",
                    "site": "generic",
                    "confidence_score": 0.3
                }
                products.append(product)
        except Exception as e:
            logger.error(f"Error in generic scraping: {str(e)}")
        return products


class MarketDataFallbackTool(BaseTool):
    name: str = "MarketDataFallback"
    description: str = "Fallback web scraping tool using requests and BeautifulSoup."

    args_schema: Type[WebScrapingToolInput] = WebScrapingToolInput

    def _run(self, url, site_name, max_products=50):
        try:
            headers = {
                'User-Agent': Config.USER_AGENT
            }
            response = requests.get(url, headers=headers, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
            for i, heading in enumerate(headings[:max_products]):
                title = heading.get_text(strip=True)
                if len(title) > 5:
                    product = {
                        "title": title,
                        "price": "Unknown",
                        "category": "Market",
                        "volume": "",
                        "url": url,
                        "site": site_name,
                        "confidence_score": 0.4
                    }
                    products.append(product)
            logger.info(f"Fallback scraping found {len(products)} products from {site_name}")
            return json.dumps({
                "site": site_name,
                "url": url,
                "products_count": len(products),
                "products": products,
                "method": "fallback_requests",
                "timestamp": time.time()
            }, indent=2)
        except Exception as e:
            logger.error(f"Fallback scraping failed for {site_name}: {str(e)}")
            return json.dumps({
                "site": site_name,
                "url": url,
                "error": str(e),
                "products": [],
                "products_count": 0,
                "method": "fallback_requests"
            })


SCRAPING_TOOLS = [PolygonMarketScraperTool(), MarketDataFallbackTool()]
