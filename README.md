# Deploying my web application to Linux

To complete this project, you`ll need a Linux server instance. We recommend using Amazon Lightsail for this. If you don`t already have an Amazon Web Services account, you`ll need to set one up. Once you`ve done that, here are the steps to complete this project.

   Username : grader
   Password : grader
   url : [link](http://ec2-52-32-219-71.us-west-2.compute.amazonaws.com/)
   IP : 52.32.219.71
   port : 2200


### 1. Get your server. Start a new Ubuntu Linux server instance on Amazon Lightsail. 

![alt text](https://github.com/Ishani1989//blob/master/static/screenshots/DishDescriptionPage.JPG "Dish Description")

### 2. Follow the instructions provided to SSH into your server.

I have deployed this project on a Windows system and SSH wasn't configured to run on terminal.
To use command line to SSH into your server, take the following steps:

	1. Open up your command prompt
	2. Check if the command SSH is recognized by the terminal by typing SSH
	3. If it is recognized skip to step 5
	4. If SSH is not recognized, add the path to ssh.exe file (USUALLY C:\Program Files\Git\usr\bin) to path variable
	5. Download private key from light sail 

![alt text](https://github.com/Ishani1989//blob/master/static/screenshots/DishDescriptionPage.JPG "Dish Description")

	6. Place it in a folder of your choice ( in this case I have used users home directory folder (C:\Users\Owner\.ssh))
	7. Since our current directory in terminal is C:\Users\Owner, we write ~/.ssh in the following command.(means .ssh folder within current directory). If you kept it in some other folder, specify the full path to your private key.
	8. By default, your instance comes with a user named 'ubuntu'. We will ssh as ubuntu using the command:
		`ssh ubuntu@52.32.219.71 -p 22 -i ~/.ssh/LightsailDefaultPrivateKey-us-west-2.pem`


### 3. Secure your server. Update all available packages on server by running the following command as root user

  `sudo apt-get update`

   Upgrade all packages on server by running the following command as root user

  `sudo apt-get upgrade`

### 4. Makechanges to include 2200 as custom port on the networking tab for your sail app.

   	Allow port 2200 on UFW

	`sudo ufw status`
	`sudo ufw allow ssh`
	`sudo ufw allow 2200/tcp`
	`sudo ufw allow www`
	`sudo ufw enable`
	`sudo ufw status`

### 5. Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.

   	login as root user by typing 

   	`sudo vim /etc/ssh/sshd_config`

   	Find the line with port number and change the number 22 to 2200.

   	Also, add a custom port to your lightsail instance having port as 2200.

![alt text](https://github.com/Ishani1989//blob/master/static/screenshots/DishDescriptionPage.JPG "Dish Description")

### 6. Disable root login and enforce key based authentication

	In the sshd_config file, 

	Find the PasswordAuthentication line and edit it to no
	Find the PermitRootLogin line and edit it to no.  Save and close this file.

    Restart the sshd service by running the following command:

    `sudo service sshd restart`

	Login again using ssh with the new port number :
	
	`ssh ubuntu@52.32.219.71 -p 2200 -i ~/.ssh/LightsailDefaultPrivateKey-us-west-2.pem`

### 7. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

	Warning: When changing the SSH port, make sure that the firewall is open for port 2200 first, so that you don`t lock yourself out of the server. Review this video for details! When you change the SSH port, the Lightsail instance will no longer be accessible through the web app `Connect using SSH` button. The button assumes the default port is being used. There are instructions on the same page for connecting from your terminal to the instance. Connect using those instructions and then follow the rest of the steps.

	`sudo ufw status`
	`sudo ufw allow 80/tcp`
	`sudo ufw allow 123/udp`

### 8. Create a new user account named grader.

	`sudo adduser grader`

### 9. Give sudo access to grader:

	`sudo touch /etc/sudoers.d/grader`
	`sudo nano /etc/sudoers.d/grader`

	Add the following line to the file to give grader sudo access:

	`grader ALL=(ALL:ALL) ALL`


### 8. Create an SSH key pair for grader using the ssh-keygen tool.

	1. From your terminal on local machine run 

		`ssh-keygen`

	By default, it generates RSA type token. Specify the file to save the key pair.

	![alt text](https://github.com/Ishani1989//blob/master/static/screenshots/DishDescriptionPage.JPG "Dish Description")

	The process generates 2 files. id_rsa and id_rsa.pub. the id_rsa.pub file will be placed on the server to allow access to users.

### 9. switch to user grader 

	`su - grader`

	and run follow the following commands :

		1.  `mkdir .ssh`
		2.  `sudo touch .ssh/authorized_keys`
		3.  Copy the contents of pub file from your local machine to the authorized_keys file
		    `nano .ssh/authorized_keys`
		4.  Paste the pub file you just copied in a single line
		5.  Set up file permissions
		    `chmod 700 .ssh`
		    `chmod 600 .ssh/authorized_keys`
		6.  Change /etc/ssh/sshd_config so it contains 'AuthorizedKeysFile %h/.ssh/authorized_keys '
		7.  `sudo service ssh restart`
		8.  Login with ssh using grader
			`ssh grader@52.32.219.71 -p 2200 -i ~/.ssh/id_rsa`


### 10. Prepare to deploy your project.
	   
	    Configure the local timezone to UTC.

		`sudo  timedatectl set-timezone Etc/UTC`

		Install and configure Apache to serve a Python mod_wsgi application.


		1. Install Apache `sudo apt-get install apache2`
		2. Install mod_wsgi `sudo apt-get install python-setuptools libapache2-mod-wsgi`
		3. Restart Apache `sudo service apache2 restart`


### 11. Install and configure PostgreSQL:

		`sudo apt-get install postgresql`
		`$ sudo apt-get install postgresql postgresql-contrib.`

Install some necessary Python packages for working with PostgreSQL:

		`$ sudo apt-get install libpq-dev python-dev.`

Login as postgres user
	`$ sudo su - postgres`, then connect to the database system with `$ psql.`
    
    Create a new user called `cuisine` with his password:
    `# CREATE USER cuisine WITH PASSWORD `cuisine`;.`

    Give cuisine user the CREATEDB capability:
    `# ALTER USER cuisine CREATEDB;.`

    Create the `cuisinewisedb` database owned by cuisine user:
    `# CREATE DATABASE cuisinewisedb WITH OWNER cuisine;.`

    Connect to the database:
    `# \c cuisinewisedb.`

    Revoke all rights: `# REVOKE ALL ON SCHEMA public FROM public;.`
    Lock down the permissions to only let cuisine role create tables: `# GRANT ALL ON SCHEMA public TO cuisine;.`

    Log out from PostgreSQL: `# \q.` Then return to the grader user: $ exit.


### 12. Install Git and Clone Repo:

	1. Install Git using `sudo apt-get install git`
	2. Use cd /var/www to move to the /var/www directory
	3. Create the application directory `sudo mkdir FlaskApp`
	4. Move inside this directory using `cd FlaskApp`
	5. Clone the Catalog App to the virtual machine 
	   `git clone https://github.com/Ishani1989/CuisineWise`
	6. `cd CuisineWise`
	7. Rename project.py to __init__.py using `sudo mv project.py __init__.py`

	We need to change the create engine statement wherever used (database_setup.py, __init__.py, addDataToCuisine.py) with the following statement to make it compatible with POSTgreSQL.
		`engine = create_engine('postgresql://cuisine:cuisine@localhost/cuisinewisedb')`

	Here, username = cuisine
		  password = cuisine
		  db name = cuisinewisedb

### 13. Install dependencies:

	`sudo apt-get install python-pip`
	`sudo pip install flask`
	`sudo pip install flask-sqlalchemy`
	`sudo apt-get install python-httplib2`
	`sudo apt-get install python-requests`
	`sudo pip install psycopg2`


### 14. Update host and wsgi file

Change the host name and port number on the app.run statement in __init__.py to include your ip and port 2200.

Create wsgi file in folder FlaskApp and add the following statements, save and quit.

#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp")

from CuisineWise import app as application
application.secret_key = 'secret key as in your init.py file'

### 15. Create virtual env config file

	`sudo touch /etc/apache2/sites-available/CuisineApp.conf`

	`sudo vim /etc/apache2/sites-available/CuisineApp.conf`

	Add the following statements

	<VirtualHost *:80><br />
		ServerName 52.32.219.71<br />
    	ServerAlias www.ec2-52-32-219-71.us-west-2.compute.amazonaws.com/<br />
    	ServerAdmin admin@52.32.219.71<br />
    	WSGIScriptAlias / /var/www/FlaskApp/cuisineapp.wsgi<br />
 	<Directory /var/www/FlaskApp/CuisineWise/><br />
    	Order allow,deny<br />
    	Allow from all<br />
	</Directory><br />
	Alias /static /var/www/FlaskApp/CuisineWise/static<br />
	<Directory /var/www/FlaskApp/CuisineWise/static/><br />
	Order allow,deny<br />
	    Allow from all<br />
	    </Directory><br />
	    ErrorLog ${APACHE_LOG_DIR}/error.log<br />
	    LogLevel warn<br />
	    CustomLog ${APACHE_LOG_DIR}/access.log combined<br />
	</VirtualHost><br />

Save and close the file.

### 16. Enable the virtual host with the following command:

	`sudo a2ensite CuisineApp`

	`sudo service apache2 reload`

	`sudo service apache2 restart`

Your application is now deployed. Check it on your browser at the given url.

[link](http://ec2-52-32-219-71.us-west-2.compute.amazonaws.com/)

### 17. Error Handling :

##### Common errors encountered:

For port already in use error :

Check which process is running on specified port 

`sudo netstat -lpn |grep :5000`

Kill all processes running on port 5000

`sudo fuser -k 5000/tcp	`

check error logs:

`sudo tail -f /var/log/apache2/error.log

users and passwords :

ubuntu password : ubuntu
grader password : grader
cuisine password : cuisine


### References :

1. https://httpd.apache.org/docs/2.2/vhosts/examples.html
2. https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
3. https://classroom.udacity.com/nanodegrees/nd004/parts/ab002e9a-b26c-43a4-8460-dc4c4b11c379
4. http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/