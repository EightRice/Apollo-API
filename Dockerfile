FROM python:3.8.0-alpine

RUN apk add --update  --no-cache libstdc++ libc6-compat openssh-client git gcc cython linux-headers make musl-dev python3-dev g++

WORKDIR /usr/service/apollo

COPY requeriments.txt .

RUN pip install --ignore-installed -r requeriments.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["python", "main.py"]
