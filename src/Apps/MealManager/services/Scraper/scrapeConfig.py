import json
import os

from HelloMeals import settings


class ScrapeConfig:
    def __init__(self):
        self.path = str(settings.BASE_DIR) + "/data/config/scraper.json"
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.config_data = json.load(f)
        else:
            self.config_data = {}
        self.hf_start_index = self.config_data["hellofresh"][
            "start_index"] if "hellofresh" in self.config_data and "start_index" in self.config_data[
            "hellofresh"] else 0
        self.hf_max_recipes = self.config_data["hellofresh"][
            "max_recipes"] if "hellofresh" in self.config_data and "max_recipes" in self.config_data[
            "hellofresh"] else 1000000
        self.ks_page = self.config_data["kitchenstories"][
            "page"] if "kitchenstories" in self.config_data and "page" in self.config_data[
            "kitchenstories"] else 1
        self.ks_max_page = self.config_data["kitchenstories"][
            "max_page"] if "kitchenstories" in self.config_data and "max_page" in self.config_data[
            "kitchenstories"] else 1000000
        self.ck_index = self.config_data["chefkoch"][
            "index"] if "chefkoch" in self.config_data and "index" in self.config_data[
            "chefkoch"] else 1
        self.ck_main_tag_index = self.config_data["chefkoch"][
            "main_tag_index"] if "chefkoch" in self.config_data and "main_tag_index" in self.config_data[
            "chefkoch"] else 0
        self.ck_tag_index = self.config_data["chefkoch"][
            "tag_index"] if "chefkoch" in self.config_data and "tag_index" in self.config_data[
            "chefkoch"] else 0
        self.ck_skip = self.config_data["chefkoch"][
            "skip"] if "chefkoch" in self.config_data and "skip" in self.config_data[
            "chefkoch"] else 1000000
        self.lk_index = self.config_data["lecker"][
            "index"] if "lecker" in self.config_data and "index" in self.config_data[
            "lecker"] else 0
        self.lk_max = self.config_data["lecker"][
            "max"] if "lecker" in self.config_data and "max" in self.config_data[
            "lecker"] else 1000000
        self.es_index = self.config_data["eatsmarter"][
            "index"] if "eatsmarter" in self.config_data and "index" in self.config_data[
            "eatsmarter"] else 0
        self.es_max = self.config_data["eatsmarter"][
            "max"] if "eatsmarter" in self.config_data and "max" in self.config_data[
            "eatsmarter"] else 100

    def set_hf_start_index(self, start_index):
        self.hf_start_index = start_index
        self.save_file()

    def set_hf_max_recipes(self, max_recipes):
        self.hf_max_recipes = max_recipes
        self.save_file()

    def set_ck_index(self, index):
        self.ck_index = index
        self.save_file()

    def set_ck_main_tag_index(self, index):
        self.ck_main_tag_index = index
        self.save_file()

    def set_ck_tag_index(self, index):
        self.ck_tag_index = index
        self.save_file()

    def set_ck_skip(self, skip):
        self.ck_skip = skip
        self.save_file()

    def set_ks_page(self, page):
        self.ks_page = page
        self.save_file()

    def set_ks_max_page(self, max_page):
        self.ks_max_page = max_page
        self.save_file()

    def set_lk_index(self, index):
        self.lk_index = index
        self.save_file()

    def set_lk_max(self, max):
        self.lk_max = max
        self.save_file()

    def set_es_index(self, index):
        self.es_index = index
        self.save_file()

    def set_es_max(self, max):
        self.es_max = max
        self.save_file()

    def save_file(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.mkdir(os.path.dirname(self.path))
        with open(self.path, "w") as f:
            json.dump({
                "hellofresh": {
                    "start_index": self.hf_start_index,
                    "max_recipes": self.hf_max_recipes,
                },
                "kitchenstories": {
                    "page": self.ks_page,
                    "max_page": self.ks_max_page,
                },
                "chefkoch": {
                    "index": self.ck_index,
                    "skip": self.ck_skip,
                    "main_tag_index": self.ck_main_tag_index,
                    "tag_index": self.ck_tag_index,
                },
                "lecker": {
                    "index": self.lk_index,
                    "max": self.lk_max,
                },
                "eatsmarter": {
                    "index": self.es_index,
                    "max": self.es_max,
                },
            }, f)


s = ScrapeConfig()


def scrapeConfig():
    global s
    return s
