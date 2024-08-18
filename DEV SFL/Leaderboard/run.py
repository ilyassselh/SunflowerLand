import subprocess

while True:
    # Exécution de app.py en arrière-plan
    app_process = subprocess.Popen(["python", "app.py"])

    # Exécution de leaderboard.py en arrière-plan
    leaderboard_process = subprocess.Popen(["python", "leaderboard.py"])
    leaderboard_process.wait()  # Attendre que le processus de leaderboard se termine

    # Terminer le processus de app.py
    app_process.terminate()

    print("Both scripts completed. Restarting leaderboard.")