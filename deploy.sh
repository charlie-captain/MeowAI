git reset --h origin/main
git pull
chmod 777 ./deploy.sh
docker build --no-cache -t meowai_image .
docker stop meow_ai || true
docker rm meow_ai || true
#docker system prune -f || true
docker run -it --name meow_ai --network -v /volume1/photo:/app/data -v /volume1/docker/github/MeowAI/results:/app/results host meowai_image
