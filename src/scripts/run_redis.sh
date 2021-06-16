#!/usr/bin/env bash
docker run -d -p 6378:6379 --name l3autoseg_redis redis redis-server
