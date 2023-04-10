from py2neo import *
import os 
import json
import itertools

class Encyclopedia():
    def __init__(self) -> None:
        self.graph = Graph('bolt://localhost:7687', auth = ('neo4j', 'botanypedia'))
        
        # 植物的性状
        self.charas = ["生活型", "高度", "叶片形状", "叶片颜色", "花朵形状", "花朵颜色", "果实形状", "果实颜色",
                       "树皮形状", "树皮颜色",
                       "温度", "光照", "保护和改造环境价值", "药用价值", "食用价值", "工业价值", "栽培价值", 
                       "抗逆性", "病害名称", "虫害名称"]
        # self.node_basic_attris = ['中文名', '别名', '描述']
        self.node_basic_attris = ['中文名', '别名']
        self.distri_attris = {'省份': 'Province', '地区': 'Area', '国家': 'Country'}
        self.family_attris = {'界': 'Kingdom', '门': 'Phylum', '纲': 'Class', '目': 'Order', '科': 'Family', '属': 'Genus'}
        self.attris_list = self.node_basic_attris + list(self.distri_attris.keys()) + list(self.family_attris.keys())
        self.attris_dict = {}
        self.attris_dict.update(self.distri_attris)
        self.attris_dict.update(self.family_attris)
        self.attri_chara_template_dict = self.attri_chara_template()
        self.other_option = "以上选项都不是您想要找的植物的信息。"
        # self.other_option_attri = "以上选项都不是您想要找的属性信息"

    def attri_chara_template(self):
        template_dict = {}
        for attri in self.node_basic_attris:
            template_dict[attri] = '它的{0}为'.format(attri)
        for chara in self.charas:
            if '颜色' in chara or '形状' in chara:
                template_dict[chara] = '它的{0}主要有'.format(chara)
            elif '高度' in chara:
                template_dict[chara] = '该种植物的{0}一般为'.format(chara)
            elif '温度' in chara or '光照' in chara:
                template_dict[chara] = '这种植物生长的{0}条件为'.format(chara)
            elif '价值' in chara:
                template_dict[chara] = '在{0}方面，其可以用于或用作'.format(chara)
            elif '害' in chara:
                template_dict[chara] = '其易得的{0}是'.format(chara)
            elif '抗逆性' in chara:
                template_dict[chara] = '这种植物的抗逆特性为'
            elif '生活型' in chara:
                template_dict[chara] = '它的生活型为'
        for attri in self.distri_attris:
            if attri == '省份':
                template_dict[attri] = '该植物广泛分布的省(市、区)有'.format(attri)
            elif attri in ('地区', '国家'):
                template_dict[attri] = '所属的{0}为'.format(attri)
        for attri in self.family_attris:
            template_dict[attri] = ''

        return template_dict

    #TODO:根据前端进行修改
    def output(self, string):
        """输出到终端。目前是标准输出，但之后可能是对接前端"""
        #print(string, end='')
        return string

    def output_node_attributes(self, attris, node_attri_dict, template_dict, isFamilyOutput=False, returnString=False):
        if not returnString:
            for attri in attris:
                if attri not in node_attri_dict:
                    continue
                template = template_dict[attri]
                if type(node_attri_dict[attri]) == list and node_attri_dict[attri] != []:
                    self.output(template)

                    for idx, item in enumerate(node_attri_dict[attri]):
                        if idx != 0:
                            self.output('、')
                        self.output(item)
                    self.output('。')
                elif type(node_attri_dict[attri]) == str:
                    if not isFamilyOutput:
                        self.output(template)
                        self.output(node_attri_dict[attri].strip('。')+'。')
                    if isFamilyOutput:
                        if attri == '界':
                            self.output('该植物属于')
                        self.output(node_attri_dict[attri])
                        self.output(template)
                        if attri == '属':
                            self.output('。')
                        else:
                            self.output('，')
            self.output('\n')
        else:
            string = ''
            for attri in attris:
                if attri not in node_attri_dict:
                    continue
                template = template_dict[attri]
                if type(node_attri_dict[attri]) == list and node_attri_dict[attri] != []:
                    string += template

                    for idx, item in enumerate(node_attri_dict[attri]):
                        if idx != 0:
                            string += '、'
                        string += item
                    string += '。'
                elif type(node_attri_dict[attri]) == str:
                    if not isFamilyOutput:
                        string += template
                        string += node_attri_dict[attri].strip('。')+'。'
                    if isFamilyOutput:
                        if attri == '界':
                            string += '该植物属于'
                        string += node_attri_dict[attri]
                        string += template
                        if attri == '属':
                            string += '。'
                        else:
                            string += '，'
            # string += '\n'
            return string

    def query(self, plant_sci_name):
        """根据植物的学名，在植物知识图谱中查找，打印输出植物的各方面数据"""
        # 植物的中文名、别名、全部性状（需要做成一个自然语言表达句来返回）
        # 植物学分类，x界x门xxx属...
        # 植物的分类
        # 植物的描述
        return_dict = {}
        template_dict = self.attri_chara_template_dict

        n_matcher = NodeMatcher(self.graph)
        node = n_matcher.match("Species", name=plant_sci_name)

        # 1.根据学名，查找结点属性
        #self.output('您要查询的植物为:'+plant_sci_name+'。\n')
        node_attri_dict = dict(node.all()[0]) # type(node.all()[0]) == Node
        for key in node_attri_dict:
            if type(node_attri_dict[key]) == str:
                node_attri_dict[key] = [node_attri_dict[key]]
        # print(node_attri_dict, '\n^^^^^^^^^^^^')
        # TODO:考虑是否在每一个attri输出后加上换行符
        # 1.1.先输出基本信息
        self.output_node_attributes(self.node_basic_attris, node_attri_dict, template_dict)
        return_dict.update(node_attri_dict)
        #1.2.其次，输出性状
        self.output_node_attributes(self.charas, node_attri_dict, template_dict)

        # 2.搜索所有的关系来输出结果

        # 2.1查询该物种分布的省份、地区、国家
        query_provinces = "MATCH (s:Species)-[:planted_in]->(p:{0}) WHERE s.name = '{1}' RETURN p.name".format('Province', plant_sci_name)
        query_areas = "MATCH (s:Species)-[:planted_in]->(p:{0}) WHERE s.name = '{1}' RETURN p.name".format('Area', plant_sci_name)
        query_country = "MATCH (s:Species)-[:planted_in]->(p:{0}) WHERE s.name = '{1}' RETURN p.name".format('Country', plant_sci_name)

        # 运行查询物种分布的省份、地区、国家
        results_provinces = self.graph.run(query_provinces)
        results_areas = self.graph.run(query_areas)
        results_country = self.graph.run(query_country)

        # 获得省份、地区、国家列表
        provinces = [record['p.name'] for record in results_provinces]
        areas = [record['p.name'] for record in results_areas]
        country = [record['p.name'] for record in results_country]
        distri_dict = {}
        if provinces != []:
            distri_dict["province"] = provinces
        elif areas != []:
            distri_dict["area"] = areas
        elif country != []:
            distri_dict['country'] = country
        # distri_dict = {"province": provinces, "area": areas, "country": country}
        self.output_node_attributes(self.distri_attris, distri_dict, template_dict)
        return_dict.update(distri_dict)
        # 2.2查询该物种的界门纲目科属并输出字符串
        results_family = self.graph.run("MATCH (:Species {name: $name})-[:type_of]->(g:Genus)-[:subclass_of]->(f:Family)-[:subclass_of]->(o:Order)-[:subclass_of]->(c:Class)-[:subclass_of]->(p:Phylum)-[:subclass_of]->(k:Kingdom) RETURN g.name, f.name, o.name, c.name, p.name, k.name", name=plant_sci_name)
        results_family = results_family.data()[0]
        family_map = {'g.name': 'genus', 'f.name': 'family', 'o.name': 'order', 'c.name': 'class', 'p.name': 'phylum', 'k.name': 'kingdom'}
        results_family = {family_map[key]: results_family[key] for key in family_map}
        # print(results_family)
        self.output_node_attributes(self.family_attris, results_family, template_dict, isFamilyOutput=True)
        return_dict.update(results_family)
        return return_dict



    def display_options(self, options:list[str], displayOtherOptions=True):
        """options:list[str]"""
        self.output("请选择以下选项中的一个:\n")
        final_options = options
        if displayOtherOptions:
            final_options.append(self.other_option)
        for i, option in enumerate(final_options):
            self.output("{0}.{1}".format(i+1, option)+'\n')

    # TODO:根据前端进行更改
    def receive_text_message(self)->str:
        text = input()
        return text

    #TODO:根据前端进行修改
    def receive_option_message(self, options)->int:
        """
            options个数为候选植物的个数
            连接前端回收的内容，然后将前端中用户的选择结果返回
            由于只是一个选择框返回的序号，则option_id应该是一个数
        """
        # 第1步，先接收前端信息
        # 第2步，整合前端信息，返回option序号（从1开头）
        while(True):
            self.output("\n请您输入您选择的选项号：\n")
            option_id = input() #TODO:根据前端进行修改
            if not option_id.isdigit():
                self.output('您输入的内容有误，请您重新输入！\n')
            elif int(option_id) > len(options) or int(option_id) <= 0:
                self.output('您的选项号有误，请您重新选择！\n')
            else:
                break
        return int(option_id)

    def integrate_information(self, preliminary_results, hasGuidedUser=False):
        """
            1.接受鉴别系统给的初步鉴定结果
            2.查询若干结果的结点信息，并对比其性状，确定提问方式
            3.制作各种问题模板（独立成一个def函数）
            4.整合问题，并输出到终端，作为引导用户信息
            5.获取用户信息
            6.从用户反馈的回复
                若用户认为都不对，就不管了
                若用户选了至少一项，就选择这个结果
            7.将最终结果返回给百科系统
        """
        # 引导用户并获取用户的进一步确认信息
        if not hasGuidedUser:
            # 1. preliminary_results的形式：{植物学名i：置信度i}
            # doFirst = len(preliminary_results) > 1
            more_than_one_plant = len(preliminary_results) > 1
            # doSecond = False
            # doSecond = True
            # already_find = False
            # final_plant = preliminary_results[0] if not doFirst else None
            if more_than_one_plant:
                # 2.查询结点信息，并对比其性状，确定提问方式
                # 2.1.查询结点信息
                plant_chara_dict = {}   # {plant1: {chara_name1:chara1value, chara_name2:chara2value}, plant2: {...}},是dict[dict]
                chara_plant_dict = {}   # {chara_name1: [plant1, plant2,...]},是dict[list]
                for plant_sci_name in preliminary_results:
                    # n_matcher = NodeMatcher(self.graph)
                    # node = n_matcher.match("Species", name=plant_sci_name)
                    # node_attri_dict = dict(node.all()[0])
                    node_attri_dict = self.query(plant_sci_name)
                    pop_attris = []
                    for key in node_attri_dict:
                        if not(('形状' in key) or ('颜色' in key) or ('生活型' in key) or ('province' in key)):
                            pop_attris.append(key)
                    for key in pop_attris:
                        node_attri_dict.pop(key)
                    node_attri_dict['image'] = '/images/%s.jpg' % plant_sci_name
                    # node_attri_dict.pop('描述')
                    # node_attri_dict.pop('name')
                    plant_chara_dict[plant_sci_name] = node_attri_dict
                    for chara_name in node_attri_dict:
                        if chara_name not in chara_plant_dict:
                            chara_plant_dict[chara_name] = []
                        chara_plant_dict[chara_name].append(plant_sci_name)
                num_candidate_plants = len(plant_chara_dict)

                # 2.2.1.1 查找共有的属性类型
                common_charas = []  # 共有的性状名
                for chara_name in chara_plant_dict:
                    if len(chara_plant_dict[chara_name]) == num_candidate_plants:
                        # 如果所有候选植物都具有该种性状
                        # 暂时不过滤分不开的性状
                        # if chara_name != 
                        common_charas.append(chara_name)


                def isDifferent(values1, values2):
                    different = False
                    if type(values1) == type(values2):
                        if type(values1) == list:
                            set1, set2 = set(values1), set(values2)
                            different = not(set1.issubset(set2) or set2.issubset(set1))
                        elif type(values1) == str:
                            different = not(values1 == values2)
                        else:
                            # 双方为空
                            return False
                    else:
                        # 双方不同且非空
                        if (type(values1) == str or type(values1) == list) and (type(values2) == str or type(values2) == list):
                            different = True
                        else:
                            return False
                    
                    return different
                
                def generatePairs(preliminary_results_plant_list):
                    pairs = list(itertools.combinations(preliminary_results_plant_list, 2))
                    return pairs


                preliminary_results_plant_list = preliminary_results
                common_but_different_attri = []
                plant_pairs = generatePairs(preliminary_results_plant_list)
                for chara_name in common_charas:
                    # print(preliminary_results[1:3])
                    
                    if 'province' in chara_name:
                        # 如果是地理位置的话
                        joint_common_provinces = set()
                        for (plant1, plant2) in plant_pairs:
                            province_set1 = set(plant_chara_dict[plant1]['province']) if type(plant_chara_dict[plant1]['province']) == list else {}
                            province_set2 = set(plant_chara_dict[plant2]['province']) if type(plant_chara_dict[plant2]['province']) == list else {}
                            intersection = province_set1.intersection(province_set2)
                            # joint_common_provinces = joint_common_provinces.union(intersection)
                            joint_common_provinces = joint_common_provinces.intersection(intersection)
                        for plant in preliminary_results_plant_list:
                            if type(plant_chara_dict[plant]['province']) == list:
                                plant_chara_dict[plant]['province'] = list(set(plant_chara_dict[plant]['province']) - joint_common_provinces.union(intersection))
                            else:
                                # 如果为空
                                plant_chara_dict[plant]['province'] = []
                        common_but_different_attri.append(chara_name)
                    else:
                        is_different_dict = {}
                        all_different = True
                        for (plant1, plant2) in plant_pairs:
                            is_different_dict[(plant1, plant2)] = isDifferent(plant_chara_dict[plant1][chara_name], plant_chara_dict[plant2][chara_name])
                        for pair in is_different_dict:
                            if is_different_dict[pair] == False:
                                all_different = False
                        if all_different:
                            common_but_different_attri.append(chara_name)
                # TODO:修改！
                return_dict = {}
                for attri in common_but_different_attri:
                    return_dict[attri] = {}
                    for plant in preliminary_results:
                        return_dict[attri][plant] = plant_chara_dict[plant][attri]
                return return_dict
            
            else:
                # 如果只有一种植物 
                plant = preliminary_results[0]
                return self.query(plant)

                # # test
                # print('\n\n')
                # # 2.2.1.2第一种提问方式的提示输出
                # options1 = []
                # id2plant = []   # 用于最后确定植物名
                # for plant in plant_chara_dict:
                #     option_content = ''
                #     for chara_name in common_charas:
                #             option_content = option_content + self.output_node_attributes([chara_name], plant_chara_dict[plant], self.attri_chara_template_dict, returnString=True)
                #     # 组成字符串添加到options集合里
                #     options1.append(option_content) 
                #     id2plant.append(plant)
                # # 2.2.1.3第一种提问方式的结果回收、分析
                # self.display_options(options1)
                # option_id = self.receive_option_message(options1)    # option_id:[1,...,n+1]
                # # # 当option_id=n+1或answer_id=n时，就是没找到，在这种情况下才进行第二次提问
                # doSecond = (option_id == len(options1))
                # answer_id = option_id - 1   # 转换成[0, 1, ..., n]
                # already_find = False if doSecond else True
                # if already_find:
                #     final_plant = id2plant[answer_id]

            # if doSecond:
            #     # 2.2.2.1第二种方式的数据准备
            #     diff_plant_chara_dict = {}  # 这个dict的内容是：对于其中的plant，它下面的chara并非全部候选的plant都有的
            #     for plant in preliminary_results:
            #         diff_plant_chara_dict[plant] = {}
            #         for chara in plant_chara_dict[plant]:
            #             if chara not in common_charas:
            #                 diff_plant_chara_dict[plant][chara] = plant_chara_dict[plant][chara]
            #     # 2.2.2.2第二种方式的提示输出
            #     options2 = []
            #     id2plant = []
            #     for plant in diff_plant_chara_dict:
            #         option_content = ''
            #         for chara_name in diff_plant_chara_dict[plant]:
            #             option_content = option_content + self.output_node_attributes([chara_name], diff_plant_chara_dict[plant], self.attri_chara_template_dict, returnString=True)
            #         if option_content != '':
            #             id2plant.append(plant)
            #             options2.append(option_content)
            #     if len(options2) == len(preliminary_results):
            #         # 表示所有的植物都有至少一种不全有的性状
            #         self.output('\n\n抱歉！由于第一次提示未能让您选择到合适的植物，以下是第二次提示：\n')
            #         self.display_options(options2)
            #         option_id = self.receive_option_message(options2)    # option_id:[1,...,n+1]
            #         already_find = True if option_id != len(options2) else False
            #         answer_id = option_id - 1   # 转换成[0, 1, ..., n]
            #         if already_find:
            #             final_plant = id2plant[answer_id]
            #     else:
            #         self.output('对不起，您找到的植物不存在或系统无法根据您提供的信息确认植物类别！\n请您重试，谢谢！')
            #         # return None     # 表示查找失败
            # if final_plant:
            #     self.output('经过以上提示和您的进一步确认，得到以下信息：\n\n'.format(final_plant))
            #     self.query(final_plant)
            #     # return final_plant
            # else:
            #     self.output('对不起，您找到的植物不存在或系统无法根据您提供的信息确认植物类别！\n请您重试，谢谢！')
            #     # return None     # 表示查找失败
            
    def query_by_basic_attris(self):
        """根据基本的属性例如植物学分类、省份、地区、国家来查找植物，返回植物名"""
        final_plant = None
        # 1.首先交互：用户输入要查询的属性名
        self.output('请选择您想要查询的属性：\n')
        self.display_options(self.attris_list, displayOtherOptions=False)
        option_id = self.receive_option_message(self.attris_list)
        answer_id = option_id - 1
        # 在这种情况下它选择的是查询别名
        query_plant_name = True if answer_id == 0  or answer_id == 1 else False
        if query_plant_name:
            # 如果是查找中文名/别名对应的植物
            self.output('请输入您想要查询的植物的{}：\n'.format(self.attris_list[answer_id]))
            text = self.receive_text_message()
            if self.attris_list[answer_id] == '中文名':
                # 如果是根据中文名查找植物
                query_c_name_node = 'MATCH (s:Species {中文名: "%s" }) RETURN s.name'%text
                result_c_name_node = self.graph.run(query_c_name_node)
                result_lst = [record["s.name"] for record in result_c_name_node]
                if result_lst == []:
                    self.output('没有找到您想要查询的植物！\n')
                else:
                    # 找到想要的植物了
                    final_plant = result_lst[0]
                    self.query(final_plant) # 返回该植物的全部信息
            else:
                # 如果是根据别名查找植物
                query_common_name_node = 'MATCH (s:Species)-[:has_common_name]->(c:CommonName { name: "%s" }) RETURN s.name' % text
                result_common_name_node = self.graph.run(query_common_name_node)
                result_lst = [record["s.name"] for record in result_common_name_node]
                if result_lst == []:
                    self.output('没有找到您想要查询的植物！\n')
                else:
                    # 找到想要的植物了
                    final_plant = result_lst[0]
                    self.query(final_plant) # 返回该植物的全部信息
                
                
        else:
            # 2.然后根据属性名，查询该属性类型的所有结点的名字
            attri_name = self.attris_list[answer_id]
            query_atrri_nodes = "MATCH (p:{0}) RETURN p.name".format(self.attris_dict[attri_name])
            result_attri_nodes = self.graph.run(query_atrri_nodes)
            candi_attri_node_names = [record["p.name"] for record in result_attri_nodes]
            # 3.再将这些候选属性结点的名字作为一个选项框全部发送给用户
            self.output("请您选择您想要具体查询的属性值：\n")
            self.display_options(candi_attri_node_names, displayOtherOptions=False)    # 将该属性下的所有候选属性值展示给用户
            option_id = self.receive_option_message(candi_attri_node_names)    # 接收用户的信息，得到选择的id
            answer_id = option_id - 1   # 将用户的选项序号转化为candi_attri_node_names列表下标
            attri_value = candi_attri_node_names[answer_id]  # 获得用户选择的属性值
            print(attri_value)
            # 4.细分属性类别进行查询
            # 4.1 第一种情况：植物学分类
            if attri_name in self.family_attris:
                # 首先根据属性名，查询该属性类型的所有结点的名字
                if attri_name == '属':
                    query_plant_nodes = 'MATCH (s:Species)-[:type_of]->(g:Genus { name:"%s" }) RETURN s.name, s.中文名' % attri_value
                else:
                    query_plant_nodes = 'MATCH (s: Species)-[:type_of]->(:Genus)-[:subclass_of*]->(f:%s { name:"%s" } ) RETURN s.name AS speciesName, s.中文名 AS speciesChName'%(self.attris_dict[attri_name], attri_value)
            elif attri_name in self.distri_attris:
                if attri_name == '省份':
                    query_plant_nodes = 'MATCH (s: Species)-[:planted_in]->(p:Province { name:"%s" }) RETURN s.name AS speciesName, s.中文名 AS speciesChName' % attri_value
                elif attri_name == '地区':
                    query_plant_nodes = 'MATCH (s: Species)-[:planted_in]->(:Province)-[:belongs_to]->(a:Area { name:"%s"}) RETURN DISTINCT s.name AS speciesName, s.中文名 AS speciesChName' % attri_value
                elif attri_name == '国家':
                    query_plant_nodes = 'MATCH (s: Species)-[:planted_in]->(:Province)-[:belongs_to]->(:Area)-[:belongs_to]->(:Country { name:"%s"}) RETURN DISTINCT s.name AS speciesName, s.中文名 AS speciesChName UNION MATCH (s: Species)-[:planted_in]->(:Country { name:"%s"}) RETURN s.name AS speciesName, s.中文名 AS speciesChName' % (attri_value, attri_value)

            
            result_plant_nodes = self.graph.run(query_plant_nodes)
            candi_plant_names = {record["speciesName"]: record['speciesChName'] for record in result_plant_nodes}
            candi_plant_ch2enNames = {candi_plant_names[plant]:plant for plant in candi_plant_names}
            if candi_plant_names == {}:
                if attri_name in self.family_attris:
                    self.output('没有植物拥有这种属性!\n')
                elif attri_name in self.distri_attris:
                    self.output('没有植物分布在这个地方！\n')
            elif len(candi_plant_names) == 1:
                # 只有一种植物的话
                final_plant = list(candi_plant_names.keys())[0]
            else:
                # 又让用户去从若干植物中去找
                self.display_options(list(candi_plant_ch2enNames.keys()), displayOtherOptions=False)  # debug
                option_id = self.receive_option_message(list(candi_plant_ch2enNames.keys()))
                answer_id = option_id - 1   # 将用户的选项序号转化为candi_attri_node_names列表下标
                final_plant = list(candi_plant_names.keys())[answer_id]  # 获得用户选择的最终植物
            if final_plant:
                self.query(final_plant)


    def query_by_names(self, name: str):
        # name可以是中文名、别名、学名
        # 返回的是候选植物种类的dict
        
        if name.isalpha():
            name = name.lower()
        # 中文名查询
        query_c_name_node = "MATCH (s:Species) WHERE s.中文名 Contains '%s' RETURN s.name" % name
        query_common_name_node = "MATCH (s:Species)-[:has_common_name]->(c:CommonName) WHERE c.name Contains '%s' RETURN s.name" % name
        query_sci_name_node = "MATCH (s:Species) WHERE s.name Contains '%s' RETURN s.name" % name
        result_c_name_node = self.graph.run(query_c_name_node)
        result_c_name_set = set([record["s.name"] for record in result_c_name_node])
        result_common_name_node = self.graph.run(query_common_name_node)
        result_common_name_set = set([record["s.name"] for record in result_common_name_node])
        result_sci_name_node = self.graph.run(query_sci_name_node)
        result_sci_name_set = set([record["s.name"] for record in result_sci_name_node])
        all_name_set = result_c_name_set.union(result_common_name_set)
        all_name_set = all_name_set.union(result_sci_name_set)
        # 模糊匹配英文
        # 全部转为小写
        if name.isalpha():
            titleName = name.title()
        query_sci_name_titled_node = query_sci_name_node = "MATCH (s:Species) WHERE s.name Contains '%s' RETURN s.name" % titleName
        result_sci_name_titled_node = self.graph.run(query_sci_name_titled_node)
        result_sci_name_titled_set = set([record["s.name"] for record in result_sci_name_titled_node])
        all_name_set = all_name_set.union(result_sci_name_titled_set)
        all_name_lst = list(all_name_set)
        # return_dict = {plant: self.query(plant) for plant in all_name_lst}
        return all_name_lst

    def get_country(self):
        query = "MATCH (c: Country) RETURN c.name"
        result = self.graph.run(query)
        result_lst = [record["c.name"] for record in result]
        return result_lst    # type: list[str]

    def get_area(self, country):
        # 输入为国家名
        # 输出为一个list，元素为地区名
        query = "MATCH (a: Area)-[:belongs_to]->(c: Country) WHERE c.name = '%s' RETURN  a.name" % country
        result = self.graph.run(query)
        result_lst = [record["a.name"] for record in result]
        return result_lst   # type: list[str]
    
    def get_province(self, area):
        # 输入为地区名
        # 输出为一个list，元素为省份名
        query = "MATCH (p: Province)-[:belongs_to]->(a: Area) WHERE a.name = '%s' RETURN  p.name" % area
        result = self.graph.run(query)
        result_lst = [record["p.name"] for record in result]
        return result_lst   # type: list[str]

    def query_province(self, province: str):
        # attri可以是1.省份2.地区3.国家4.界5.目6.科7.属
        # 返回的是植物种类的若干选项
        query = "MATCH (s: Species)-[:planted_in]->(p: Province) WHERE p.name = '%s' RETURN s.name" % province
        result = self.graph.run(query)
        result_lst = [record["s.name"] for record in result]
        return result_lst   # type: list[str]

    def get_kingdom(self):
        query = "MATCH (k: Kingdom) RETURN k.name"
        result = self.graph.run(query)
        result_lst = [record["k.name"] for record in result]
        return result_lst    # type: list[str]

    def get_phylum(self, kingdom):
        query = "MATCH (p: Phylum)-[:subclass_of]->(k:Kingdom) WHERE k.name = '%s' RETURN p.name" % kingdom
        result = self.graph.run(query)
        result_lst = [record["p.name"] for record in result]
        return result_lst # type: list[str]

    def get_class(self, phylum):
        query = "MATCH (c: Class)-[:subclass_of]->(p: Phylum) WHERE p.name = '%s' RETURN c.name" % phylum
        result = self.graph.run(query)
        result_lst = [record["c.name"] for record in result]
        return result_lst # type: list[str]

    def get_order(self, class_name):
        query = "MATCH (o: Order)-[:subclass_of]->(c: Class) WHERE c.name = '%s' RETURN o.name" % class_name
        result = self.graph.run(query)
        result_lst = [record["o.name"] for record in result]
        return result_lst # type: list[str]

    def get_family(self, order):
        query = "MATCH (f: Family)-[:subclass_of]->(o: Order) WHERE o.name = '%s' RETURN f.name" % order
        result = self.graph.run(query)
        result_lst = [record["f.name"] for record in result]
        return result_lst # type: list[str]

    def get_genus(self, family):
        query = "MATCH (g: Genus)-[:subclass_of]->(f: Family) WHERE f.name = '%s' RETURN g.name" % family
        result = self.graph.run(query)
        result_lst = [record["g.name"] for record in result]
        return result_lst # type: list[str]
    
    def query_genus(self, genus: str):
        query = "MATCH (s: Species)-[:type_of]->(g: Genus) WHERE g.name = '%s' RETURN s.name" % genus
        result = self.graph.run(query)
        result_lst = [record["s.name"] for record in result]
        return result_lst # type: list[str]

    def query_all_plants(self, plant_list: list[str]):
        return_dict = {}
        for plant in plant_list:
            return_dict[plant] = self.query(plant)
        return return_dict

if __name__ == '__main__':
    pedia = Encyclopedia()
    # pedia.query('Prunus mume')
    pedia.integrate_information(['Vitis amurensis', 'Vitis vinifera', 'Prunus mume'])
    #pedia.integrate_information(['Prunus mume'])
    # pedia.query_by_basic_attris()
    # pedia.query_by_names('花')