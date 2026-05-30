from prompt_generator.BasePromptGenerator import BasePromptGenerator

class ActorsPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Identify the Actors (users, systems, or specific roles) who initiate the provided Commands."
        
    def get_rules(self) -> str:
        return (
            "CRITICAL INSTRUCTIONS:\n"
            "1. Output ONLY a valid JSON object matching the exact schema.\n"
            "2. Map each Actor to the Command they execute.\n"
            "3. If a command is triggered automatically, the Actor is usually 'System'.\n"
            "4. DO NOT copy dummy values from the schema."
        )
        
    def get_output_schema(self) -> dict:
        return {
            "Actors": [
                {
                    "Actor": "ExampleRole",
                    "Command": "ExecuteAction"
                }
            ]
        }