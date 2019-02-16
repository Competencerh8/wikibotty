import json
import requests
import unittest
from unittest import TestCase
from bs4 import BeautifulSoup



class Beaut(unittest.TestCase):
    def test_assertin(self):
        
        resp = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&titles=Albert%20Einstein&prop=revisions&rvprop=content')
        soup = BeautifulSoup(resp.text)
        for paragraph in soup:
            print(soup.find_all( "p"))
         
        
        self.assertIn(paragraph,soup)
    
     
if __name__ == '__main__':
    
    unittest.main()         