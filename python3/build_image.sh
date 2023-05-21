set -x
cp lib/corda5Interface.py app/corda5/lib/
cp requirements.txt app/
cd app/
docker build --platform linux/amd64 -t manojdjango:test1 .
docker tag manojdjango:test1 manojkrgupta/manojdjango_amd64:test1
docker push manojkrgupta/manojdjango_amd64:test1
cd -
