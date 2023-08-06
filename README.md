# fast-stem
Libraries behind ASGI server

## Guide line
1. edit api yaml
   `vim server/swagger/stem.yaml`
2. gen api code
   `sh ./scripts/gen_swagger_server.sh`
3. run server
   `sh ./scripts/run_http_server.sh`
4. local develop
   `ln -s ./scripts ./bin`


## Deploy FC

### local build
```shell
docker build -t tests -f deploy/http_server/Dockerfile .
```
local swagger
[http://0.0.0.0:9000/api/docs](http://0.0.0.0:9000/api/docs)


### upload image
```shell
docker login --username=ben.song@samarkand registry-intl.cn-shanghai.aliyuncs.com
docker tag tests registry-intl.cn-shanghai.aliyuncs.com/smk_fc/cbec
docker push registry-intl.cn-shanghai.aliyuncs.com/smk_fc/cbec
```