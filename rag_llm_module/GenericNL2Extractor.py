import logging
from rag_llm_module.BaseNL2Service import BaseNL2Service
from prompt_generator.BasePromptGenerator import BasePromptGenerator

logger = logging.getLogger(__name__)

class GenericNL2Extractor(BaseNL2Service):
    """通用的自然語言萃取服務，繼承自 BaseNL2Service，套用依賴注入"""
    
    def __init__(self, llm_connector, parser, prompt_generator: BasePromptGenerator, expected_key: str):
        # 1. 將共用資源 (llm, parser, expected_key) 往上傳遞給父類別
        super().__init__(llm_connector, parser, expected_key)
        
        # 2. 把外部注入的 prompt_generator 存起來
        self._prompt_generator = prompt_generator

    # 3. 實作父類別 (BaseNL2Service) 規定的抽象方法
    def get_generator(self) -> BasePromptGenerator:
        return self._prompt_generator

    # 💡 亮點：這裡「完全不需要」寫 execute() 方法！
    # 因為當你在 main.py 呼叫 step1_service.execute() 時，
    # Python 會自動去執行 BaseNL2Service 裡面那個包含「組裝、打API、印Debug、驗證JSON」的完美流程！