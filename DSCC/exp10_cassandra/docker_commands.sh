# Step 1: Pull Cassandra
sudo docker pull cassandra:latest

# Step 2: Create Network
sudo docker network create cassandralab

# Step 3: Start Cassandra
sudo docker run -d --name cassandralab \
--network cassandralab cassandra:latest

# Step 4: Connect to Cassandra
sudo docker exec -it cassandralab cqlsh
