import asyncio
import dotenv
import parserURL

from firecrawl import Firecrawl, AsyncFirecrawl
from firecrawl.types import ScrapeOptions

FIRECRAWL_URL = dotenv.get_key(".env", "FIRECRAWL_URL")
print(f"FIRECRAWL_URL = {FIRECRAWL_URL}")

async def scrape():
    firecrawl = AsyncFirecrawl(api_url=FIRECRAWL_URL)

    sources = parserURL.parseURLFileUserInput('url.txt')
    job = await firecrawl.batch_scrape(urls=sources, formats=["markdown"], poll_interval=1, timeout=20)
    print(job.status, job.completed, job.total)
    print(job)


if __name__ == "__main__":
    asyncio.run(scrape())
