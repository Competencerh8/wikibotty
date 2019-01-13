# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json as js


def clean_text(text, b):
    soup = BeautifulSoup(text, 'html.parser')
    list_TEXT = []
    for text_html in soup.find_all('p'):
        list_TEXT.append(text_html.text)
    list_TEXT2 = []
    for k in range(len(list_TEXT)):
        if list_TEXT[k] != '\n':
            list_TEXT2.append(list_TEXT[k][0:-1])
        
    def delete_crochets(text):
        new_text = ''
        k=0
        while k<len(text):
            if text[k] == '[':
                k = k + 3
            if k< len(text):
                new_text = new_text + text[k]
            k = k + 1
        return new_text

    for k in range(len(list_TEXT2)):
        list_TEXT2[k] = delete_crochets(list_TEXT2[k])
    
    def delete_listen(text):
        new_text = ''
        k=0
        while k<len(text):
            if text[k] == '\xa0':
                k = k + 11
            if k< len(text):
                new_text = new_text + text[k]
            k = k + 1
        return new_text

    for k in range(len(list_TEXT2)):
        list_TEXT2[k] = delete_listen(list_TEXT2[k])
    
    
    text_final = list_TEXT2[0] + '\n\n' + list_TEXT2[1] + '\n\n' +list_TEXT2[2]

    if b ==True:
        text_final = list_TEXT2[5] + '\n\n' + list_TEXT2[6] + '\n\n' +list_TEXT2[7]
    
    
    return (text_final)


def resume_en(lieu):
    resp = requests.get("http://en.wikipedia.org/w/api.php?action=parse&page="+ lieu +"&format=json")
    data = resp.json()
    
    #check if the page exists
    if 'error' in data.keys():
        return -1
    
    text_html = data['parse']['text']['*']

    # clean bandeau-cell
    soup = BeautifulSoup(text_html, 'html.parser')
    #check if bandeau-cell
    if len(soup.findAll("div", {"class": "bandeau-cell"}))>0:
        clean_text(text_html, True)
    
    return clean_text(text_html,False)
    


def get_coordinates(page):
    resp = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=coordinates&titles=" + page)
    data = resp.json()

    lat = ""
    lon = ""
    if '-1' not in  data['query']['pages'].keys():
        print(data.keys())
        lat = data['query']['pages'][list(data['query']['pages'].keys())[0]]['coordinates'][0]['lat']
        lon = data['query']['pages'][list(data['query']['pages'].keys())[0]]['coordinates'][0]['lon']

    return lat, lon



def chat_json(text, n_etape, q):
    
    # load fichier json
    json_file = open("chatbot_content2.json", encoding = 'utf-8')
    json_str = json_file.read()
    dict = js.loads(json_str)

    if n_etape == 1:
        if text in dict['0']['a']:
            return dict['1']['q'], 2, ""
        else:
            return dict['error'], 1, ""
    elif n_etape == 2:
        if text in dict['1']['a']:
            return dict['2']['q'], 3, ""
        else:
            return dict['error'], 2, ""
        
    elif n_etape == 3:
        if text in dict['2']['a']['n']:
            return dict['3']['q']['n'], -1, ""
        elif text in dict['2']['a']['y']:
            return dict['3']['q']['y'], 4, ""
        else:
            return dict['error'], 3, ""

    elif n_etape == 4:
        
        # requete à wikimedia
        L = query_wikimedia(text)

        # réponse nulle => on renvoit dict['4'] qui correspond à "il n'y a pas de ..."
        if len(L) == 0:
            return dict['4'], 4, ""
        
        # s'il n'y a pas d'erreur on crée la liste des éléments trouvés + numérotation
        string_list = []
        for k in range(len(L)):
            string_list.append(str(k)+ ') '+ L[k][1])

        return string_list, 5, text


    elif n_etape == 5:
        
        string, L = search(q) # recherche api openstreetmap
        L1 = query_wikimedia(q) # recherche api wikimedia

        # on gère l'erreur: la réponse de l'utilisateur n'est pas un numéro
        if text.isdigit() == False:
            return "Je ne sais pas quoi vous dire, je n'ai pas été programmé pour répondre à ça ...", 5, q

        # s'il n'y a pas eu d'erreur, on récupère les coordonnées et le résumé et on les envoie à js
        if int(text) in range(len(L1)):
            c = get_coordinates(L1[int(text)][1])
            resume = resume_en(L1[int(text)][1])
            return " Souhaitez vous visiter un autre lieu ?" , 6, (c, resume)
        else:
            return "Je ne sais pas quoi vous dire, je n'ai pas été programmé pour répondre à ça ...", 5, q
        
    elif n_etape == 6:
        # étape de fin ou de recommencement

        if text in ["non"]:
            return "Bonne visite !", -1, ""
        elif text in ["oui"]:
            return "Quel autre lieu souhaiteriez vous visitez ?", 4, ""
        else:
            return "Je ne sais pas quoi vous dire, je n'ai pas été programmé pour répondre à ça ...", 6, ""
    



# requête open street map
def search(q):
    

    resp = requests.get("https://nominatim.openstreetmap.org/search?q=" + q + "&format=json&polygon=1&addressdetails=0")
    data = resp.json()

    L = []
    string = ''
    for k in range(len(data) - 1):
        L.append(data[k]['display_name'])
        string += '(' +str(k) +') ' + data[k]['display_name'] + ' / '
    k = len(data)-1
    if len(data) == 0:
        return -1, ''
    string += '(' +str(k) +') ' + data[k]['display_name']

    return string, data


# requête/recherche wikimedia, on demande des pages en lien avec la variable text, pas de nettoyage,
# renvoie de réponse bien orthographiées, l'utilisateur choisi parmi celles-ci.
def query_wikimedia(text):

    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    # page recherchée
    SEARCHPAGE = text

    PARAMS = {
    'action':"query",
    'list':"search",
    'srsearch': SEARCHPAGE,
    'format':"json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    L = []
    for page in DATA['query']['search']:
        L.append((page["pageid"], page['title']))
    return L