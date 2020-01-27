import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup

from .base import Metadata
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


class KenyanBills(BaseCrawler):
    def __init__(self, path):
        name = "Kenyan"
        self.path = path
        self.site = "http://kenyalaw.org/kl/"
        self.ids = [9091, 7938, 6819, 5991, 5189, 4250, 4251, 525, 523, 522, 521, 520, 519]
        super(KenyanBills, self).__init__(name=name)

    def get_urls(self, clean_url=True):
        links = {}
        for id in self.ids:
            url = '{}index.php?id={}'.format(self.site, id)
            page = requests.get(url)
            page_dtl = BeautifulSoup(page.content, "html.parser")
            div = page_dtl.find('div' , {'id': 'inner-section'})
            table = div.find_next('table', 'contenttable')
            links = dict([(i.get_text(), self.site + i.get('href')) for i in table.findAll('a')])
            if len(links) == 0:
                second_table = page_dtl.findAll('table')[1]
                links = dict([(i.get_text(), self.site+i.get('href')) for i in second_table.findAll('a')])

        all_urls = [v for k, v in links.items()]
        
        return all_urls, links

    
    def download_and_save(self, links):
        for name, _ in links.items():
            path = Path(self.path + name + '.pdf')
            path.write_bytes(requests.get(links[name]).content)

    def crawl(self):
        urls, links = self.get_urls()
        self.download_and_save(links)


class KenyanBillsMetadata(Metadata):
    def __init__(self, paths):
        self.paths = paths
        self.site = "http://kenyalaw.org/kl/"
        self.ids = [9091, 7938, 6819, 5991, 5189, 4250, 4251, 525, 523, 522, 521, 520, 519]
        super(KenyanBillsMetadata, self).__init__()

    def get_rows(self, idx):
        url = '{}index.php?id={}'.format(self.site, idx)
        page = requests.get(url)
        page_dtl = BeautifulSoup(page.content, "html.parser")
        div = page_dtl.find('div' , {'id': 'inner-section'})
        table = div.find_next('table', 'contenttable')
        trs = table.find_all('tr')
        if len(trs) < 3: #2011 has two tables
            print(id)
            second_table = page_dtl.findAll('table')[1]
            trs = second_table.find_all('tr')
            
        return trs

    def __retrive_metadata_2013_2019(self, idx):
        trs = self.get_rows(idx)
        rows = []
        for tr in trs:
            rows.append([td.get_text() for td in tr.find_all('td')])
        df = pd.DataFrame(rows)
        df = df[1:]
        if id == 5189: #2015
            df.columns = ['NO', 'BILL', 'SPONSOR', 'NA BILL/NO.','GAZETTE NO.','DATED', 'MATURITY', '1ST READ',\
                    '2ND READ', '3RD READ', 'REMARKS', 'ASSENT']

        else:
            df.columns = ['NO', 'BILL', 'SPONSOR', 'NA BILL/NO.', 'DATED', 'MATURITY', 'GAZETTE NO.', '1ST READ',\
                    '2ND READ', '3RD READ', 'REMARKS', 'ASSENT']
            
        df = df.set_index(df.columns[0])
        return df

    def __retrive_metadata_2007_2012(self, idx):
        trs = self.get_rows(idx)
        rows = []
            
        for tr in trs:
            rows.append([td.get_text() for td in tr.find_all('td')])
            
        df = pd.DataFrame(rows)
        columns = df.iloc[0]
        df = df[1:]
        df.columns = columns
        df = df.set_index(df.columns[0])
        df.to_csv('{} metadata.csv'.format(idx))
        return

    def combine_metadata(self, ids):
        all_df = []
        for idx in ids:
            try:
                df = self.__retrive_metadata_2013_2019(idx)
                all_df.append(df)
            except:
                self.__retrive_metadata_2007_2012(idx)

        df_2013_2019 = pd.concat(all_df, ignore_index=True, sort=False)
        return df_2013_2019

    def grabtable(self):
        self.data = self.combine_metadata(self.ids)
        if self.data.to_csv(self.path, encoding='utf-8', index=False):
            return True
        raise NotImplementedError("Implement a logic to grab data from table and return the data as dictionary or pandas DataFrame")



