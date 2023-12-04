Here are the steps (for whoever runs into this problem):
1. Empty the django_migrations table: delete from django_migrations;
2. For every app, delete its migrations folder: rm -rf <app>/migrations/
3. Reset the migrations for the "built-in" apps: python manage.py migrate --fake
4. For each app run: python manage.py makemigrations <app>. Take care of dependencies (models with ForeignKey's should run after their parent model).
5. Finally: python manage.py migrate --fake-initial