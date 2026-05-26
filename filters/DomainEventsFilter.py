class DomainEventsFilter:
    """filter Domain Events data"""
    def __init__(self, retriever):
        self.retriever = retriever # inject Retriever
        self.target_collection = "log_domain_events"

    def get_clean_examples(self, query_text: str, top_k: int = 3) -> list:
        # 1. retrieve the original data (Already sorted by Qdrant)
        raw_results = self.retriever.search(query_text, self.target_collection, top_k)
        
        # 2. Precise Extraction: Only append the domain_event field.
        clean_rag_examples = []
        for item in raw_results:
            output_data = item.get("output", {})
            
            # Check if domain_event exists and is not None
            if output_data.get("domain_event") is not None:
                clean_rag_examples.append(output_data["domain_event"])
                
        print(f"[Filter] DomainEvents successfully filtered {len(clean_rag_examples)} pieces of precise data.")
        
        # ===== only for debug =====
        print("\n=== [Debug] 準備餵給 LLM 的 RAG 範例 ===")
        for i, example in enumerate(clean_rag_examples):
            print(f"  [{i+1}] {example}")
        print("========================================\n")
        # ==========================

        return clean_rag_examples