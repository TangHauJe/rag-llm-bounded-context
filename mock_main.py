import logging
import json

from logger_config import setup_logger
setup_logger()
logger = logging.getLogger(__name__)

from rag_llm_module.LLMConnector import LLMConnector
from rag_llm_module.ResponseParser import ResponseParser
from rag_llm_module.GenericNL2Extractor import GenericNL2Extractor

from filters.MockFilters import (
    BusinessLogicMockFilter, DomainEventsMockFilter, CommandsMockFilter,
    ActorsMockFilter, CommandEventPairsMockFilter, PoliciesMockFilter
)

from prompt_generator.BusinessLogicPromptGenerator import BusinessLogicPromptGenerator
from prompt_generator.DomainEventsPromptGenerator import DomainEventsPromptGenerator
from prompt_generator.CommandsPromptGenerator import CommandsPromptGenerator
from prompt_generator.ActorsPromptGenerator import ActorsPromptGenerator
from prompt_generator.CommandEventPairsPromptGenerator import CommandEventPairsPromptGenerator
from prompt_generator.PoliciesPromptGenerator import PoliciesPromptGenerator


def load_use_case(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()


if __name__ == "__main__":
    logger.info("System initialization in progress...")

    # ==================================================
    # Core Dependency Injection: All resources are instantiated only once
    # ==================================================
    llm_connector = LLMConnector() # 確保裡面是最新的 API 設定與 Port
    response_parser = ResponseParser()
    
    raw_user_input = load_use_case("test_case1.txt")
    logger.info(f"Input Use Case: {raw_user_input}")

    # ==================================================
    # Step 1: Business Logic
    # ==================================================
    logger.info("\n=== Step 1: Business Logic ===")
    s1_filter = BusinessLogicMockFilter()
    s1_service = GenericNL2Extractor(llm_connector, response_parser, BusinessLogicPromptGenerator(), "BusinessLogic")
    
    logic_out = s1_service.execute(raw_user_input, s1_filter.get_clean_examples())
    logger.info(f"S1 output:\n{json.dumps(logic_out, indent=2, ensure_ascii=False)}")
    clean_logic = ", ".join(logic_out.get("BusinessLogic", []))
    logger.info(f"S1 trans: {clean_logic}")

    # ==================================================
    # Step 2: Domain Events
    # ==================================================
    logger.info("\n=== Step 2: Domain Events ===")
    s2_filter = DomainEventsMockFilter()
    s2_service = GenericNL2Extractor(llm_connector, response_parser, DomainEventsPromptGenerator(), "DomainEvents")
    
    events_out = s2_service.execute(clean_logic, s2_filter.get_clean_examples())
    logger.info(f"S2 output:\n{json.dumps(events_out, indent=2, ensure_ascii=False)}")
    clean_events = ", ".join(events_out.get("DomainEvents", []))
    logger.info(f"S2 trans: {clean_events}")

    # ==================================================
    # Step 3: Commands
    # ==================================================
    logger.info("\n=== Step 3: Commands ===")
    s3_filter = CommandsMockFilter()
    s3_context = f"Business Logic: {clean_logic} | Domain Events: {clean_events}"
    s3_service = GenericNL2Extractor(llm_connector, response_parser, CommandsPromptGenerator(), "Commands")
    
    commands_out = s3_service.execute(s3_context, s3_filter.get_clean_examples())
    logger.info(f"S3 output:\n{json.dumps(commands_out, indent=2, ensure_ascii=False)}")
    clean_commands = ", ".join(commands_out.get("Commands", []))
    logger.info(f"S3 trans: {clean_commands}")

    # ==================================================
    # Step 4: Actors
    # ==================================================
    logger.info("\n=== Step 4: Actors ===")
    s4_filter = ActorsMockFilter()
    s4_context = f"Commands: {clean_commands}"
    s4_service = GenericNL2Extractor(llm_connector, response_parser, ActorsPromptGenerator(), "Actors")
    
    actors_out = s4_service.execute(s4_context, s4_filter.get_clean_examples())
    logger.info(f"S4 JSON:\n{json.dumps(actors_out, indent=2, ensure_ascii=False)}")

    # ==================================================
    # Step 5: Command/Event Pairs
    # ==================================================
    logger.info("\n=== Step 5: Command/Event Pairs ===")
    s5_filter = CommandEventPairsMockFilter()
    s5_context = f"Commands: {clean_commands} | Domain Events: {clean_events}"
    s5_service = GenericNL2Extractor(llm_connector, response_parser, CommandEventPairsPromptGenerator(), "CommandEventPairs")
    
    pairs_out = s5_service.execute(s5_context, s5_filter.get_clean_examples())
    logger.info(f"S5 JSON:\n{json.dumps(pairs_out, indent=2, ensure_ascii=False)}")

    # ==================================================
    # Step 6: Policies
    # ==================================================
    logger.info("\n=== Step 6: Policies ===")
    s6_filter = PoliciesMockFilter()
    s6_context = f"Pairs: {json.dumps(pairs_out.get('CommandEventPairs', []))}"
    s6_service = GenericNL2Extractor(llm_connector, response_parser, PoliciesPromptGenerator(), "Policies")
    
    policies_out = s6_service.execute(s6_context, s6_filter.get_clean_examples())
    logger.info(f"S6 JSON:\n{json.dumps(policies_out, indent=2, ensure_ascii=False)}")