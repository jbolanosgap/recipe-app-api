#!/bin/bash

set -e

# This script uses the `envsubst` command to substitute environment variables in the `/etc/nginx/default.conf.tpl` file
# and then redirects the output to the `/etc/nginx/conf.d/default.conf` file.
# The `envsubst` command replaces any occurrences of `$VAR` or `${VAR}` with the value of the corresponding environment variable.
# This script is typically used in a Docker container to dynamically configure the NGINX server based on environment variables.
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# This script starts the Nginx server and keeps it running in the foreground.
# It uses the 'daemon off;' option to prevent Nginx from running as a background daemon.
nginx -g 'daemon off;'
