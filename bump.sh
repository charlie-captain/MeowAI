git fetch origin
git add .
time=$(date "+%Y-%m-%d %H:%M:%S")
echo $time
branch=main
git commit -m "bump : ${time}"
git rebase origin/$branch
git push origin $branch