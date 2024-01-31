#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Exiting..."
    exit 1
fi

# Update package information
apt-get update

# Install Nginx if not already installed
apt-get install -y nginx

# Create necessary directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a simple HTML file for testing
echo "Holberton School" > /data/web_static/releases/test/index.html

# Create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership
chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Create a separate Nginx configuration file
nginx_config="/etc/nginx/sites-available/web_static"

printf %s "server {
    listen 80;
    server_name _;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > "$nginx_config"

# Create a symbolic link to the sites-enabled directory
ln -sf "$nginx_config" /etc/nginx/sites-enabled/

# Restart Nginx
service nginx restart

# Exit successfully
exit 0