import re
from datetime import datetime
from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.errors import ElementNotFound

br = Selenium()


class Robot:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello, my name is {self.name}. Here are the steps I'm about to take:\n")
        print("1. Navigate to the Wikipedia page of each scientist in the provided list.")
        print("2. Retrieve the dates, these scientists were born and died on and calculate their age.")
        print("3. Calculate the age of the scientists.")
        print("4. Retrieve the first paragraph of their respective Wikipedia page.")
        print("5. Display all of this information :)\n")
        print("Let's start...")

    def say_goodbye(self):
        print("\nGoodbye, my name is " + self.name)

    def open_webpage(self, webpage):
        br.open_available_browser(webpage)

    def open_wikipedia_page(self, scientist):
        self.open_webpage(f"https://en.wikipedia.org/wiki/{scientist.replace(' ', '_')}")

    def extract_scientist_information(self):
        name = br.get_text("xpath://h1[@id='firstHeading']")

        try:
            element = br.find_element("xpath://span[@class='bday']")
            birth_date = element.get_attribute('innerHTML')
            reformatted_birth_date = datetime.strptime(birth_date, '%Y-%m-%d').strftime('%d %B %Y')

        except ElementNotFound:
            reformatted_birth_date = "Not Available"

        try:
            death_date = br.get_text("xpath://table[contains(@class, 'infobox')]//th[text("
                                     ")='Died']/following-sibling::td")
            match = re.search("(\d{1,2} \w+ \d{4})", death_date)
            death_date = match.group(0) if match else "Not Available"

        except ElementNotFound:
            death_date = "Not Available"

        intro_element = br.find_element("xpath://div[@id='bodyContent']//p[not(@class)]")
        intro = re.sub(r'\. ', '.\n', intro_element.get_attribute('textContent').replace('\n', ' ').replace('\t', ' ').strip())

        print(f"\nScientist Name: {name}\nBorn: {reformatted_birth_date}\nDied: {death_date}")

        age = self.calculate_age(reformatted_birth_date, death_date)
        if age:
            print(f"Age: {age} years")
        print(f"Introduction: {intro}")

    @staticmethod
    def calculate_age(birth_date, death_date):
        if birth_date != "Not Available" and death_date != "Not Available":
            birth = datetime.strptime(birth_date, "%d %B %Y")
            death = datetime.strptime(death_date, "%d %B %Y")
            age = death.year - birth.year
            if (death.month, death.day) < (birth.month, birth.day):
                age -= 1
            return age
        return "Not Available"

    def close_browser(self):
        br.close_all_browsers()
