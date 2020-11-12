import os
from flask import Flask
from flask import render_template, render_template_string
from flask import request

app = Flask(__name__, static_url_path='/', static_folder='')
fs = []
@app.route('/')
def index():
    global fs
    fs = []
    for root, dirs, files in os.walk("./templates", topdown=False):
        for name in files:
            fs.append({'p':os.path.join(root, name).replace('./templates', ''), 'name':name})
    print(fs)
    return render_template('index.html', name='学习者', fs=fs)

@app.before_request
def reject():
    if not request.path or request.path == '/':
        return 
    req_p_id = request.path.split('/')[1:]
    for f in fs:
        f_id = f['p'].split(os.sep)[1:]
        if identify(f_id, req_p_id):
            print(f['p'][2:])
            return render_template(f['p'][len(os.sep):].replace("\\", "/"))

def identify(f_id, req_p_id):
    if len(f_id) != len(req_p_id):
        return False
    for i, p in enumerate(req_p_id):
        if (i != len(req_p_id) - 1 and p == f_id[i]) or \
            (i == len(req_p_id) - 1 and f_id[i].startswith(p)):
            continue
        else:
            return False
    print(f_id, req_p_id)
    return True

app.run(debug=True, host='0.0.0.0')
