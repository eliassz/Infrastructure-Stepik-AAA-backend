#!/bin/bash
docker run -d --restart unless-stopped -v $PWD:/app -p 8080:8080 ds-backend
