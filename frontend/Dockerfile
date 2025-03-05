FROM nginx:alpine

LABEL maintainer="Teacher Portfolio Team"
LABEL description="Teacher portfolio website frontend"
LABEL version="1.0"

WORKDIR /usr/share/nginx/html

# Copy and rename the main HTML file to index.html
COPY teacher-website.html index.html

# Copy the styles directory with CSS files
COPY styles/ styles/

# Copy error pages
COPY 50x.html 50x.html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Add healthcheck to verify nginx is working properly
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
CMD wget --no-verbose --tries=1 --spider http://127.0.0.1/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
