from prompt_generator.BasePromptGenerator import BasePromptGenerator

class BusinessLogicPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Analyze the raw user input and extract the core Business Logic, concepts, and triggering conditions clearly and concisely."
        
    def get_rules(self) -> str:
        return (
            "CRITICAL INSTRUCTIONS:\n"
            "1. Output ONLY a valid JSON object matching the exact schema.\n"
            "2. Extract the key business rules, policies, and concepts (e.g., thresholds, roles, specific logic).\n"
            "3. DO NOT copy the dummy values from the schema. Generate your own array of strings based on the input."
        )
        
    def get_output_schema(self) -> dict:
        return {
            "BusinessLogic": [
                "Example Rule or Concept 1",
                "Example Condition 2"
            ]
        }