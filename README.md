# driver-deploy-hackathon

Сервер управления (Control Node):
ОС: Ubuntu Server 22.04 LTS
Система автоматизации: Ansible
Веб-интерфейс: Python 3 + Flask
Система контроля версий: Git
Управляемые узлы (Managed Nodes):
Windows Server 2022 / Windows 10
Ubuntu Server 22.04 LTS
Протоколы и технологии:
Для Windows: WinRM
Для Linux: SSH
Хранение драйверов: GitHub Releases
Логи в реальном времени: Server-Sent Events (SSE)

Проект работает по схеме браузер → Flask → Ansible → хост → лог → браузер.

1. Пользователь через браузер выбирает хост и драйверы на странице index.html.
2. Flask (app.py) принимает запрос, формирует команду для ansible-playbook install_drivers.yml и запускает её.
3. Ansible подключается к указанному хосту (из hosts.ini) и устанавливает выбранные драйверы.
4. Вывод Ansible в реальном времени передаётся обратно через Server-Sent Events (SSE).
5. Страница `result.html` отображает лог выполнения и сообщает об окончании процесса.
