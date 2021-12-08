import os
import sys

from github import Github

SCRIPT_DIR = os.path.dirname(__file__)
token = os.getenv("GITHUB_TOKEN")
user = sys.argv[1]

g = Github(token)
usr = g.get_user(user)
repos = usr.get_repos()

repo_dir = os.path.join(SCRIPT_DIR, user) + "/"

if not os.path.isdir(user):
    os.mkdir(user)

os.chdir(user)

for repo in repos:
    cmd = "git clone {}".format(repo.ssh_url)
    print("Starting to clone {}".format(repo.name))
    print("Running command '{}'".format(cmd))
    os.system(cmd)
    print("Finshed cloning {}".format(repo.name))
    print("#####################################")
    print("")
