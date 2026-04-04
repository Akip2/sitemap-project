import requests
from lxml import etree

def fetch(url: str):
    response = requests.get(url)
    return response.content

def setup_namespaces(root):
    namespaces = root.nsmap.copy()
    if None in namespaces:
        namespaces["ns"] = namespaces.pop(None)

    return namespaces

def parse(url: str):
    xml_content = fetch(url)
    root = etree.fromstring(xml_content)
    namespaces = setup_namespaces(root)

    urls = root.xpath("//ns:url", namespaces=namespaces)

    result = []
    
    for url in urls:
        loc = url.xpath("ns:loc/text()", namespaces=namespaces)[0]
        
        news = url.xpath("news:news", namespaces=namespaces)[0]
        
        title = news.xpath("news:title/text()", namespaces=namespaces)[0]
        keywords = news.xpath("news:keywords/text()", namespaces=namespaces)[0]
        publication_date = news.xpath("news:publication_date/text()", namespaces=namespaces)[0]

        article = {
            loc: loc,
            title: title,
            keywords: keywords.split(", "),
            publication_date: publication_date
        }        

        result.append(article)

    return result

print(parse("https://www.lefigaro.fr/sitemap_news.xml"))