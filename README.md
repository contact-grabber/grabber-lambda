# Grabber Backend:

This is a web scraper that runs off of Serverless Technology from AWS.

## Infrastructure Design

![Screen Shot 2021-04-12 at 7 25 45 AM](https://media.git.generalassemb.ly/user/33394/files/a9086f00-9b60-11eb-8dcf-2d4b0bac792c)

Inside of AWS Amplify, we built and API Gateway that leads to the route [https://fpsazf1gfi.execute-api.us-west-2.amazonaws.com/staging/items](https://fpsazf1gfi.execute-api.us-west-2.amazonaws.com/staging/items)
This route works with GET PUT and POST requests.
When this route is executed, it will trigger a Lambda function which contains our scraper located in index.py:
![Screen Shot 2021-04-12 at 7 36 25 AM](https://media.git.generalassemb.ly/user/33394/files/e3bed700-9b61-11eb-869a-cfb0a89bbfef)

## Web Scraping:

We built a web scraper for a static page on a job search website using the BeautifulSoup Python framework and the Requests module. The Requests module allowed us to send a get request to the web page URL, which the response is then passed to Beautiful Soup to parse and send back to us in a legible format. We used the basic html parser built into Python, and our scraper simply returns any of the title data that is used on the page and is returned in a JSON format.

## Technologies Used:

- AWS Amplify
- AWS Lambda
- AWS API Gateway
- Python
- BeautifulSoup library
- Requests module

## What Went Wrong?

Everythin. In all seriousness we got everything to work from the Lambda function to the web scraper. We found that when the scraper is used in the Lambda function, there is intermittent loss in functionality. When the URL is called, we think the issue is the parser is not able to parse the function before the Lambda function finished it's operation. Causing a "cannot find_all from NONE Type". We also learned about the limitations of BeautifulSoup and not being able to parse dynamic JavaScript created page contents.

## Try For Your Self!

Here is some code to test scraping youself in the terminal!

```
from bs4 import BeautifulSoup
import requests
entry_lvl_url = "https://www.indeed.com/q-Entry-Level-Software-Engineer-l-Remote-jobs.html?vjk=5f913bcfecb065a5"
page = requests.get(entry_lvl_url)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='resultsBodyContent')
job_deets = results.find_all('div', class_='jobsearch-SerpJobCard')
for job_deets in job_deets:
    title = job_deets.find('h2', class_='title')
    company = job_deets.find('div', class_='sjcl')
    summary = job_deets.find('div', class_='summary')
    print(title.text.strip())
    print(company.text.strip())
    print(summary.text.strip())
    print()
jr_lvl_url = "https://www.indeed.com/jobs?q=JrSoftware%20Engineer&l=Remote&vjk=737e4eb14613515c"
page = requests.get(jr_lvl_url)
soupy = BeautifulSoup(page.content, 'html.parser')
results = soupy.find(id='resultsBodyContent')
gig_deets = results.find_all('div', class_='jobsearch-SerpJobCard')
for gig_deets in gig_deets:
    title = gig_deets.find('h2', class_='title')
    company = gig_deets.find('div', class_='sjcl')
    summary = gig_deets.find('div', class_='summary')
    print(title.text.strip())
    print(company.text.strip())
    print(summary.text.strip())
    print()

```

Make sure to download bs4

```
pipenv install bs4
```

As well as requests

```
pipenv install requests
```

Here is the deployed version to try as well:

```
import json
import time
from bs4 import BeautifulSoup
import requests


def handler(event, context):

    URL = "https://www.indeed.com/jobs?q=Entry+Level+Software+Engineer&l=Remote"
    page = requests.get(URL)
    time.sleep(5)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='resultsCol')
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
```

Now You can see the output in your terminal!

```
python3 index.py
```

## Next Steps / Goals

- Working functionality on Lambda
- Using Selenium for dynamic data scraping
- Adding a frontend for better display and requesting
