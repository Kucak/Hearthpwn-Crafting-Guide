import requests
from bs4 import BeautifulSoup as bs4
import urlparse
from operator import itemgetter
from collections import OrderedDict

counts = dict()
neutral_counts = dict()
card_dict = dict()
url_base = "http://www.hearthpwn.com/"

def insert_dict(card):
    global  card_dict
    if card.get('data-id') not in card_dict.keys():
        res = dict()
        res["rarity"] = card.get('class')[0]
        res["set"] = card.get('class')[1]
        res["name"] = card.text.strip()
        card_dict[card.get('data-id')] = res

def get_cards_by_deck(url):
    global  counts
    r = requests.get(url).content
    s = bs4(r,'html.parser')

    trs = s.findAll('section',{"class":["t-dect-details-card-list","class-listing"]})[0].select('tr')
    for tr in trs:
        tds = tr.select('td')
        if tds:
            cards = tds[0].select('a')
            if len(cards):
                card = cards[0]
                try:
                    if card.get('data-id') in counts.keys():
                        counts[card.get('data-id')] += int(card.get('data-count'))
                    else:
                        counts[card.get('data-id')] = int(card.get('data-count'))
                        insert_dict(card)
                except:
                    if card.get('data-id') in counts.keys():
                        counts[card.get('data-id')] += 1
                    else:
                        counts[card.get('data-id')] = 1
                        insert_dict(card)
    trs = s.findAll('section',{"class":["t-dect-details-card-list","neutral-listing"]})[0].select('tr')
    for tr in trs:
        tds = tr.select('td')
        if tds:
            cards = tds[0].select('a')
            if len(cards):
                card = cards[0]
                try:
                    if card.get('data-id') in neutral_counts.keys():
                        neutral_counts[card.get('data-id')] += int(card.get('data-count'))
                    else:
                        neutral_counts[card.get('data-id')] = int(card.get('data-count'))
                        insert_dict(card)
                except:
                    if card.get('data-id') in neutral_counts.keys():
                        neutral_counts[card.get('data-id')] += 1
                    else:
                        neutral_counts[card.get('data-id')] = 1
                        insert_dict(card)








def get_decks_by_class(url):
    global url_base
    r = requests.get(url).content
    s = bs4(r,'html.parser')

    deckTRS = s.select('tr')[1:]
    for deckTR in deckTRS:
        if str(deckTR.select('td.col-deck-type ')[0].text) != "PvE Adventure":
            deck_url = deckTR.select('span > a')[0].get('href')
            deck_url = urlparse.urljoin(url_base, deck_url)
            get_cards_by_deck(deck_url)




def print_class(urls):
    global counts
    global card_dict
    for url in urls:
        get_decks_by_class(url[1])
        ordered_dict = OrderedDict(sorted(counts.items(), key=itemgetter(1)))

        dosya = open(url[0]+".txt","w")

        dosya.write( "--------------------LEGENDARIES--------------------\n")
        for card in ordered_dict:
            if card_dict[card]['rarity'] == 'rarity-5':
                dosya.write( card_dict[card]['name'] + " , counts : " + str(counts[card])+"\n")
        dosya.write( "--------------------EPIC--------------------\n")
        for card in ordered_dict:
            if card_dict[card]['rarity'] == 'rarity-4':
                dosya.write(card_dict[card]['name'] + " , counts : " + str(counts[card])+"\n")
        dosya.write( "--------------------RARE--------------------\n")
        for card in ordered_dict:
            if card_dict[card]['rarity'] == 'rarity-3':
                dosya.write(card_dict[card]['name'] + " , counts : " + str(counts[card])+"\n")
        counts = dict()
        dosya.close()

def print_neutral():
    global neutral_counts
    global card_dict
    ordered_dict = OrderedDict(sorted(neutral_counts.items(), key=itemgetter(1)))
    dosya = open("neutral.txt", "w")
    dosya.write( "--------------------LEGENDARIES--------------------\n")
    for card in ordered_dict:
        if card_dict[card]['rarity'] == 'rarity-5':
            dosya.write(card_dict[card]['name'] + " , counts : " + str(neutral_counts[card])+"\n")
    dosya.write( "--------------------EPIC--------------------\n")
    for card in ordered_dict:
        if card_dict[card]['rarity'] == 'rarity-4':
            dosya.write(card_dict[card]['name'] + " , counts : " + str(neutral_counts[card])+"\n")
    dosya.write( "--------------------RARE--------------------\n")
    for card in ordered_dict:
        if card_dict[card]['rarity'] == 'rarity-3':
            dosya.write(card_dict[card]['name'] + " , counts : " + str(neutral_counts[card])+"\n")


link_list = []
link_list.append(("priest","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=64"))
link_list.append(("rogue","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=128"))
link_list.append(("warlock","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=512"))
link_list.append(("warrior","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=1024"))
link_list.append(("mage","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=16"))
link_list.append(("hunter","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=8"))
link_list.append(("paladin","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=32"))
link_list.append(("druid","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=4"))
link_list.append(("shaman","http://www.hearthpwn.com/decks?filter-show-standard=1&filter-deck-tag=1&filter-class=256"))
print_class(link_list)
print_neutral()
