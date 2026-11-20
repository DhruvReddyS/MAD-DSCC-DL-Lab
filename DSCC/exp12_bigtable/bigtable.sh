# 1. Select project and enable the Bigtable API
gcloud init
gcloud config set project YOUR_PROJECT_ID
gcloud services enable bigtable.googleapis.com

# 2. Create an instance (1 node cluster)
gcloud bigtable instances create my-instance --display-name="My Instance" \
  --cluster-config=id=my-cluster,zone=asia-south1-a,nodes=1

# 3. Install cbt and save defaults in ~/.cbtrc (so -project/-instance are not repeated)
gcloud components install cbt
echo "project = YOUR_PROJECT_ID" > ~/.cbtrc
echo "instance = my-instance" >> ~/.cbtrc

# 4. Create table + column family, insert, read, delete
cbt createtable my-table
cbt createfamily my-table cf1
cbt set my-table row1 cf1:name=Alice cf1:age=25 cf1:dept=CSE
cbt read my-table
cbt deleterow my-table row1
cbt deletetable my-table
