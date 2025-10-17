import subprocess
import configparser
import os
from flask import Flask, render_template, request, Response, stream_with_context

app = Flask(__name__)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
inventory_path = os.path.join(project_root, 'hosts.ini')

def get_hosts():
    config = configparser.ConfigParser()
    config.read(inventory_path)
    hosts = []
    
    sections = ['windows', 'linux']
    for section in sections:
        if config.has_section(section):
            for option in config.options(section):
                # Разделяем строку по пробелу и берем только первое слово (имя хоста)
                hostname = option.split(' ')[0]
                hosts.append(hostname)
    return hosts

@app.route('/')
def index():
    hosts = get_hosts()
    return render_template('index.html', hosts=hosts)

@app.route('/run_playbook', methods=['POST'])
def run_playbook():
    hostname = request.form.get('hostname')
    selected_drivers = request.form.getlist('drivers')

    if not hostname or not selected_drivers:
        return "Ошибка: не все параметры выбраны!", 400

    return render_template('result.html', hostname=hostname, drivers=",".join(selected_drivers))

@app.route('/stream')
def stream():
    hostname = request.args.get('hostname')
    drivers_str = request.args.get('drivers')

    command = [
        "ansible-playbook",
        "install_drivers.yml",
        "-i", "hosts.ini",
        "-t", drivers_str
    ]

    if hostname != "all":
        command.extend(["--limit", hostname])

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=project_root,
        bufsize=1
    )

    def generate():
        yield f"data: Запускаем команду: {' '.join(command)}\n\n"
        
        for line in iter(process.stdout.readline, ''):
            yield f"data: {line}\n\n"
        
        process.stdout.close()
        return_code = process.wait()
        yield f"data: \n--- ПРОЦЕСС ЗАВЕРШЕН С КОДОМ: {return_code} ---\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
