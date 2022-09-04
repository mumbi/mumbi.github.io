#!/bin/sh
docker stop mumbi.github.io
docker rm mumbi.github.io
docker build -t mumbi.github.io:latest .
docker run --name mumbi.github.io -d -p 4000:4000 mumbi.github.io:latest
docker logs mumbi.github.io --follow