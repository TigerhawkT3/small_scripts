from multiprocessing.pool import ThreadPool
import subprocess
import glob
import sys
import os

# py script.py "C:\images" "cjxl -d 0" "png jpg jpeg" "4"
directory = sys.argv[1]
command = sys.argv[2]
extensions = set(sys.argv[3].split())
batchsize = int(sys.argv[4])
template = '{command} "{inp}" "{outp}"; if ($?) {{ rm -literalpath "{inp}" }}'

# adapted from https://stackoverflow.com/a/26783779/2617068
def work(command, name):
    command = template.format(command=command, inp=name, outp=name + '.jxl')
    result = subprocess.run(('powershell', '-noprofile', '-command', command))

tp = ThreadPool(batchsize)

for file in glob.iglob(os.path.join(directory, '**', '*.*'), recursive=True):
    if os.path.splitext(file)[1].lstrip('.').lower() in extensions:
        tp.apply_async(work, (command, file))

tp.close()
tp.join()