import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

jobs = []
page = 1

while True:
    url = f'https://www.google.com/about/careers/applications/jobs/results?page={page}#!t=jo&jid=127025001&'
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')

    table = soup.find('ul', class_="spHGqe")
    if not table:
        break

    listings = table.find_all('li', class_="lLd3Je")
    if not listings:
        break

    for listing in listings:
        title = listing.find('h3', class_="QJPWVe").text.strip()
        details = listing.find('p', class_="l103df").text.strip()
        jobs.append([title, details])

    page += 1

df = pd.DataFrame(jobs, columns=['Title', 'Details'])
file_path = r'C:\Users\EKaralar\OneDrive - CBRE, Inc\Desktop\Job Listings\google_job_data.xlsx'
df.to_excel(file_path, index=False)
