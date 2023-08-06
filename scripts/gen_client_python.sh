#!/usr/bin/env sh

# configuration
input="server/swagger/stem.yml"
output="server/python_client"
type="python"
pkg_name="http_client"
pkg_version="0.0.1"

source ./scripts/generate_swagger_lib.sh
generate_swagger_lib $input $output $type $pkg_name $pkg_version