import os
import datetime
import uuid
from flask import Flask, make_response
from flask import render_template, render_template_string
from flask import request, redirect, url_for
from config import Config

app = Flask(__name__, static_url_path='/', static_folder='')

fs = []
first_layer = []
filter_p = ['/login', '/check']
session = {}

@app.route('/check', methods=['POST'])
def check():
    r = request.form
    print(r)
    if checkLogin():
        return redirect(url_for('index'))
    if checkAccount(r['account'], r['passwd']):
        session[r['account']] = uuid.uuid4().hex
        outdate = datetime.datetime.today() + datetime.timedelta(minutes=10)
        resp = make_response(redirect("index"))
        resp.set_cookie("easyBee", session[r['account']], expires=outdate)
        resp.set_cookie("name", r['account'], expires=outdate)
        return resp
    return "无权访问！"

@app.route('/login', methods=['get'])
def login_page():
    return render_template('index.html', first_layer=first_layer)

@app.route('/index')
def index():
    global fs, first_layer
    fs = first_layer = []
    first_layer = sorted(os.listdir("./templates"))
    first_layer = [f for f in first_layer if f!= 'index.html']
    for root, dirs, files in os.walk("./templates", topdown=False):
        for name in files:
            if name != 'index.html':
                path = os.path.join(root, name).replace('./templates', '')
                fs.append({'p':path, 'name':name, 'layer':path.split(os.sep)[1]})
    fs.sort(key = lambda k:k['p'])
    print(fs)
    return render_template('index.html', first_layer=first_layer, name=request.cookies.get("name"))

@app.before_request
def reject():
    print(request.path, checkLogin())
    if request.path == '/' and not checkLogin(): # 首页未登录
        return redirect(url_for('login_page'))
    if request.path == '/login' and checkLogin(): # login页面已登录
        return redirect(url_for('index'))
    if request.path in filter_p:
        return
    if not checkLogin():
        return "无权访问"
    if request.path == '/index': # 首页让 view func 处理
        return

    if len(request.path.split("/")) == 2: # 处理 first_layer
        layer = request.path.split('/')[1]
        return render_template('index.html', name='学习者', fs=[f for f in fs if f['layer'] == layer]) #temp
    # 处理其他页面
    for f in fs:
        if f['p'].replace('\\', '/').replace(' ', '') == request.path:
            return render_template(f['p'][len(os.sep):].replace("\\", "/"))

def checkLogin():
    name = request.cookies.get("name")
    return name and name in session and session[name] == request.cookies.get("easyBee")

def checkAccount(name, passwd):
    for account in Config.accounts:
        if passwd == account['passwd'] and name == account['name']:
            return True

app.run(debug=True, host='0.0.0.0')
