class BusinessLogicFilter:
    """filter Business Logic data"""
    def __init__(self, retriever):
        self.retriever = retriever
        # According to Reggie's README, Business Logic uses the BPC dataset.
        self.target_collection = "bpc_finance" # or using bpc_medical ...etc

    def get_clean_examples(self, query_text: str, top_k: int = 3) -> list:
        raw_results = self.retriever.search(query_text, self.target_collection, top_k)
        
        clean_rag_examples = []
        for item in raw_results:
            # Assuming the data structure of BPC is also contained within the output.
            if "output" in item:
                clean_rag_examples.append(item["output"])
                
        print(f"[Filter] BusinessLogic successfully {len(clean_rag_examples)} pieces of data")
        return clean_rag_examples