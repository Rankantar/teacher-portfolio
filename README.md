# Teacher Portfolio

This repository contains a teacher portfolio website project.

## Prerequisites

- Git (to clone the repository)
- For Docker option: Docker installed on your machine
- For non-Docker option: A web browser or a basic HTTP server (Python, Node.js, etc.)

## Project Structure

The project is organized as follows:
- `frontend/` - Contains the static website files
- `teacher-website.html` - The main HTML file
- `styles/` - Directory containing CSS files
- `Dockerfile` - Configuration for containerizing the application
- `nginx.conf` - Configuration for the Nginx web server used in Docker

## Running the Application

### Option 1: Using Docker (Recommended)

1. Make sure you have Docker installed on your machine
2. Navigate to the frontend directory:
```
cd frontend
```
3. Build the Docker image:
```
docker build -t teacher-portfolio-frontend .
```
4. Run the Docker container:
```
docker run -p 8080:80 teacher-portfolio-frontend
```
5. Access the website in your browser at: http://localhost:8080

### Option 2: Running Locally without Docker

#### Method A: Using Python's built-in HTTP server
1. Navigate to the frontend directory:
```
cd frontend
```
2. Start a simple HTTP server:
```
python -m http.server
```
3. Access the website in your browser at: http://localhost:8000/teacher-website.html

#### Method B: Direct browser access
1. Navigate to the frontend directory
2. Open the teacher-website.html file directly in your browser:
```
start teacher-website.html
```
or simply double-click on the file in your file explorer.

## Development

To make changes to the project:
1. Modify the HTML, CSS, or JavaScript files as needed
2. If using Docker, rebuild the Docker image after making changes
3. Restart the server or refresh the browser to see your changes
