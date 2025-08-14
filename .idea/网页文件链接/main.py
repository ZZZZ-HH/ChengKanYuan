from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import webbrowser
from threading import Timer
import configparser
import platform
import subprocess
import json

app = Flask(__name__, template_folder='.')

# 配置文件路径
CONFIG_FILE = 'config.ini'

def get_config():
    """读取配置文件"""
    config = configparser.ConfigParser()
    default_path = os.path.join(os.getcwd(), 'files')

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    else:
        config['SETTINGS'] = {'FILE_PATH': default_path}
    
    file_path = config['SETTINGS'].get('FILE_PATH', default_path)
    
    # 确保路径存在
    os.makedirs(file_path, exist_ok=True)
    
    return {'FILE_PATH': os.path.abspath(file_path)}

def save_config(file_path):
    """保存配置文件"""
    config = configparser.ConfigParser()
    config['SETTINGS'] = {'FILE_PATH': os.path.abspath(file_path)}
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def get_files():
    """获取文件列表"""
    config = get_config()
    file_path = config['FILE_PATH']
    
    files = []
    for f in os.listdir(file_path):
        if f.lower().endswith(('.docx', '.xlsx', '.doc', '.xls')):
            files.append(f)
    
    return files, file_path

def open_browser():
    """自动打开浏览器"""
    webbrowser.open_new('http://localhost:5000/')

def open_file_with_default_app(file_path):
    """使用系统默认应用打开文件"""
    try:
        if platform.system() == 'Windows':
            os.startfile(file_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', file_path))
        else:  # Linux
            subprocess.call(('xdg-open', file_path))
        return True
    except Exception as e:
        print(f"打开文件失败: {e}")
        return False

@app.route('/')
def index():
    """主页面"""
    files, current_path = get_files()
    return render_template('index.html', files=files, current_path=current_path)

@app.route('/update_path', methods=['POST'])
def update_path():
    """更新文件存储路径"""
    new_path = request.form.get('new_path')
    
    if new_path and os.path.isdir(new_path):
        save_config(new_path)
        return redirect(url_for('index'))
    else:
        return f"无效路径！<a href='/'>返回首页</a>"

@app.route('/open_file', methods=['POST'])
def open_file():
    """打开指定文件"""
    data = request.get_json()
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'success': False, 'error': '未提供文件名'})
    
    _, file_path = get_files()
    full_path = os.path.join(file_path, filename)
    
    if not os.path.exists(full_path):
        return jsonify({'success': False, 'error': '文件不存在'})
    
    # 使用系统默认应用打开文件
    success = open_file_with_default_app(full_path)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': '无法打开文件'})

if __name__ == '__main__':
    # 确保配置文件存在
    if not os.path.exists(CONFIG_FILE):
        save_config(os.path.join(os.getcwd(), 'files'))
    
    # 3秒后自动打开浏览器
    Timer(3, open_browser).start()
    app.run(debug=False, port=5000)