from flask import Flask, request, redirect, url_for, abort, render_template, send_file
from flask_cors import *
import os 
from Encyclopedia import Encyclopedia
app = Flask(__name__)
CORS(app, supports_credentials=True)
pedia = Encyclopedia()


# 根据植物学名，返回植物指定属性的值
@app.route('/queryInfo', methods=['GET'])
def query():
    name = request.args.get('name') # 获取学名 TODO:两种获取方式
    plant_dict = pedia.query(name)  # {attri1: ..., atrri2: ...}
    
    attri_wanted_lst = request.args.get('attribute')   # 获取所指定的性状 type:list
    if attri_wanted_lst != None:
        return_dict = {}
        for attri in attri_wanted_lst:
            return_dict[attri] = plant_dict[attri]
        return_dict['image'] = './images/%s.jpg' % name
        # return_dict['image'] = './server/images/%s.jpg' % name # .表示BotanyPedia作为根目录时运行
        return return_dict
    else:
        # 返回植物图片链接
        plant_dict['image'] = './images/%s.jpg' % name  # .表示server作为根目录时运行
        # plant_dict['image'] = './server/images/%s.jpg' % name # .表示BotanyPedia作为根目录时运行
        return plant_dict

# 根据GET到的链接，返回server/images文件夹中的 <学名.jpg>文件
@app.route('/images', methods=['GET'])
def display_image():
    # 从前端GET到一个链接
    # 请求报文主体信息：{link:'./images/plant_name.jpg}'
    path = request.args.get('link')
    return send_file(path, mimetype='image/jpeg')
    


# # TODO:思考如何解析从客户端发送到服务端的选项信息，把它转换成选项号
# TODO:最后应该可以删掉这几行！！但先再观察一下qwq
# @app.route('/receive_option_message', methods=["GET"])
# def receive_option_message(message):
#     return None


"""植物识别系统"""
@app.route('/integrate_information', methods=['GET'])
def integrate_information():
    # 1.如果是只有一个植物，返回的只有一个植物的字典 
    # 2.如果是有两个及以上植物，返回的有多个植物的字典
    # 每一个字典格式为{}
    preliminary_results = request.args.get('preliminary_results')
    return pedia.integrate_information(preliminary_results)


# TODO:需要完成的部分：
# 1.从前端接收图片文件，并丢进PlantInferer进行预测，得到预测结果即若干候选植物的list，并把list返回前端
# 2.然后前端把这个list又返回给后端路由/integrate_information，然后返回若干植物的字典

# 1.从上传的图像中进行获取
# ↓用于渲染上传图片的页面
@app.route('/upload_image') # TODO:这是示例代码，需要修改以适配前端
def index():
    return render_template('upload.html')
    # return '1'
# ↓当通过POST得到了img之后，就保存图片到本地
@app.route('/get_image', methods=['POST'])
def get_image():    # TODO:这是上传图片之后跳转到的url
    # Get the uploaded file
    img = request.files['image']    # img是一个FileStorage类型的对象
    print('type of img is', type(img))
    # Save the file to disk
    filename = img.filename
    img.save(os.path.join('uploads', filename))

    # Return a success response
    return 'File uploaded successfully!'



"""百科系统"""
# 1.根据中文名/别名/学名查询植物
@app.route('/searchName', methods=['GET'])
def query_by_name():
    # name是客户端输入的主体内容
    name = request.args.get('name') # TODO:'name'是form框的名字
    plant_list = pedia.query_by_names(name)
    return plant_list   # 这里返回跟这个name相关的所有植物的学名
    # type: list[str]
    # 返回的name list是用来展示候选的植物选项的

# 2.按分类浏览
@app.route('/classification', methods=['GET'])
def query_by_classification():
    # 点进了“按分类浏览”后，进入本页面
    return pedia.get_kingdom()  # type: list[str]

@app.route('/kingdom', methods=['GET'])
def kingdom2phylum():
    # 点击了某kingdom，如“植物界”之后，进入本页面
    # 并返回渲染phylum的表单选项
    # 在这个页面下，用户选择phylum
    kingdom = request.args.get('kingdom')
    phylum_lst = pedia.get_phylum(kingdom)
    return phylum_lst  # type: list[str]


@app.route('/phylum', methods=['GET'])
def phylum2class():
    # 点击了某phylum之后，进入本页面
    # 并返回渲染class的表单选项
    # 在这个页面下，用户选择class
    phylum = request.args.get('phylum')
    class_lst = pedia.get_class(phylum)
    return class_lst  # type: list[str]

@app.route('/class', methods=['GET'])
def class2order():
    # 点击了某class之后，进入本页面
    # 并返回渲染order的表单选项
    # 在这个页面下，用户选择order
    class_name = request.args.get('class')
    order_lst = pedia.get_order(class_name)
    return order_lst  # type: list[str]

@app.route('/order', methods=['GET'])
def order2family():
    # 点击了某order之后，进入本页面
    # 并返回渲染family的表单选项
    # 在这个页面下，用户选择family
    order = request.args.get('order')
    family_lst = pedia.get_family(order)
    return family_lst  # type: list[str]

@app.route('/family', methods=['GET'])
def family2genus():
    # 点击了某family之后，进入本页面
    # 并返回渲染genus的表单选项
    # 在这个页面下，用户选择genus
    family = request.args.get("family")
    genus_lst = pedia.get_genus(family)
    return genus_lst  # type: list[str]

@app.route('/genus', methods=['GET'])
def query_genus():
    # 点击了某个genus之后，进入本页面
    # 并返回渲染所有植物的名字
    genus = request.args.get("genus")
    # 获取该genus下的所有植物名
    plant_list = pedia.query_genus(genus)
    # 这个plant_list用来展示所有候选选项
    return plant_list   # type: list[str]


# 3.根据国家/地区/省份查询
@app.route('/distribution', methods=['GET'])
def query_by_location():
    # 点进了“按地点浏览”后，进入本页面
    return pedia.get_country() # type: list[str]

@app.route('/country', methods=['GET'])
def country2area():  
    # 选择了“中国”之后进入该页面，渲染输出area的选项表单
    country = request.args.get("country")
    area_lst = pedia.get_area(country)
    return area_lst # type: list[str]

@app.route('/area', methods=['GET'])
def area2province():
    # 选择了某地区如“长江流域”之后进入该页面，渲染输出province的选项表单
    area = request.args.get("area")
    province_lst = pedia.get_province(area)
    return province_lst # type: list[str]

@app.route('/province', methods=['GET'])
def query_province():
    # 选择了某个省份如“重庆”之后进入该页面，渲染输出在重庆的所有植物名的选项表单
    # 获取该province中的所有植物名
    province = request.args.get('province')
    plant_list = pedia.query_province(province)
    # 这个plant_list用来展示所有候选选项
    return plant_list   # type: list[str]