from watercrawl import WaterCrawlAPIClient
from parserURL import parseURLFileUserInput

def main():
    # client = WaterCrawlAPIClient('your-api-key')
    client = WaterCrawlAPIClient('wc-as699k976rgw0b5syk97czzmher7lnds', base_url='http://100.82.70.109')

    # Simple URL scraping
    #result = client.scrape_url('https://docs.astral.sh/uv/concepts/projects/sync/')
    # print(result)

    sources = parseURLFileUserInput('url.txt')

    for element in sources:
        # Advanced crawling with options
        crawl_request = client.create_crawl_request(
            url=element,
            spider_options={},
            page_options={},
            plugin_options={},
        )

        # Monitor and download results
        for result in client.monitor_crawl_request(crawl_request['uuid'], download=False):
            if result['type'] == 'result':
                print(result['data'])  # it is a result object per page
                print()


if __name__ == "__main__":
    main()
