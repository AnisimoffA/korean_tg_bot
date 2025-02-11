from urllib.parse import urlparse, parse_qs
import re


def get_id_from_url(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    carid = params.get("carid", [None])[0]

    if carid is None:
        match = re.search(r"/cars/detail/(\d{8})", parsed_url.path)
        if match:
            carid = match.group(1)
    return carid
