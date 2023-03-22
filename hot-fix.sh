git reset --h origin/main
git pull
docker cp main.py meowai:/app/
docker cp src meowai:/app/
echo 'done'
