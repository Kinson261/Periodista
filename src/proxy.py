from fp.fp import FreeProxy


def proxiesRotation(number:int):
    """
    Scrapes proxies from <https://www.sslproxies.org/>,
    <https://www.us-proxy.org/>, <https://free-proxy-list.net/uk-proxy.html>,
    and <https://free-proxy-list.net> and checks if proxy is working.

    Args:
        number (int): Number of proxy IP to generate

    Returns:
        proxies: A list of working proxies
    """
    proxies: list = []
    for i in range(number):
        proxies.append(FreeProxy().get())

    return proxies

if __name__ == "__main__":
    print(proxiesRotation(5))
