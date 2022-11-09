FROM docker.io/library/python:3.9-alpine
WORKDIR /a2c
COPY . .
EXPOSE 6454
CMD [ "python", "-m", "artnet2crap.server_main" ]
