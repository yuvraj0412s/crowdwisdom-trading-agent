"""
LLM Integration for CrowdWisdomTrading AI Agent
Handles Mistral API integration through litellm
"""

import os
from crewai import LLM
import litellm
from config import Config, logger

class MistralLLMIntegration:
    def __init__(self):
        self.setup_litellm()

    def setup_litellm(self):
        os.environ["MISTRAL_API_KEY"] = Config.MISTRAL_API_KEY
        litellm.set_verbose = False
        self.model_name = Config.DEFAULT_MODEL
        logger.info(f"LiteLLM configured with model: {self.model_name}")

    def get_crewai_llm(self, temperature=None):
        return LLM(
            model=self.model_name,
            temperature=temperature or Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            api_key=Config.MISTRAL_API_KEY
        )

    def test_connection(self):
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hello, this is a connection test."}],
                max_tokens=10
            )
            if response and response.choices:
                logger.info("Mistral API connection test successful")
                return True
            return False
        except Exception as e:
            logger.error(f"Mistral API connection test failed: {str(e)}")
            return False

    def get_completion(self, messages, **kwargs):
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=messages,
                temperature=kwargs.get('temperature', Config.TEMPERATURE),
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting completion from Mistral: {str(e)}")
            raise e

mistral_integration = MistralLLMIntegration()
if Config.MISTRAL_API_KEY:
    try:
        mistral_integration.test_connection()
    except Exception as e:
        logger.warning(f"Initial Mistral connection test failed: {str(e)}")
else:
    logger.warning("MISTRAL_API_KEY not found. Please set it in your environment.")
