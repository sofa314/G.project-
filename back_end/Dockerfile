FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Remove default Nginx config and copy custom one
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/
RUN ln -sf /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf

# Create a script to run Gunicorn and Nginx
RUN echo '#!/bin/bash\n\ngunicorn --bind 0.0.0.0:8000 app:app &\n\nnginx -g "daemon off;"' > start.sh
RUN chmod +x start.sh

EXPOSE 80

CMD ["./start.sh"] 