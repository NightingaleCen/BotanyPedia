"""将命名实体识别NER进行predict后的结果ner_result.json转化为性状列表，对原始的info_list进行更新"""

import json

ner_result_path = './ner_result.json'
chara_path = './characteristics.json'
info_list_path = './info_list.json'
chara_map_dict = {'color': '颜色', 'shape': '形状', 'ind_value': '工业价值', 'med_value': '药用价值', 'edi_value': '食用价值',
                          'cult_value': '栽培价值', 'pro_value': '保护和改造环境价值', 'height': '高度', 'disease': '病害名称', 'pest': '虫害名称', 'illumination': '光照', 
                          'temp': '温度', 'resilience': '抗逆性'}
key_map_dict = {'花': '花朵', '叶': '叶子', '茎': '树皮', '果': '果实'}
class Filter():
    """
        主要过滤ner_result.json中每个植物花、果、叶、茎等形状，并重新建一个所有植物的性状(Characteristic)的json，
        再将characteristics装进info_list.json中，并去掉info_list.json中attributes，只保留characteristics
    """
    def __init__(self, ner_result_path, chara_path, info_list_path, key_map_dict, chara_map_dict) -> None:
        self.ner_result_path = ner_result_path  # ner_result.json
        self.chara_path = chara_path    # 性状json
        self.info_list_path = info_list_path    # 用来建图的info_list
        self.key_map_dict = key_map_dict
        self.chara_map_dict = chara_map_dict

    def read_ner_result(self):
        """读取ner_result.json，得到一个字典，{plant:{charakey:chara_value}}"""
        with open(self.ner_result_path,  'r', encoding='utf-8') as f:
            plant_dict = json.load(f)
        plant_chara_dict = {}

        # 判断key是否为color 或 shape
        def isColorOrShape(chara_key):
            return (chara_key == 'color' or  chara_key == 'shape')
        
        for plant in plant_dict:
            plant_chara_dict[plant] = {}
            ner_result = plant_dict[plant]  # 在plant_dict中每个植物的各项提取结果字典
            for key in ner_result:
                if key in self.key_map_dict:
                    # 如果是花叶茎果
                    for chara_key in ner_result[key]:
                        if isColorOrShape(chara_key):
                            plant_chara_dict[plant][self.key_map_dict[key]+self.chara_map_dict[chara_key]] = ner_result[key][chara_key] 
                else:
                    # key是description的情况下
                    for chara_key in ner_result[key]:
                        if not isColorOrShape(chara_key):
                            plant_chara_dict[plant][self.chara_map_dict[chara_key]] = ner_result[key][chara_key]
        return plant_chara_dict
    
    def read_original_info_list(self, plant_chara_dict):
        """主要是读取info_list中每个植物的attributes中的生活型，并加入到plant_chara_dict中"""
        with open(self.info_list_path, 'r', encoding='utf-8') as f:
            original_info_list_dict = plant_info_dict = json.load(f)
            for plant in plant_info_dict:
                if '生活型' in plant_info_dict[plant]['attributes']:
                    plant_chara_dict[plant]['生活型'] = plant_info_dict[plant]['attributes']['生活型'].strip("；").strip('，')
        return plant_chara_dict, original_info_list_dict
    
    def output_plant_chara_json(self, plant_chara_dict):
        with open(self.chara_path, 'w+', encoding='utf-8') as f:
            json.dump(plant_chara_dict, f, indent=4, ensure_ascii=False, separators=(',', ': '))

    def update_info_list_json(self, plant_chara_dict, original_info_list_dict):
        # with open(self.info_list_path,)
        # 删掉attributes键值对
        for plant in original_info_list_dict:
            original_info_list_dict[plant].pop('attributes')
        new_info_list_dict = original_info_list_dict
        for plant in new_info_list_dict:
            new_info_list_dict[plant]['characteristics'] = plant_chara_dict[plant]
        with open(self.info_list_path, 'w+', encoding='utf-8') as f:
            json.dump(new_info_list_dict, f, indent=4, ensure_ascii=False, separators=(',', ': '))

    def run(self):
        plant_chara_dict = self.read_ner_result()
        plant_chara_dict, original_info_list_dict = self.read_original_info_list(plant_chara_dict)
        self.output_plant_chara_json(plant_chara_dict)
        self.update_info_list_json(plant_chara_dict, original_info_list_dict)

if __name__ == '__main__':
    filter = Filter(ner_result_path, chara_path, info_list_path, key_map_dict, chara_map_dict)
    filter.run()