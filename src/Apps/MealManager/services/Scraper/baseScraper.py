import logging
import threading

from .scrapeConfig import scrapeConfig


class BaseScraper:
    """Shared start/stop/status/progress lifecycle for the source-specific recipe scrapers.

    Subclasses set `config_key` (their entry in ScrapeConfig.DEFAULTS) and implement `work()`,
    the loop that drives their own `scrape(...)` method - that method's field mappings differ
    too much per source to unify, so it stays with each subclass.
    """
    config_key = None

    def __init__(self):
        self.exception = None
        self.last_error = False
        self.active = False
        self.config = scrapeConfig()
        self.work_thread = self._new_thread()

    def _new_thread(self):
        return threading.Thread(target=self._run, args=(), daemon=True)

    def get_index(self):
        return self.config.get(self.config_key, "index")

    def set_index(self, value):
        self.config.set(self.config_key, "index", value)

    def get_max(self):
        return self.config.get(self.config_key, "max")

    def set_max(self, value):
        self.config.set(self.config_key, "max", value)

    def get_status(self):
        return {
            "max": self.get_max(),
            "index": self.get_index(),
            "running": self.is_running(),
            "exception": self.exception,
        }

    def is_running(self):
        return self.work_thread.is_alive()

    def start(self):
        self.exception = None
        self.active = True
        if self.is_running():
            return
        self.work_thread.start()

    def stop(self):
        if not self.active:
            return
        self.active = False
        self.work_thread.join()
        self.work_thread = self._new_thread()

    def set_progress(self, index):
        self.set_index(index)

    def reset_progress(self):
        self.set_index(0)

    def restart(self):
        self.stop()
        self.reset_progress()
        self.start()

    def _run(self):
        try:
            self.work()
        except Exception as e:
            self.exception = str(e)
            self.active = False
            self.work_thread = self._new_thread()
            raise e

    def work(self):
        raise NotImplementedError

    def handle_scrape_error(self, e, context):
        if not self.last_error:
            logging.warning(f"{context} failed. Skipping... - Error: {e}")
            self.last_error = True
        else:
            logging.error(f"{context} failed second time. Canceling")
        raise e
