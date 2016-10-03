source env/bin/activate
gunicorn -b 0.0.0.0:8000 --workers=3 wsgi:app --reload
