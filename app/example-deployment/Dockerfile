FROM node:18-slim

ENV MESSAGE=$MESSAGE

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./

COPY app.js .

RUN npm install

CMD [ "npm", "start" ]
