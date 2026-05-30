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
        
        # call the llm
        raw_response = self.llm.post_to_llm(prompt)
        
        # Force print the original LLM response (use repr to display hidden characters)
        logger.debug("\n" + "="*40 + f"\n[LLM Raw Response]:\n{repr(raw_response)}\n" + "="*40)
        
        return self.parser.sanitize_json(raw_response)