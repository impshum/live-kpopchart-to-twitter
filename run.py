import tweepy
from bs4 import BeautifulSoup
from datetime import datetime
from requests import get
from time import sleep
import schedule
from halo import Halo


consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_key = 'XXXX'
access_secret = 'XXXX'

test = 0
replace_arrows = 1
sleep_timer = 60

spinner = Halo(text='Booting up...', spinner='dots')
spinner.start()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def lovely_soup(url):
    r = get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')
    return soup


def get_table(soup, melon):
    table = soup.find('table', {'class': melon})
    rank = table.find('span', {'class': 'data-rank'}).text.strip()
    if replace_arrows:
        move = table.find('span', {'class': 'data-chagestatus'}).text.strip().replace('▼ ', '⇩').replace('▲ ', '⇧')
    else:
        move = table.find('span', {'class': 'data-chagestatus'}).text.strip()
    return [rank, move]


def get_ranks():
    soup = lovely_soup('http://www.kpopchart.kr/?a=마마무(Mamamoo)')
    bands = {'Melon': 'table_MELON', 'Genie': 'table_GENIE', 'Mnet': 'table_MNET', 'Bugs': 'table_BUGS', 'Soribada': 'table_SORIBADA'}
    ranks = {}
    for k, v in bands.items():
        table = get_table(soup, v)
        ranks.update({k: {'rank': table[0], 'move': table[1]}})
    return ranks


def main():
    ranks = get_ranks()
    melon_rank = ranks['Melon']['rank']
    melon_move = ranks['Melon']['move']
    genie_rank = ranks['Genie']['rank']
    genie_move = ranks['Genie']['move']
    mnet_rank = ranks['Mnet']['rank']
    mnet_move = ranks['Mnet']['move']
    bugs_rank = ranks['Bugs']['rank']
    bugs_move = ranks['Bugs']['move']
    sorb_rank = ranks['Soribada']['rank']
    sorb_move = ranks['Soribada']['move']
    msg = f'마마무(#Mamamoo)\n\n{melon_rank} Melon {melon_move}\n{genie_rank} Genie {genie_move}\n{mnet_rank} Mnet {mnet_move}\n{bugs_rank} Bugs {bugs_move}\n{sorb_rank} Soribada {sorb_move}'
    if not test:
        api.update_status(msg)
    spinner.text = 'Twatted some stuff'


main()
schedule.every(sleep_timer).minutes.do(main)
count = sleep_timer * 60
while True:
    try:
        schedule.run_pending()
        sleep(1)
        count -= 1
        spinner.text = 'Tweeting again in {} seconds'.format(count)
    except Exception as e:
        print(e)
        break
