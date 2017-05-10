import bs4
import json
import nltk
import requests


def scrape_spells(url):
    """
    Scrapes wikipedia page showing all of the
    Harry Potter spells. Takes a url (string) as input,
    and returns a dictionary with spell (dictionary key) 
    mapped to the spell description (dictionary value).
    """

    # Get web page
    response = requests.get(url)

    # Create soup object from page content
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    main_text = soup.findAll('h3', limit=142)

    # Get spell names and descriptions
    list_of_spells = []
    list_of_descriptions = []
    
    for h3 in main_text:        
        spell_info = h3.find_next_sibling('dl').findAll('b')  
        
        for info in spell_info:
            if info.get_text() == 'Description:':
                list_of_descriptions.append(info.nextSibling)  
                
                try:
                    list_of_spells.append(h3.i.get_text())   
                except:
                    list_of_spells.append(h3.get_text())       
    
    spell_dict = {}
    for idx, spell in enumerate(list_of_spells):
        spell_dict[spell] = list_of_descriptions[idx]
        
    with open('spell_dict.json','wb') as outfile:
        json.dump(spell_dict, outfile, indent = 2, separators = (',', ': '))
    
    return spell_dict