# On the Ubuntu EC2 instance (after: ssh -i key.pem ubuntu@PUBLIC-IP)
sudo apt update
sudo apt install nodejs npm -y
node --version
mkdir MyApp && cd MyApp
nano app.js          # paste the code, save
node app.js
# Browser: http://PUBLIC-IP:3000  (allow TCP 3000 in the security group)
