FROM nginx:alpine

LABEL maintainer="Teacher Portfolio Team"
LABEL description="Teacher portfolio website frontend"
LABEL version="1.0"

WORKDIR /usr/share/nginx/html

# Copy the main HTML file
COPY index.html .
COPY 50x.html .

# Copy the styles and public directories directly
COPY styles/ styles/
COPY public/ public/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Add a debug file to verify file structure
RUN echo "This is a test file" > test.txt
RUN ls -la > file_structure.txt

EXPOSE 80

# Add healthcheck to verify nginx is working properly
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
CMD wget --no-verbose --tries=1 --spider http://127.0.0.1/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
