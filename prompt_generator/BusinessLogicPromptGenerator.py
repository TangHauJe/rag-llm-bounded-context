from prompt_generator.BasePromptGenerator import BasePromptGenerator

class BusinessLogicPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Analyze the raw user input and extract the core Business Logic, concepts, and triggering conditions clearly and concisely."

    def get_rules(self) -> str:
        return (
            "CRITICAL INSTRUCTIONS:\n"
            "1. You MUST output ONLY a valid JSON object.\n"
            "2. Extract the core business concepts, rules, and conditions (e.g., 'VIP Customers', 'discount conditions').\n"
            "3. DO NOT output step-by-step action sentences, but convert them into a list of key terms.\n"
            "4. DO NOT DROP TRIGGERS: You MUST include the initial preconditions or user actions that start the process (e.g., 'Customer food order', 'Invoice overdue'). These are essential business conditions."
        )

    def get_output_schema(self) -> dict:
        return {
            "BusinessLogic": [
                "VIP Customers",
                "Discounts",
                "Discount Conditions"
            ]
        }