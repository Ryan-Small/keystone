FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

# Use Docker-specific proxy config
RUN mv proxy.conf.docker.json proxy.conf.json

EXPOSE 4200

CMD ["npm", "start", "--", "--host", "0.0.0.0"]
