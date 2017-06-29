# Deploying my web application to Linux

To complete this project, you`ll need a Linux server instance. We recommend using Amazon Lightsail for this. If you don`t already have an Amazon Web Services account, you`ll need to set one up. Once you`ve done that, here are the steps to complete this project.

   Username : grader
   Password : grader
   url : [link](http://ec2-13-59-193-116.us-east-2.compute.amazonaws.com/)
   port : 2200


### 1. Get your server. Start a new Ubuntu Linux server instance on Amazon Lightsail. There are full details on setting up your Lightsail instance on the next page.

### 2. Follow the instructions provided to SSH into your server.


### 3. Secure your server. Update all available packages on server by running the following command as root user

  `sudo apt-get update`

   Upgrade all packages on server by running the following command as root user

  `sudo apt-get upgrade`

   Makechanges to include 2200 as custom port on the networking tab for your sail app.

   Allow port 2200 on UFW

	`sudo ufw status`
	`sudo ufw allow ssh`
	`sudo ufw allow 2200/tcp`
	`sudo ufw allow www`
	`sudo ufw enable`
	`sudo ufw status`

### 4. Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.

   login as root user by typing 

   `sudo vim /etc/ssh/sshd_config`
   The # symbol tells the server to ignore anything after it on the same line, so we will need to remove that character and then change the number 22 to 2200.

   Restart the sshd service by running the following command:

   `sudo service sshd restart`

### 5. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

Warning: When changing the SSH port, make sure that the firewall is open for port 2200 first, so that you don`t lock yourself out of the server. Review this video for details! When you change the SSH port, the Lightsail instance will no longer be accessible through the web app `Connect using SSH` button. The button assumes the default port is being used. There are instructions on the same page for connecting from your terminal to the instance. Connect using those instructions and then follow the rest of the steps.
Give grader access.
In order for your project to be reviewed, the grader needs to be able to log in to your server.

### 6. Create a new user account named grader.

`sudo adduser grader`
password : grader

### 7. Give grader the permission to sudo.

`usermod -aG sudo grader`
`su - grader`

[Source](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart)


### 8. Create an SSH key pair for grader using the ssh-keygen tool.

Using GitBash from your windows machine, run ssh-keygen command
Specify the file to save the key pair.
enter passphrase as "grader"
The process generates 2 files. token and token.pub. the token.pub file will be placed on the server to allow access to users.

generate a key pair with puttygen.exe (length: 1024 bits)
load the private key in the PuTTY profile
enter the public key in ~/.ssh/authorized_keys in one line (needs to start with ssh-rsa)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chown $USER:$USER ~/.ssh -R
change /etc/ssh/sshd_config so it contains AuthorizedKeysFile %h/.ssh/authorized_keys
sudo service ssh restart

[Source](https://askubuntu.com/questions/306798/trying-to-do-ssh-authentication-with-key-files-server-refused-our-key)


### 9. Prepare to deploy your project.
	   Configure the local timezone to UTC.

`sudo  timedatectl set-timezone Etc/UTC`


### 10. Install and configure Apache to serve a Python mod_wsgi application.

`sudo apt-get install apache2`
`https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-16-04`
`sudo service apache2 restart`

### 11. Install and configure PostgreSQL:

`sudo apt-get install postgresql`

Install some necessary Python packages for working with PostgreSQL: 

`$ sudo apt-get install libpq-dev python-dev.`

Install PostgreSQL: 

`$ sudo apt-get install postgresql postgresql-contrib.`
Login as postgres user 
`$ sudo su - postgres`, then connect to the database system with $ psql.
	Create a new user called `cuisine` with his password: 
	# CREATE USER catalog WITH PASSWORD `sillypassword`;.
	Give catalog user the CREATEDB capability: 
	# ALTER USER catalog CREATEDB;.
	Create the `catalog` database owned by catalog user: 
	# CREATE DATABASE catalog WITH OWNER catalog;.
	Connect to the database: 
	# \c catalog.
	Revoke all rights: # REVOKE ALL ON SCHEMA public FROM public;.
	Lock down the permissions to only let catalog role create tables: # GRANT ALL ON SCHEMA public TO catalog;.
	Log out from PostgreSQL: # \q. Then return to the grader user: $ exit.
	Inside the Flask application, change the create engine statement as follows:
	engine = create_engine(`postgresql://catalog:sillypassword@localhost/catalog`)
	Setup the database with: $ python /var/www/catalog/catalog/setup_database.py.

[Source](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)

Do not allow remote connections

`sudo vim /etc/postgresql/9.3/main/pg_hba.conf`

Create a new database user named catalog that has limited permissions to your catalog application database.

Switch accounts to postgres user
`sudo -i -u postgres`

`createdb catalog`

`sudo adduser catalog`

`GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;`

Quit postgreSQL postgres=# \q

Exit from user "postgres"

exit

[Source](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)
[Source](https://www.a2hosting.com/kb/developer-corner/postgresql/managing-postgresql-databases-and-users-from-the-command-line)

### 12. Install git.

`sudo apt-get install git`

Deploy the Item Catalog project.

### 13. Clone and setup your Item Catalog project from the Github repository you created earlier in this Nanodegree program.


Give access to current user to var directory
sudo chown -R username.www-data /var/www

sudo chmod -R +rwx /var/www

create a new dir catalog

cd /var/www 
sudo mkdir catalog 
cd catalog 

Make sure the .git directory is not publicly accessible via a browser 
At the root of the web directory, add a .htaccess file and include this line: 
RedirectMatch 404 /\.git


Move to your project folder :

cd /var/www/catalog/CuisineWise

Rename project.py to __init__.py using sudo mv project.py __init__.py

install python and virtual env

sudo apt-get install python-pip
sudo pip install virtualenv

install dependencies:

sudo pip install flask-sqlalchemy
sudo apt-get install python-httplib2
sudo apt-get install python-requests


Give the following command (where catalogapp is the name you would like to give your temporary environment):

sudo virtualenv catalogapp

Now, install Flask in that environment by activating the virtual environment with the following command 
source catalogapp/bin/activate

sudo pip install Flask

Run the following command to test if the installation is successful and the app is running 
sudo python __init__.py renamed project.py to init.py 
It should display “Running on http://localhost:5000/” or "Running on http://127.0.0.1:5000/". 
If you see this message, you have successfully configured the app.

To deactivate the environment, give the following command 
deactivate

Configure and Enable the new Virtual Host sudo nano /etc/apache2/sites-available/CuisineApp.conf

<VirtualHost *:80>
		ServerName 13.59.193.116
		ServerAdmin admin@13.59.193.116
		WSGIScriptAlias / /var/www/catalog/catalog.wsgi
		<Directory /var/www/catalog/CuisineWise/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/catalog/CuisineWise/static
		<Directory /var/www/catalog/CuisineWise/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

Save and close the file.

Enable the virtual host with the following command:

sudo a2ensite CuisineApp

sudo service apache2 reload

sudo service apache2 restart

create wsgi file :

#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog")

from CuisineWise import app as application
application.secret_key = `....secret key....` (hidden for security)


### 14. Set it up in your server so that it functions correctly when visiting your server’s IP address in a browser. Make sure that your .git directory is not publicly accessible via a browser!


### 15. Error Handling :

For port already in use error :

Check which process is running on specified port 

sudo netstat -lpn |grep :5000

Kill all processes running on port 5000

sudo fuser -k 5000/tcp	


sample wsgi that works :

def application(environ, start_response):
    status = `200 OK`
    output = b`Hello World!`

    response_headers = [(`Content-type`, `text/plain`),
                        (`Content-Length`, str(len(output)))]
    start_response(status, response_headers)

    return [output]

check error logs:

sudo tail -f /var/log/apache2/error.log

users and passwords :

ubuntu password : ubuntu
grader password : grader
catalog password : catalog
lightsail static password : light

### References :

1. https://httpd.apache.org/docs/2.2/vhosts/examples.html
2. https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
3. https://classroom.udacity.com/nanodegrees/nd004/parts/ab002e9a-b26c-43a4-8460-dc4c4b11c379
4. http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/