# Bench and frappe Bench Installation Setup:
## Pre-requisites
```
  OS: Ubuntu 22.04
  Python 3.10
  Redis 6
  yarn 1.12+
  pip 20+
  Node.js 14 above
  MariaDB 10.6.6+
```

## Step 1: Install python, and redis
```

sudo apt install python3-dev python3-pip redis-server
```
## Step 2: Install MariaDB
```
sudo apt install software-properties-common
sudo apt-get install mariadb-server mariadb-client
```
## Step 3: MariaDB Password Setup:
```
sudo mysql_secure_installation

```
> [!NOTE]
> The Above command will be prompted to set the MySQL root password
> During the setup process, the server will prompt you with a few questions as given below. Follow the instructions to continue the setup;
```
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
## Step 4: Edit the MariaDB configuration file (this step is not required for Frappe v15.21.0 or above)
```
nano /etc/mysql/my.cnf

```
### And add this configuration in my.cnf
```
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```
### Now, just restart the mysql service
```
service mysql restart
```

## Step 5: Install Node and Yarn

Add the NodeSource repository to your system:
```
curl -sL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh
```

Now you can inspect the contents of the downloaded script:
```
sudo nano nodesurce_setup.sh
```

Once you are satisfied with the script’s contents you can run the script:
```
sudo bash nodesource_setup.sh
```

This script will automatically update the apt list. Now you can install nodejs on your server:
```
sudo apt install nodejs
```

Next, install yarn globally using the npm package manager:
```
sudo npm install -g yarn
```
Install wkhtmltopdf
```
apt-get install xvfb libfontconfig
```
## Step 6: Install Bench CLI

```
sudo apt install python3.10-venv
```
Install bench via pip3
```
pip3 install frappe-bench
```
Confirm the bench installation by checking version
```
bench --version
```

## Step 7: Install Frappe Bench

```
bench init frappe-bench
```

Go to frappe-bench folder
```
cd frappe-bench
```
Create The Site
```
bench new-site localhost
```
> [!NOTE]
> The above command asks DB root password and app admin password

Enable scheduler on Site
```
bench --site localhost enable-scheduler
```
Start the Bench
```
bench start
```
> [!NOTE]
> Check HTTP://localhost:8000

## Commands
List The app
```
bench --site localhost list-apps
```
Get App
```
bench get-app erpnext
```
Install App
```
bench --site localhost install-app erpnext
```



