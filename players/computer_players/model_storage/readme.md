If using s3 storage our recommendation is to use MinIO

Please note that MinIO has a AGPL v3 License.
All source for minio can be found:
https://github.com/minio/minio

Use to initialize minio container during testing

```bash
sudo docker run -d \
  --name minio_tic_tac \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minio \
  -e MINIO_ROOT_PASSWORD=minio123 \
  minio/minio server /data --console-address ":9001"
```

Log into your minio console at 
http:localhost:9001 using the user and password that you set.