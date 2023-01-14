# Проект по БД

## Для запуска в docker последовательно ввести
```docker
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```
###После перейти на http://localhost/
###Дока swagger на http://localhost/swagger/
