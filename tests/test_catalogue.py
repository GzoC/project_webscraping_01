import unittest
from statistics import mean

from src.catalogue import parse_catalogue


def card(price_html):
    return (
        '<article class="product_pod">'
        '<h3><a title="Libro completo">Libro...</a></h3>'
        '<p class="Three star-rating"></p>'
        '<p class="availability instock"> In stock </p>'
        + price_html + '</article>'
    )


class CatalogueTests(unittest.TestCase):
    def test_missing_and_bad_prices_do_not_lower_the_average(self):
        html = "".join(card(p) for p in (
            '<p class="price_color">£12.00</p>',
            '<p class="price_color">£0.00</p>',
            "",
            '<p class="price_color">N/D</p>',
            '<p class="price_color">$4.25</p>',
        ))
        rows = parse_catalogue(html)
        prices = [r["price_gbp"] for r in rows]
        self.assertEqual(prices, [12.0, 0.0, None, None, None])
        self.assertEqual(mean(p for p in prices if p is not None), 6.0)
        self.assertEqual(rows[0]["title"], "Libro completo")
        self.assertEqual(rows[0]["stars"], 3)
        self.assertEqual(rows[0]["availability"], "In stock")

    def test_incomplete_card_remains_visible(self):
        row, = parse_catalogue('<article class="product_pod"><h3></h3><p class="star-rating Other"></p></article>')
        self.assertTrue(all(val is None for val in row.values()))

    def test_unexpected_page_fails_explicitly(self):
        with self.assertRaisesRegex(ValueError, "no contiene fichas"):
            parse_catalogue("<html><h1>Página de error</h1></html>")
