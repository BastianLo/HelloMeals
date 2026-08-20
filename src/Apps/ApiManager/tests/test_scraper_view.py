import os
import tempfile

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from Apps.ApiManager.views import scraperView
from Apps.MealManager.services.Scraper.scrapeConfig import ScrapeConfig

from .utils import authenticated_client, create_admin, create_user

EXPECTED_SOURCES = {"hellofresh", "kitchenstories", "chefkoch", "lecker", "eatsmarter", "mob"}
EXPECTED_DISPLAY_NAMES = {"HelloFresh", "KitchenStories", "Chefkoch", "Lecker", "EatSmarter", "Mob"}


class ScraperRegistryTests(TestCase):
    def test_registry_keys_match_expected_sources(self):
        self.assertEqual(set(scraperView.SCRAPERS.keys()), EXPECTED_SOURCES)


class ScraperEndpointTests(TestCase):
    """Exercises the generic scraper views/urls end-to-end. Swaps every registered scraper's
    `.config` for an isolated, temp-file-backed one for the duration of the test so hitting the
    real HTTP endpoints doesn't write to the project's real data/config/scraper.json."""

    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        os.unlink(tmp.name)  # ScrapeConfig must work fine when the file doesn't exist yet
        self.addCleanup(lambda: os.path.exists(tmp.name) and os.unlink(tmp.name))
        test_config = ScrapeConfig(path=tmp.name)

        self._original_configs = {}
        for source, module in scraperView.SCRAPERS.items():
            instance = module.get_scraper()
            self._original_configs[source] = instance.config
            instance.config = test_config
        self.addCleanup(self._restore_configs)

        self.admin = create_admin()
        self.client_ = authenticated_client(self.admin)

    def _restore_configs(self):
        for source, module in scraperView.SCRAPERS.items():
            module.get_scraper().config = self._original_configs[source]

    def test_get_all_status_uses_expected_display_names(self):
        response = self.client_.get("/api/Scraper/status")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.json().keys()), EXPECTED_DISPLAY_NAMES)

    def test_status_roundtrip_for_every_source(self):
        for source in EXPECTED_SOURCES:
            with self.subTest(source=source):
                response = self.client_.get(f"/api/Scraper/{source}/status")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(set(response.json().keys()), {"max", "index", "running", "exception"})

    def test_unknown_source_returns_404(self):
        response = self.client_.get("/api/Scraper/doesnotexist/status")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_setprogress_roundtrip(self):
        response = self.client_.post("/api/Scraper/mob/setprogress/7")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["index"], 7)

    def test_anonymous_is_rejected(self):
        response = APIClient().get("/api/Scraper/status")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_non_admin_is_rejected(self):
        client = authenticated_client(create_user("regular"))
        response = client.get("/api/Scraper/status")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
