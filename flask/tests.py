from flask_app import application as app
import unittest

class FlaskTest(unittest.TestCase):

    def test_get_dates(self):
        tester = app.test_client(self)
        response = tester.get('/dates')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    
    def test_get_dates_content(self):
        tester = app.test_client(self)
        response = tester.get('/dates')
        self.assertEqual(response.content_type, "application/json")


    def test_det_dates_response(self):
        tester = app.test_client(self)
        response = tester.get('/dates')
        self.assertTrue(b'fact' in response.data)

if __name__ == "__main__":
    unittest.main()
