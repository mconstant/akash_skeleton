import requests
import yaml
import base64
import json
import nacl.public
import subprocess
from getpass import getpass

def prompt_for_pat():
    print("To use this script, you need a Fine Grained GitHub Personal Access Token (PAT) with the following scopes:")
    print("- ability to write to Actions Secrets for this repository")
    print("You can create a PAT here: https://github.com/settings/tokens")
    pat = getpass("Enter your GitHub Personal Access Token (PAT): ")
    print("Optionally you can also sync with the original template repo")
    print("For this you will need a classic PAT with workflow scope")
    pat_classic = getpass("Enter optional classic Workflow scoped GitHub Personal Access Token (PAT) to sync with the original template repo: ")
    return pat, pat_classic

def read_secrets(file_path):
    with open(file_path, 'r') as file:
        secrets = yaml.safe_load(file)
    return secrets

def get_public_key(repo, headers):
    url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def encrypt_secret(public_key, secret_value):
    public_key_bytes = base64.b64decode(public_key["key"])
    sealed_box = nacl.public.SealedBox(nacl.public.PublicKey(public_key_bytes))
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def add_secret(repo, secret_name, encrypted_value, key_id, headers):
    url = f"https://api.github.com/repos/{repo}/actions/secrets/{secret_name}"
    data = {
        "encrypted_value": encrypted_value,
        "key_id": key_id
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print(f"Secret '{secret_name}' added successfully.")

def main():
    pat, pat_classic = prompt_for_pat()
    # get the current repo extracted from the git remote url
    current_repo = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).decode("utf-8").strip().split(":")[-1].replace(".git", "")
    repo = current_repo
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }

    secrets = read_secrets('repo_secrets.yml')
    public_key = get_public_key(repo, headers)

    for secret_name, secret_value in secrets.items():
        encrypted_value = encrypt_secret(public_key, secret_value)
        add_secret(repo, secret_name, encrypted_value, public_key["key_id"], headers)

    encryped_workflow_token = encrypt_secret(public_key, pat_classic)
    add_secret(repo, "WORKFLOW_TOKEN", encryped_workflow_token, public_key["key_id"], headers) 
if __name__ == "__main__":
    main()