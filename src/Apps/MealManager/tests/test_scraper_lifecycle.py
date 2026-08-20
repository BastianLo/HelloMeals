import os
import tempfile

from django.test import SimpleTestCase

from Apps.MealManager.services.Scraper import (
    scraper,
    scraperChefKoch,
    scraperEatSmarter,
    scraperKitchenStories,
    scraperLecker,
    scraperMob,
)
from Apps.MealManager.services.Scraper.scrapeConfig import ScrapeConfig

SCRAPER_MODULES = {
    "hellofresh": scraper,
    "kitchenstories": scraperKitchenStories,
    "chefkoch": scraperChefKoch,
    "lecker": scraperLecker,
    "eatsmarter": scraperEatSmarter,
    "mob": scraperMob,
}


class BaseScraperLifecycleTests(SimpleTestCase):
    """Exercises BaseScraper's shared start/stop/status/progress lifecycle through each real
    scraper subclass, using an isolated on-disk config so the tests don't touch the project's
    real data/config/scraper.json. Doubles as the regression test for the Stage 1 bug where
    HelloFresh/KitchenStories progress was silently never persisted (mismatched read/write keys
    in the old hand-written ScrapeConfig)."""

    def _isolated_instance(self, module):
        instance = module.get_scraper().__class__()
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        os.unlink(tmp.name)  # ScrapeConfig must work fine when the file doesn't exist yet
        self.addCleanup(lambda: os.path.exists(tmp.name) and os.unlink(tmp.name))
        instance.config = ScrapeConfig(path=tmp.name)
        return instance

    def test_status_shape_and_defaults(self):
        for name, module in SCRAPER_MODULES.items():
            with self.subTest(scraper=name):
                instance = self._isolated_instance(module)
                status = instance.get_status()
                self.assertEqual(set(status.keys()), {"max", "index", "running", "exception"})
                self.assertFalse(status["running"])
                self.assertIsNone(status["exception"])

    def test_is_running_false_initially(self):
        for name, module in SCRAPER_MODULES.items():
            with self.subTest(scraper=name):
                self.assertFalse(self._isolated_instance(module).is_running())

    def test_set_progress_persists_correctly(self):
        for name, module in SCRAPER_MODULES.items():
            with self.subTest(scraper=name):
                instance = self._isolated_instance(module)
                instance.set_progress(42)
                self.assertEqual(instance.get_status()["index"], 42)
                # confirm it was actually written to disk, not just held in memory
                reloaded = ScrapeConfig(path=instance.config.path)
                self.assertEqual(reloaded.get(instance.config_key, "index"), 42)

    def test_default_reset_progress_resets_index_to_zero(self):
        # KitchenStories and ChefKoch override reset_progress (tested separately below) since
        # pages are 1-indexed / there's extra multi-field state to reset.
        for name, module in SCRAPER_MODULES.items():
            if name in ("kitchenstories", "chefkoch"):
                continue
            with self.subTest(scraper=name):
                instance = self._isolated_instance(module)
                instance.set_progress(10)
                instance.reset_progress()
                self.assertEqual(instance.get_status()["index"], 0)

    def test_kitchenstories_reset_progress_resets_to_one(self):
        instance = self._isolated_instance(scraperKitchenStories)
        instance.set_progress(10)
        instance.reset_progress()
        self.assertEqual(instance.get_status()["index"], 1)

    def test_chefkoch_reset_progress_resets_all_three_fields(self):
        instance = self._isolated_instance(scraperChefKoch)
        instance.set_index(10)
        instance.config.set(instance.config_key, "main_tag_index", 3)
        instance.config.set(instance.config_key, "tag_index", 2)

        instance.reset_progress()

        self.assertEqual(instance.get_index(), 0)
        self.assertEqual(instance.config.get(instance.config_key, "main_tag_index"), 0)
        self.assertEqual(instance.config.get(instance.config_key, "tag_index"), 0)

    def test_start_sets_active_and_stop_clears_it(self):
        instance = self._isolated_instance(scraperMob)
        instance.work = lambda: None  # avoid a real network scrape in the background thread

        instance.start()
        try:
            self.assertTrue(instance.active)
        finally:
            instance.stop()
        self.assertFalse(instance.active)
        self.assertFalse(instance.is_running())
