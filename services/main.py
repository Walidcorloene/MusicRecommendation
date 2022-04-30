from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

import re


class Artist():
    def __init__(self, name, headless=True, chromedriver_path="chromedriver"):
        self.name = name
        self.display = headless
        self.chromedriver_path = chromedriver_path

        self.driver = False

        self.concerts = self.__retrieving_concerts()

        if not self.concerts:
            self.concerts = self.__scrape_concerts_init()

    def __repr__(self) -> str:
        return f'Artist name: {self.name} \
                Concerts : {self.concerts}'

    def __getDriver(self) -> webdriver.chrome.webdriver.WebDriver:
        """
        Provides a driver (chrome window) to the other functions of the class
        """
        if not self.driver:
            options = webdriver.ChromeOptions()
            options.headless = self.display

            driver = webdriver.Chrome(executable_path=self.chromedriver_path, options=options)
            self.driver = driver

        return self.driver
    
    
    def __retrieving_concerts(self):
        """
        Getting events we already scraped from a SQLite DB
        """
        ###############################
        # TODO : GET CONCERTS FROM DB #
        ###############################

        print("Retrieving concerts...\n")
        return []

    def __scrape_concerts_init(self) -> list:
        """
        Scraping concerts for an artist that has currently no concerts in the DB
        """
        driver = self.__getDriver()

        driver.get(f'https://www.infoconcert.com/recherche-concert.html?motclef={self.name}')

        # Getting search results
        try:
            results = driver.find_element(By.CLASS_NAME, 'bg_content_search')
            links = results.find_elements(By.CLASS_NAME, 'results-line')
            artists = [x.text for x in links]
        except NoSuchElementException:
            print("No results for this search")

        # Getting text from search results
        artists = [x.text for x in links]

        # Picking just the artisnt name without text between parenthesis
        matches = []
        for i in artists:
            x = re.match(r'^[a-zA-Z0-9&]+\s?([a-zA-Z0-9&]+\s?)+', i).group(0)
            matches.append(x.rstrip())

        # Scoring entries depending on their length correspondance with the query
        matches_score = [(len(self.name)) / len(i) for i in matches]


        try:
            # Getting the artist that fully corresponds to the query
            artist_index = matches_score.index(1.0) 
            assert matches[artist_index].lower() == self.name.lower()
        except AssertionError:
            print("No entry corresponding to the artist we are searching")

        # Retrieving link to artist page
        artist_url = links[artist_index].find_element_by_xpath('./*').get_attribute('href')
        driver.get(artist_url)
        
        try:
            close_popup = WebDriverWait(driver, 4).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'btn-default'))).click()
        except:
            pass

        # Principal page element that contain panels
        main = driver.find_element_by_class_name('main-content-dates')

        panels = main.find_elements_by_xpath('./*')

        concerts = []

        # Iterating through panels (e.g. concerts)
        for p in panels:
            concert = {}

            concert["artiste"] = self.name.capitalize()

            date_raw = p.find_element_by_class_name('date')
            
            date = re.sub(r'\s', ' ', date_raw.text)
            
            print(date)
            
            # Certain dates are intervals (example : June XX to June xx), in this case we treat them differently
            date_is_interval = re.match(r'^Du\s(\d+)\sau\s(\d+)\s(.{6,})', date)

            if date_is_interval:
                concert["date_debut"] = date_is_interval.group(1) + ' '+  date_is_interval.group(3)
                concert["date_fin"] = date_is_interval.group(2) + ' '+  date_is_interval.group(3)
            else:
                concert["date_debut"] = date
                concert["date_fin"] = date

            spectacle = p.find_element_by_class_name('spectacle')
            concert["spectacle"] = spectacle.text

            # find_elements allows us not to raise an error if there is not festival associated
            festival = p.find_elements_by_class_name('festival-associe')
            if festival:
                concert["festival"] = re.sub('Dans le cadre du festival ', '', festival[0].text)
            else:
                concert["festival"] = None
            
            salle = p.find_element_by_class_name('salle')
            concert["salle"] = salle.text

            lieu = p.find_element_by_class_name('ville-dpt')
            concert["lieu"] = lieu.text

            prix = p.find_element_by_class_name('price')
            concert["prix"] = prix.text
            
            print(prix.text)

            concerts.append(concert)

        ####################
        # TODO : UPDATE DB #
        ####################

        print(f"Scraped {len(concerts)} and added them to DB")

        return concerts


# CHANGE TO PUT THE ARTIST YOU WANT
artist = ""

artiste = Artist(artist, headless=False)
print(artiste, artiste.concerts, sep="\n" )
