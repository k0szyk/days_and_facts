from flask_app import application as app
from faker import Faker
from random import randrange
import datetime
import unittest
import json
import requests
import calendar
import sys



def generate_random_date(year: int):
    fake = Faker()
    random_date = fake.date_between(start_date = datetime.date(year=year, month=1, day=1),
                             end_date = datetime.date(year=year, month=12, day=31))
    day = int(random_date.day)
    month = int(random_date.month)
    return {"day": day, "month":  month}

class FlaskTest(unittest.TestCase):

    def test_get_dates(self):
        # Simple test to check for 200 OK response from flask_app
        tester = app.test_client(self)
        response = tester.get('/dates')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    
    def test_get_dates_content(self):
        # Checks for the content type value
        tester = app.test_client(self)
        response = tester.get('/dates')
        self.assertEqual(response.content_type, "application/json; charset=UTF-8")


    def test_get_dates_response(self):
        # Simple check to veryfy if a key "fact" is available in response from flask_app
        tester = app.test_client(self)
        response = tester.get('/dates')
        self.assertTrue(b'fact' in response.data)
    

    def test_post_dates(self):
        # Simple test to verify if the response of POST /dates gives a correct day, month and if key 'fact' are in the response.
        tester = app.test_client(self)
        payload = generate_random_date(2020)
        response_app = tester.post('/dates', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        response_app_data = json.loads(response_app.data)
        self.assertTrue(payload["day"] == response_app_data["day"] and 
                        calendar.month_name[payload["month"]] in response_app_data["month"] and
                        'fact' in response_app_data.keys())


    def test_popular(self):
        # Test to verify if the POST /dates increments the "days_checked" value.
        tester = app.test_client(self)
        payload = generate_random_date(2020)
        tester.post('/dates', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        response = tester.get('/popular', headers={'Content-Type': 'application/json'})
        response = json.loads(response.data)
        for item in response:
            if item["month"] == calendar.month_name[payload["month"]]:
                checks = item["days_checked"]
        self.assertTrue(checks > 0)


    def test_incorrect_secret(self):
        # Test to verify if incorrect X-Api-Key gives a 401 response.
        tester = app.test_client(self)
        secret = {'X-Api-Key': 'gibberish'}
        response = tester.delete('/dates/'+str(randrange(367)), headers=secret)
        self.assertEqual(response.status_code, 401)

    
    def test_correct_secret(self):
        # Test to verify if correct X-Api_Key provides a 200 OK response.
        tester = app.test_client(self)
        secret = {'X-Api-Key': 'SECRET_API_KEY'}
        response = tester.delete('/dates/'+str(randrange(367)), headers=secret)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
