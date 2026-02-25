from botasaurus.browser import browser, Driver
from botasaurus import calc_max_parallel_browsers
from parserURL import parseURLFileUserInput
from proxy import proxiesRotation

fileInput = 'url2.txt'
LINKS= parseURLFileUserInput(fileInput)
proxies = proxiesRotation(5)

@browser(data=LINKS, parallel=3, reuse_driver=True, cache=True, block_images=True, proxy=proxies[0] )
def scrape_heading_task(driver: Driver, data):
    driver.get(link=data, bypass_cloudflare=True)

    # Retrieve the heading element's text
    # heading1 = driver.get_text("h1")
    # heading2 = driver.get_text("h2")
    # heading3 = driver.get_text("h3")
    links = driver.get_all_links()
    detected = driver.get_bot_detected_by()
    # print(f"heading = {heading1}")
    print(f"detected = {detected}")

    # Save the data as a JSON file in output/scrape_heading_task.json
    # output_filename =
    return {
        # "heading1": heading1,
        # "heading2": heading2,
        # "heading3": heading3,
        "links": links,
        "detected": detected,
    }

if __name__ == "__main__":
    # Initiate the web scraping task of each link
    scrape_heading_task()  # pyright: ignore[reportCallIssue]
