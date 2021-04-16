import json
import time
from bs4 import BeautifulSoup
import requests
from scraper_api import ScraperAPIClient
import os

def handler(event, context):
    
    client = ScraperAPIClient(os.environ.get('API_KEY'))
    URL = "https://www.indeed.com/jobs?q=Entry+Level+Software+Engineer&l=Remote"
    page = client.get(url = URL)
    print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    results = soup.find(id='resultsCol')
    print(results)
    job_elems = results.find_all('div', class_='jobsearch-SerpJobCard')
    titles = []
    companies = []
    summaries = []
    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('div', class_='sjcl')
        summary_elem = job_elem.find('div', class_='summary')
        titles.append(title_elem.text.strip())
        companies.append(company_elem.text.strip())
        summaries.append(summary_elem.text.strip())

    response ={
        "titles": titles,
        "companies": companies,
        "summaries": summaries
    }
    

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(response)
    }