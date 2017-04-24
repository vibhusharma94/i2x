
**App Setup (Ubuntu)**

1. Dev tools Installations
  * sudo apt-get update
	* sudo apt-get install build-essential python-dev libevent-dev libxml2-dev libmysqlclient-dev python-setuptools python-pip libpq-dev libxslt1-dev
2. Install Git
  * sudo apt-get install git
3. Clone Repository
  * git clone git@github.com:vibhusharma94/i2x.git
4. Install PIP and VirtualEnv.
  * sudo apt-get install python-pip
  * sudo apt-get install python-virtualenv
5. Install Mysql
    * sudo apt-get install mysql-server
    * sudo service mysql stop
    * sudo service mysql start
    


====================================================================

**Setup Steps:**


1. Environment Setup:
       * Create a virtual environment
           * virtualenv env
       * Activate virtual environment
           * source env/bin/activate
       * Install the requirements by running the command:
           * pip install -r requirements.txt
               
2. Database Setup:
       * Create a database with the name 'i2x_db'
           * mysql -u root -p
           * create database i2x_db;
           * CREATE USER 'mcblab'@'%' IDENTIFIED BY PASSWORD 'elonmusk';
           * GRANT ALL PRIVILEGES ON * . * TO 'mcblab'@'localhost';
           * FLUSH PRIVILEGES;
       * Django db setup: 
           * Run `python manage.py makemigrations userauth`
           * Run `python manage.py makemigrations team`
           * Run `python manage.py migrate`
       * Create SuperUser: 
           * Run `python manage.py createsuperuser`

3. Starting the Django server locally:
       * python manage.py runserver 8000

4. Heroku deployment:
       * git clone git@github.com:vibhusharma94/i2x.git
       * cd i2x
       * heroku login
       * heroku create <app_name>
       * git push heroku master
       * heroku run python manage.py migrate
       * heroku run python manage.py createsuperuser
       * heroku run python manage.py collectstatic




 Rest API Documentation
-----------------------------

##**User API**

###  **User Signup**
    
  http://127.0.0.1:8000/signup

##### **POST**

*Request*

  #!shell
  curl -i -H "Content-Type: application/json" -X POST  -d '{"email": "john.doe@gmail.com","password": "mystrongpassword","first_name": "John", "last_name": "Doe"}' "http://127.0.0.1:8000/signup/"

*Response*
```
#!json
{
    "data": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@gmail.com",
        "is_verified": false
    }
}
```

###  **Email Verification**
    
  http://127.0.0.1:8000/email-verification/<key>

##### **GET**

*Request*

  #!shell
  curl -i -H "Content-Type: application/json" "http://127.0.0.1:8000/email-verification/bd3a839c-8b6c-44b7-8e76-5114dd843be1"

*Response*
```
#!json
{
    "message": "Account successfully verified.",
    "data": {}
}
```

###  **User Login**
    
  http://127.0.0.1:8000/login/

##### **POST**

*Request*

  #!shell
  curl -i -H "Content-Type: application/json" -X POST  -d '{"username": "john.doe@gmail.com","password": "mystrongpassword"}' "http://127.0.0.1:8000/login/"

*Response*
```
#!json
{
    "data": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@gmail.com",
        "is_verified": true,
        "token": "845393af198fa24ea0e071742fdd7d8f95b2c292",
        "expiry_time": 1492830810,
        "refresh_token": "a46e8faa160611c8ef52314efac85042508ce0da"
    }
}
```


###  **Forgot Password**
    
  http://127.0.0.1:8000/forgot-password/

##### **POST**

*Request*

  #!shell
  curl -i -H "Content-Type: application/json" -X POST  -d '{"email": "john.doe@gmail.com"}' "http://127.0.0.1:8000/forgot-password/"

*Response*
```
#!json
{
    "message": "We just sent you the link with which you will able to reset your password at john.doe@gmail.com",
    "data": {}
}
```


###  **Reset Password**
    
  http://127.0.0.1:8000/reset-password/<key>

##### **POST**

*Request*

  #!shell
  curl -i -H "Content-Type: application/json" -X POST  -d '{"password": "newstrongpassword"}' "http://127.0.0.1:8000/reset-password/b4678d1a06e906fa36cb2e2c95c735be/"

*Response*
```
#!json
{
    "message": "Password successfully reset.",
    "data": {}
}
```

###  **Create Team**
    
  http://127.0.0.1:8000/team

##### **POST**

*Request*

  #!shell
  curl -i -H "Content-Type: application/json" -H "Authorization: Token 845393af198fa24ea0e071742fdd7d8f95b2c292" -X POST  -d '{"name": "google"}' "http://127.0.0.1:8000/team/"

*Response*
```
#!json
{
    "data": {
        "id": 4,
        "name": "google",
        "is_active": true,
        "created": "2017-04-22T03:22:58.041653Z"
    }
}
```

