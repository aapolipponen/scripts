import os
import requests

# Prompt for GitHub username
USERNAME = input("Enter the GitHub username: ").strip()

# Prompt for directory selection
print("\nSelect the base directory for cloning:")
base_dir_option = input("1. Current directory\n2. Home directory\n3. Specific directory\n4. Under a directory named by the GitHub username in the home directory\nEnter choice (1/2/3/4): ").strip()

if base_dir_option == "1":
    BASE_DIR = os.getcwd()
elif base_dir_option == "2":
    BASE_DIR = os.path.expanduser("~")
elif base_dir_option == "3":
    BASE_DIR = input("Enter the full path to the directory: ").strip()
elif base_dir_option == "4":
    BASE_DIR = os.path.join(os.path.expanduser("~"), USERNAME)
else:
    print("Invalid choice!")
    exit()

TOKEN = input("\nEnter your GitHub Personal Access Token (leave empty for public repos only): ").strip()

HEADERS = {
    'Authorization': f'token {TOKEN}'
} if TOKEN else {}

# Fetch repositories
response = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=HEADERS)
repos = response.json()

# Check for errors (e.g., invalid token or user not found)
if 'message' in repos:
    print(f"Error: {repos['message']}")
    exit()

# Display the repositories and get the user's choice
print("\nSelect repositories to clone by their numbers separated by commas (or 'a' for all):\n")
for idx, repo in enumerate(repos, 1):
    print(f"{idx}. {repo['name']}")

choice = input("\nEnter your choices (e.g. 1,3,5 or 'a'): ")

def clone_or_pull(repo):
    repo_url = repo['clone_url']
    if TOKEN:
        repo_url = repo_url.replace('https://', f'https://{USERNAME}:{TOKEN}@')
    
    repo_name = repo['name']
    repo_path = os.path.join(BASE_DIR, repo_name)

    if os.path.exists(repo_path):
        print(f"Pulling {repo_name}...")
        os.system(f"cd {repo_path} && git pull")
    else:
        print(f"Cloning {repo_name}...")
        os.system(f"git clone {repo_url} {repo_path}")

if choice == 'a':
    for repo in repos:
        clone_or_pull(repo)
else:
    try:
        indices = [int(idx.strip()) for idx in choice.split(',')]
        for idx in indices:
            if 0 < idx <= len(repos):
                clone_or_pull(repos[idx-1])
            else:
                print(f"Invalid choice: {idx}! Skipping...")
    except ValueError:
        print("Please enter valid numbers separated by commas or 'a'.")

print("\nOperation completed.")
