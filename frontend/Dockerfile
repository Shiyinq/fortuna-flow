# Use an official node image with Node.js version 20.10.0
FROM node:20.10.0-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Svelte application
RUN npm run build

# Expose port 5000
EXPOSE 5000

# Command to run the app
CMD ["node","build/index.js"]
