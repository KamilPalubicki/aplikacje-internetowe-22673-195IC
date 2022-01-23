from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from bs4 import BeautifulSoup
from lxml import html
import requests
import re


def home(request):
    page = requests.get("https://deadbydaylight.fandom.com/pl/wiki/Michael_Myers")
    soup = BeautifulSoup(page.content, "html.parser")
    all_p_tags = []
    for element in soup.select("p"):
        all_p_tags.append(element.text)
    all_p_tagslen = len(all_p_tags)
    seventh_p_text = soup.select("p")[7].text
    page = requests.get("https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/")
    soup = BeautifulSoup(page.content, "html.parser")
    top_items = []
    products = soup.select("div.thumbnail")
    for elem in products:
        title = elem.select("h4 > a.title")[0].text
        review_label = elem.select("div.ratings")[0].text
        info = {"title": title.strip(), "review": review_label.strip()}
        top_items.append(info)

    image_data = []
    images = soup.select("img")
    for image in images:
        src = image.get("src")
        alt = image.get("alt")
        image_data.append({"src": src, "alt": alt})
    all_products = []

    products = soup.select('div.thumbnail')
    for product in products:
        name = product.select('h4 > a')[0].text.strip()
        description = product.select('p.description')[0].text.strip()
        price = product.select('h4.price')[0].text.strip()
        reviews = product.select('div.ratings')[0].text.strip()
        image = product.select('img')[0].get('src')

        all_products.append({
            "name": name,
            "description": description,
            "price": price,
            "reviews": reviews,
            "image": image
        })
    return render(request, 'home.html', {'top_items': top_items, 'all_p_tagslen': all_p_tagslen,
                                         'seventh_p_text': seventh_p_text, 'image_data': image_data,
                                         'all_products': all_products})


def scraping(request):
    if request.method == "POST":
        allElements = []
        web_link = request.POST.get('web_link', None)
        element = request.POST.get('element', None)
        url = web_link
        source = requests.get(url).text
        soup = BeautifulSoup(source, "html.parser")
        items = soup.find_all(element)
        amount = len(items)

        for i in items:
            # Szukanie klasy
            findClass = i.get('class')
            if findClass is None:
                findClass = "Brak"

                # Szukanie id
            findId = i.get('id')
            findId = findId.strip() if findId is not None else "Brak"

            # Szukanie article
            findArticle = i.get('article')
            findArticle = findArticle.strip() if findArticle is not None else "Brak"

            # Szukanie atrybutu
            find_alt = i.get('alt')
            find_alt = find_alt.strip() if find_alt is not None else "Brak"

            # Szukanie tekstu
            getText = i.text
            getText = getText.strip() if getText is not None else "Brak"

            # Szukanie spanów
            findSpan = i.get('span')
            findSpan = findSpan.strip() if findSpan is not None else "Brak"

            # Szukanie linków
            findHref = i.get('href')
            findHref = findHref.strip() if findHref is not None else "Brak"

            allElements.append(
                {"findId": findId, "findClass": findClass, "find_alt": find_alt, "findArticle": findArticle,
                 "getText": getText, 'findHref': findHref, 'findSpan': findSpan})
        return render(request, 'scrap.html',
                      {'allElements': allElements, 'amount': amount, 'web_link': web_link, 'element': element})
    return render(request, 'scrap.html')


def xml(request):
    # xPath
    url = 'https://www.mediaexpert.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy/apple'
    path_name = '/html/body/div[1]/div[3]/div[3]/div/div[1]/div[2]/div[3]/div[2]/div/span[1]/div/div[1]/div[1]/div[2]/h2/a'
    path_price = '/html/body/div[1]/div[3]/div[3]/div/div[1]/div[2]/div[3]/div[2]/div/span[1]/div/div[2]/div/div[1]/div[1]/div/div'
    response = requests.get(url)
    source = html.fromstring(response.content)
    price_name = source.xpath(path_name)
    price_tree = source.xpath(path_price)
    lxmlPrzyklad3 = price_name[0].text_content()
    lxmlPrzyklad4 = price_tree[0].text_content()

    # klasy
    url = 'https://pogoda.interia.pl/prognoza-szczegolowa-gdansk,cId,8048'
    path_city = '//*[@class="weather-currently-city"]'
    path_temp = '//*[@class="weather-currently-temp-strict"]'
    response = requests.get(url)
    source = html.fromstring(response.content)
    tree_city = source.xpath(path_city)
    tree_temp = source.xpath(path_temp)
    lxmlPrzyklad1 = tree_city[0].text_content()
    lxmlPrzyklad2 = tree_temp[0].text_content()

    return render(request, 'xpath.html', {'lxml1': lxmlPrzyklad1, 'lxml2': lxmlPrzyklad2, 'lxml3': lxmlPrzyklad3, 'lxml4': lxmlPrzyklad4})
