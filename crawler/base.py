import csv
import pandas


class BaseCrawler(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.urls = None
    
    def __str__(self):
        return f"NASS Data Crawler for {self.name}"

    def clean_urls(self, urls):
        """
        Optional method to clean URLs.
        """
        return urls

    def get_urls(self, clean_url=False):
        """
        Your logic to retrieve URLs should be here.
        """
        self.urls = self.clean_urls(self.urls) if clean_url else self.urls
        raise NotImplementedError('Please, implement a logic to retrieve all urls')

    def download_and_save(self):
        """
        Download your pdfs here.
        """
        raise NotImplementedError("Implement the logic to download bills here.")


class Metadata(object):
    def __init__(self, path=None):
        self.data = None
        self.path = path if path else f"output.csv"
        self.meta_urls = None

    def get_urls(self):
        raise NotImplementedError('Please, implement a logic to retrieve urls and assign the result to meta_urls')

    def grabtable(self):
        """
        Grab table and store values in variable. You can access the urls here with self.meta_urls.
        """
        if type(self.data) == pandas.DataFrame:
            self.data.to_csv(self.path, encoding='utf-8', index=False)
            return True
        else:
            with open(self.path, 'w', newline="") as csv_file:  
                writer = csv.writer(csv_file)
                for key, value in self.data.items():
                    writer.writerow([key, value])
                return True
        raise NotImplementedError("Implement a logic to grab data from table and return the data as dictionary or pandas DataFrame")
