from typing import List
from fp.fp import FreeProxy
import time

DEBUG = False

def proxiesRotation(number:int, countries: List[str] = ["US"]):
    """
    Scrapes proxies from <https://www.sslproxies.org/>,
    <https://www.us-proxy.org/>, <https://free-proxy-list.net/uk-proxy.html>,
    and <https://free-proxy-list.net> and checks if proxy is working.

    Args:
        number (int): Number of proxy IP to generate

    Returns:
        proxies: A list of working proxies
    """

    proxies = set()
    cnt = 0
    fp = FreeProxy(rand=True, timeout=0.3, country_id=countries)
    while True:
        start_time = time.time()

        proxies.add(fp.get())

        if DEBUG:
            print(f"number of proxies = {number}, countries = {countries}")
            cnt += 1
            if (cnt % 10 == 0):
                print(f"cnt = {cnt}")

            cycle_time = time.time() - start_time
            print(f"cycle_time = {cycle_time} s, proxy = {proxies}")

        if (len(proxies) == number):
            break

    return proxies

if __name__ == "__main__":
    print(proxiesRotation(5))
