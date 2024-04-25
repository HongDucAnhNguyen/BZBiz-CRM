
python manage.py migrate

gunicorn --worker-tmp-dir /dev/shm bzbizcrm.wsgi