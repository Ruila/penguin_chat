from bs4 import BeautifulSoup
import requests
from abc import ABC, abstractmethod
import json

class Weather(ABC):
    def __init__(self, area):
        self.area = area

        @abstractmethod
        def scrape(self):
            pass


class WhatWeather(Weather):

    def scrape(self):
        content = "ggg"
        response = requests.get('')
        data = json.loads(response.text)
        print("data hahaha", data['records']['datasetDescription'])






        return data['records']['datasetDescription']

       