# Shields Aesthetics Deployment Notes

## Required Environment Variables

Set these in the hosting dashboard before deploying:

- `SECRET_KEY`: generate a new long random Django secret key.
- `DJANGO_DEBUG`: `False`
- `ALLOWED_HOSTS`: comma-separated domains, for example `shieldsaesthetics.com,www.shieldsaesthetics.com`
- `CSRF_TRUSTED_ORIGINS`: comma-separated HTTPS origins, for example `https://shieldsaesthetics.com,https://www.shieldsaesthetics.com`
- `DATABASE_URL`: the hosted PostgreSQL connection string.
- `TIME_ZONE`: `Asia/Manila`
- `SECURE_SSL_REDIRECT`: `True`
- `SESSION_COOKIE_SECURE`: `True`
- `CSRF_COOKIE_SECURE`: `True`
- `SECURE_HSTS_SECONDS`: `31536000`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`: `True`
- `SECURE_HSTS_PRELOAD`: `True`
- `PYTHON_VERSION`: `3.12.1` if you prefer setting it in Render instead of using `.python-version`

## Build And Start Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Collect static files:

```bash
python manage.py collectstatic --no-input
```

Apply database migrations:

```bash
python manage.py migrate
```

Start the web server:

```bash
gunicorn core.wsgi:application
```

On Render, use this build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input
```

Use this pre-deploy command:

```bash
python manage.py migrate
```

For Render free accounts without Shell access, the start command may include
the one-time superuser bootstrap command:

```bash
python manage.py migrate && python manage.py bootstrap_superuser && gunicorn core.wsgi:application
```

Set these temporary environment variables before using it:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_PASSWORD`
- `DJANGO_SUPERUSER_EMAIL` optional

After the admin account works, remove `DJANGO_SUPERUSER_PASSWORD` from Render and
switch the start command back to:

```bash
python manage.py migrate && gunicorn core.wsgi:application
```

If you specifically need to create a doctor login without Shell access, use:

```bash
python manage.py migrate && python manage.py bootstrap_doctor && gunicorn core.wsgi:application
```

## Important Client-Ready Notes

- Do not upload `.env` to GitHub. Use `.env.example` as the safe template.
- Change the local PostgreSQL password before pushing publicly, because the old value was previously hardcoded in `settings.py`.
- For uploaded profile images, use persistent disk storage or a cloud media service on the host. Temporary hosting filesystems can lose `media/` uploads after redeploys.
- Create production admin, doctor, and secretary accounts directly on the live server after migrations.
