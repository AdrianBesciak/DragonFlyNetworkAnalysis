#!/bin/bash

# remember to run with sudo

systemctl stop netbox netbox-rq
echo "DROP DATABASE netbox; CREATE DATABASE netbox; CREATE USER netbox WITH PASSWORD 'r5t6^7$%gyuuyt4'; GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;" | sudo -u postgres psql
/opt/netbox/upgrade.sh
source /opt/netbox/venv/bin/activate
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@admin.com
export DJANGO_SUPERUSER_PASSWORD=admin
python3 /opt/netbox/netbox/manage.py createsuperuser --noinput
systemctl restart netbox netbox-rq

#Generate api endpoint
sleep 3
KEY=`curl -X POST -H "Content-Type: application/json" -H "Accept: application/json; indent=4" http://127.0.0.1/api/users/tokens/provision/ --data '{
    "username": "admin",
    "password": "admin"
}' | grep "key" | cut -d':' -f2`

echo 'NETBOX_TOKEN =' $KEY > generatedNetboxToken.py
