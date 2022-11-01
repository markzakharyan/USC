import re
import requests
from bs4 import BeautifulSoup

r = requests.get("https://dornsife.usc.edu/cf/phys/phys_faculty_roster.cfm")
html = r.text

soup = BeautifulSoup(html, "html.parser")

# print(soup.prettify())

# regex for anything that contains faculty_display.cfm

facultyHtml = soup.find_all("a", href=re.compile("faculty_display.cfm"))

names = [i.text.lower() for i in facultyHtml if i.text != ""]

print(names)