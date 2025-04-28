#!/usr/bin/env sh

set -ex

for path in sentinel-2-l2a.parquet/*.parquet; do
    ndjson_path=${path%.parquet}.ndjson
    rustac translate $path $ndjson_path
    pypgstac --dsn=$1 load items $ndjson_path
    rm $ndjson_path
done
