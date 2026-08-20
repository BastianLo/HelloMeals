from django.test import SimpleTestCase

from Apps.MealManager.services.recipe_share import make_share_token, resolve_share_token


class ShareTokenTests(SimpleTestCase):
    def test_roundtrip(self):
        token = make_share_token("r1")
        self.assertEqual(resolve_share_token(token), "r1")

    def test_tampered_token_rejected(self):
        token = make_share_token("r1")
        tampered = token[:-1] + ("a" if token[-1] != "a" else "b")
        self.assertIsNone(resolve_share_token(tampered))

    def test_garbage_token_rejected(self):
        self.assertIsNone(resolve_share_token("not-a-real-token"))

    def test_token_for_one_recipe_does_not_resolve_to_another(self):
        token = make_share_token("r1")
        self.assertNotEqual(resolve_share_token(token), "r2")
