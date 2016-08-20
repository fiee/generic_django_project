#!/bin/sh
# renew all Let’s encrypt certificates
# put this in /etc/cron.monthly

$LOG = /var/log/letsencrypt/letsencrypt.log

cd /opt/certbot

for conf in $(ls /etc/letsencrypt/configs/*.conf); do

    date "+%Y-%m-%d %H:%M:%S" >> $LOG
    echo "Renew certificate for $conf:" >> $LOG

    ./certbot-auto certonly --config "$conf" --non-interactive --keep-until-expiring --expand --quiet

    if [ $? -ne 0 ]; then
        echo "The Let's Encrypt certificate $conf has not been renewed!" >> $LOG
    fi
    
done

# make sure nginx picks them up
/etc/init.d/nginx reload
service nginx reload

exit 0
