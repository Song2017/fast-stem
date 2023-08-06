# Application
export APP_TIMEOUT='5'
export SECURITY_KEY='tests'
export APP_MODE='debug' # debug release

# DB
export REDIS_HOST='r-h.redis.rds.aliyuncs.com:6379'
export REDIS_PASS='pass!'
export PG_URI='postgresql://u:tests@pgm-tests.pg.rds.aliyuncs.com/db'

# Biz
export APP_SETTINGS="{
  \"app_conf\": {
    \"APP_NAME\":\"CBEC\",
    \"APP_TIMEOUT\":\"$APP_TIMEOUT\",
    \"APP_MODE\":\"$APP_MODE\",

    \"SECURITY_KEY\":\"$SECURITY_KEY\"
  },
  \"redis_conf\": {
    \"db\":\"5\",
    \"REDIS_HOST\":\"$REDIS_HOST\",
    \"REDIS_PASS\":\"$REDIS_PASS\"
  },
  \"pg_conf\": {
    \"PG_URI\":\"$PG_URI\",
    \"NAME\":\"test\"
  }
}"

echo "$APP_SETTINGS" >app_settings.txt
export APP_SETTINGS=$(python -c "import os; import json; print(json.dumps(json.loads(os.environ['APP_SETTINGS'].replace('\n', '')), separators=(',', ':')))" | base64)
echo "$APP_SETTINGS" >>app_settings.txt
