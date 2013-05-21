import requests
import re
import os
import tempfile
import Image
from subprocess import Popen


def get_prices(station_code):
    """
    station_code is the identifier that you can find in the URL of your local
    gas station, e.g.
    https://www.jet-tankstellen.de/kraftstoff/filialfinder/XJ00690
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31',
    }

    request = requests.get('https://www.jet-tankstellen.de/kraftstoff/filialfinder/%s' % station_code,
        headers=headers)
    cookies = request.cookies
    html_content = request.text

    link_finder = re.compile('marker/\?a=(?P<hex1>[0-9a-fA-F]+)&b=(?P<hex2>[0-9a-fA-F]+)')
    findings = link_finder.findall(html_content)

    a = findings[0][0]
    b = findings[0][1]

    tmp_img = tempfile.NamedTemporaryFile(delete=False)
    image_request = requests.get('https://www.jet-tankstellen.de/marker/?a=%s&b=%s' % (a, b),
        headers=headers, cookies=cookies)
    tmp_img.write(image_request.content)
    tmp_img.close()
    filename = tmp_img.name
    placeholder_name = '%s%s.tiff'

    coordinates = {
        'diesel': (12, 63, 52, 88),
        'e10': (12, 99, 52, 124),
        'super': (12, 135, 52, 160),
        'superplus': (12, 172, 52, 195),
    }

    im = Image.open(filename)

    prices = {}

    for kind in coordinates:
        tmp = im.crop(coordinates[kind])
        kindname = placeholder_name % (filename, kind)
        tmp.save(kindname)

        fh = open('NUL', 'w')
        Popen(['tesseract', kindname, kindname], stdout=fh, stderr=fh).wait()
        fh.close()
        reader = open('%s.txt' % kindname, 'r')

        prices[kind] = reader.read().strip()

        reader.close()

        os.unlink(kindname)
        os.unlink('%s.txt' % kindname)

    os.unlink(filename)

    return prices
