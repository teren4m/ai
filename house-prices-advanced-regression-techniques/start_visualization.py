import subprocess as sb
import threading
import time
import webbrowser


def start_dashboard():
    sb.run(["optuna-dashboard", "sqlite:///../study.db"])

t = threading.Thread(name='dashboard', target=start_dashboard)

t.start()
time.sleep(2)
webbrowser.open("http://127.0.0.1:8080/")
t.join()