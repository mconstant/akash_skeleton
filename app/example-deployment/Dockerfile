FROM node:18-slim

ENV TOP_SECRET_MESSAGE=$TOP_SECRET_MESSAGE

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./

COPY app.js .

RUN npm install

CMD [ "npm", "start" ]
