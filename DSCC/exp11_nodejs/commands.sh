# Step 1: Update Ubuntu
sudo apt update
sudo apt upgrade -y

# Step 2: Install Node.js
sudo apt install nodejs npm -y
node --version

# Step 3: Create Project
mkdir MyApp
cd MyApp
nano app.js

# Step 4: Write JavaScript Code (paste app.js)

# Step 5: Run Application
node app.js

# Step 6: Open Browser
# Allow inbound TCP port 3000 in the EC2 security group and enter:
# http://PUBLIC-IP:3000
