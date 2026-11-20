# 1. Start Cassandra in Docker (wait ~1 min for it to boot)
docker run -d --name cassandralab cassandra:latest
# 2. Open the CQL shell
docker exec -it cassandralab cqlsh
