FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
COPY .npmrc ./
RUN npm install

COPY . .

ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true

EXPOSE 3000

CMD ["npm", "start"]
