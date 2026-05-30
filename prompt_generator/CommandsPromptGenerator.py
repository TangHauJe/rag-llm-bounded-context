from prompt_generator.BasePromptGenerator import BasePromptGenerator

class CommandsPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Analyze the provided context (Business Logic and Domain Events) and identify the Commands."
        
    def get_rules(self) -> str:
        return (
            "CRITICAL INSTRUCTIONS:\n"
            "1. Output ONLY a valid JSON object matching the exact schema.\n"
            "2. A Command represents an intent or action to be executed.\n"
            "3. A Command MUST be written in PascalCase.\n"
            "4. A Command MUST be expressed as an Imperative Verb Phrase (e.g., 'PlaceOrder', 'ApproveInvoice').\n"
            "5. DO NOT copy the dummy values from the schema."
        )
        
    def get_output_schema(self) -> dict:
        return {
            "Commands": [
                "ExecuteAction",
                "PerformTask"
            ]
        }