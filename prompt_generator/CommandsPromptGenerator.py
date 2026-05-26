from prompt_generator.BasePromptGenerator import BasePromptGenerator

class CommandsPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Analyze the business logic and domain events, identify user intents or system actions, and CONVERT them into Commands."

    def get_rules(self) -> str:
        return (
            "CRITICAL INSTRUCTIONS:\n"
            "1. Output ONLY a valid JSON object matching the exact schema. No markdown, no preambles, no explanations.\n"
            "2. A Command represents an intent or a request to do something (e.g., a user clicking a button or making an API call).\n"
            "3. Convert every identified intent into an IMPERATIVE verb phrase in PascalCase (e.g., 'PlaceOrder', 'ApproveInvoice', 'UpdateProfile').\n"
            "4. DO NOT copy the dummy values from the output schema. You MUST generate commands strictly based on the provided input text."
        )

    def get_output_schema(self) -> dict:
        # Abstract Schema: Use meaningless dummy actions to prevent LLM from being copied randomly.
        return {
            "Commands": [
                "ExecuteActionA",
                "PerformTaskB",
                "ProcessEntityC"
            ]
        }