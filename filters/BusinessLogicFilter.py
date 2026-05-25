class BusinessLogicFilter:
    """filter Business Logic data across all BPC domains"""
    def __init__(self, retriever):
        self.retriever = retriever
        # 1. 建立清單：涵蓋睿傑建立的所有產業 BPC (Business Process Corpora) 資料庫
        self.bpc_collections = [
            "bpc_finance",
            "bpc_education",
            "bpc_retail",
            "bpc_medical",
            "bpc_human_resources",
            "bpc_transportation",
            "bpc_insurance",
            "bpc_manufacturing",
            "bpc_logistics"
        ]

    def get_clean_examples(self, query_text: str, top_k: int = 3) -> list:
        all_raw_results = []
        
        # 2. 遍歷搜尋：去每一個產業的資料庫都搜出前 K 名
        for collection in self.bpc_collections:
            try:
                results = self.retriever.search(query_text, collection, top_k)
                all_raw_results.extend(results)
            except Exception as e:
                # 🛡️ 防護網：如果某個資料表剛好被刪除或連線失敗，跳出警告但繼續搜下一個
                print(f"[Warning] Failed to search in {collection}: {e}")
        
        # 3. 全域排序：將所有找出來的結果，依照向量相似度 (score) 由高到低重新排序
        # ⚠️ 注意：這裡假設你的 retriever 回傳的字典裡有 "score" 這個 key。
        # 如果沒有，請確保 QdrantRetriever.search() 有把 score 保留下來！
        all_raw_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        # 4. 菁英決選：只留下全域分數最高的前 K 筆資料
        global_top_k_results = all_raw_results[:top_k]
        
        # 5. 資料清洗：維持你原本的邏輯，只抽出 output 欄位
        clean_rag_examples = []
        for item in global_top_k_results:
            if "output" in item:
                clean_rag_examples.append(item["output"])
                
        print(f"[Filter] BusinessLogic successfully retrieved {len(clean_rag_examples)} pieces of cross-domain data")
        return clean_rag_examples