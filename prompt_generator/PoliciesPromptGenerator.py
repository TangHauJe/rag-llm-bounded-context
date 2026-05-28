from prompt_generator.BasePromptGenerator import BasePromptGenerator

class PoliciesPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Identify the business rules (Policies) that dictate 'WHEN an event happens, THEN a command is triggered'."
    def get_rules(self) -> str:
        return (
            "1. Output ONLY a valid JSON object matching the schema.\n"
            "2. Format policies as 'WHEN [Event] THEN [Command]'.\n"
            "3. DO NOT copy dummy values."
        )
    def get_output_schema(self) -> dict:
        return {"Policies": [{"WhenEvent": "ExampleEventOccurred", "ThenCommand": "ExecuteResponseAction"}]}