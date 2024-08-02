# akash_skeleton

## prereqs

1. Docker or Docker Desktop needs to be installed on your system

## quickstart

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