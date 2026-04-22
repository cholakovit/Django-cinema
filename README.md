uv run python manage.py runserver 8001
uv run --active waitress-serve --listen=127.0.0.1:8001 config.wsgi:application

http://127.0.0.1:8001/accounts/login/

http://127.0.0.1:8001/genres/