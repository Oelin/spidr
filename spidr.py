from requests import session
from re import findall
from urllib.parse import urlparse as parse


urlre = 'src|href=["\']([a-zA-Z0-9\./\-%\?=:]+)["\']'


def urls(page, path):
  found = set(findall(urlre, page)) - {''}

  for url in found:
    yield (parse(url).netloc and url) or f'https://{path}/{url}'


def crawl(url):
  s = session()
  children = [url]
  visited = set()

  while children:
    current = children.pop(0)
    visited.add(current)

    path = parse(url).path

    try:
      page = s.get(current).text

    except:
      continue

    if len(children) < 32:
      children += list(set(urls(page, path)) - visited)

    yield current
