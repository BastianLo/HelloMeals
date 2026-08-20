from django.test import SimpleTestCase

from Apps.MealManager.services.Scraper.scraperLecker import extract_servings


class ExtractServingsTests(SimpleTestCase):
    """Regression test for a live-scraping crash: Lecker's recipeYield is free text like
    "4 Personen", not a plain number, and the model's `servings` field is an IntegerField."""

    def test_extracts_leading_number_from_german_text(self):
        self.assertEqual(extract_servings("4 Personen"), 4)

    def test_plain_number_string(self):
        self.assertEqual(extract_servings("12"), 12)

    def test_none_input(self):
        self.assertIsNone(extract_servings(None))

    def test_no_digits(self):
        self.assertIsNone(extract_servings("Personen"))
