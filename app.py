from datetime import datetime
import math
import os
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
import pymysql
from math import ceil

import os

# 2. 完整防治措施字典
prevention_measures = {
    "水稻细菌性谷枯病": """
        <ol style="margin: 5px 0; padding-left: 20px;">
            <li>使用20%噻菌铜悬浮剂500倍液喷雾</li>
            <li>播种前用50%氯溴异氰尿酸浸种6小时</li>
            <li>发病初期及时拔除病株</li>
            <li>保持田间排水通畅</li>
        </ol>
    """,
    "稻瘟病": """
        <ol style="margin: 5px 0; padding-left: 20px;">
            <li>使用40%稻瘟灵乳油1000倍液喷雾</li>
            <li>合理施用硅肥增强抗病性</li>
            <li>保持合理种植密度（丛距20×20cm）</li>
            <li>及时处理病稻草，减少菌源</li>
        </ol>
    """,
    "水稻细菌性褐斑病": """
        <ol style="margin: 5px 0; padding-left: 20px;">
            <li>使用20%叶枯唑可湿性粉剂500倍液</li>
            <li>增施钾肥（每亩氯化钾5-7公斤）</li>
            <li>避免深水灌溉，采用浅湿灌溉</li>
            <li>收获后深耕灭茬（深度15-20cm）</li>
        </ol>
    """,
    "水稻东格鲁病毒病": """
        <ol style="margin: 5px 0; padding-left: 20px;">
            <li>使用10%吡虫啉防治叶蝉等传毒媒介</li>
            <li>发现病株立即拔除并销毁</li>
            <li>选用抗病品种（如IR36、IR50）</li>
            <li>避免晚稻早栽（避开6月虫媒高峰期）</li>
        </ol>
    """
}
from test import user_predict

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='rice_recognition',
    charset='utf8'
)

cursor = conn.cursor()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjjy'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        select_sql = 'select id,password from user where username = %s'
        cursor.execute(select_sql, username)
        userobj = cursor.fetchone()
        if userobj is None:
            return jsonify({'state': 'error', 'message': '用户不存在'})
        elif userobj[1] != password:
            return jsonify({'state': 'error', 'message': '密码错误'})
        else:
            session.clear()  # 清除旧的会话信息
            session['userid'] = userobj[0]  # 设置新的会话信息
            return jsonify({'state': 'success', 'message': '登录成功'})
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    select_sql = 'select username from user where username = %s'
    cursor.execute(select_sql, username)
    exit_username = cursor.fetchone()
    if exit_username is None:
        insert_sql = 'insert into user(username,password) values (%s,%s)'
        cursor.execute(insert_sql, (username, password))
        conn.commit()
        return jsonify({'state': 'success', 'message': '注册成功'})
    else:
        return jsonify({'state': 'error', 'message': '用户已存在'})


@app.route('/index')
def index():
    select_sql = 'select id,title,content,datetime,img_url from knowledge limit 4'
    cursor.execute(select_sql)
    knowledge_list = cursor.fetchall()
    count = len(knowledge_list)
    return render_template('index.html', knowledge_list=knowledge_list, count=count)


@app.route('/detail', methods=['GET', 'POST'])
def detail():
    id = request.args.get('id')
    select_sql = 'select id,title,content,datetime,detail,img_url from knowledge where id = %s'
    cursor.execute(select_sql, id)
    detail_list = cursor.fetchall()
    id = detail_list[0][0]
    title = detail_list[0][1]
    content = detail_list[0][2]
    datetime = detail_list[0][3]
    detail = detail_list[0][4]
    img_url = detail_list[0][5]
    return render_template('detail.html', id=id, title=title, content=content, datetime=datetime, detail=detail,
                           img_url=img_url)


@app.route('/right_base', methods=['GET', 'POST'])
def right_base():
    select_sql = 'select id,title from knowledge limit 4'
    cursor.execute(select_sql)
    right_list = cursor.fetchall()
    # print(right_list)
    return jsonify(right_list)


@app.route('/image_recognition', methods=['GET', 'POST'])
def image_recognition():
    if request.method == 'POST':
        file = request.files['file']
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"image_{timestamp}.jpg"
        # 保存图片到指定路径
        file.save(f'static/all_records/{filename}')

        result, max_confidence = user_predict(f'static/all_records/{filename}')
        user_id = session['userid']

        select_sql = "INSERT INTO recognition_records (user_id, recognition_time, image_url, recognition_result) VALUES (%s, NOW(), %s, %s)"
        cursor.execute(select_sql, (user_id, os.path.join('static/all_records/', filename), result))
        conn.commit()

        select_id = 'select id,img_url from category_list where title like %s'
        cursor.execute(select_id, result)
        identify_result = cursor.fetchall()
        print('...............................', identify_result)
        return jsonify({'result': '有' + str(max_confidence) + '% 的可能性是' + result, 'identify_result': identify_result})
    return render_template('image_recognition.html')


@app.route('/knowledge')
def knowledge():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    select_sql = 'select id,title,content,datetime from knowledge'
    cursor.execute(select_sql)
    knowledge_list = cursor.fetchall()

    total_pages = ceil(len(knowledge_list) / per_page)
    knowledge_list_paginated = knowledge_list[(page - 1) * per_page:page * per_page]

    return render_template('knowledge.html', knowledge_list_paginated=knowledge_list_paginated, total_pages=total_pages,
                           page=page)


@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('keyword')
    select_sql = 'select id, title, content, datetime from knowledge where title REGEXP %s'
    cursor.execute(select_sql, keyword)
    rows = cursor.fetchall()
    knowledge_list_paginated = [row for row in rows if re.search(keyword, row[1], re.IGNORECASE)]

    return render_template('knowledge.html', knowledge_list_paginated=knowledge_list_paginated, page=1, total_pages=1)


@app.route('/category_list', methods=['GET', 'POST'])
def category_list():
    # 获取当前页数，默认为第1页
    page = request.args.get('page', 1, type=int)
    # 每页显示的数量
    per_page = 6
    # 查询总的数据条数
    select_count_sql = 'SELECT COUNT(*) FROM category_list'
    cursor.execute(select_count_sql)
    total_count = cursor.fetchone()
    total_pages = math.ceil(total_count[0] / per_page)

    # 查询当前页的数据
    select_sql = f'SELECT id, title, img_url, category_id FROM category_list LIMIT {(page - 1) * per_page}, {per_page}'
    cursor.execute(select_sql)
    category_list = cursor.fetchall()
    # 分类列表
    select_category = 'SELECT id, name FROM category'
    cursor.execute(select_category)
    all_category = cursor.fetchall()
    return render_template('category_list.html', category_list=category_list, page=page, total_pages=total_pages,
                           all_category=all_category)


@app.route('/category_detail')
def category_detail():
    uid = request.args.get('id')
    select_sql = 'select id,title,img_url,detail,category_id from category_list where id = %s'
    cursor.execute(select_sql, uid)
    datalist = cursor.fetchall()
    id = datalist[0][0]
    title = datalist[0][1]
    img_url = datalist[0][2]
    detail = datalist[0][3]
    category_id = datalist[0][4]
    return render_template('category_detail.html', id=id, title=title, img_url=img_url, detail=detail,
                           category_id=category_id)


@app.route('/sort', methods=['GET', 'POST'])
def sort():
    selected_value = request.args.get('selectedValue')
    print(selected_value)
    if selected_value is None or selected_value == '':
        # 获取当前页数，默认为第1页
        page = request.args.get('page', 1, type=int)
        # 每页显示的数量
        per_page = 6
        # 查询总的数据条数
        select_count_sql = 'SELECT COUNT(*) FROM category_list'
        cursor.execute(select_count_sql)
        total_count = cursor.fetchone()
        total_pages = math.ceil(total_count[0] / per_page)
        # 查询当前页的数据
        select_sql = f'SELECT id, title, img_url, category_id FROM category_list LIMIT {(page - 1) * per_page}, {per_page}'
        cursor.execute(select_sql)
        category_list = cursor.fetchall()
        # 分类列表
        select_category = 'SELECT id, name FROM category'
        cursor.execute(select_category)
        all_category = cursor.fetchall()
        print(all_category)
        return render_template('sort.html', category_list=category_list, page=page, total_pages=total_pages,
                               all_category=all_category, selected_value='')
    else:
        selectedValue = request.args.get('selectedValue')
        # 获取当前页数，默认为第1页
        page = request.args.get('page', 1, type=int)
        # 每页显示的数量
        per_page = 6
        # 查询总的数据条数
        select_count_sql = 'SELECT COUNT(*) FROM category_list where category_id = %s'
        cursor.execute(select_count_sql, selectedValue)
        total_count = cursor.fetchone()
        total_pages = math.ceil(total_count[0] / per_page)
        # 查询当前页的数据
        select_sql = f'SELECT id, title, img_url, category_id FROM category_list where category_id = %s LIMIT {(page - 1) * per_page}, {per_page}'
        cursor.execute(select_sql, selectedValue)
        category_list = cursor.fetchall()
        # print(category_list)
        # 分类列表
        select_category = 'SELECT id, name FROM category'
        cursor.execute(select_category)
        all_category = cursor.fetchall()
        return render_template('sort.html', category_list=category_list, page=page, total_pages=total_pages,
                               all_category=all_category, selectedValue=selectedValue)


@app.route('/identification_record')
def identification_record():
    user_id = session['userid']
    select_sql = 'SELECT id, user_id, recognition_time, image_url, recognition_result FROM recognition_records WHERE user_id = %s'
    cursor.execute(select_sql, (user_id,))
    all_records = cursor.fetchall()

    # 分页逻辑
    per_page = 8  # 每页显示的数据量
    total_records = len(all_records)
    total_pages = (total_records + per_page - 1) // per_page  # 总页数
    current_page = request.args.get('page', type=int, default=1)  # 从 URL 参数获取当前页码，默认为第一页
    start = (current_page - 1) * per_page
    end = start + per_page

    datalist = all_records[start:end]  # 获取指定页码的数据
    # 查询防治建议信息
    sql = 'select title,content from prevention_suggestion where title = %s'
    # 1. 统计病害次数
    cursor.execute('''
    #        SELECT recognition_result, COUNT(*) as count
    #        FROM recognition_records
    #        WHERE user_id = %s
    #       GROUP BY recognition_result
    #        HAVING count >= 2
    #    ''', (user_id,))
    warning_diseases = cursor.fetchall()
    warnings = []
    for disease, count in warning_diseases:
        cursor.execute(sql, (disease,))
        measure = cursor.fetchall()[0][1]

        # measure = prevention_measures.get(disease, "暂无防治措施信息")
        warnings.append({
            "disease": disease,
            "count": count,
            "measure": measure
        })

    return render_template('identification_record.html', datalist=datalist, total_pages=total_pages, warnings=warnings,
                           # 传递预警信息到模板
                           current_page=current_page)
@app.route('/prevention')
def prevention():
    user_id = session['userid']
    select_sql = 'SELECT id, user_id, recognition_time, image_url, recognition_result FROM recognition_records WHERE user_id = %s'
    cursor.execute(select_sql, (user_id,))
    all_records = cursor.fetchall()

    # 分页逻辑
    per_page = 8  # 每页显示的数据量
    total_records = len(all_records)
    total_pages = (total_records + per_page - 1) // per_page  # 总页数
    current_page = request.args.get('page', type=int, default=1)  # 从 URL 参数获取当前页码，默认为第一页
    start = (current_page - 1) * per_page
    end = start + per_page

    datalist = all_records[start:end]  # 获取指定页码的数据
    # 查询防治建议信息
    sql = 'select title,content from prevention_suggestion where title = %s'
    # 1. 统计病害次数
    cursor.execute('''
            SELECT recognition_result, COUNT(*) as count 
            FROM recognition_records 
            WHERE user_id = %s 
            GROUP BY recognition_result 
            HAVING count >= 2
        ''', (user_id,))
    warning_diseases = cursor.fetchall()
    warnings = []
    for disease, count in warning_diseases:
        cursor.execute(sql, (disease,))
        measure = cursor.fetchall()[0][1]

        # measure = prevention_measures.get(disease, "暂无防治措施信息")
        warnings.append({
            "disease": disease,
            "count": count,
            "measure": measure
        })
        # 药材识别统计
        select_sql = 'SELECT recognition_result, COUNT(recognition_result) FROM recognition_records GROUP BY recognition_result;'
        cursor.execute(select_sql)
        drug_count = cursor.fetchall()
        pie_data = [{'value': count, 'name': recognition_result} for recognition_result, count in drug_count]

        # 每个用户识别的次数
        select_sql1 = 'SELECT user_id, COUNT(user_id) FROM recognition_records GROUP BY user_id;'
        cursor.execute(select_sql1)
        user_count = cursor.fetchall()
        user_count_data = [{'value': count, 'name': user_id} for user_id, count in user_count]

        # 执行查询
        date_sql = 'SELECT DATE(recognition_time) AS recognition_date, COUNT(*) AS recognition_count FROM recognition_records GROUP BY recognition_date ORDER BY recognition_date;'
        cursor.execute(date_sql)
        date_list = cursor.fetchall()

        # 提取日期和统计次数
        dates = [str(d[0]) for d in date_list]
        counts = [d[1] for d in date_list]

        user_all_sql = 'select count(*) from user '
        cursor.execute(user_all_sql)
        user_num = cursor.fetchone()[0]

        drug_all_sql = 'select count(*) from category_list'
        cursor.execute(drug_all_sql)
        drug_num = cursor.fetchone()[0]

        category_all_sql = 'select count(*) from category'
        cursor.execute(category_all_sql)
        category_num = cursor.fetchone()[0]

        knowledge_all_sql = 'select count(*) from knowledge'
        cursor.execute(knowledge_all_sql)
        knowledge_num = cursor.fetchone()[0]

        recognition_all_sql = 'select count(*) from recognition_records'
        cursor.execute(recognition_all_sql)
        recognition_num = cursor.fetchone()[0]

        return render_template('prevention.html', datalist=datalist, total_pages=total_pages, warnings=warnings,
                               # 传递预警信息到模板
                               current_page=current_page, pie_data=pie_data, user_count_data=user_count_data,
                               dates=dates,
                               counts=counts,
                               user_num=user_num, drug_num=drug_num, category_num=category_num,
                               knowledge_num=knowledge_num,
                               recognition_num=recognition_num)
    #return render_template('prevention.html', datalist=datalist, total_pages=total_pages, warnings=warnings,
                           # 传递预警信息到模板
                           #current_page=current_page)



@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        select_sql = 'select password from admin where username = %s'
        cursor.execute(select_sql, username)
        exit_password = cursor.fetchone()
        if exit_password is None:
            return jsonify({'state': 'error', 'message': '用户不存在'})
        elif exit_password[0] != password:
            return jsonify({'state': 'error', 'message': '密码错误'})
        else:
            return jsonify({'state': 'success', 'message': '登录成功'})
    else:
        return render_template('admin/login.html')


# @app.route('/admin_index')
# def admin_index():
#     return render_template('admin/index.html')


@app.route('/knowledge_list')
def knowledge_list():
    select_sql = 'select id,title,content,datetime,detail,img_url from knowledge'
    cursor.execute(select_sql)
    knowledge_list = cursor.fetchall()
    return render_template('admin/knowledge_list.html', knowledge_list=knowledge_list)


@app.route('/knowledge_update', methods=['GET', 'POST'])
def knowledge_update():
    if request.method == 'GET':
        id = request.args.get('id')
        select_sql = 'select id,title,content,datetime,detail,img_url from knowledge where id = %s'
        cursor.execute(select_sql, id)
        datalist = cursor.fetchall()
        id = datalist[0][0]
        title = datalist[0][1]
        content = datalist[0][2]
        datetime = datalist[0][3]
        detail = datalist[0][4]
        img_url = datalist[0][5]
        return jsonify(
            {'id': id, 'title': title, 'content': content, 'datetime': datetime, 'detail': detail, 'img_url': img_url})
    else:
        id = request.form['id']
        knowledge_title = request.form['knowledge_title']
        knowledge_content = request.form['knowledge_content']
        knowledge_datetime = request.form['knowledge_datetime']
        knowledge_detail = request.form['knowledge_detail']
        knowledge_img_url = request.form['knowledge_img_url']
        update_sql = 'update knowledge set title=%s,content=%s,datetime=%s,detail=%s,img_url=%s where id = %s'
        cursor.execute(update_sql, (
            knowledge_title, knowledge_content, knowledge_datetime, knowledge_detail, knowledge_img_url, id))
        conn.commit()
        return jsonify({'status': 'success'})


@app.route('/knowledge_add', methods=['GET', 'POST'])
def knowledge_add():
    knowledge_title = request.form.get('knowledge_title')
    knowledge_content = request.form.get('knowledge_content')
    knowledge_datetime = request.form.get('knowledge_datetime')
    knowledge_detail = request.form.get('knowledge_detail')
    knowledge_img_url = request.form.get('knowledge_img_url')
    insert_sql = 'insert into knowledge(title,content,datetime,detail,img_url) values(%s,%s,%s,%s,%s)'
    cursor.execute(insert_sql,
                   (knowledge_title, knowledge_content, knowledge_datetime, knowledge_detail, knowledge_img_url))
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/knowledge_del', methods=['GET', 'POST'])
def knowledge_del():
    id = request.form.get('id')
    del_sql = 'delete from knowledge where id = %s'
    cursor.execute(del_sql, id)
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/admin_category_list')
def admin_category_list():
    select_sql = 'select id,title,img_url,detail,category_id from category_list'
    cursor.execute(select_sql)
    category_list = cursor.fetchall()
    return render_template('admin/category_list.html', category_list=category_list)


@app.route('/category_update', methods=['GET', 'POST'])
def category_update():
    if request.method == 'GET':
        id = request.args.get('id')
        select_sql = 'select id,title,img_url,detail,category_id from category_list where id = %s'
        cursor.execute(select_sql, id)
        datalist = cursor.fetchall()
        id = datalist[0][0]
        title = datalist[0][1]
        img_url = datalist[0][2]
        detail = datalist[0][3]
        category_id = datalist[0][4]
        return jsonify({'id': id, 'title': title, 'img_url': img_url, 'detail': detail, 'category_id': category_id})
    else:
        id = request.form['id']
        title = request.form['title']
        img_url = request.form['img_url']
        detail = request.form['detail']
        category_id = request.form['category_id']

        update_sql = 'update category_list set title=%s,img_url=%s,detail=%s,category_id=%s where id = %s'
        cursor.execute(update_sql, (title, img_url, detail, category_id, id))
        conn.commit()
        return jsonify({'status': 'success'})


@app.route('/category_add', methods=['GET', 'POST'])
def category_add():
    title = request.form.get('title')
    img_url = request.form.get('img_url')
    detail = request.form.get('detail')
    category_id = request.form.get('category_id')

    insert_sql = 'insert into category_list(title,img_url,detail,category_id) values(%s,%s,%s,%s)'
    cursor.execute(insert_sql, (title, img_url, detail, category_id))
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/category_del', methods=['GET', 'POST'])
def category_del():
    id = request.form.get('id')
    del_sql = 'delete from category_list where id = %s'
    cursor.execute(del_sql, id)
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/user_list')
def user_list():
    select_sql = 'select id,username,password from user'
    cursor.execute(select_sql)
    user_list = cursor.fetchall()
    return render_template('admin/user_list.html', user_list=user_list)


@app.route('/user_update', methods=['GET', 'POST'])
def user_update():
    if request.method == 'GET':
        id = request.args.get('id')
        select_sql = 'select id,username,password from user where id = %s'
        cursor.execute(select_sql, id)
        datalist = cursor.fetchall()
        id = datalist[0][0]
        username = datalist[0][1]
        password = datalist[0][2]
        return jsonify({'id': id, 'username': username, 'password': password})
    else:
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        update_sql = 'update user set username=%s,password=%s where id = %s'
        cursor.execute(update_sql, (username, password, id))
        conn.commit()
        return jsonify({'status': 'success'})


@app.route('/user_add', methods=['GET', 'POST'])
def user_add():
    username = request.form.get('username')
    password = request.form.get('password')
    insert_sql = 'insert into user(username,password) values(%s,%s)'
    cursor.execute(insert_sql, (username, password))
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/user_del', methods=['GET', 'POST'])
def user_del():
    id = request.form.get('id')
    del_sql = 'delete from user where id = %s'
    cursor.execute(del_sql, id)
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/prevention_list')
def prevention_list():
    select_sql = 'select id,title,content from prevention_suggestion'
    cursor.execute(select_sql)
    prevention_list = cursor.fetchall()
    return render_template('admin/prevention_list.html', prevention_list=prevention_list)


@app.route('/prevention_update', methods=['GET', 'POST'])
def prevention_update():
    if request.method == 'GET':
        id = request.args.get('id')
        select_sql = 'select id,title,content from prevention_suggestion where id = %s'
        cursor.execute(select_sql, id)
        datalist = cursor.fetchall()
        id = datalist[0][0]
        title = datalist[0][1]
        content = datalist[0][2]
        print(id, title, content)
        return jsonify({'id': id, 'title': title, 'content': content})
    else:
        id = request.form['id']
        title = request.form['title']
        content = request.form['content']
        update_sql = 'update prevention_suggestion set title=%s,content=%s where id = %s'
        cursor.execute(update_sql, (title, content, id))
        conn.commit()
        return jsonify({'status': 'success'})


@app.route('/prevention_add', methods=['GET', 'POST'])
def prevention_add():
    title = request.form.get('title')
    content = request.form.get('content')
    insert_sql = 'insert into prevention_suggestion(title,content) values(%s,%s)'
    cursor.execute(insert_sql, (title, content))
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/prevention_del', methods=['GET', 'POST'])
def prevention_del():
    id = request.form.get('id')
    del_sql = 'delete from prevention_suggestion where id = %s'
    cursor.execute(del_sql, id)
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/category_management')
def category_management():
    select_sql = 'select id,name from category'
    cursor.execute(select_sql)
    category_list = cursor.fetchall()
    return render_template('admin/category_management.html', category_list=category_list)


@app.route('/category_management_update', methods=['GET', 'POST'])
def category_management_update():
    if request.method == 'GET':
        id = request.args.get('id')
        select_sql = 'select id,name from category where id = %s'
        cursor.execute(select_sql, id)
        datalist = cursor.fetchall()
        id = datalist[0][0]
        name = datalist[0][1]

        return jsonify({'id': id, 'name': name})
    else:
        id = request.form['id']
        name = request.form['name']
        update_sql = 'update category set name=%s where id = %s'
        cursor.execute(update_sql, (name, id))
        conn.commit()
        return jsonify({'status': 'success'})


@app.route('/category_management_add', methods=['GET', 'POST'])
def category_management_add():
    name = request.form.get('name')
    insert_sql = 'insert into category(name) values(%s)'
    cursor.execute(insert_sql, (name))
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/category_management_del', methods=['GET', 'POST'])
def category_management_del():
    id = request.form.get('id')
    del_sql = 'delete from category where id = %s'
    cursor.execute(del_sql, id)
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/admin_identification_record_list')
def admin_identification_record():
    select_sql = 'select id,user_id,recognition_time,image_url,recognition_result from recognition_records'
    cursor.execute(select_sql)
    data_list = cursor.fetchall()
    return render_template('admin/identification_record_list.html', data_list=data_list)


@app.route('/identification_update', methods=['GET', 'POST'])
def identification_update():
    if request.method == 'GET':
        id = request.args.get('id')
        select_sql = 'select id,user_id,recognition_time,image_url,recognition_result from recognition_records where id = %s'
        cursor.execute(select_sql, id)
        datalist = cursor.fetchall()
        id = datalist[0][0]
        user_id = datalist[0][1]
        recognition_time = datalist[0][2].strftime("%Y-%m-%d %H:%M:%S")
        image_url = datalist[0][3]
        recognition_result = datalist[0][4]
        return jsonify({'id': id, 'user_id': user_id, 'recognition_time': recognition_time, 'image_url': image_url,
                        'recognition_result': recognition_result})
    else:
        id = request.form['id']
        user_id = request.form['user_id']
        recognition_time = request.form['recognition_time']
        image_url = request.form['image_url']
        recognition_result = request.form['recognition_result']
        update_sql = 'update recognition_records set user_id=%s,recognition_time=%s,image_url=%s,recognition_result=%s where id = %s'
        cursor.execute(update_sql, (user_id, recognition_time, image_url, recognition_result, id))
        conn.commit()
        return jsonify({'status': 'success'})


@app.route('/identification_add', methods=['GET', 'POST'])
def identification_add():
    user_id = request.form.get('user_id')
    recognition_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_url = request.form.get('image_url')
    recognition_result = request.form.get('recognition_result')
    insert_sql = 'insert into recognition_records(user_id,recognition_time,image_url,recognition_result) values(%s,%s,%s,%s)'
    cursor.execute(insert_sql, (user_id, recognition_time, image_url, recognition_result))
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/identification_del', methods=['GET', 'POST'])
def identification_del():
    id = request.form.get('id')
    del_sql = 'delete from recognition_records where id = %s'
    cursor.execute(del_sql, id)
    conn.commit()
    return jsonify({'status': 'success'})


@app.route('/admin_analysis')
def admin_analysis():
    # 药材识别统计
    select_sql = 'SELECT recognition_result, COUNT(recognition_result) FROM recognition_records GROUP BY recognition_result;'
    cursor.execute(select_sql)
    drug_count = cursor.fetchall()
    # print(drug_count)
    pie_data = [{'value': count, 'name': recognition_result} for recognition_result, count in drug_count]

    # 每个用户识别的次数
    select_sql1 = 'SELECT user_id, COUNT(user_id) FROM recognition_records GROUP BY user_id;'
    cursor.execute(select_sql1)
    user_count = cursor.fetchall()
    user_count_data = [{'value': count, 'name': user_id} for user_id, count in user_count]

    # 执行查询
    date_sql = 'SELECT DATE(recognition_time) AS recognition_date, COUNT(*) AS recognition_count FROM recognition_records GROUP BY recognition_date ORDER BY recognition_date;'
    cursor.execute(date_sql)
    date_list = cursor.fetchall()

    # 提取日期和统计次数
    dates = [str(d[0]) for d in date_list]
    counts = [d[1] for d in date_list]

    user_all_sql = 'select count(*) from user '
    cursor.execute(user_all_sql)
    user_num = cursor.fetchone()[0]

    drug_all_sql = 'select count(*) from category_list'
    cursor.execute(drug_all_sql)
    drug_num = cursor.fetchone()[0]

    category_all_sql = 'select count(*) from category'
    cursor.execute(category_all_sql)
    category_num = cursor.fetchone()[0]

    knowledge_all_sql = 'select count(*) from knowledge'
    cursor.execute(knowledge_all_sql)
    knowledge_num = cursor.fetchone()[0]

    recognition_all_sql = 'select count(*) from recognition_records'
    cursor.execute(recognition_all_sql)
    recognition_num = cursor.fetchone()[0]

    return render_template('admin/analysis.html', pie_data=pie_data, user_count_data=user_count_data, dates=dates,
                           counts=counts,
                           user_num=user_num, drug_num=drug_num, category_num=category_num, knowledge_num=knowledge_num,
                           recognition_num=recognition_num)


if __name__ == '__main__':
    app.run()
