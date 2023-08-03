#!/usr/bin/env sh

set -o errexit
set -o nounset

cmd="$*"

postgres_ready () {
  # Check that postgres is up and running on port `5432`:
  sh "/tgbot/wait-for-command.sh" -t 5 -s 0 52 -c "curl postgres:5432"
}
until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
done

# It is also possible to wait for other services as well: redis, elastic, etcd
>&2 echo "Postgres is up - continuing..."

elastic_ready () {
  # Check that postgres is up and running on port `5432`:
  sh "/tgbot/wait-for-command.sh" -t 5 -s 0 52 -c "curl http://elastic:9200"
}
until elastic_ready; do
  >&2 echo "Elastic is unavailable - sleeping"
done

# It is also possible to wait for other services as well: redis, elastic, etcd
>&2 echo "Elastic is up - continuing..."

# Evaluating passed command:
exec $cmd