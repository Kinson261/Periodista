# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator, RelevantContentFilter
import random
import crawl4ai
import asyncio
import dotenv
from typing import Any, List

from crawl4ai import (
    AsyncWebCrawler,
    BrowserAdapter,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    CrawlStrategy,
    DeepCrawlStrategy,
    ExtractionStrategy,
    ProxyConfig,
    RoundRobinProxyStrategy,
)

from parserURL import parseURLFileUserInput
from proxy import proxiesRotation

"""
async def quick_parallel_example() -> None:
    urls = SOURCES

    relevance_filter = crawl4ai.ContentRelevanceFilter(
        query="Web crawling and data extraction with Python",
        threshold=0.7,  # Minimum similarity score (0.0 to 1.0)
    )

    md_generator = crawl4ai.DefaultMarkdownGenerator(
        content_filter=crawl4ai.PruningContentFilter(
            threshold=0.4,
            threshold_type="fixed",
        ),
    )

    crawl_strategy = crawl4ai.BFSDeepCrawlStrategy(
        max_depth=2,
        filter_chain= crawl4ai.FilterChain([relevance_filter]),
        include_external=False,
        )

    scrape_strategy = crawl4ai.LXMLWebScrapingStrategy()


    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        stream=True,  # Enable streaming mode
        only_text=True,
        exclude_all_images=True,
        exclude_external_links=True,
        exclude_social_media_links=True,
        proxy_rotation_strategy=RoundRobinProxyStrategy(proxies),
        check_cache_freshness=True,
        remove_overlay_elements=True,
        process_iframes=True,
        markdown_generator=md_generator,
        # deep_crawl_strategy=crawl_strategy,
        scraping_strategy= scrape_strategy,
    )

    browser_conf = BrowserConfig(
        browser_type="chromium",
        headless=False,
        proxy_config=proxies[0],
        verbose=True,
    )

    async with AsyncWebCrawler() as crawler:
        # Stream results as they complete
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"[OK] {result.url}, length: {len(result.markdown.raw_markdown)}")
            else:
                print(f"[ERROR] {result.url} => {result.error_message}")

        # Or get all results at once (default behavior)
        run_conf = run_conf.clone(stream=False)
        results = await crawler.arun_many(urls, config=run_conf)
        for res in results:
            if res.success:
                print(f"[OK] {res.url}, length: {len(res.markdown.raw_markdown)}")
                # print(f"content = {res.markdown.fit_markdown}")
                print(f"content = {res.markdown.raw_markdown}")
            else:
                print(f"[ERROR] {res.url} => {res.error_message}")
"""

class ScraperCrawl4Ai:
    def __init__(self, n_proxy:int = 1) -> None:
        self.n_proxy: int = n_proxy
        self.proxies: List[ProxyConfig] = []

    def __repr__(self) -> str:
        return f"ScraperCrawl4Ai()"

    def __str__(self) -> str:
        return f"\nScraperCrawl4Ai() \
                \nn_proxy: {self.n_proxy} \
                \nproxies: {self.proxies}"

    def getProxy(self, n_proxy:int ,country_id:List[str]):
        # self.proxies = proxiesRotation(number=self.n_proxy)
        return proxiesRotation(number=n_proxy, countries=country_id)


    async def parallel_crawling(self, sources) -> None:
        urls = sources

        relevance_filter = crawl4ai.ContentRelevanceFilter(
            query="Web crawling and data extraction with Python",
            threshold=0.7,  # Minimum similarity score (0.0 to 1.0)
        )

        md_generator = crawl4ai.DefaultMarkdownGenerator(
            content_filter=crawl4ai.PruningContentFilter(
                threshold=0.4,
                threshold_type="fixed",
            ),
        )

        crawl_strategy = crawl4ai.BFSDeepCrawlStrategy(
            max_depth=2,
            filter_chain= crawl4ai.FilterChain([relevance_filter]),
            include_external=False,
            )

        scrape_strategy = crawl4ai.LXMLWebScrapingStrategy()


        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            stream=True,  # Enable streaming mode
            only_text=True,
            exclude_all_images=True,
            exclude_external_links=True,
            exclude_social_media_links=True,
            proxy_rotation_strategy=RoundRobinProxyStrategy(self.proxies),
            check_cache_freshness=True,
            remove_overlay_elements=True,
            process_iframes=True,
            markdown_generator=md_generator,
            # deep_crawl_strategy=crawl_strategy,
            scraping_strategy= scrape_strategy,
        )

        browser_conf = BrowserConfig(
            browser_type="chromium",
            headless=False,
            proxy_config=random.choice(self.proxies),
            verbose=True,
        )

        async with AsyncWebCrawler() as crawler:
            # Stream results as they complete
            async for result in await crawler.arun_many(urls, config=run_conf):
                if result.success:
                    print(f"[OK] {result.url}, length: {len(result.markdown.raw_markdown)}")
                else:
                    print(f"[ERROR] {result.url} => {result.error_message}")

            # Or get all results at once (default behavior)
            run_conf = run_conf.clone(stream=False)
            results = await crawler.arun_many(urls, config=run_conf)
            for res in results:
                if res.success:
                    print(f"[OK] {res.url}, length: {len(res.markdown.raw_markdown)}")
                    # print(f"content = {res.markdown.fit_markdown}")
                    print(f"content = {res.markdown.raw_markdown}")
                else:
                    print(f"[ERROR] {res.url} => {res.error_message}")


async def crawler_async_function(scraper: ScraperCrawl4Ai, sources:List[str]):
    res = await scraper.parallel_crawling(sources)


if __name__ == "__main__":
    config = dotenv.dotenv_values()
    source_file = config["SOURCE_FILE"]
    links: List[str] = parseURLFileUserInput(source_file)
    print(f"Config:\n{config}")
    scraper = ScraperCrawl4Ai()
    scraper.proxies = [ProxyConfig.from_string(element) for element in scraper.getProxy(n_proxy=int(config["PROXY_NUMBER"]),
                                                                                                  country_id=config["PROXY_COUNTRY"])]
    asyncio.run(crawler_async_function(scraper, links))
