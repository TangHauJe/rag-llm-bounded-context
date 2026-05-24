from prompt_generator.BasePromptGenerator import BasePromptGenerator

class DomainEventsPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        # using "convert" not only extract
        return "Analyze the business logic, identify the key actions, and CONVERT them into Domain Events."

    def get_rules(self) -> str:
        # 
        return (
            "1. You MUST output ONLY a single, valid JSON object. Nothing else.\n"
            "2. DO NOT wrap the JSON in Markdown (e.g., NO ```json ... ```).\n"
            "3. DO NOT output any conversational text, greetings, or explanations.\n"
            "4. DO NOT write or generate any code snippets (JavaScript, Python, etc.).\n"
            "5. You MUST strictly follow the Output Format schema. IGNORE the formatting of the provided examples.\n"
            "--- EXAMPLE ---\n"
            "Input: The system processes payment and notifies the kitchen.\n"
            "Output: {\n  \"DomainEvents\": [\n    \"PaymentProcessed\",\n    \"KitchenNotified\"\n  ]\n}\n"
            "---------------"
        )

    def get_output_schema(self) -> dict:
        return {"DomainEvents": ["Event1", "Event2"]}