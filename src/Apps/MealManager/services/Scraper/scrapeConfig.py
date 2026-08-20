import json
import os

from HelloMeals import settings


class ScrapeConfig:
    """Persists per-scraper progress (`index`/`max` and a few source-specific extra fields)
    to a single JSON file, keyed by scraper name. Replaces one hand-written attribute+setter
    pair per field with a generic get/set so every scraper reads and writes through the same
    path - the previous per-field getters and setters used mismatched JSON keys, so a saved
    HelloFresh/KitchenStories progress was silently never read back."""

    DEFAULTS = {
        "hellofresh": {"index": 0, "max": 1000000},
        "kitchenstories": {"index": 1, "max": 1000000},
        "chefkoch": {"index": 1, "max": 1000000, "main_tag_index": 0, "tag_index": 0},
        "lecker": {"index": 0, "max": 1000000},
        "eatsmarter": {"index": 0, "max": 100},
        "mob": {"index": 0, "max": 1000000},
    }

    def __init__(self, path=None):
        self.path = path or (str(settings.BASE_DIR) + "/data/config/scraper.json")
        stored = {}
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                stored = json.load(f)
        self.data = {
            scraper: {**fields, **stored.get(scraper, {})}
            for scraper, fields in self.DEFAULTS.items()
        }

    def get(self, scraper, field):
        return self.data[scraper][field]

    def set(self, scraper, field, value):
        self.data[scraper][field] = value
        self.save_file()

    def save_file(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.mkdir(os.path.dirname(self.path))
        with open(self.path, "w") as f:
            json.dump(self.data, f)


s = ScrapeConfig()


def scrapeConfig():
    global s
    return s
