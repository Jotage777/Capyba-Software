import subprocess

from dotenv import load_dotenv, set_key
import os


set_key('.env', 'TESTING', 'False')

load_dotenv()

if os.environ.get('TESTING') == 'False':
    # Roda o aplicativo app.py
    subprocess.run(["python3", "../app.py"])
