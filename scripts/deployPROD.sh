pip freeze > requirements.txt
docker build -t hellomeals:localdev . && docker compose --env-file .env -f docker/docker-compose-prod.yml up