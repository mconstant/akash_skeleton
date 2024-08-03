# akash_skeleton

## prereqs

1. create an akash wallet and fund it with maybe 0.75 AKT or more to ensure you have enough for deployment escrow. Copy the mnemonic.
2. 
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

1. Copy the .env.example and start your own .env to hold all your secrets 
```bash
$ cp infra/akash/docker/.env.example infra/akash/docker/.env
```

2. Follow the instructions in the `.env` file (it is commented with directions) to set yourself up  
Currently this involves:  
    - Getting Keplr, making an Akash wallet and getting the mnemonic
    - Getting a free Terraform Cloud account and doing some basic setup
    - Copying various secrets and storing them in the `.env`

3. Deploy
```bash
$ cd infra/akash/docker
$ docker compose up
```

4. View your deployment
    - Go to https://console.akash.network/deployments
    - Click Connect Wallet
    - Connect your Akash Wallet you deployed with
    - Click deployments
    - Click anywhere on your active deployment
    - Click `Create Certificate`
    - Click `Approve`
    - Click `Logs`
