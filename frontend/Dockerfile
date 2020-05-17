# pull official base image
FROM node:12.16.0-alpine

# set working directory
WORKDIR /frontend

# add `/frontend/node_modules/.bin` to $PATH
ENV PATH /frontend/node_modules/.bin:$PATH

# install frontend dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm cache clean -f
RUN rm -rf /frontend/node_modules
RUN npm install --silent
RUN npm audit fix
RUN npm install react-scripts@3.4.1 -g --silent
WORKDIR /frontend/
RUN npm run build
# add frontend
COPY . ./
EXPOSE 3000
# start frontend
CMD ["npm", "start"]