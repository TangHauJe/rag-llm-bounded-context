from prompt_generator.BasePromptGenerator import BasePromptGenerator

class CommandEventPairsPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Identify the cause-and-effect relationships mapping which Command triggers which Domain Event."
    def get_rules(self) -> str:
        return (
            "1. Output ONLY a valid JSON object matching the schema.\n"
            "2. Map the trigger (Command) to the outcome (Domain Event).\n"
            "3. DO NOT copy dummy values."
        )
    def get_output_schema(self) -> dict:
        return {"CommandEventPairs": [{"Command": "ActionTrigger", "Event": "StateChanged"}]}