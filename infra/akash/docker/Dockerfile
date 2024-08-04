FROM ghcr.io/akash-network/provider:latest

ENV AKASH_SEED_PHRASE=$AKASH_SEED_PHRASE
ENV AKASH_KEY_NAME=$AKASH_KEY_NAME
ENV AKASH_KEYRING_PASSPHRASE=$AKASH_KEYRING_PASSPHRASE

RUN apt-get update && apt-get install -y curl jq wget

# Install golang
RUN wget https://go.dev/dl/go1.22.5.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz
ENV PATH=$PATH:/usr/local/go/bin

# Terraform dependencies
RUN apt-get install -y gnupg software-properties-common
# Install the HashiCorp GPG key.
RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
# Verify the key's fingerprint.
RUN gpg --no-default-keyring \
    --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    --fingerprint
# Add the official HashiCorp Linux repository.
RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com bullseye main" | \
    tee /etc/apt/sources.list.d/hashicorp.list
# Update and install Terraform.
RUN apt-get update && apt-get install -y terraform

# install opentofu
# RUN wget --secure-protocol=TLSv1_2 --https-only https://get.opentofu.org/install-opentofu.sh -O install-opentofu.sh
# RUN chmod +x install-opentofu.sh
# RUN ./install-opentofu.sh --install-method deb
# RUN rm install-opentofu.sh

# copy *.tf files in ../../ to /terraform directory we don't want the akash directory
COPY ./terraform /terraform
RUN ls -la /terraform

# copy sdl.yaml to /akash directory
# COPY ./sdl.yaml /akash/sdl.yaml

COPY ./akash_settings.sh ./akash_settings.sh
COPY ./entrypoint.sh ./entrypoint.sh
COPY ./destroy.sh ./destroy.sh

RUN chmod +x entrypoint.sh
RUN chmod +x destroy.sh

ENTRYPOINT ["./entrypoint.sh"]
