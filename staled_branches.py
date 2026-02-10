import subprocess
from datetime import datetime, timedelta
import os

# Config
REPO_LINK = "repo_link"
FOLDER_NAME = "repo_name"
DAYS_CUTOFF = 90
DEFAULT_BRANCH = "main"
DELETE_REMOTE = True
DRY_RUN = True
GET_BRANCHES = True

def run_git_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
    return result.stdout.strip()

def get_stale_branches(branch_list_output, is_remote=False):
    stale_branches = []
    lines = branch_list_output.splitlines()
    for line in lines:
        branch_name = line.strip().split()[-1]
        if DEFAULT_BRANCH in branch_name or branch_name.startswith('HEAD'):
            continue
            
        # Get the last commit date
        try:
            date_str = run_git_command(f'git show --format="%ci" {branch_name} | head -n 1')
            last_commit_date = datetime.strptime(date_str.split(' ')[0], '%Y-%m-%d')
            
            if (datetime.now() - last_commit_date) > timedelta(days=DAYS_CUTOFF):
                stale_branches.append(f"{branch_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing branch {branch_name}: {e}")
            continue
    return stale_branches

def dry_run(branches):
    if DRY_RUN:
        with open(f"{FOLDER_NAME}.txt", "w", encoding="utf-8") as file:
            file.write(f"Branches older than {DAYS_CUTOFF} days:\n")
            for branch in branches:
                file.write(f"- {branch}\n")
        return

def delete_branches(branches, is_remote=False):
    with open(f"{FOLDER_NAME}_DELETED.txt", "w", encoding="utf-8") as output:
        output.write(f"Deleting the following {'remote' if is_remote else 'local'} branches:\n")
        for branch in branches:
            clean_branch_name = branch.replace('remotes/origin/', '')
            try:
                if is_remote:
                    result = run_git_command(f"git push origin --delete {clean_branch_name.replace('origin/', '')}")
                    output.write(f"{result}\n")
                    output.write(f"Deleted remote branch: {clean_branch_name}\n")
            except subprocess.CalledProcessError as e:
                print(f"Error deleting branch {clean_branch_name}: {e.stderr}")

    print("Cleanup process finished.")

if __name__ == "__main__":
    try:
        print(f"Checking for branches older than {DAYS_CUTOFF} days.")
        
        repo_dir = os.path.join(os.getcwd(), FOLDER_NAME)
        
        if os.path.isdir(repo_dir):
            os.chdir(repo_dir)
        else:
            run_git_command(f'git clone {REPO_LINK}')
            os.chdir(repo_dir)
            
        run_git_command(f'git checkout {DEFAULT_BRANCH}')
        
        if GET_BRANCHES:
            local_branches_output = run_git_command('git branch -a')
            stale_branches = get_stale_branches(local_branches_output)
            dry_run(stale_branches)
            
        if DELETE_REMOTE:
            delete_branches(stale_branches, is_remote=True)
    finally:
        pass
