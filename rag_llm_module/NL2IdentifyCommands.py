from rag_llm_module.BaseNL2Service import BaseNL2Service
from prompt_generator.BasePromptGenerator import BasePromptGenerator
from prompt_generator.CommandsPromptGenerator import CommandsPromptGenerator

class NL2IdentifyCommands(BaseNL2Service):
    def get_generator(self) -> BasePromptGenerator:
        return CommandsPromptGenerator()