import dotenv
from pydantic import FilePath
import parserURL
import AI

from firecrawl import Firecrawl, AsyncFirecrawl
from firecrawl.types import ScrapeOptions

FIRECRAWL_URL = dotenv.get_key(".env", "FIRECRAWL_URL")
OUTPUT_FILE="results.md"
print(f"FIRECRAWL_URL = {FIRECRAWL_URL}")


def outputScrapeJob(job, outputFile:str):
    with open(outputFile, "+w") as file:
        for doc in job.data:
            file.write(doc.markdown)

def scrape():
    sources = parserURL.parseURLFileUserInput('url2.txt')
    print(f"sources = {sources}")
    firecrawl = Firecrawl(api_url=FIRECRAWL_URL)

    # start = firecrawl.start_batch_scrape(sources, formats=["markdown"], max_age=172800000,
    #  only_main_content=False, parsers=["pdf"], block_ads=True, fast_mode=True)
    job = firecrawl.batch_scrape(sources, formats=[
                                 "markdown"], max_age=172800000, only_main_content=False, poll_interval=2, wait_timeout=30,
                                 parsers=["pdf"])

    # print(job.status, job.completed, job.total)
    # print(job.data)

    # for el in sources:
    #     # docs = firecrawl.crawl(el, max_discovery_depth=2, max_concurrency=2)
    #     docs = firecrawl.scrape(el, fast_mode=True, block_ads=True, only_main_content=True, formats=["markdown"], max_age=172800000)
    #     print(docs)

    outputScrapeJob(job, OUTPUT_FILE)
    # AI.summarize(job)

if __name__ == "__main__":
    scrape()
