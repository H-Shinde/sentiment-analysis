from bs4 import BeautifulSoup
import requests
import pickle
import re
def getEmotions(word):

    with open("Models\LinReg-Model",'rb') as f:
        model = pickle.load(f)

    emotions ={'positive':0,'negative':0}
    wrd = word

    url =f"https://myanimelist.net/anime.php?cat=anime&q={wrd}&type=0&score=0&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c%5B%5D=a&c%5B%5D=b&c%5B%5D=c&c%5B%5D=f"

    anime = requests.get(url).text
    doc = BeautifulSoup(anime,"html.parser")
    link_to_anime = doc.find('a',class_="hoverinfo_trigger fw-b fl-l").get('href')

    anime = requests.get(link_to_anime).text
    doc = BeautifulSoup(anime,"html.parser")
    link_to_reviews = doc.find(class_="rightside js-scrollfix-bottom-rel").find(string="Reviews").parent.get('href')
    fin = requests.get(link_to_reviews).text
    doc = BeautifulSoup(fin,"html.parser")
    items=[]

    item = doc.find_all("div",class_="text")
    items.append(item)


    link_to_next = doc.find('div',class_="ml4 mb8").find(string="More Reviews").parent.get('href')
    while doc.find('div',class_="ml4 mb8").find(string="More Reviews")!=None:
        file = requests.get(link_to_next).text
        doc = BeautifulSoup(file,"html.parser")
        item = doc.find_all("div",class_="text")
        items.append(item)
        if doc.find('div',class_="ml4 mb8").find(string="More Reviews")!=None:
            link_to_next = doc.find('div',class_="ml4 mb8").find(string="More Reviews").parent.get('href')


    for item1 in items:
        for item2 in item1:
            # Replace <br> tags with an empty string
            for br in item2.find_all("br"):
                br.replace_with("")

    for item in items:            
        for ite in item:
        
            pred = model.predict([ite.get_text()])
            if pred == 0:
                emotions["negative"] += 1
            else:
                emotions["positive"] += 1
    return emotions


def getDescription(word):
    wrd = word

    url =f"https://myanimelist.net/anime.php?cat=anime&q={wrd}&type=0&score=0&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c%5B%5D=a&c%5B%5D=b&c%5B%5D=c&c%5B%5D=f"

    anime = requests.get(url).text
    doc = BeautifulSoup(anime,"html.parser")
    link_to_anime = doc.find('a',class_="hoverinfo_trigger fw-b fl-l").get('href')

    anime = requests.get(link_to_anime).text
    doc = BeautifulSoup(anime,"html.parser")
    description = doc.find(class_="rightside js-scrollfix-bottom-rel").find('table').find('p',itemprop= "description")
    return description.text

def getStrPlatforms(word):
    wrd = word

    url =f"https://myanimelist.net/anime.php?cat=anime&q={wrd}&type=0&score=0&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c%5B%5D=a&c%5B%5D=b&c%5B%5D=c&c%5B%5D=f"

    anime = requests.get(url).text
    doc = BeautifulSoup(anime,"html.parser")
    link_to_anime = doc.find('a',class_="hoverinfo_trigger fw-b fl-l").get('href')

    anime = requests.get(link_to_anime).text
    doc = BeautifulSoup(anime,"html.parser")
    platforms = doc.find('div',class_='leftside').find('div',class_="pb16 broadcasts").find_all('a',title=re.compile(".*"))
    titles = [a['title'] for a in platforms if 'title' in a.attrs]

    return titles
s = getStrPlatforms('demon slayer')
print(s)