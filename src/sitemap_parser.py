import requests
from lxml import etree
from BdMongo import insert_articles

def fetch(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
        
    response = requests.get(url, headers=headers)
    return response.content

def setup_namespaces(root):
    namespaces = root.nsmap.copy()
    if None in namespaces:
        namespaces["ns"] = namespaces.pop(None)

    return namespaces

def get_source_name(url: str):
    xml_content = fetch(url)
    root = etree.fromstring(xml_content)
    namespaces = setup_namespaces(root)

    origin = root.xpath("//news:publication/news:name/text()", namespaces=namespaces)[0]
    return origin

def parse(origin: str, url: str):
    xml_content = fetch(url)
    root = etree.fromstring(xml_content)
    namespaces = setup_namespaces(root)

    urls = root.xpath("//ns:url", namespaces=namespaces)

    result = []
    
    for url in urls:
        loc = url.xpath("ns:loc/text()", namespaces=namespaces)[0]
        
        news = url.xpath("news:news", namespaces=namespaces)[0]
        
        title = news.xpath("news:title/text()", namespaces=namespaces)[0]
        publication_date = news.xpath("news:publication_date/text()", namespaces=namespaces)[0]

        article = {
            "loc": loc,
            "title": title,
            "origin": origin,
            "publication_date": publication_date
        }

        result.append(article)

    return result

if(__name__ == "__main__"):
    urls = [
        "https://www.lemonde.fr/sitemap_news.xml",
        "https://www.lefigaro.fr/sitemap_news.xml",
        "https://www.lesechos.fr/sitemap_news.xml",
    ]

    for url in urls:
        result = parse("", url)
        insert_articles(result)