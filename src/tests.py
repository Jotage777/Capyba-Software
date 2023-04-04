import subprocess

from dotenv import load_dotenv, set_key
import os


set_key('.env', 'TESTING', 'True')

load_dotenv()

if os.environ.get('TESTING') == 'True':
    # Roda o aplicativo app.py
    subprocess.run(["pytest", "tests/conftest.py"])
