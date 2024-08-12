# Table of Contents
```
Step 1: Server Setup
Step 2: Install Required Packages
Step 3: Configure MySQL Server
Step 4: Install CURL, Node, NPM, Yarn
Step 5: Install Frappe Bench
Step 6: Install ERPNext and other Apps
Step 7: Setup Production Server

```
# 1. SERVER SETUP:
```
Operating System: Linux Ubuntu 22.04 LTS
Type: t2.medium
Storage: 50 GB Disk
```
# 2. INSTALL REQUIRED PACKAGES
```
Frappe Bench and ERPNext requires many packages to run smoothly. In this step we will install all the required packages for the system to work correctly.

Note: During the installation of these packages the server might prompt you to confirm if you want to continue installing the package [Y/n]. Just hit “y” on your keyboard to continue.
```
## 2.1 Install GIT
```
sudo apt-get install git

Check if GIT is correctly installed by running git --version
```
## 2.2 Install Python
```
sudo apt-get install python3-dev python3.10-dev python3-setuptools python3-pip python3-distutils
```
## 2.3 Install Python Virtual Environment
```
sudo apt-get install python3.10-venv
Check if Python is correctly installed by running python3 -V
```
## 2.4 Install Software Properties Common (for repository management)
```
sudo apt-get install software-properties-common
```
## 2.5 Install MariaDB (MySQL server)
```
sudo apt install mariadb-server mariadb-client
Check if MariaDB is correctly installed by running mariadb --version
```
## 2.6 Install Redis Server
```
sudo apt-get install redis-server
```
## 2.8 Change Port redis Server
```
sudo nano /etc/redis/redis.conf

#port 6379
port 13000
```
## 2.8 Install other necessary packages (for fonts, PDFs, etc)
```
sudo apt-get install xvfb libfontconfig wkhtmltopdf
sudo apt-get install libmysqlclient-dev
```
# 3. CONFIGURE MYSQL SERVER

## 3.1 Setup the server
```
sudo mysql_secure_installation
```
```
During the setup process, the server will prompt you with a few questions as given below. Follow the instructions to continue the setup;

  Enter current password for root: (Enter your SSH root user password)
  Switch to unix_socket authentication [Y/n]: Y
  Change the root password? [Y/n]: Y
  It will ask you to set new MySQL root password at this step. This can be different from the SSH root user password.
  Remove anonymous users? [Y/n] Y
  Disallow root login remotely? [Y/n]: N
  This is set as N because we might want to access the database from a remote server for using business analytics software like Metabase / PowerBI / Tableau, etc.
  Remove test database and access to it? [Y/n]: Y
  Reload privilege tables now? [Y/n]: Y
```
## 3.2 Edit the MySQL default config file
```
sudo nano /etc/mysql/my.cnf
```
```
Add the below code block at the bottom of the file;
```
```
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```
```
sudo systemctl stop mariadb
```
```
sudo nano /etc/mysql/mariadb.conf.d/mariadb.cnf
```

```
[mysqld]

# GENERAL #
user                           = mysql
default-storage-engine         = InnoDB
socket                         = /var/lib/mysql/mysql.sock
pid-file                       = /var/lib/mysql/mysql.pid

# MyISAM #
key-buffer-size                = 32M
myisam-recover                 = FORCE,BACKUP

# SAFETY #
max-allowed-packet             = 256M
max-connect-errors             = 1000000
innodb                         = FORCE

# DATA STORAGE #
datadir                        = /var/lib/mysql/

# BINARY LOGGING #
log-bin                        = /var/lib/mysql/mysql-bin
expire-logs-days               = 14
sync-binlog                    = 1

# REPLICATION #
server-id                      = 1

# CACHES AND LIMITS #
tmp-table-size                 = 32M
max-heap-table-size            = 32M
query-cache-type               = 0
query-cache-size               = 0
max-connections                = 500
thread-cache-size              = 50
open-files-limit               = 65535
table-definition-cache         = 4096
table-open-cache               = 10240

# INNODB #
innodb-flush-method            = O_DIRECT
innodb-log-files-in-group      = 2
innodb-log-file-size           = 512M
innodb-flush-log-at-trx-commit = 1
innodb-file-per-table          = 1
innodb-buffer-pool-size        = 5462M
innodb-file-format             = barracuda
innodb-large-prefix            = 1
collation-server               = utf8mb4_unicode_ci
character-set-server           = utf8mb4
character-set-client-handshake = FALSE
max_allowed_packet             = 256M

# LOGGING #
log-error                      = /var/lib/mysql/mysql-error.log
log-queries-not-using-indexes  = 0
slow-query-log                 = 1
slow-query-log-file            = /var/lib/mysql/mysql-slow.log

# CONNECTIONS #

pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
bind-address    = 0.0.0.0

[mysql]
default-character-set = utf8mb4

[mysqldump]
max_allowed_packet=256M
```

## 3.3 Restart the MySQL server (for the config to take effect)

```
sudo systemctl start mariadb

sudo service mysql restart

sudo systemctl restart mariadb

sudo systemctl enable mariadb
```
# 4 . Instal CURL, Node, NPM and Yarn

4.1 Add the NodeSource repository to your system:
```
curl -sL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh
```

4.2 Now you can inspect the contents of the downloaded script:
```
sudo nano nodesurce_setup.sh
```

4.3 Once you are satisfied with the script’s contents you can run the script:
```
sudo bash nodesource_setup.sh
```

4.4 This script will automatically update the apt list. Now you can install nodejs on your server:
```
sudo apt install nodejs
```

4.5 Next, install yarn globally using the npm package manager:
```
sudo npm install -g yarn
```
# 5. INSTALL FRAPPE BENCH
## 5.1 Install Frappe Bench
```
sudo pip3 install frappe-bench
```
```
Check if Frappe Bench is correctly installed by running bench --version
```
## 5.2 Initialize Frappe Bench
```
bench init --frappe-branch version-15 frappe-bench
```
## 5.3 Go to Frappe Bench directory
```
This will be the main directory from where we will be running all the commands.
The full path of this directory will be: /home/ubuntu/frappe-bench/
```
```
cd frappe-bench/
```
## 5.4 Change user directory permissions
```
This will allow execution permission to the home directory of the frappe user we created in step 1.4
```
```
chmod -R o+rx /home/ubuntu/
```
## 5.5 Create a New Site

We will use this as the default site where ERPNext and other apps will be installed.
```
bench new-site site1.local
```
# 6 . Install ERPNext and other Apps

Finally, we’re at the last stage of the installation process!

## 6.1 Download the necessary apps to our server

Download the payments apps . This app is required during ERPNext installation
```
bench get-app payments
```
Download the main ERPNext app
```
bench get-app --branch version-15 erpnext
```
Download the HR & Payroll app (optional)
```
bench get-app hrms
```
Check if all the apps are correctly downloaded by running bench version --format table
## 6.2 Install all the Apps

Install the main ERPNext app
```
bench --site site1.local install-app erpnext
```
Install the HR & Payroll app (optional)
```
bench --site site1.local install-app hrms
```

## 6.3 Check common_site_config.json file in site directory
```
  Check redis ports is 13000 in common_site_config.json file
```
Note: You might get some warnings / error messages while trying to install apps on the default site. These messages can be ignored and you can proceed further.

# 7. SETUP PRODUCTION SERVER

## 7.1 Enable scheduler service
```
bench --site site1.local enable-scheduler
```
## 7.2 Disable maintenance mode
```
bench --site site1.local set-maintenance-mode off
```
## 7.3 Setup production config
```
sudo bench setup production ubuntu
```
## 7.4 Setup NGINX web server
```
bench setup nginx
```
## 7.5 Final server setup
```
sudo supervisorctl restart all
sudo bench setup production ubuntu
```
# Port Setup
```
You can now go to your server [IP-address]:80 and you will have a fresh new installation of ERPNext ready to be configured!

If you are facing any issues with the ports, make sure to enable all the necessary ports on your firewall using the below commands;
```
```
sudo ufw allow 22,25,143,80,443,3306,3022,8000/tcp
sudo ufw enable
```
