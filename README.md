# akash_skeleton

## prereqs

1. create an akash wallet and fund it with maybe 0.75 AKT or more to ensure you have enough for deployment escrow. Copy the mnemonic.
2. Click the green `Use This Template` button in this project and choose `Create a new repository`
3. make an account on Terraform cloud
   - make an Organization and keep track of your org name
   - inside the org make a workspace under the `default` project called `deploy` choose `API-Based` for the workspace type
   - go to `Settings > General` for the Workspace `deploy` and set the `Execution Mode` to `Local (custom)`
   - Make a Terraform Cloud API token by going to your user settings and choosing `Tokens`. Generate a new one, give it any name you like, make it expire never and copy the secret value it gives you and store it. You'll need it to set the `TF_TOKEN_app_terraform_io` secret in the next step.
4. set the following secrets in Github > Settings > Secrets > Actions > Repo Secrets
   - AKASH_SEED_PHRASE -> your akash wallet mnemonic
   - AKASH_KEY_NAME -> deploy
   - AKASH_KEYRING_PASSPHRASE -> somepassyoumakeup
   - TF_ORG_NAME -> your org on Terraform Cloud
   - TF_TOKEN_app_terraform_io -> your Terraform Cloud Token

## deploying

1. Run the Deploy Github action

## view your deployment
    - Go to https://console.akash.network/deployments
    - Click Connect Wallet
    - Connect your Akash Wallet you deployed with
    - Click deployments
    - Click anywhere on your active deployment
    - Click `Create Certificate`
    - Click `Approve`
    - Click `Logs`

## to allow your copied template repo to automatically get pull requests from the original template as we update it

```You need to grant the workflows permission to your GitHub App.

Go to the settings page of your GitHub App.
Under "Actions > General" scroll down to "Workflow Permissions".
Select the "Read and write permissions" and check the box that says "Allow GitHub Actions to create and approve pull requests"
In the "Repository permissions" section, check the "Read & write" permission for the "Workflows" option.
Click on "Save changes".```

Also you need to generate a classic PAT (personal access token) with workflow capabilities and store it in the Actions Secret `WORKFLOW_TOKEN`