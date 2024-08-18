import subprocess
import threading

def run_script(script_name):
    subprocess.call(["python", script_name])

# Noms des fichiers de script à exécuter
scripts_to_run = ["nifty_24h.py", "api.py"]

# Créer une liste de threads pour exécuter les scripts en parallèle
threads = [threading.Thread(target=run_script, args=(script,)) for script in scripts_to_run]

# Démarrer tous les threads
for thread in threads:
    thread.start()

# Attendre que tous les threads se terminent
for thread in threads:
    thread.join()

print("Tous les scripts ont été exécutés.")