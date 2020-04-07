# Pur Beurre Food Facts application

This application allow users to obtain a healthiest substitution food for an industrial food given. This application interact with **Open Food Facts API** and is based on a database. Users data and food search result are stock in a local database. 
See: https://en.wiki.openfoodfacts.org/API

## List of fonctionnalities

* Create an account.
* Record useful information.
* Consult the information of the account. 
* Login in a session.
* Search a food from a list of food category. 
and find the healthiest food of the category.
* Record the history of search on the database. 
* Consult the history of search.
* Add a category of food at the database.  

## Used technology

### Back End 
For the back end, this web application use Python 3.6.9. 

### Database
Database use MySQL (mysql  Ver 14.14 Distrib 5.7.29, for Linux (x86_64))
Mysql-connector if used for relation between Python and MySQL. 

### Front End
On the front, html 5 with Jinja2 is used. 

## Requirement 

* certifi==2019.11.28
* chardet==3.0.4
* Click==7.0
* Flask==1.1.1
* idna==2.8
* itsdangerous==1.1.0
* Jinja2==2.11.1
* MarkupSafe==1.1.1
* mysql-connector==2.2.9
* requests==2.22.0
* urllib3==1.25.8
* Werkzeug==1.0.0



