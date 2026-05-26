class CommandsFilter:
    """Filter Commands data across MTOP and LOG domains"""
    def __init__(self, retriever):
        self.retriever = retriever
        # Target database: A combination of MTOP and LOG command datasets
        self.target_collections = [
            "mtop_commands",
            "log_commands"
        ]

    def get_clean_examples(self, query_text: str, top_k: int = 3) -> list:
        all_raw_results = []
        
        # search cross database
        for collection in self.target_collections:
            try:
                results = self.retriever.search(query_text, collection, top_k)
                all_raw_results.extend(results)
            except Exception as e:
                print(f"[Warning] Failed to search in {collection}: {e}")
                
        # sort by distance (score)
        all_raw_results.sort(key=lambda x: x.get("distance", 0), reverse=True)
        global_top_k_results = all_raw_results[:top_k]
        
        # Only extracts the command field from the output.
        clean_rag_examples = []
        for item in global_top_k_results:
            output_data = item.get("output", {})
            command_text = output_data.get("command")
            
            # Ensure the command field exists and is not None.
            if command_text is not None:
                clean_rag_examples.append(command_text)
                
        print(f"[Filter] Commands successfully retrieved {len(clean_rag_examples)} precise examples.")
        return clean_rag_examples