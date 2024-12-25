from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import requests
from pathlib import Path
import os

PATH = r"https://adventofcode.com/2024/day/"
parent = Path(__file__).parent

with open(parent / "template.txt") as f:
    template = f.read()

def main():
    # Login
    chromedriver_autoinstaller.install() 
    driver = webdriver.Firefox()
    driver.get("https://adventofcode.com/2024/auth/github")
    input("Press RETURN after logging in.")
    
    # Create directories for each day
    for day in range(1, 26):
        (new := (parent / f"Day {day}")).mkdir(parents=True, exist_ok=True)    
        
        # Question page html
        with open(new / "question.html", "w+", encoding="utf-8") as f:
            try:
                f.write(
                    BS(
                        requests.get(PATH + str(day)).text, 
                        "html.parser"
                    ).find("article", class_="day-desc").prettify()
                )
            
            except Exception as e:
                print(f"Failed to generate Day {day}: {e}")
            
        # Python file 
        if not os.path.exists(new / "solution.py"):
            with open(new / "solution.py", "w+") as f:
                f.write(template)
        
        # Puzzle input
        with open(new / "input_data.txt", "w+") as f:
            driver.get(PATH + f"{day}/input")
            f.write(driver.find_element(By.TAG_NAME, "pre").text)
            
if __name__ == "__main__":
    main()
    
