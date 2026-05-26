import json
from QdrantRetriever import QdrantRetriever
from filters.BusinessLogicFilter import BusinessLogicFilter
from filters.DomainEventsFilter import DomainEventsFilter
from filters.CommandsFilter import CommandsFilter
from rag_llm_module.NL2IdentifyBusinessLogic import NL2IdentifyBusinessLogic
from rag_llm_module.NL2IdentifyDomainEvents import NL2IdentifyDomainEvents
from rag_llm_module.NL2IdentifyCommands import NL2IdentifyCommands

def load_use_case(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

if __name__ == "__main__":
    # 1. start (Retriever)
    db_retriever = QdrantRetriever()

    # 2. equip (Filters)
    logic_filter = BusinessLogicFilter(db_retriever)
    events_filter = DomainEventsFilter(db_retriever)
    # ==== user input ====
    #raw_user_input = "When a customer places a food order, the system must process the payment successfully. After that, the kitchen is notified to prepare the meal."
    raw_user_input = user_input = load_use_case("test_case2.txt")

    print("==================================================")
    print("Pipeline Step 1: NL2IdentifyBusinessLogic")
    print("==================================================")
    
    # Use a filter to retrieve all the data -> feed it to the NL2 service.
    logic_examples = logic_filter.get_clean_examples(raw_user_input)
    step1_service = NL2IdentifyBusinessLogic()
    logic_output = step1_service.execute(raw_user_input, top_k_examples=logic_examples)
    #clean_logic_str = logic_output.get("BusinessLogic", raw_user_input)
    business_logic_list = logic_output.get("BusinessLogic", [])
    clean_logic_str = ", ".join(business_logic_list)

    print(f"\nStep 1 final output JSON:\n{json.dumps(logic_output, indent=2, ensure_ascii=False)}")
    print(f"Clean string passed to the next step: \"{clean_logic_str}\"")

    print("\n==================================================")
    print("Pipeline Step 2: NL2IdentifyDomainEvents")
    print("==================================================")
    
    # Use a filter to retrieve all the data -> feed it to the NL2 service.
    events_examples = events_filter.get_clean_examples(clean_logic_str)
    step2_service = NL2IdentifyDomainEvents()
    events_output = step2_service.execute(clean_logic_str, top_k_examples=events_examples)
    
    events_list = events_output.get("DomainEvents", [])
    clean_events_str = ", ".join(events_list)
    print(f"\nStep 2 final output JSON:\n{json.dumps(events_output, indent=2, ensure_ascii=False)}")

    print("\n==================================================")
    print("Pipeline Step 3: NL2IdentifyCommands")
    print("==================================================")
    
    # 1. Combine the context (use the essence of the first two steps as a query)
    # And, both LLM and Qdrant can see both the "rules" and the "events" simultaneously.
    step3_query_context = f"Business Logic: {clean_logic_str} | Domain Events: {clean_events_str}"
    print(f"Combined Context passed to Step 3: \"{step3_query_context}\"")
    
    # 2. retrieve clean command example
    commands_filter = CommandsFilter(db_retriever)
    command_examples = commands_filter.get_clean_examples(step3_query_context, top_k=3)
    
    # Print out the RAG sample to be fed to the LLM and confirm that the filtration is clean.
    if command_examples:
        print("\n=== [Debug] RAG Examples for Commands ===")
        for i, ex in enumerate(command_examples):
            print(f"  [{i+1}] {ex}")
        print("=========================================\n")
    
    step3_service = NL2IdentifyCommands()
    commands_output = step3_service.execute(step3_query_context, top_k_examples=command_examples)
    
    print(f"\nStep 3 final output JSON:\n{json.dumps(commands_output, indent=2, ensure_ascii=False)}")