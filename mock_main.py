import logging
import json
from rag_llm_module.LLMConnector import LLMConnector
from rag_llm_module.ResponseParser import ResponseParser
from rag_llm_module.GenericNL2Extractor import GenericNL2Extractor
from filters.MockFilter import MockFilter

# 引入所有 Prompt Generators
from prompt_generator.BusinessLogicPromptGenerator import BusinessLogicPromptGenerator
from prompt_generator.DomainEventsPromptGenerator import DomainEventsPromptGenerator
from prompt_generator.CommandsPromptGenerator import CommandsPromptGenerator
from prompt_generator.ActorsPromptGenerator import ActorsPromptGenerator
from prompt_generator.CommandEventPairsPromptGenerator import CommandEventPairsPromptGenerator
from prompt_generator.PoliciesPromptGenerator import PoliciesPromptGenerator

# 設定 Logging: 將 DEBUG 改為 INFO 即可隱藏繁瑣的過程訊息
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)-8s | %(message)s')
logger = logging.getLogger(__name__)

def load_use_case(file_path: str) -> str:
    # 模擬讀取 (這裡直接回傳字串方便測試)
    return "When a customer places a food order, the system must process the payment successfully. After that, the kitchen is notified to prepare the meal."

if __name__ == "__main__":
    logger.info("系統初始化中...")

    # 🌟 依賴注入核心：只建立一次實體
    llm_connector = LLMConnector()
    response_parser = ResponseParser()
    mock_filter = MockFilter()

    raw_user_input = load_use_case("test_case3.txt")
    logger.info(f"輸入文本: {raw_user_input}")

    # ==================================================
    # Step 1: Business Logic
    # ==================================================
    logger.info("\n=== Step 1: Business Logic ===")
    s1_examples = mock_filter.get_clean_examples("BusinessLogic")
    s1_service = GenericNL2Extractor(llm_connector, response_parser, BusinessLogicPromptGenerator(), "BusinessLogic")
    
    logic_out = s1_service.execute(raw_user_input, s1_examples)
    clean_logic = ", ".join(logic_out.get("BusinessLogic", []))
    logger.info(f"✅ S1 輸出: {clean_logic}")

    # ==================================================
    # Step 2: Domain Events
    # ==================================================
    logger.info("\n=== Step 2: Domain Events ===")
    s2_examples = mock_filter.get_clean_examples("DomainEvents")
    s2_service = GenericNL2Extractor(llm_connector, response_parser, DomainEventsPromptGenerator(), "DomainEvents")
    
    events_out = s2_service.execute(clean_logic, s2_examples)
    clean_events = ", ".join(events_out.get("DomainEvents", []))
    logger.info(f"✅ S2 輸出: {clean_events}")

    # ==================================================
    # Step 3: Commands
    # ==================================================
    logger.info("\n=== Step 3: Commands ===")
    s3_examples = mock_filter.get_clean_examples("Commands")
    s3_context = f"Business Logic: {clean_logic} | Domain Events: {clean_events}"
    s3_service = GenericNL2Extractor(llm_connector, response_parser, CommandsPromptGenerator(), "Commands")
    
    commands_out = s3_service.execute(s3_context, s3_examples)
    clean_commands = ", ".join(commands_out.get("Commands", []))
    logger.info(f"✅ S3 輸出: {clean_commands}")

    # ==================================================
    # Step 4: Actors
    # ==================================================
    logger.info("\n=== Step 4: Actors ===")
    s4_examples = mock_filter.get_clean_examples("Actors")
    s4_context = f"Commands: {clean_commands}"
    s4_service = GenericNL2Extractor(llm_connector, response_parser, ActorsPromptGenerator(), "Actors")
    
    actors_out = s4_service.execute(s4_context, s4_examples)
    logger.info(f"✅ S4 JSON:\n{json.dumps(actors_out, indent=2, ensure_ascii=False)}")

    # ==================================================
    # Step 5: Command/Event Pairs
    # ==================================================
    logger.info("\n=== Step 5: Command/Event Pairs ===")
    s5_examples = mock_filter.get_clean_examples("CommandEventPairs")
    s5_context = f"Commands: {clean_commands} | Domain Events: {clean_events}"
    s5_service = GenericNL2Extractor(llm_connector, response_parser, CommandEventPairsPromptGenerator(), "CommandEventPairs")
    
    pairs_out = s5_service.execute(s5_context, s5_examples)
    logger.info(f"✅ S5 JSON:\n{json.dumps(pairs_out, indent=2, ensure_ascii=False)}")

    # ==================================================
    # Step 6: Policies
    # ==================================================
    logger.info("\n=== Step 6: Policies ===")
    s6_examples = mock_filter.get_clean_examples("Policies")
    s6_context = f"Pairs: {json.dumps(pairs_out.get('CommandEventPairs', []))}"
    s6_service = GenericNL2Extractor(llm_connector, response_parser, PoliciesPromptGenerator(), "Policies")
    
    policies_out = s6_service.execute(s6_context, s6_examples)
    logger.info(f"✅ S6 JSON:\n{json.dumps(policies_out, indent=2, ensure_ascii=False)}")