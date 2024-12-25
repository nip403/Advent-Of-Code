from bs4 import BeautifulSoup as BS
import requests
from pathlib import Path

PATH = r"https://adventofcode.com/2024/day/"
parent = Path(__file__).parent

def main():
    for day in range(1, 26):
        (new := (parent / f"Day {day}")).mkdir(parents=True, exist_ok=True)    
        
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
            
        with open(new / "solution.py", "a+") as f:
            if not f.read().strip():
                f.write("\n\ndef main():\n\tpass\n\nif __name__ == \"__main__\":\n\tmain()")
    
if __name__ == "__main__":
    main()
    
