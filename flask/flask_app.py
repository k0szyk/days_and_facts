import flask
import os
import logging
import pymongo
import calendar
from flask import request, jsonify
from flask_api import status

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='./flask_app.log', filemode='a')

application = flask.Flask(__name__)

#To allow for unittest against live mongoDB
if not os.environ.get('MONGODB_HOSTNAME', None):
    mongodb_uri = 'mongodb://localhost:27017/'
else:
    mongodb_uri = 'mongodb://{}:27017/'.format(os.environ['MONGODB_HOSTNAME'])

def valid_date(m: int, d: int) -> bool:
    """
    Validates date(month and corresponding day) against a 366 days year

    :param m: integer representing a month.
    :param d: integer representing a day.
    :return: Boolean value stating if the given month and day is a valid in a 366 days year.
    """
    # Verify if month is valid and day is not greater than 31
    if m not in range(1, 13) or d > 31:
        return False
    day_list = list()
    # Verify if day is valid day in a given month
    cal = calendar.Calendar()
    for day in cal.itermonthdates(2020, m):
        if day.month == m:
            day_list.append(day.day)
    if d in day_list:
        return True
    else:
        return False


def dates_single_query(request: dict, mongodb_uri: str):
    """
    Queries the DB for single day and a fact.

    :param request: Dictionary containing month and date for queried fact.
    :param mongodb_uri: String containing the MongoDB URI.
    :return: A flask jsonified response ready to be sent over HTTP.
    """
    client = pymongo.MongoClient(mongodb_uri)
    db = client["facts_db"]
    col = db["facts"]
    db_response_list = list()
    # Reformat the request to match data type in MongoDB.
    request["month"], request["day"] = calendar.month_name[request["month"]], request["day"]
    logging.debug("MongoDB query: {}".format(request))
    # Checks if retrieved documents are non zero.
    if not col.count_documents(request):
        logging.error("MongoDB returned 0 responses. Will return 404 Not Found.")
        return "Not Found", status.HTTP_404_NOT_FOUND
    # Fetches the documents from DB.
    response = col.find(request)
    for item in response:
        db_response_list.append(item)
    logging.debug("MongoDB response: {}".format(db_response_list[0]))
    # Increases by 1 the hits value for the document.
    new_values = {"$set": {"hits": db_response_list[0]["hits"]+1}}
    col.update_one(request, new_values)
    # Prepares the response.
    response = jsonify({"id": db_response_list[0]["id"],
                        "month": db_response_list[0]["month"],
                        "day": db_response_list[0]["day"],
                        "fact": db_response_list[0]["fact"]})
    response.headers.set('Content-Type', 'application/json; charset=UTF-8')
    return response


def dates_all_query(mongodb_uri: str):
    """
    Queries the DB for single day and a fact.Queries the DB for single day and a fact.

    :param mongodb_uri: String containing the MongoDB URI.
    :return: A flask jsonified response ready to be sent over HTTP.
    """
    client = pymongo.MongoClient(mongodb_uri)
    db = client["facts_db"]
    col = db["facts"]
    db_response_list = list()
    # Creates a list with all documents as the response.
    for document in col.find():
        db_response_list.append({"id": document["id"],
                                 "month": document["month"],
                                 "day": document["day"],
                                 "fact": document["fact"]})
    # Prepares the response.
    response = jsonify(db_response_list)
    response.headers.set('Content-Type', 'application/json; charset=UTF-8')
    return response


@application.route('/dates', methods=['POST', 'GET'])
def dates():
    """
    Returns a response to POST or GET requests with a single entry or all entries.

    :return: HTTP response.
    """
    req = request.json
    logging.debug("Received a {} request: {}".format(request.method, request))
    # Checks for the POST request.
    if request.method == "POST":
        # Check for the valid dates. Taking into account a year with 366 days.
        if not valid_date(req["month"], req["day"]):
            return "Bad Request", status.HTTP_400_BAD_REQUEST
        response = dates_single_query(req, mongodb_uri)
    # Checks for the GET request.
    else:
        response = dates_all_query(mongodb_uri)
    return response


@application.route('/dates/<id>', methods=['DELETE'])
def delete_dates(id: str):
    """
    Deletes the date by ID from DB.

    :param id: String representation of the ID value.
    :return: HTTP response.
    """
    logging.debug("Received a {} request with id: {}.".format(request.method, id))
    headers = flask.request.headers
    headers_dict = dict()
    # Create a dictionary with HTTP headers.
    for h in headers:
        headers_dict[h[0]] = h[1]
    # Checks for "X-Api-Key" key in dictionary.
    if "X-Api-Key" not in headers_dict:
        logging.debug("Request does not contain the required X-Api-Key header.")
        return "Unauthorized ", status.HTTP_401_UNAUTHORIZED
    # Checks if value for "X-Api-Key" is correct.
    elif headers_dict["X-Api-Key"] != "SECRET_API_KEY":
        logging.debug("Request does not contain the required X-Api-Key value.")
        return "Unauthorized ", status.HTTP_401_UNAUTHORIZED
    client = pymongo.MongoClient(mongodb_uri)
    db = client["facts_db"]
    col = db["facts"]
    db_response_list = list()
    # Find document by id.
    response = col.find({"id": int(id)})
    for item in response:
        db_response_list.append(item)
    # Checks for the empty response
    if not db_response_list:
        return "Not Found", status.HTTP_404_NOT_FOUND
    # Checks for the non-existent ID in DB.
    elif int(id) != db_response_list[0]["id"]:
        return "Not Found", status.HTTP_404_NOT_FOUND
    # Deletes the entry
    col.delete_one({"id": int(id)})
    logging.debug("A document deleted from DB.")
    response = jsonify({"id": db_response_list[0]["id"],
                        "month": db_response_list[0]["month"],
                        "day": db_response_list[0]["day"],
                        "fact": db_response_list[0]["fact"]})
    response.headers.set('Content-Type', 'application/json; charset=UTF-8')
    return response


@application.route('/popular', methods=['GET'])
def popular():
    """
    Queries the DB for the amount of checks/hits per all months.

    :return: HTTP response.
    """
    logging.debug("Received a {} request.".format(request.method))
    # Connect to MongoDB
    client = pymongo.MongoClient(mongodb_uri)
    db = client["facts_db"]
    col = db["facts"]
    response_list = list()
    for month in range(1, 13):
        sum_hits = 0
        # Queries the DB for the documents with a month value
        response = col.find({"month": calendar.month_name[month]})
        # Sums the checks/hits for each day in a month.
        for document in response:
            sum_hits += document["hits"]
        # Prepares a list of months and checks.
        response_list.append({"id": month,
                              "month": calendar.month_name[month],
                              "days_checked": sum_hits})
    response = jsonify(response_list)
    response.headers.set('Content-Type', 'application/json; charset=UTF-8')
    return response


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5002)
#app.run(host='0.0.0.0', port=5002)

