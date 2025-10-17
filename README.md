# driver-deploy-hackathon
Стек технологий: 
1. Сервер управления (Control Node):
- 1.1. ОС: Ubuntu Server 22.04 LTS
- 1.2. Система автоматизации: Ansible
- 1.3. Веб-интерфейс: Python 3 + Flask
- 1.4. Система контроля версий: Git
2. Управляемые узлы (Managed Nodes):
- 2.1 Windows Server 2022 / Windows 10
- 2.2 Ubuntu Server 22.04 LTS
4. Протоколы и технологии:
- 3.1 Для Windows: WinRM
- 3.2 Для Linux: SSH
5. Хранение драйверов: GitHub Releases
6. Логи в реальном времени: Server-Sent Events (SSE)

Проект работает по схеме браузер → Flask → Ansible → хост → лог → браузер.

1. Пользователь через браузер выбирает хост и драйверы на странице index.html.
2. Flask (app.py) принимает запрос, формирует команду для ansible-playbook install_drivers.yml и запускает её.
3. Ansible подключается к указанному хосту (из hosts.ini) и устанавливает выбранные драйверы.
4. Вывод Ansible в реальном времени передаётся обратно через Server-Sent Events (SSE).
5. Страница `result.html` отображает лог выполнения и сообщает об окончании процесса.
