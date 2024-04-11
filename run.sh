#!/bin/bash
docker run -d -v $PWD:/app -p 8080:8080 ds-backend
