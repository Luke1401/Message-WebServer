
import subprocess

for index in range(1000):
    print('Count in: ', index)
    subprocess.check_call(['python3','test_server.py'])