import sys
import subprocess
from datetime import datetime, timezone
from time import sleep
sys.path.append('.')

bb_project = sys.argv[1]
branch = sys.argv[2]
commit = sys.argv[3]
#stdout = subprocess.run('cp ./temp_results/temp_results.txt ./temp_results/'+product, shell=True)
#stdout = subprocess.run('mv ./temp_results/'+product+'/temp_results.txt ./temp_results/'+product+'/'+date+'_'+bb_project+'_'+product+'.txt', shell=True)

good_commits = open('./configs/good_commits.py')
temp_good_commits = open('./configs/temp_good_commits.py', 'w+', encoding="utf-8")
branch_written = 0
branch_found = 0
project_flag = 0
project_found =0
for line in good_commits:
    if bb_project in line:
        project_flag = 1
        project_found = 1
        print(line, end='', file=temp_good_commits)
    elif project_flag == 1:
        if branch in line:
            print("\t\t'"+branch+"':'"+commit+"',\n", end='', file=temp_good_commits)
            branch_written = 1
            project_flag = 0
        elif ('},' in line and branch_written == 0):
            print("\t\t'"+branch+"':'"+commit+"',\n", end='', file=temp_good_commits)
        else:
            print(line, end='', file=temp_good_commits)
    elif '#EOF' in line:
        if project_found == 0:
            print("\t'"+bb_project+"':{'"+commit+"',\n", end='', file=temp_good_commits)
            print("'"+branch+"':'"+commit+"',\n", end='', file=temp_good_commits)
        else:
            print(line, end='', file=temp_good_commits)
    else:
        print(line, end='', file=temp_good_commits)
good_commits.close()
temp_good_commits.close()

