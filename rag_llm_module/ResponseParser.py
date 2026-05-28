import json
import re
import logging

logger = logging.getLogger(__name__)

class ResponseParser:
    """Responsible for accurately extracting JSON from the raw text returned by the model."""
    
    # 🌟 升級：加入 expected_key 參數
    def sanitize_json(self, raw_text: str, expected_key: str) -> dict:
        extracted_jsons = []
        
        # Strategy A: Prioritize JSON within Markdown tags
        md_match = re.search(r'```json\s*\n(.*?)\n```', raw_text, re.DOTALL | re.IGNORECASE)
        if md_match:
            try:
                extracted_jsons.append(json.loads(md_match.group(1)))
            except json.JSONDecodeError:
                pass
                
        # Strategy B: A JSON Scanner
        decoder = json.JSONDecoder()
        pos = 0
        while True:
            match = raw_text.find('{', pos)
            if match == -1:
                break
            try:
                result, index = decoder.raw_decode(raw_text[match:])
                extracted_jsons.append(result)
                pos = match + index
            except json.JSONDecodeError:
                pos = match + 1

        # ==========================================
        # Step 2: Dynamic Validation (動態校驗)
        # ==========================================
        for json_obj in extracted_jsons:
            if isinstance(json_obj, dict):
                # 🌟 精準打擊：只找我們這一步預期的 Key
                if expected_key in json_obj:
                    return json_obj
                    
        # 若找不到預期的 Key，印出警告
        logger.warning(f"[Parser Error] 找不到預期的 Key: '{expected_key}'。")
        return {"error": "Invalid JSON format"}