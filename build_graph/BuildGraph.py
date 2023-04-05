import json 
from py2neo import Graph, Node 
import os 
data_path = os.path.join('.', 'data', 'info_list.json')
class BotanyGraph:
    """
        实体
            distribution
            国家、地区（东北、西北、南方、北方、长江以南地区、中部、长江流域、黄河流域、中国南方热带地区）、省市区（34个）
            
            c_family
            界、门、纲、目、科、属、种(均为拉丁文)
        关系
            地区-[属于]->国家，省市区-[属于]->地区，省市区-[属于]->国家
            种-[属于]->属、属-[属于]->科、科-[属于]->目、目-[属于]->纲、纲-[属于]->门、门-[属于]->界
        属性
            ……
    """
    def __init__(self,data_path) -> None:
        # self.data_path = os.path.join('.', 'data', 'info_list.json')
        self.data_path = data_path
        self.graph = Graph('bolt://localhost:7687', auth = ('neo4j', 'botanypedia'))

        self.provinces = ['河北',
                            '山西',
                            '辽宁',
                            '吉林',
                            '黑龙江',
                            '江苏',
                            '浙江',
                            '安徽',
                            '福建',
                            '江西',
                            '山东',
                            '河南',
                            '湖北',
                            '湖南',
                            '广东',
                            '海南',
                            '四川',
                            '贵州',
                            '云南',
                            '陕西',
                            '甘肃',
                            '青海',
                            '台湾',
                            '内蒙古',
                            '广西',
                            '西藏',
                            '宁夏',
                            '新疆',
                            '北京',
                            '天津',
                            '上海',
                            '重庆',
                            '香港',
                            '澳门',]
        self.country = ['中国']
        self.areas = [ '长江以南',
                        '南方',
                        '中部',
                        '北方',
                        '长江流域',
                        '黄河流域',
                        '西北',
                        '南方热带地区',
                        '东北']

    # 操作：创建实体节点 在此处不能建立‘种’的结点
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
            count += 1
        print(f'Successfully established {label}: {count} nodes')
        

    # 操作：创建实体关系边
    def create_rel_edge(self, start_node_label, end_node_label, edges, relationship_type, relationship_name):
        count = 0 
        #  第一步，去重
        set_edges = []
        for edge in edges:
            set_edges.append('##'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('##')
            start_node_name = edge[0]
            end_node_name = edge[1]
            query = "match(p:%s), (q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)"%(
                start_node_label, end_node_label, start_node_name, end_node_name, relationship_type, relationship_name)
            try:
                self.graph.run(query)
                count += 1
            except Exception as e:
                print(e)
        print(f'Relationship {relationship_name} has {all} types, and has built {count} nodes!')
        return

    # 创建实体类型1：分布的实体，专门创建地区的结点
    def create_distribution_nodes_and_relations(self):
        # 获取省份与地区的关系
        # 1.长江以南
        South_Yangzi = ['湖南','江西','浙江','福建','广东','贵州','云南']
        rel_southYangzi_province = []
        for province in South_Yangzi:
            rel_southYangzi_province.append([province, '长江以南'])
        # 2.南方
        south = ['江苏','安徽','浙江','上海','湖北','湖南','江西','福建','云南','贵州','四川','重庆','广西','广东','香港','澳门','海南','台湾']
        rel_south_province = []
        for province in south:
            rel_south_province.append([province, '南方'])
        # 3.北方
        north = ['北京', '天津', '河北', '山西', '陕西', '河南', '山东', '黑龙江', '吉林', '辽宁']
        rel_north_province = []
        for province in north:
            rel_north_province.append([province, '北方'])
        # 4.中部
        central = ['山西', '安徽', '江西', '河南', '湖北', '湖南']
        rel_central_province = []
        for province in central:
            rel_central_province.append([province, '中部'])
        # 5.长江流域
        Changjiang = ['青海', '西藏', '四川', '云南', '重庆', '湖北', '湖南', '江西', '安徽', '江苏', '上海']
        rel_changjiang_province = []
        for province in Changjiang:
            rel_changjiang_province.append([province, '长江流域'])
        # 6.黄河流域
        Yellowriver = ['青海', '四川', '甘肃', '宁夏', '内蒙古', '陕西', '山西', '河南', '山东']
        rel_Yellowriver_province = []
        for province in Yellowriver:
            rel_Yellowriver_province.append([province, '黄河流域'])
        # 7.西北
        northwest = ['陕西', '宁夏', '甘肃', '青海', '新疆']
        rel_northwest_province = []
        for province in northwest:
            rel_northwest_province.append([province, '西北'])
        # 8.南方热带地区
        south_tropics = ['云南', '广西', '广东', '台湾', '海南']
        rel_south_tropics_province = []
        for province in south_tropics:
            rel_south_tropics_province.append([province, '南方热带地区'])
        # 9.东北
        northeast = ['辽宁', '吉林', '黑龙江']
        rel_northeast_province = []
        for province in northeast:
            rel_northeast_province.append([province, '东北'])
        
        # 下面是构建国家、地区、省份的结点
        # 创建国家的结点
        country_node = Node('Country', name=self.country[0])
        self.graph.create(country_node)
        # 创建地区的结点
        for area in self.areas:
            area_node = Node('Area', name=area)
            self.graph.create(area_node)
        # 创建省份的结点
        for province in self.provinces:
            province_node = Node('Province', name=province)
            self.graph.create(province_node)
        
        # 下面是构建国家、地区、省份之间的隶属关系
        # 地区与国家
        rel_area_country = []
        for area in self.areas:
            rel_area_country.append([area, '中国'])
        self.create_rel_edge('Area', 'Country', rel_area_country, 'belongs_to', '所属国家')
        # 省份与地区
        self.create_rel_edge('Province', 'Area', rel_southYangzi_province, 'belongs_to', '位于')
        self.create_rel_edge('Province', 'Area', rel_south_province, 'belongs_to', '位于')
        self.create_rel_edge('Province', 'Area', rel_north_province, 'belongs_to', '位于')
        self.create_rel_edge('Province', 'Area', rel_central_province, 'belongs_to', '位于')
        self.create_rel_edge('Province', 'Area', rel_changjiang_province, 'belongs_to', '位于')
        self.create_rel_edge('Province', 'Area', rel_Yellowriver_province, 'belongs_to', '位于')
        self.create_rel_edge('Province', 'Area', rel_northwest_province, 'belongs_to', '位于')
        self.create_rel_edge('Province', 'Area', rel_south_tropics_province, 'belongs_to', '位于')
        self.create_rel_edge('Province', 'Area', rel_northeast_province, 'belongs_to', '位于')
        
        return

    # 创建分类的各级结点
    def create_family_nodes(self, kingdom_nodes, phylum_nodes, class_nodes, order_nodes, family_nodes, genus_nodes):
        kingdom_nodes = list(set(kingdom_nodes))
        phylum_nodes = list(set(phylum_nodes))
        class_nodes = list(set(class_nodes))
        order_nodes = list(set(order_nodes))
        family_nodes = list(set(family_nodes))
        genus_nodes = list(set(genus_nodes))
        self.create_node('Kingdom', kingdom_nodes)
        self.create_node('Phylum', phylum_nodes)
        self.create_node('Class', class_nodes)
        self.create_node('Order', order_nodes)
        self.create_node('Family', family_nodes)
        self.create_node('Genus', genus_nodes)
        return
    
    def create_common_name_nodes(self, common_name_nodes):
        self.create_node('CommonName', common_name_nodes)
        return

    # 创建分类的各级节点之间的关系
    def create_family_relationship(self, rel_genus_family, rel_family_order, rel_order_class, rel_class_phylum, rel_phylum_kingdom):
        self.create_rel_edge('Genus', 'Family', rel_genus_family, 'subclass_of', '属于')
        self.create_rel_edge('Family', 'Order', rel_family_order, 'subclass_of', '属于')
        self.create_rel_edge('Order', 'Class', rel_order_class, 'subclass_of', '属于')
        self.create_rel_edge('Class', 'Phylum', rel_class_phylum, 'subclass_of', '属于')
        self.create_rel_edge('Phylum', 'Kingdom', rel_phylum_kingdom, 'subclass_of', '属于')
        return
    
    # 创建实体类型：种类（将除了distribution分布、c_family植物分类外的全部作为property）
    def create_plant_node(self, species_nodes, all_property):
        count = 0
        for species_name, property_dict in zip(species_nodes, all_property):
            print(property_dict)
            characteristics = property_dict['characteristics']
            node = Node('Species', name=species_name, 中文名=property_dict['c_name'], 别名=property_dict["common_name"],
                        描述=property_dict['description'], **characteristics)
            self.graph.create(node)
            count += 1
        print(f"{count} species's nodes have been established!")
        return

    def create_plant_distribution_relationship(self, rel_plant_country, rel_plant_province, rel_plant_area):
        self.create_rel_edge('Species', 'Country', rel_plant_country, 'planted_in', '广泛分布于')
        self.create_rel_edge('Species', 'Area', rel_plant_area, 'planted_in', '广泛分布于')
        self.create_rel_edge('Species', 'Province', rel_plant_province, 'planted_in', '广泛分布于')
        return 
    
    def create_plant_family_relationship(self, rel_plant_kingdom, rel_plant_phylum, rel_plant_class, rel_plant_order, rel_plant_family, rel_plant_genus):
        # self.create_rel_edge('Species', 'Kingdom', rel_plant_kingdom, 'type_of', '是一种')
        # self.create_rel_edge('Species', 'Phylum', rel_plant_phylum, 'type_of', '是一种')
        # self.create_rel_edge('Species', 'Class', rel_plant_class, 'type_of', '是一种')
        # self.create_rel_edge('Species', 'Order', rel_plant_order, 'type_of', '是一种')
        # self.create_rel_edge('Species', 'Family', rel_plant_family, 'type_of', '是一种')
        self.create_rel_edge('Species', 'Genus', rel_plant_genus, 'type_of', '是一种')
        return

    def create_plant_common_name_relationship(self, rel_plant_common_name):
        self.create_rel_edge('Species', 'CommonName', rel_plant_common_name, 'has_common_name', '有别名')
        return

    # 从json中抽取信息
    def read_json(self):
        # NOTE:需要去重！
        kingdom_nodes = []   # 界
        phylum_nodes = []   # 门
        class_nodes = []    # 纲
        order_nodes = []    # 目
        family_nodes = []   # 科
        genus_nodes = []    # 属

        common_name_nodes = []  # 别名

        # NOTE:不需要去重
        species_nodes = []  # 种，具体的某种植物
        all_property = []   # 列表，保存各个植物节点的全部属性构成的字典

        # NOTE:注意这里界门纲目科属种的上下属级关系需要去重！！
        rel_genus_family = []
        rel_family_order = []
        rel_order_class = []
        rel_class_phylum = []
        rel_phylum_kingdom = []


        # NOTE:这里就不需要去重
        rel_plant_kingdom = []   # 植物 属于界 
        rel_plant_phylum = []   # 植物 属于门
        rel_plant_class = []    # 植物 属于纲
        rel_plant_order = []    # 植物 属于目
        rel_plant_family = []   # 植物 属于科
        rel_plant_genus = []    # 植物 属于属
        
        rel_plant_country = []  # 植物 属于国家
        rel_plant_province = [] # 植物 属于省份
        rel_plant_area = [] # 植物 属于地区

        rel_plant_common_name = []  # 植物 has_common_name 别名
        with open(self.data_path, 'r', encoding='UTF-8') as file:
            all_info_dict = json.load(file)

            # def exist(dict_name, key):
            #     return dict_name[key] != None

            for species in all_info_dict:
                info_dict = all_info_dict[species]
                species_nodes.append(species)
                property_dict = {}
                for property_key in info_dict:
                    if property_key != 'c_family' and property_key != 'distribution':
                        # 抛除这两个类型不作为property，加入属性
                        property_dict[property_key] = info_dict[property_key]
                    
                    # 下面建立关系集
                    elif property_key == 'c_family':
                        c_family_dict = info_dict[property_key]
                        kingdom_nodes.append(c_family_dict['界'])
                        phylum_nodes.append(c_family_dict['门'])
                        class_nodes.append(c_family_dict['纲'])
                        order_nodes.append(c_family_dict['目'])
                        family_nodes.append(c_family_dict['科'])
                        genus_nodes.append(c_family_dict['属'])

                        rel_genus_family.append([c_family_dict['属'], c_family_dict['科']])
                        rel_family_order.append([c_family_dict['科'], c_family_dict['目']])
                        rel_order_class.append([c_family_dict['目'], c_family_dict['纲']])
                        rel_class_phylum.append([c_family_dict['纲'], c_family_dict['门']])
                        rel_phylum_kingdom.append([c_family_dict['门'], c_family_dict['界']])

                        rel_plant_kingdom.append([species, c_family_dict['界']])
                        rel_plant_phylum.append([species, c_family_dict['门']])
                        rel_plant_class.append([species, c_family_dict['纲']])
                        rel_plant_order.append([species, c_family_dict['目']])
                        rel_plant_family.append([species, c_family_dict['科']])
                        rel_plant_genus.append([species, c_family_dict['属']])

                    elif property_key == 'distribution':
                        distribution_list = info_dict[property_key]
                        if distribution_list:
                            for location in distribution_list:
                                if location in self.provinces:
                                    rel_plant_province.append([species, location])
                                elif location in self.country or '全国' in location or '中国各地' in location:
                                    rel_plant_country.append([species, '中国'])
                                else:
                                    rel_plant_area.append([species, location])
                    
                    if property_key == 'common_name':
                        if type(info_dict[property_key]) == str:
                            common_name_nodes.append(info_dict[property_key])
                            rel_plant_common_name.append([species, info_dict[property_key]])
                        elif type(info_dict[property_key]) == list:
                            for common_name in info_dict[property_key]:
                                common_name_nodes.append(common_name)
                                rel_plant_common_name.append([species, common_name])
                all_property.append(property_dict)
        
        return (kingdom_nodes, phylum_nodes, class_nodes, order_nodes, family_nodes, genus_nodes,
                species_nodes, common_name_nodes, all_property, rel_genus_family, rel_family_order, rel_order_class,
                rel_class_phylum, rel_phylum_kingdom, rel_plant_kingdom, rel_plant_phylum, rel_plant_class,
                rel_plant_order, rel_plant_family, rel_plant_genus, rel_plant_country, rel_plant_province,
                rel_plant_area, rel_plant_common_name)
    
    def build_graph(self):
        (kingdom_nodes, phylum_nodes, class_nodes, order_nodes, family_nodes, genus_nodes,
                species_nodes, common_name_nodes, all_property, rel_genus_family, rel_family_order, rel_order_class,
                rel_class_phylum, rel_phylum_kingdom, rel_plant_kingdom, rel_plant_phylum, rel_plant_class,
                rel_plant_order, rel_plant_family, rel_plant_genus, rel_plant_country, rel_plant_province,
                rel_plant_area, rel_plant_common_name) = self.read_json()
        # 第一步，先创建结点
        self.create_distribution_nodes_and_relations()
        self.create_plant_node(species_nodes, all_property)
        self.create_family_nodes(kingdom_nodes, phylum_nodes, class_nodes, order_nodes, family_nodes, genus_nodes)
        self.create_common_name_nodes(common_name_nodes)
        # 第二步，创建关系
        self.create_plant_distribution_relationship(rel_plant_country, rel_plant_province, rel_plant_area)
        self.create_plant_family_relationship(rel_plant_kingdom, rel_plant_phylum, rel_plant_class, rel_plant_order, rel_plant_family, rel_plant_genus)
        self.create_family_relationship(rel_genus_family, rel_family_order, rel_order_class, rel_class_phylum, rel_phylum_kingdom)
        self.create_plant_common_name_relationship(rel_plant_common_name)
    def clean_graph(self):
        # 最先，必须清空整个图
        print('clean all nodes and edges.')
        delete_query = 'MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r'
        self.graph.run(delete_query)



if __name__ == '__main__':
    graph = BotanyGraph(data_path)
    graph.clean_graph()
    graph.build_graph()