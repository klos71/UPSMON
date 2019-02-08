# UPSMON
UPSMON is a tool to monitor upses, will be able to send warnings, display everything in a web interface and check multiple upses

# API SERVER
To start the API server run "gunicorn -w 4 -b 127.0.0.1:5000" request:app on API server
the 10 min update is runned with cron job, check ubuntu 14.04 cron jobs

# MAILER
E-mails are sent from server/upsWarning/mailer.php & date.php check comments for more information
