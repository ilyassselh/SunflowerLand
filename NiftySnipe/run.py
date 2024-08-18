import subprocess

def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {script_name}: {e}")

if __name__ == "__main__":
    script1 = "nifty.py"
    script2 = "nifty_24h.py"
    script3 = "api.py"

    # Lancer les deux scripts en parallèle
    process1 = subprocess.Popen(['python', script1])
    process2 = subprocess.Popen(['python', script2])
    process3 = subprocess.Popen(['python', script3])


    # Attendre que les deux processus se terminent
    process1.wait()
    process2.wait()
    process3.wait()

    print("Les deux scripts ont été exécutés en même temps.")