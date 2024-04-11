#!/bin/bash
docker run -d --rm -v $PWD:/app -p 8080:8080 ds-backend
