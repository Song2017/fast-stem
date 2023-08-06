set -e
#flake8  --exclude server,tmp
source ./scripts/configuration.sh
if [ -d ../_config/ ]; then
  source ../_config/stem/configuration.sh
fi
export PYTHONPATH="."
python3.9 server/http_server.py
