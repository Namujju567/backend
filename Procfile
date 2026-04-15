web: python manage.py migrate && gunicorn config.wsgi --worker-class gevent --workers 2 --worker-connections 100 --timeout 120 --log-file -
