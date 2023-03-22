git reset --h origin/main
git pull
docker cp main.py meow_ai:/app/
echo 'done'
