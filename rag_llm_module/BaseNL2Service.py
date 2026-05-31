from abc import ABC, abstractmethod
from rag_llm_module.LLMConnector import LLMConnector
from rag_llm_module.ResponseParser import ResponseParser
from prompt_generator.BasePromptGenerator import BasePromptGenerator
import logging
logger = logging.getLogger(__name__)

class BaseNL2Service(ABC):
    def __init__(self, llm_connector, parser, expected_key: str):
        self.llm = llm_connector
        self.parser = parser
        self.expected_key = expected_key

    @abstractmethod
    def get_generator(self) -> BasePromptGenerator:
        pass

    def execute(self, input_text: str, top_k_examples: list) -> dict:
        generator = self.get_generator()
        prompt = generator.generate(top_k_examples, input_text)

        max_retries = 3
        
        for attempt in range(max_retries):
            raw_response = self.llm.post_to_llm(prompt)
            
            logger.debug("\n" + "="*40 + f"\n[LLM Raw Response - Attempt {attempt+1}]:\n{repr(raw_response)}\n" + "="*40)
            
            # Cleanup and Analysis
            parsed_result = self.parser.sanitize_json(raw_response, self.expected_key)
            
            if "error" not in parsed_result:
                return parsed_result
                
            logger.warning(f"[Retry {attempt+1}/{max_retries}] Model output format error, call LLM again...")
            
        logger.error(f"[{self.expected_key}] retries still failed...")
        return {self.expected_key: []}