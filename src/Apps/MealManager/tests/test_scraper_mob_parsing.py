from django.test import SimpleTestCase

from Apps.MealManager.services.Scraper.scraperMob import (
    extract_image,
    extract_name,
    extract_number,
    flatten_instructions,
    parse_amount,
    parse_ingredient,
)


class ParseAmountTests(SimpleTestCase):
    def test_integer(self):
        self.assertEqual(parse_amount("100"), 100.0)

    def test_decimal_with_comma(self):
        self.assertEqual(parse_amount("1,5"), 1.5)

    def test_decimal_leading_dot(self):
        self.assertEqual(parse_amount(".5"), 0.5)

    def test_fraction(self):
        self.assertEqual(parse_amount("1/2"), 0.5)

    def test_invalid_returns_none(self):
        self.assertIsNone(parse_amount("abc"))


class ParseIngredientTests(SimpleTestCase):
    """Mob concatenates the unit directly onto the amount with no space ("160g Tahini"), while
    amounts with no unit are followed by a space straight into the name ("6 Garlic Clove")."""

    def test_unit_concatenated_to_amount(self):
        self.assertEqual(parse_ingredient("160g Dried Soy Mince"), (160.0, "g", "Dried Soy Mince"))

    def test_tbsp_unit(self):
        self.assertEqual(parse_ingredient("2tbsp Gochujang"), (2.0, "tbsp", "Gochujang"))

    def test_no_unit_when_space_follows_amount(self):
        # Regression test: "Garlic" used to be misread as the unit and "Clove" as the name.
        self.assertEqual(parse_ingredient("6 Garlic Clove"), (6.0, None, "Garlic Clove"))

    def test_no_unit_single_word_item(self):
        self.assertEqual(parse_ingredient("1 Egg"), (1.0, None, "Egg"))

    def test_leading_dot_amount_no_unit(self):
        self.assertEqual(parse_ingredient(".5 Courgette"), (0.5, None, "Courgette"))

    def test_no_amount_at_all(self):
        self.assertEqual(parse_ingredient("Salt"), (None, None, "Salt"))

    def test_decimal_amount_with_unit(self):
        self.assertEqual(parse_ingredient("1.5tbsp American Mustard"), (1.5, "tbsp", "American Mustard"))


class ExtractNumberTests(SimpleTestCase):
    def test_plain_int(self):
        self.assertEqual(extract_number(12), 12)

    def test_string_with_unit_suffix(self):
        self.assertEqual(extract_number("312 calories"), 312)

    def test_none_input(self):
        self.assertIsNone(extract_number(None))

    def test_no_digits(self):
        self.assertIsNone(extract_number("n/a"))


class ExtractImageTests(SimpleTestCase):
    def test_plain_string(self):
        self.assertEqual(extract_image("https://x/img.jpg"), "https://x/img.jpg")

    def test_list_of_strings(self):
        self.assertEqual(extract_image(["https://x/img.jpg", "https://x/other.jpg"]), "https://x/img.jpg")

    def test_dict_with_url(self):
        self.assertEqual(extract_image({"url": "https://x/img.jpg"}), "https://x/img.jpg")

    def test_none(self):
        self.assertIsNone(extract_image(None))


class ExtractNameTests(SimpleTestCase):
    def test_dict_with_name(self):
        self.assertEqual(extract_name({"name": "Mob"}), "Mob")

    def test_plain_string(self):
        self.assertEqual(extract_name("Mob"), "Mob")

    def test_none(self):
        self.assertIsNone(extract_name(None))


class FlattenInstructionsTests(SimpleTestCase):
    def test_flat_howto_steps(self):
        instructions = [
            {"@type": "HowToStep", "text": "Do this."},
            {"@type": "HowToStep", "text": "Then that."},
        ]
        self.assertEqual(flatten_instructions(instructions), ["Do this.", "Then that."])

    def test_nested_howto_sections(self):
        instructions = [
            {"@type": "HowToSection", "itemListElement": [{"@type": "HowToStep", "text": "Step A"}]}
        ]
        self.assertEqual(flatten_instructions(instructions), ["Step A"])

    def test_plain_string_split_on_newlines(self):
        self.assertEqual(flatten_instructions("Step 1\nStep 2"), ["Step 1", "Step 2"])

    def test_none(self):
        self.assertEqual(flatten_instructions(None), [])
