from bs4 import BeautifulSoup

def get_images(html):
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img')
    res = []
    for image in images:
        res.append(image['src'])
    return res