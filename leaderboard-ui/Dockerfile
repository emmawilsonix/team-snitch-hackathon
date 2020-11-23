FROM node:14.1.0

# Set working directory
WORKDIR /app
# Add node modules to path
ENV PATH /app/node_modules/.bin:$PATH

# Copy package.json and download dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install -g @angular/cli@7.3.10

# Add app
COPY . /app

# Start app
CMD ng serve --host 0.0.0.0