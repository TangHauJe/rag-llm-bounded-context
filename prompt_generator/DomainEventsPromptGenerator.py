from prompt_generator.BasePromptGenerator import BasePromptGenerator

class DomainEventsPromptGenerator(BasePromptGenerator):
    def get_task(self) -> str:
        return "Analyze the business logic, identify all state changes (including initial triggers), and CONVERT them into Domain Events."

    def get_rules(self) -> str:
        return (
            "CRITICAL INSTRUCTIONS:\n"
            "1. You MUST output ONLY a single, valid JSON object. Nothing else.\n"
            "2. DO NOT wrap the JSON in Markdown (e.g., NO ```json ... ```).\n"
            "3. DO NOT output any conversational text or explanations.\n"
            "4. Domain Events MUST be written in PascalCase and PAST TENSE verbs (e.g., 'OrderPlaced', 'PaymentProcessed'). DO NOT use nouns like 'KitchenNotification'.\n"
            "5. CAREFULLY analyze preconditions, triggers, or user actions. These represent state changes and MUST be extracted as Domain Events (e.g., 'Customer food order' -> 'OrderPlaced'). DO NOT ignore the first action that starts the workflow."
        )

    def get_output_schema(self) -> dict:
        return {
            "DomainEvents": [
                "OrderPlaced",
                "EventCompleted"
            ]
        }