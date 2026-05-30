import logging

def setup_logger():
    # 設定基本的 logging 格式
    log_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    
    # 建立 logger
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=[
            # 將 DEBUG 以上的詳細訊息寫入 pipeline_debug.log 檔案
            logging.FileHandler("pipeline_debug.log", encoding='utf-8'),
            # 在終端機只顯示 INFO 以上的訊息，保持畫面乾淨
            logging.StreamHandler()
        ]
    )
    # 將終端機的層級調高，這樣螢幕就不會被一大堆 Prompt 洗版
    logging.getLogger().handlers[1].setLevel(logging.INFO)

setup_logger()