from prompt_generator.BasePromptGenerator import BasePromptGenerator

class ActorsPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Identify the actors (users, systems, or roles) who initiate the provided Commands."
    def get_rules(self) -> str:
        return (
            "1. Output ONLY a valid JSON object matching the exact schema.\n"
            "2. Map each Actor to the Command they execute.\n"
            "3. DO NOT copy dummy values from the schema."
        )
    def get_output_schema(self) -> dict:
        return {"Actors": [{"Actor": "ExampleRole", "Command": "ExecuteAction"}]}