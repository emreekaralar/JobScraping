import scrapy
import json
import pandas as pd
import openpyxl

class AmazonJobsSpider(scrapy.Spider):
    name = "amazon_jobs_spider"
    start_urls = ["https://amazon.jobs/en/search.json?radius=24km&facets%5B%5D=normalized_country_code&facets%5B%5D=normalized_state_name&facets%5B%5D=normalized_city_name&facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&facets%5B%5D=schedule_type_id&facets%5B%5D=employee_class&facets%5B%5D=normalized_location&facets%5B%5D=job_function_id&facets%5B%5D=is_manager&facets%5B%5D=is_intern&offset=0&result_limit=10&sort=recent&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&"]

    def __init__(self):
        self.jobs_data = []

    def parse(self, response):
        try:
            data = json.loads(response.text)
            print(json.dumps(data, indent=4))

            jobs = data.get('jobs', [])
            if not jobs:
                self.log("No jobs found in the response.")
            for item in jobs:
                job_info = {
                    'JobId': item.get('id_icims'),
                    'Title': item.get('title'),
                    'PostingDate': item.get('posted_date'),
                    'Company': item.get('company_name'),
                    'Location': item.get('normalized_location')
                }
                self.jobs_data.append(job_info)

            current_offset = response.meta.get('offset', 0)
            self.log(f"Current offset: {current_offset}")

            max_offset = 9990
            if current_offset < max_offset:
                next_offset = current_offset + 10
                next_url = f"https://amazon.jobs/en/search.json?radius=24km&facets%5B%5D=normalized_country_code&facets%5B%5D=normalized_state_name&facets%5B%5D=normalized_city_name&facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&facets%5B%5D=schedule_type_id&facets%5B%5D=employee_class&facets%5B%5D=normalized_location&facets%5B%5D=job_function_id&facets%5B%5D=is_manager&facets%5B%5D=is_intern&offset={next_offset}&result_limit=10&sort=recent&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&"
                self.log(f"Following next page: {next_url}")
                yield scrapy.Request(next_url, callback=self.parse, meta={'offset': next_offset})
            else:
                df = pd.DataFrame(self.jobs_data)
                df.to_excel(r"C:\Users\EKaralar\OneDrive - CBRE, Inc\Desktop\Job Listings\amazon_jobs_data.xlsx", index=False)
                self.log("Job data saved to amazon_jobs_data.xlsx")
        except json.JSONDecodeError as e:
            self.log(f"JSON decode error: {e}")
        except KeyError as e:
            self.log(f"Key error: {e}")
        except Exception as e:
            self.log(f"An error occurred: {e}")
