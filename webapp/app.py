import subprocess
import configparser
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Определяем путь к корневой папке проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_hosts():
    """Читает хосты из файла hosts.ini."""
    inventory_path = os.path.join(project_root, 'hosts.ini')
    config = configparser.ConfigParser()
    config.read(inventory_path)
    if 'windows' in config:
        # Возвращаем список имен хостов (то что до ansible_host=...)
        return [host for host, _ in config.items('windows')]
    return []

@app.route('/')
def index():
    """Главная страница, показывает список хостов."""
    hosts = get_hosts()
    return render_template('index.html', hosts=hosts)

@app.route('/run_playbook', methods=['POST'])
def run_playbook():
    """Запускает плейбук для выбранного хоста."""
    hostname = request.form.get('hostname')
    if not hostname:
        return "Ошибка: хост не выбран!", 400

    # Формируем команду для запуска Ansible
    # Мы запускаем ее из корневой папки проекта
    command = [
        "ansible-playbook",
        "playbook.yml",
        "-i", "hosts.ini",
        "--limit", hostname
    ]

    # Запускаем процесс и получаем результат
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=project_root  # Указываем рабочую директорию
    )

    # Форматируем вывод для отображения в HTML
    output = result.stdout + result.stderr

    return render_template('result.html', output=output, hostname=hostname)

if __name__ == '__main__':
    # 0.0.0.0 чтобы было доступно по сети, а не только с localhost
    app.run(host='0.0.0.0', port=5000, debug=True)
