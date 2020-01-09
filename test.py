import subprocess

process = subprocess.run(['ntpq','-p'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout.split('\n')
for line in output:
    if len(line) > 0:
        if line[0] == "*":
            a = ' '.join(line.split())
            print(a.split(' ')[1].replace('.', ''))
