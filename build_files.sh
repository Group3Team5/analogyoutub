pip install -r requirements.txt --root-user-action=ignore requests
python3.9 manage.py collectstatic --no-input
