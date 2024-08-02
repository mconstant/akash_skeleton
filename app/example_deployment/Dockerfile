FROM nodejs:12

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./

RUN npm install

CMD [ "npm", "start" ]
