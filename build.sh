git reset --h origin/main
git pull
chmod 777 ./build.sh
docker build --no-cache -t meowai_image .
docker stop meow || true
docker rm meow || true
#docker system prune -f || true
docker run -it --name meow --network host -v /volume1/photo:/app/data -v /volume1/docker/github/MeowAI/results:/app/results  meowai_image
