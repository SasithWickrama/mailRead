import sys
from subprocess import call



if sys.argv[1] == 'OFFNET':
    call(["python", "offnet.py"])
if sys.argv[1] == 'CRMSMS':
    call(["python", "crmsms.py"])
if sys.argv[1] == 'OFFNETMOBITEL':
    call(["python", "offnetmobitel.py"])