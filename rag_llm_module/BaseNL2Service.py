import logging
from abc import ABC, abstractmethod
from prompt_generator.BasePromptGenerator import BasePromptGenerator

logger = logging.getLogger(__name__) # 加入這行

class BaseNL2Service(ABC):
    def __init__(self, llm_connector, parser, expected_key: str):
        self.llm = llm_connector
        self.parser = parser
        self.expected_key = expected_key

    @abstractmethod
    def get_generator(self) -> BasePromptGenerator: pass

    def execute(self, input_text: str, top_k_examples: list) -> dict:
        generator = self.get_generator()
        prompt = generator.generate(top_k_examples, input_text)
        
        raw_response = self.llm.post_to_llm(prompt)
        
        # 🚨 全部改用 logger.debug，確保它能跟 main.py 的日誌對齊印出
        logger.debug("\n" + "="*40 + f"\n[LLM Raw Response]:\n{repr(raw_response)}\n" + "="*40)
        
        return self.parser.sanitize_json(raw_response, expected_key=self.expected_key)