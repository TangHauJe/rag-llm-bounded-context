from prompt_generator.BasePromptGenerator import BasePromptGenerator

class BusinessLogicPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Analyze the raw user input and extract the core Business Logic clearly and concisely."

    def get_rules(self) -> str:
        return (
            "1. Remove conversational text (e.g., 'Hi', 'Thanks').\n2. Summarize the core operational flow step-by-step.\n"
            "2. DO NOT omit any triggering actions, user inputs, or preconditions."
        )

    def get_output_schema(self) -> dict:
        return {"BusinessLogic": "The cleaned business logic string."}