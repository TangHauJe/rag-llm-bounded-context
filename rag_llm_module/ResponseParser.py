import json
import re
import logging

logger = logging.getLogger(__name__)

class ResponseParser:
    """Responsible for accurately extracting JSON from the raw text returned by the model."""
    
    # expected_key: str
    def sanitize_json(self, raw_text: str, expected_key: str) -> dict:
        extracted_jsons = []
        
        md_match = re.search(r'```json\s*\n(.*?)\n```', raw_text, re.DOTALL | re.IGNORECASE)
        if md_match:
            try:
                extracted_jsons.append(json.loads(md_match.group(1)))
            except json.JSONDecodeError:
                pass
                
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

        # filter with expected_key
        for json_obj in extracted_jsons:
            if isinstance(json_obj, dict):
                if expected_key in json_obj:
                    return json_obj
                    
        logger.warning(f"[Parser Error] Can't find expected Key: '{expected_key}'。")
        return {"error": "Invalid JSON format"}