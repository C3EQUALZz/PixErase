#!/bin/sh
set -e

isAlive() { curl -sf http://127.0.0.1:9000/minio/health/live; }    # check if Minio is alive
minio $0 "$@" --quiet & echo $! > /tmp/minio.pid                   # start Minio in the background
while ! isAlive; do sleep 0.1; done                                # wait until Minio is alive
mc alias set minio http://127.0.0.1:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD} # setup Minio client
mc mb minio/${MINIO_IMAGES_BUCKET} || true                                    # create a test bucket
mc anonymous set public minio/${MINIO_IMAGES_BUCKET}                          # make the test bucket public
kill -s INT $(cat /tmp/minio.pid) && rm /tmp/minio.pid             # stop Minio
while isAlive; do sleep 0.1; done                                  # wait until Minio is stopped
exec minio $0 "$@"                                                 # start Minio in the foreground