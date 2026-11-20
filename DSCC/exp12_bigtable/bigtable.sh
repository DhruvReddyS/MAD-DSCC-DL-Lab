# Step 1: Configure Project
gcloud init
gcloud config set project YOUR_PROJECT_ID

# Step 2: Enable Bigtable API
gcloud services enable bigtable.googleapis.com

# Step 3: Create Instance
gcloud bigtable instances create my-instance \
--cluster=my-cluster \
--cluster-zone=asia-south1-a \
--display-name="My Bigtable Instance" \
--cluster-num-nodes=1

# Step 4: Install CBT
gcloud components install cbt

# Step 5: Create Table
cbt -project=YOUR_PROJECT_ID \
-instance=my-instance createtable my-table

# Step 6: Create Column Family
cbt -project=YOUR_PROJECT_ID \
-instance=my-instance createfamily my-table cf1

# Step 7: Insert Records
cbt -project=YOUR_PROJECT_ID \
-instance=my-instance set my-table row1 cf1:name=Alice
cbt -project=YOUR_PROJECT_ID \
-instance=my-instance set my-table row1 cf1:age=25
cbt -project=YOUR_PROJECT_ID \
-instance=my-instance set my-table row1 cf1:dept=CSE

# Step 8: Read Records
cbt -project=YOUR_PROJECT_ID \
-instance=my-instance read my-table

# Step 9: Delete Column Family
cbt -project=YOUR_PROJECT_ID \
-instance=my-instance deletefamily my-table cf1

# Step 10: Delete Row
cbt -project=YOUR_PROJECT_ID \
-instance=my-instance deleterow my-table row1
