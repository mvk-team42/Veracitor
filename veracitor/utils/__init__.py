def httpify(url):
    if url.startswith("http://"):
        return url
    return "http://" + url
