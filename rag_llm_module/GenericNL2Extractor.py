from rag_llm_module.BaseNL2Service import BaseNL2Service
from prompt_generator.BasePromptGenerator import BasePromptGenerator

class GenericNL2Extractor(BaseNL2Service):
    """A general-purpose natural language extraction service, inheriting from BaseNL2Service and applying dependency injection."""
    
    def __init__(self, llm_connector, parser, prompt_generator: BasePromptGenerator, expected_key: str):
        # Pass the connector, parser, and expected key up to parent.
        super().__init__(llm_connector, parser, expected_key)
        
        # Stores a dedicated Prompt Generator from external sources.
        self._prompt_generator = prompt_generator

    # Implement the abstract methods specified by the parent class.
    def get_generator(self) -> BasePromptGenerator:
        return self._prompt_generator
