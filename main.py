import os
from flask import Flask
from flask import render_template, render_template_string
from flask import request

app = Flask(__name__, static_url_path='/', static_folder='')
fs = []
first_layer = []

@app.route('/')
def index():
    global fs, first_layer
    fs = first_layer = []
    first_layer = sorted(os.listdir("./templates"))
    first_layer = [f for f in first_layer if f!= 'index.html']
    for root, dirs, files in os.walk("./templates", topdown=False):
        print(root)
        for name in files:
            if name != 'index.html':
                path = os.path.join(root, name).replace('./templates', '')
                fs.append({'p':path, 'name':name, 'layer':path.split(os.sep)[1]})
    fs.sort(key = lambda k:k['p'])
    print(fs)
    return render_template('index.html', name='学习者', first_layer=first_layer)

@app.before_request
def reject():
    print(request.path.split("/"))
    if request.path == '/':
        return
    elif len(request.path.split("/")) == 2: #first_layer
        layer = request.path.split('/')[1]
        return render_template('index.html', name='学习者', fs=[f for f in fs if f['layer'] == layer]) #temp
    for f in fs:
        if f['p'].replace('\\', '/').replace(' ', '') == request.path:
            return render_template(f['p'][len(os.sep):].replace("\\", "/"))

app.run(debug=True, host='0.0.0.0')
