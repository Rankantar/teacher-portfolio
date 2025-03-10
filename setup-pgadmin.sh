#!/bin/bash
set -e

# Wait for pgAdmin to be ready
sleep 10

# Create the server connection
curl --request POST \
  --url http://pgadmin:80/api/servers/ \
  --header 'Content-Type: application/json' \
  --header "X-CSRF-TOKEN: $(curl -c - http://pgadmin:80/login | grep csrf_token | awk '{print $7}')" \
  --cookie "PGADMIN_SESSION_ID=$(curl -c - http://pgadmin:80/login | grep PGADMIN_SESSION_ID | awk '{print $7}')" \
  --data '{
    "name": "Teacher Database",
    "group_id": 1,
    "host": "db",
    "port": 5432,
    "maintenance_db": "postgres",
    "username": "postgres",
    "password": "postgres",
    "ssl_mode": "prefer",
    "save_password": true
  }'

echo "PgAdmin server setup completed" 