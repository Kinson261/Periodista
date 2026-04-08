# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator, RelevantContentFilter
import asyncio
import random
from typing import Dict, List

import crawl4ai
import dotenv
import pydantic
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    ProxyConfig,
    RoundRobinProxyStrategy,
)

import agent
from parserURL import parseURLFileUserInput
from proxy import proxiesRotation

env = dotenv.dotenv_values()


class ScraperCrawl4Ai:
    def __init__(self, n_proxy: int = 1, AIAgent: agent.Agent = agent.Agent(local=True, model="Llama3.1:8b", role="user", streaming=False), streaming: bool = False) -> None:
        self.n_proxy: int = n_proxy
        self.proxies: List[ProxyConfig] = []
        self.retrieved_content: Dict[str, str] = dict()  # TODO: transform this into a dictionnary
        self.agent = AIAgent
        self.streaming: bool = streaming

    def __repr__(self) -> str:
        return "ScraperCrawl4Ai()"

    def __str__(self) -> str:
        return f"\nScraperCrawl4Ai() \
                \nn_proxy: {self.n_proxy} \
                \nproxies: {self.proxies}"

    def getProxy(self, n_proxy: int, country_id: List[str]):
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
            filter_chain=crawl4ai.FilterChain([relevance_filter]),
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
            scraping_strategy=scrape_strategy,
        )

        browser_conf = BrowserConfig(
            browser_type="chromium",
            headless=False,
            proxy_config=random.choice(self.proxies),
            verbose=True,
        )

        async with AsyncWebCrawler() as crawler:
            if self.streaming:
                # Stream results as they complete
                async for result in await crawler.arun_many(urls, config=run_conf):
                    if result.success:
                        print(f"[OK] {result.url}, length: {len(result.markdown.raw_markdown)}")
                        self.retrieved_content.update({result.url: result.markdown.raw_markdown})
                    else:
                        print(f"[ERROR] {result.url} => {result.error_message}")
            else:
                # Or get all results at once (default behavior)
                run_conf = run_conf.clone(stream=False)
                results = await crawler.arun_many(urls, config=run_conf)
                for result in results:
                    if result.success:
                        print(f"\n\n\n\n\n\n\n[OK] {result.url}, length: {len(result.markdown.raw_markdown)}")
                        # print(f"content = {res.markdown.fit_markdown}")
                        print(f"content = {result.markdown.raw_markdown}")
                        self.retrieved_content.update({result.url: result.markdown.raw_markdown})
                    else:
                        print(f"[ERROR] {result.url} => {result.error_message}")

    async def crawler_async_function(self, sources: List[str]):
        res = await self.parallel_crawling(sources)

    async def rag(self):
        for key in self.retrieved_content:
            print(f"\n\n\nURL= {key}")
            res = await self.agent.chat(prompt=f"{self.retrieved_content[key]}. {env['PROMPT']}")


if __name__ == "__main__":
    STREAMING = pydantic.TypeAdapter(bool).validate_strings(env["STREAMING"])
    source_file = pydantic.TypeAdapter(str).validate_strings(env["SOURCE_FILE"])
    print(f"source file = {source_file}")

    links: List[str] = parseURLFileUserInput(source_file)
    print(f"Config:\n{env}")
    m_agent = agent.Agent(local=True, model=env["OLLAMA_MODEL"], role="user", streaming=STREAMING)
    scraper = ScraperCrawl4Ai(AIAgent=m_agent, streaming=STREAMING)
    scraper.proxies = [ProxyConfig.from_string(element) for element in scraper.getProxy(n_proxy=int(env["PROXY_NUMBER"]), country_id=env["PROXY_COUNTRY"])]
    asyncio.run(scraper.parallel_crawling(sources=links))
    asyncio.run(scraper.rag())
