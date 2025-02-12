import scrapy
import json
import pandas as pd
import openpyxl

class MySpiderSpider(scrapy.Spider):
    name = "my_spider"
    start_urls = ["https://gcsservices.careers.microsoft.com/search/api/v1/search?l=en_us&pg=1&pgSz=20&o=Recent&flt=true"]

    def __init__(self):
        self.jobs_data = []

    def parse(self, response):
        try:
            data = json.loads(response.text)
            print(json.dumps(data, indent=4))

            jobs = data.get('operationResult', {}).get('result', {}).get('jobs', [])
            if not jobs:
                self.log("No jobs found in the response.")
            for item in jobs:
                job_info = {
                    'jobId': item.get('jobId'),
                    'title': item.get('title'),
                    'postingDate': item.get('postingDate')
                }
                self.jobs_data.append(job_info)

            current_page = response.meta.get('page', 1)
            self.log(f"Current page: {current_page}")

            max_pages = 170
            if current_page < max_pages:
                next_page = current_page + 1
                next_url = f"https://gcsservices.careers.microsoft.com/search/api/v1/search?l=en_us&pg={next_page}&pgSz=20&o=Recent&flt=true"
                self.log(f"Following next page: {next_url}")
                yield scrapy.Request(next_url, callback=self.parse, meta={'page': next_page})
            else:
                df = pd.DataFrame(self.jobs_data)
                df.to_excel(r"C:\Users\EKaralar\OneDrive - CBRE, Inc\Desktop\Job Listings\microsoft_jobs_data.xlsx", index=False)
                self.log("Job data saved to jobs_data.xlsx")
        except json.JSONDecodeError as e:
            self.log(f"JSON decode error: {e}")
        except KeyError as e:
            self.log(f"Key error: {e}")
        except Exception as e:
            self.log(f"An error occurred: {e}")

# To run the spider, use the Scrapy command line tool:
# pip install scrapy
# scrapy crawl my_spider
