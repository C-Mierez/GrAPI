release: python manage.py reset_db --no-input
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn GrAPI.wsgi --log-file -