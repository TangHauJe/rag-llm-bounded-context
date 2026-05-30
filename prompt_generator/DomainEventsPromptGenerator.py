from prompt_generator.BasePromptGenerator import BasePromptGenerator

class DomainEventsPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Analyze the provided context and identify the Domain Events (things that have happened in the system)."
        
    def get_rules(self) -> str:
        return (
            "CRITICAL INSTRUCTIONS:\n"
            "1. Output ONLY a valid JSON object matching the exact schema.\n"
            "2. A Domain Event MUST be written in PascalCase.\n"
            "3. A Domain Event MUST be expressed in the Past Tense (e.g., 'OrderPlaced', 'PaymentProcessed').\n"
            "4. DO NOT copy the dummy values from the schema."
        )
        
    def get_output_schema(self) -> dict:
        return {
            "DomainEvents": [
                "ExampleStateChanged",
                "AnotherActionHappened"
            ]
        }