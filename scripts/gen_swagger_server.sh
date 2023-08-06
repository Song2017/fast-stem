#!/usr/bin/env sh

# configuration
input="server/swagger/stem.yml"
output="server/python_server"
type="python-fastapi"
pkg_name="http_server"
pkg_version="1.5.1"

source ./scripts/generate_swagger_lib.sh
generate_swagger_lib $input $output $type $pkg_name $pkg_version