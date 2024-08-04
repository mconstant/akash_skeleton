import requests
import yaml
import base64
import json
from getpass import getpass

def prompt_for_pat():
    print("To use this script, you need a GitHub Personal Access Token (PAT) with the following scopes:")
    print("- repo (Full control of private repositories)")
    print("- admin:repo_hook (Full control of repository hooks)")
    print("You can create a PAT here: https://github.com/settings/tokens")
    pat = getpass("Enter your GitHub Personal Access Token (PAT): ")
    return pat

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
    pat = prompt_for_pat()
    repo = input("Enter the repository name (e.g., username/repo): ")
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }

    secrets = read_secrets('repo_secrets.yml')
    public_key = get_public_key(repo, headers)

    for secret_name, secret_value in secrets.items():
        encrypted_value = encrypt_secret(public_key, secret_value)
        add_secret(repo, secret_name, encrypted_value, public_key["key_id"], headers)

if __name__ == "__main__":
    main()