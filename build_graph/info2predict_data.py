"""用来将原始的info_list.json进行转换，更新info_list.json并得到用来命名实体识别的数据"""
import json
info_list_path = './info_list(1).json'
ner_predict_data_path = './ner_predict_data.json'

class Converter():
    """用来将原始的info_list.json进行转换，更新info_list.json并得到用来命名实体识别的数据"""
    def __init__(self, info_list_path, ner_predict_data_path) -> None:
        self.info_list_path = info_list_path
        self.ner_predict_data_path = ner_predict_data_path
    
    def read_info_list(self):
        """读取获得info_list每一个植物的description"""
        with open(self.info_list_path, 'r', encoding='utf-8') as f:
            plant_dict = json.load(f)
            description_dict = {plant: plant_dict[plant]['description'] for plant in plant_dict}
        return description_dict

    def process_description(self, description_dict):
        """将每一个植物的description转化为列表，每一个列表不超过512个字符"""
        info_list_description_dict = {}
        predict_data_description_dict = {}
        for plant in description_dict:
            description = description_dict[plant]
            if type(description) != str:
                predict_data_description_dict[plant] = []
            else:
                descriptions_list = description.split('\r\n')
                descriptions = ''.join([string.strip() for string in descriptions_list[2:]])
                info_list_description_dict[plant] = descriptions
                descriptions = descriptions.split('。')
                descriptions_list = []
                for string in descriptions:
                    if string != '':
                        descriptions_list.append(string[-500:])
                predict_data_description_dict[plant] = descriptions_list
        return info_list_description_dict, predict_data_description_dict
    
    def description_to_prediction(self, predict_data_description_dict):
        """将info_list部分属性、description作为预测数据，生成到ner_predict_data.json中"""
        with open(self.info_list_path, 'r', encoding='utf-8') as f:
            plant_dict = json.load(f)
            new_dict = {}
            attr_list = ['花', '叶', '果', '茎']
            for plant in predict_data_description_dict:
                new_dict[plant] = {attr_key : plant_dict[plant]['attributes'][attr_key] for attr_key in plant_dict[plant]['attributes'] if attr_key in attr_list}
                new_dict[plant]["description"] = predict_data_description_dict[plant]
        with open(self.ner_predict_data_path, 'w+', encoding='utf-8') as f:
            json.dump(new_dict, f, indent=4, ensure_ascii=False, separators=(',', ': '))
    
    def update_info_list(self, info_list_description_dict):
        """更新info_list的description"""
        with open(self.info_list_path, 'r', encoding='utf-8') as f:
            plant_dict = json.load(f)
            for plant in info_list_description_dict:
                plant_dict[plant]['description'] = info_list_description_dict[plant]
        with open(self.info_list_path, 'w', encoding='utf-8') as f:
            json.dump(plant_dict, f, indent=4, ensure_ascii=False, separators=(',', ': '))
    
    def run(self):
        description_dict = self.read_info_list()
        info_list_description_dict, predict_data_description_dict = self.process_description(description_dict)
        self.description_to_prediction(predict_data_description_dict)
        # self.update_info_list(info_list_description_dict)

if __name__ == '__main__':
    converter = Converter(info_list_path, ner_predict_data_path)
    converter.run()