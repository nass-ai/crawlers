from .base import BaseCrawler

class NigerianBills(BaseCrawler):
    def __init__(self, path):
        name = "Nigeria"
        self.path = path
        super(NigerianBills, self).__init__(name=name)

    def get_urls(self, clean_url=False):
        pass

    def download_and_save(self):
        if not self.path:
            pass # Save in current path or some other arbitary place.
        pass
    
    def crawl(self):
        self.get_urls()
        self.download_and_save()
