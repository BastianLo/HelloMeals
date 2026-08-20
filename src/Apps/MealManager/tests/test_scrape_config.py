import os
import tempfile

from django.test import SimpleTestCase

from Apps.MealManager.services.Scraper.scrapeConfig import ScrapeConfig


class ScrapeConfigTests(SimpleTestCase):
    def _tmp_path(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        os.unlink(tmp.name)  # ScrapeConfig must work fine when the file doesn't exist yet
        self.addCleanup(lambda: os.path.exists(tmp.name) and os.unlink(tmp.name))
        return tmp.name

    def test_defaults_for_every_scraper(self):
        config = ScrapeConfig(path=self._tmp_path())
        for scraper_key, fields in ScrapeConfig.DEFAULTS.items():
            for field, default in fields.items():
                with self.subTest(scraper=scraper_key, field=field):
                    self.assertEqual(config.get(scraper_key, field), default)

    def test_set_persists_across_instances(self):
        path = self._tmp_path()
        ScrapeConfig(path=path).set("mob", "index", 17)
        reloaded = ScrapeConfig(path=path)
        self.assertEqual(reloaded.get("mob", "index"), 17)

    def test_set_does_not_clobber_other_scrapers_or_fields(self):
        # Regression test for the Stage 1 bug: the old per-field getters/setters used mismatched
        # JSON keys between read and write, so unrelated fields could get silently reset.
        path = self._tmp_path()
        config = ScrapeConfig(path=path)
        config.set("mob", "index", 5)
        config.set("chefkoch", "main_tag_index", 2)

        reloaded = ScrapeConfig(path=path)
        self.assertEqual(reloaded.get("mob", "index"), 5)
        self.assertEqual(reloaded.get("mob", "max"), ScrapeConfig.DEFAULTS["mob"]["max"])
        self.assertEqual(reloaded.get("chefkoch", "main_tag_index"), 2)
        self.assertEqual(reloaded.get("chefkoch", "index"), ScrapeConfig.DEFAULTS["chefkoch"]["index"])
