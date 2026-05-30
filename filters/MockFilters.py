import logging

logger = logging.getLogger(__name__)

class BusinessLogicMockFilter:
    def get_clean_examples(self, query_text: str = "", top_k: int = 3) -> list:
        logger.debug("Executing BusinessLogicMockFilter")
        examples = [
            "Related Rule: VIP customers get a 10% discount if their order exceeds $200.",
            "Related Rule: When an invoice is overdue by 30 days, automatically add a 5% late fee and suspend the account."
        ]
        return examples[:top_k]

class DomainEventsMockFilter:
    def get_clean_examples(self, query_text: str = "", top_k: int = 3) -> list:
        logger.debug("Executing DomainEventsMockFilter")
        # 嚴格遵守 PascalCase 與 過去式 (Past Tense)
        examples = [
            "OrderPlaced", 
            "InventoryChecked", 
            "OrderConfirmed", 
            "PaymentTaken", 
            "OrderShipped", 
            "UserLoggedIn"
        ]
        return examples[:top_k]

class CommandsMockFilter:
    def get_clean_examples(self, query_text: str = "", top_k: int = 3) -> list:
        logger.debug("Executing CommandsMockFilter")
        # 嚴格遵守 PascalCase 與 祈使句 (Imperative)
        examples = [
            "AddShippingAddress",
            "SetParticipateStatus"
        ]
        return examples[:top_k]

class ActorsMockFilter:
    def get_clean_examples(self, query_text: str = "", top_k: int = 3) -> list:
        logger.debug("Executing ActorsMockFilter")
        examples = [
            "Actor: Customer. Command: AddShippingAddress",
            "Actor: System. Command: SetParticipateStatus"
        ]
        return examples[:top_k]

class CommandEventPairsMockFilter:
    def get_clean_examples(self, query_text: str = "", top_k: int = 3) -> list:
        logger.debug("Executing CommandEventPairsMockFilter")
        examples = [
            "Command: InitiateMeeting -> Event: MeetingMessageSent",
            "Command: SolveConflict -> Event: MeetingDateChanged"
        ]
        return examples[:top_k]

class PoliciesMockFilter:
    def get_clean_examples(self, query_text: str = "", top_k: int = 3) -> list:
        logger.debug("Executing PoliciesMockFilter")
        examples = [
            "WHEN PaymentOverdue THEN BlockAccount",
            "WHEN FormSubmitted THEN DecideAttendingTime"
        ]
        return examples[:top_k]