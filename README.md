## This is the DAYS and FACTS project.

### Description

The goal of the project is to build a simple REST API using Flask to retrieve data from http://numbersapi.com.

### Design

The project is build from 5 main parts:
1. MongoDB - a noSQL database that stores the data. MongoDB was selected as this is a fairly lightweight DB. The data model does not require any complex operations, therefore a selection of lightweight MongoDB.
2. Flask - a Python library that is a webb framework that will handle the logic behind the REST API.
3. Gunicorn (WSGI) - acting as the Web Server Gateway to allow the scalability for the REST API.
4. Nginx - a web server that provides the security and scalability and acts as the proxy server.
5. populate_db.py - a Python script used to pre-populate the MongoDB with data from http://numbersapi.com.

![alt text](https://github.com/k0szyk/days_and_facts/blob/main/diagram.png?raw=true)

### Instructions



#### Note: 
#### Note: 