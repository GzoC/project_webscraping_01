"""Lectura de las fichas de una sola página de Books to Scrape."""

import re

from bs4 import BeautifulSoup

STARS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_price(text):
    """Aceptar un precio en GBP con dos decimales. Un dato inválido queda ausente."""
    match = re.fullmatch(r"£\s*([0-9]+\.[0-9]{2})", text.strip())
    return float(match.group(1)) if match else None


def parse_catalogue(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("article.product_pod")
    if not cards:
        raise ValueError("La página no contiene fichas article.product_pod")

    books = []
    for card in cards:
        link = card.select_one("h3 a[title]")
        price = card.select_one(".price_color")
        stock = card.select_one(".availability")
        rating = card.select_one(".star-rating")
        classes = rating.get("class", []) if rating else []
        books.append({
            "title": (link["title"].strip() or None) if link else None,
            "price_gbp": parse_price(price.get_text(strip=True)) if price else None,
            "availability": (stock.get_text(" ", strip=True) or None) if stock else None,
            "stars": next((STARS[name] for name in classes if name in STARS), None),
        })
    return books
