from crawler.custom import NigerianBills, KenyanBills
from crawler.base import Metadata

import click


@click.command()
@click.argument('action', type=click.Choice(['crawl', 'extract', 'metadata', 'sample']))
@click.argument('country',type=click.Choice(['nigeria', 'south_africa', 'kenya']))
@click.option('--path',type=click.Path(exists=True))

def nassai(action, country, path=None):
    if action == "crawl":
        if country == "nigeria":
            crawler = NigerianBills(path=path)
            return crawler.crawl()
        elif country == "kenya":
            crawler = KenyanBills(path=path)
            return crawler.crawl()
    elif action == "metadata":
        meta = Metadata(path)
        return meta.grabtable()


if __name__ == "__main__":
    nassai()
