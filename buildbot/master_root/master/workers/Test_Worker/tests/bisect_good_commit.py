import sys
import subprocess
sys.path.append('.')
mode = sys.argv[1]

if sys.argv[1] == 'read':
    saved = __import__('bisect_good_commits')
    if (len(sys.argv) <4):
        print("You must give BuildBot project['name'] and branch!")
    else:
        bb_project = sys.argv[2]
        branch = sys.argv[3]
        if bb_project not in saved.good_commits:
            print("No saved commits for '"+bb_project+"'!")
            sys.exit(1)
        elif branch not in saved.good_commits[bb_project]:
            print("No commit saved for the branch '"+branch+"'!")
            sys.exit(1)
        else:
            print(saved.good_commits[bb_project][branch])

elif sys.argv[1] == 'write':
    bb_project = sys.argv[2]
    branch = sys.argv[3]
    commit = sys.argv[4]
    commit = commit.split('\n')
    commit = commit[0]
    good_commits = open('./bisect_good_commits.py')
    temp_good_commits = open('./bisect_temp_good_commits.py', 'w+', encoding="utf-8")
    branch_written = 0
    branch_found = 0
    project_flag = 0
    project_found = 0

    for line in good_commits:
        if project_found ==0:
            if bb_project in line:
                project_flag = 1
                project_found = 1
                print(line, end='', file=temp_good_commits)
            elif '#EOF' in line:
                print("\t'"+bb_project+"':{\n", end='', file=temp_good_commits)
                print("\t\t'"+branch+"':'"+commit+"',\n", end='', file=temp_good_commits)
                print("},\n", end='', file=temp_good_commits)
                print("#EOF\n", end='', file=temp_good_commits)
            else:
                print(line, end='', file=temp_good_commits)
        elif project_flag == 1:
            if branch in line:
                print("\t\t'"+branch+"':'"+commit+"',\n", end='', file=temp_good_commits)
                branch_written = 1
                project_flag = 0
            elif '},' in line:
                if branch_written == 0:
                    print("\t\t'"+branch+"':'"+commit+"',\n", end='', file=temp_good_commits)
                    print("},\n", end='', file=temp_good_commits)
                    project_flag = 0
            else:
                print(line, end='', file=temp_good_commits)

        elif '#EOF' in line:
            if project_found == 0:
                print("\t'"+bb_project+"':{'"+commit+"',\n", end='', file=temp_good_commits)
                print("\t\t'"+branch+"':'"+commit+"',\n", end='', file=temp_good_commits)
            else:
                print(line, end='', file=temp_good_commits)
        else:
            print(line, end='', file=temp_good_commits)
    good_commits.close()
    temp_good_commits.close()

    stdout = subprocess.run('mv ./bisect_temp_good_commits.py ./bisect_good_commits.py', shell=True)
else:
    print("Unknown mode, use bisect_good_commit.py read/write!")
    sys.exit(1)
