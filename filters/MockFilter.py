import logging

logger = logging.getLogger(__name__)

class MockFilter:
    """提供全管線 (Step 1~6) 的 RAG 假資料，用於隔離測試 LLM Prompts"""
    
    def get_clean_examples(self, step_name: str, top_k: int = 3) -> list:
        examples = []
        
        # ==========================================
        # Step 1 ~ 3: 基礎 DDD 元素 (你負責設計與改良的格式)
        # ==========================================
        
        if step_name == "BusinessLogic":
            # 加上 "Related Rule:" 前綴，防止 LLM 把這當成真正的指令
            examples = [
                "Related Rule: VIP customers get a 10% discount if their order exceeds $200.",
                "Related Rule: When an invoice is overdue by 30 days, automatically add a 5% late fee."
            ]
            
        elif step_name == "DomainEvents":
            # 嚴格遵守 PascalCase 與 過去式 (Past Tense)
            # 參考之前你 Debug 撈出來的會議系統與購物範例
            examples = [
                "OrderPlaced",
                "MeetingLevelUpdated",
                "FormReceived"
            ]
            
        elif step_name == "Commands":
            # 嚴格遵守 PascalCase 與 祈使句 (Imperative)
            examples = [
                "PlaceOrder",
                "UpdateMeetingLevel",
                "AddShippingAddress"
            ]
            
        # ==========================================
        # Step 4 ~ 6: 進階關聯元素 (來自 Sal 投影片的完美範例)
        # ==========================================
            
        elif step_name == "Actors":
            # 來自 PDF Slide 6
            examples = [
                "Actor: Customer. Command: AddShippingAddress",
                "Actor: System. Command: SetParticipateStatus"
            ]
            
        elif step_name == "CommandEventPairs":
            # 來自 PDF Slide 2 (Causal Relation) & 7
            examples = [
                "Command: InitiateMeeting -> Event: MeetingMessageSent",
                "Command: SolveConflict -> Event: MeetingDateChanged"
            ]
            
        elif step_name == "Policies":
            # 來自 PDF Slide 8
            examples = [
                "WHEN PaymentOverdue THEN BlockAccount",
                "WHEN FormSubmitted THEN DecideAttendingTime"
            ]
            
        else:
            logger.warning(f"[MockFilter] 找不到對應 '{step_name}' 的假資料設定！")
            
        logger.debug(f"[MockFilter] 成功為 {step_name} 載入 {len(examples[:top_k])} 筆完美測試範例。")
        return examples[:top_k]