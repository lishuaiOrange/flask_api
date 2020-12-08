from flask import Flask,make_response,jsonify,request
import pymysql


app = Flask(__name__)

"""初始化数据库"""
def select(sentence):
    try:
        conn = pymysql.connect(
            host='47.100.164.202',
            user='root',
            password='123456',
            database='Testcases',
        )
        cursor = conn.cursor()
        sql = sentence
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except IndexError:
        return jsonify({'message':' select IndexError '})
    except pymysql.err.OperationalError:
        return jsonify({'message':' select OperationalError'})


@app.errorhandler(404)
def not_found(error):
     return make_response(jsonify({'error':'Not found'}),404)

@app.errorhandler(405)
def not_found(error):
     return make_response(jsonify({'error':'Method Not Allowed'}),405)

"""获取用户信息"""
@app.route('/userinfo/',methods=['GET'],strict_slashes=False)
def user_info():
    """从params获取参数"""
    username = request.args.get('username')
    """
    从path路径获取参数
    /userinfo/<username>/
    """
    try :
        sql = "select * from member"
        result = select(sql)
        message = []
        for i in range(len(result)):
            id = result[i][0]
            name = result[i][1]
            pwd = result[i][2]
            email = result[i][3]
            start_message = {
                'id': id,
                'name': name,
                'pwd': pwd,
                'email': email
            }
            message.append(start_message)
        return jsonify({'code':200,'data':message})
    except IndexError:
        return jsonify({'user_info': 'user_info index error','code': 200})
    except pymysql.err.ProgrammingError:
        return jsonify({'user_info': 'user_info ProgrammingError','code': 200})

"""登录"""
@app.route('/login/',methods=['POST'],strict_slashes=False)
def user_login():
    """ 
    request.get_data接收raw参数
    request.form.get接收form_data参数fsf
    """
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "select name from member"
    select_username = select(sql)
    list_name = []
    for i in range(len(select_username)):
        name = select_username[i][0]
        list_name.append(name)

    sql = "select pwd from member where name = '%s'" %username
    pwd = select(sql)[0][0]

    if password == pwd and username in list_name:
        return jsonify({'message': 'success','code': 200})
    else:
        return jsonify({'message': '用户名或密码错误','code': 200})

"""注册"""
@app.route('/register/',methods=['POST'],strict_slashes=False)
def user_register():
    get_username = request.form.get('username')
    get_password = request.form.get('password')

    sql = "select name from member"
    select_username = select(sql)
    list_name = []
    for i in range(len(select_username)):
        name = select_username[i][0]
        list_name.append(name)

    if get_username in list_name:
        return jsonify({'message': '用户名已存在','code': 200})
    elif get_password not in list_name:
        return jsonify({'message': '注册成功','code': 200})
def demo():
    pass
"""测试一下"""


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
