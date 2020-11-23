FROM node:14.1.0 AS compile-image

# Set working directory
WORKDIR /opt/ng

# Copy package.json and download dependencies
COPY package.json package-lock.json ./
RUN npm install

# Add node modules to path
ENV PATH="./node_modules/.bin:$PATH" 

# Add app
COPY . ./

# Build prod version
RUN ng build --prod

# Use nginx
FROM nginx
COPY --from=compile-image /opt/ng/dist/leaderboard-ui /usr/share/nginx/html
EXPOSE 80