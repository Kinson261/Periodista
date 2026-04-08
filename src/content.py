class content:
    g_id = 0

    def __init__(self, url: str, found: bool, summary: str, fetched_url: list[str]) -> None:
        self.id = content.g_id
        self.url = url
        self.found = found
        self.summary = summary
        self.fetched_url = fetched_url
        content.g_id += 1

    # Getters
    def getId(self):
        return self.g_id

    def getURL(self):
        return self.url

    def getFound(self):
        return self.found

    def getSummary(self):
        return self.summary

    def getFetchedURL(self):
        return self.fetched_url

    """ TODO:
    Not sure if `setters` are needed since it shouldn't be interacted with the user, only
    fetch pages
    """

    # Setters
    def setURL(self, url):
        self.url = url

    def addFetchedURL(self, url):
        self.fetched_url.append(url)
