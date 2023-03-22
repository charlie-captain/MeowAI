git reset --h origin/main
git pull
docker cp main.py meowai:/app/
docker cp src meowai:/app/
docker restart meowai
echo 'done'