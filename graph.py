import requests
import json
from config import DefaultConfig
config = DefaultConfig()
import string

token_data = {
        'grant_type': 'password',
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'resource': config.RESOURCE,
        'scope':config.RESOURCE,
        'username':config.MAIL,
        'password':config.PASS,}

token_req = requests.post(config.URL2, data=token_data)
token = token_req.json().get('access_token')
query = config.RESOURCE + config.API_VERSION + '/sites/' + config.SITE_ID
headers = {
    'Authorization': 'Bearer {}'.format(token)
    }


def welcome():

    data = json.loads(requests.get(query, headers=headers).text)
    return(data['displayName'])

def getList(intent: string):
    if(intent=="listes_cours"):
        l='courses'
    elif(intent == "listes_livre"):
        l = "books"
    elif(intent == "listes_formation"):
        l = "trainings"
    return(l)

def getData(intent: string, entity: string):
    products = []
    if(intent == "Acheter_livre"):
        l = "Livre"
        t = "Book"
    elif(intent == "suivre_cours"):
        l = "Cours"
        t = "Course"
    elif(intent == "suivre_formation"):
        l = "Formation"
        t = "Training"
    endpoint = query + "/Lists/"+ l + "/items/?expand=fields"
    data = json.loads(requests.get(endpoint, headers=headers).text)
    for dic in data["value"]:
        items={}
        items['id']=dic["fields"]["id"]
        items['Title']=dic["fields"]["Title"]
        items['Type']=dic["fields"][t+"Type"]
        items['Price']=str(dic["fields"][t+"Price"])+" €"
        if(len(dic["fields"][t+"Description"]) >= 200):
            items['Description']=dic["fields"][t+"Description"][0:200:1]+"..."
        else:
            items['Description']=dic["fields"][t+"Description"]
        if(t+"Author" in dic["fields"].keys()):
            items['Author']=dic["fields"][t+"Author"]
        else:
            items['Author']=""
        products.append(items)
    if('-' in entity.split("_")):
        prod = "".join(entity.split("_"))
    else:
        prod = " ".join(entity.split("_"))
    final_list = []
    final_list.append(l)
    i = 0
    while(i < len(products)):
        prodl = products[i]['Title'].lower()
        if(prod.lower() in prodl):
            final_list.append(products[i])
        i=i+1
    return(final_list)