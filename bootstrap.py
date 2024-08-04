import yaml
import shutil
import tempfile

def prompt_for_value(prompt_message, default_value):
    input_value = input(f"{prompt_message} [{default_value}]: ")
    return input_value if input_value else default_value

def main():
    # Copy repo_secrets.example.yml to repo_secrets.yml
    shutil.copy('repo_secrets.example.yml', 'repo_secrets.yml')

    with open('repo_secrets.example.yml', 'r') as example_file:
        example_data = yaml.safe_load(example_file)

    updated_data = {}
    for key, value in example_data.items():
        if isinstance(value, str):
            prompt_message = f"Enter value for {key}"
            updated_value = prompt_for_value(prompt_message, value)
            updated_data[key] = updated_value
        else:
            updated_data[key] = value

    with open('repo_secrets.yml', 'w') as secrets_file:
        yaml.safe_dump(updated_data, secrets_file)

    print("Bootstrap completed. The repo_secrets.yml file has been updated.")

if __name__ == "__main__":
    main()