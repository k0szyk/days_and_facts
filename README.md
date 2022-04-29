## This is the DAYS and FACTS project.

### Description

The goal of the project is to build a simple REST API using Flask to retrieve data from http://numbersapi.com.

### Design

The project is build from 5 main parts:
1. **MongoDB** - a noSQL database that stores the data. MongoDB was selected for its lightweight requirements. The data model does not require any complex operations, therefore a selection of MongoDB.
2. **Flask** - a Python library that is a web framework that will handle the logic behind the REST API.
3. **Gunicorn** (WSGI) - acting as the Web Server Gateway to allow the scalability for the REST API.
4. **Nginx** - a web server that provides the security and scalability and acts as the reverse proxy server.
5. **populate_db.py** - a Python script used to pre-populate the MongoDB with data from http://numbersapi.com.

![alt text](https://github.com/k0szyk/days_and_facts/blob/main/diagram.png?raw=true)

### Instructions

The project is meant for containerized deployment using Docker and Docker-Compose. Make sure that those are installed on target host before proceeding.

In order to build and start Docker containers run the following command in the folder containing ```docker-compose.yml```:

```
sudo docker-compose up -d
```
#### Note: Docker version 20.10.14 and Docker-Compose version 1.29.2 was used for testing of this project.

### Containers
The ```docker-compose.yml``` will build 4 containers:
1. **mongodb** - a container with MongoDB.
2. **populate_db** - a container used to populate the MongoDB with data from http://numbersapi.com.
3. **flask_app** - a container with Flask application and Gunicorn serving the REST API.
4. **webserver** - a container with Nginx web server acting as the frontend HTTP server and reverse proxy.

### Usage

The application is currently available at ```3.220.133.33:80```

There are 4 endpoints available for REST API:
1. **POST /dates** - retrieves a fact for the specified day and month. 
- Sample POST /dates request body:
```json
{
  "month": 12,
  "day": 31
}
```
- Sample POST /dates response body:
```json
{
  "id": 366,
  "day": 31,
  "month": "December", 
  "fact": "December 31st is the day in 1759 that Arthur Guinness signs a 9,000 year lease at £45 per annum and starts brewing Guinness.",
}
```
2. **DELETE /dates/{id}** - deletes an entry by id. Requires HTTP header: ```X-Api-Key: SECRET_API_KEY```
3. **GET /dates** - retrieves all the days and facts available at the time in the database.
- Sample GET /dates response body:
```json
[
  {
    "id": 1,  
    "day": 1,
    "month": "January",
    "fact": "January 1st is the day in 1973 that Denmark, the United Kingdom, and Ireland are admitted into the European Community."
  },
  {
    "id": 2,
    "day": 2,
    "month": "January",
    "fact": "January 2nd is the day in 1949 that Luis Muñoz Marín becomes the first democratically elected Governor of Puerto Rico."
  }
]
```
4. **GET /popular** - retrieves the months and the value representing number of times facts for the days in a respective month were checked.
- Sample GET /popular response body:
```json
[
  {
    "days_checked": 1,
    "id": 1,
    "month": "January"
  },
  {
    "days_checked": 6,
    "id": 2,
    "month": "February"
  },
  {
    "days_checked": 4,
    "id": 3,
    "month": "March"
  }
]
```
