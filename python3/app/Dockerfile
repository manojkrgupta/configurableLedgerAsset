# syntax=docker/dockerfile:1.4

FROM ubuntu AS builder
EXPOSE 8880
WORKDIR /app/corda5 
COPY requirements.txt /app/corda5
RUN <<EOF
apt-get update
apt-get install -y python3 pip curl vim telnet
python3 -m pip install -r requirements.txt --no-cache-dir
EOF
COPY . /app
#ENTRYPOINT ["python3"] 
#CMD ["manage.py", "runserver", "0.0.0.0:8880"]
CMD ["bash"]

FROM builder as dev-envs
RUN <<EOF
echo yahoooo
apk update
apk add git
ls -l /app/
#echo python3 manage.py migrate
#python3 manage.py migrate # not needed since it has been ran once
EOF

RUN <<EOF
echo ijkkkk
mkdir /log
#addgroup -S docker
#adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8880"]
#CMD ["bash", "sleep", "10000000000"]
#CMD ["tail", "-f", "/dev/null"]
