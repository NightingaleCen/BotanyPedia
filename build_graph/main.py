from info2predict_data import Converter
from preprocess_ner_result import Filter
from BuildGraph import BotanyGraph
import os

ner_result_path = "./ner_result.json"
chara_path = "./characteristics.json"
info_list_path = "./info_list.json"
chara_map_dict = {
    "color": "颜色",
    "shape": "形状",
    "ind_value": "工业价值",
    "med_value": "药用价值",
    "edi_value": "食用价值",
    "cult_value": "栽培价值",
    "pro_value": "保护和改造环境价值",
    "height": "高度",
    "disease": "病害名称",
    "pest": "虫害名称",
    "illumination": "光照",
    "temp": "温度",
    "resilience": "抗逆性",
}
key_map_dict = {"花": "花朵", "叶": "叶片", "茎": "树皮", "果": "果实"}
ner_predict_data_path = "./ner_predict_data.json"


def exist_ner_result():
    return os.path.exists(ner_result_path)


if __name__ == "__main__":
    if exist_ner_result():
        # 如果存在ner_result.json，则对原始的info_list进行更新
        # filter = Filter(ner_result_path, chara_path, info_list_path, key_map_dict, chara_map_dict)
        # filter.run()
        # filter.preprocess_info_list_data()    # 直接在info_list中处理掉" "这样的空格串/空串
        # 构建Graph
        graph = BotanyGraph(info_list_path)
        graph.clean_graph()
        
        graph.build_graph()

    else:
        # 如果不存在ner_result.json，则需要从原始的info_list生成用于ner的预测数据
        converter = Converter(info_list_path, ner_predict_data_path)
        converter.run()
