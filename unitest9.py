# -*- coding: utf-8 -*-
import requests
import unittest


class Beaut(unittest.TestCase):
   
    def test_request_response(self):
        
    # Send a request to the API server and store the response.
        response = requests.get('http://jsonplaceholder.typicode.com/todos')

    # Confirm that the request-response cycle completed successfully.
        self.assertTrue(response.ok)
        
if __name__ == '__main__':
    
    unittest.main()        