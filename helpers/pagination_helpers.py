

def httpToHttpsReplacement(url):
    url=str(url)
    url=url.replace('http','https')
    return url

def get_url(base_url,page):
    url = httpToHttpsReplacement(base_url) + "?page=" + str(page)
    return url