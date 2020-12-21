from botbuilder.core import TurnContext,ActivityHandler,RecognizerResult,MessageFactory,CardFactory
from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer
from config import DefaultConfig
from graph import getData,getList
import json
import os.path
from botbuilder.schema import Attachment,AttachmentLayoutTypes
import string


CONFIG = DefaultConfig()

class SmartBot(ActivityHandler):
    def __init__(self):
        #connect to LUIS library app
        luis_app = LuisApplication(CONFIG.LUIS_APP_ID,CONFIG.LUIS_API_KEY,CONFIG.LUIS_API_HOST_NAME)
        luis_option = LuisPredictionOptions(include_all_intents=True,include_instance_data=True)
        self.LuisReg = LuisRecognizer(luis_app,luis_option,True)
    
    async def on_message_activity(self,turn_context: TurnContext):
        result = await self.LuisReg.recognize(turn_context)
        entity_list = list(result.entities.keys())
        intent = LuisRecognizer.top_intent(result)
        l = [ 'it','management','softskills']
        i = [ 'listes_cours' , 'listes_livre' , 'listes_formation' ]
        a = [ 'Acheter_livre' , 'suivre_cours' , 'suivre_formation']
        if(intent == "None" ):
            await turn_context.send_activity("j'ai pas compris ! réenvoyer votre question s'il vous plait!")
        if(result.text.lower() in l and intent == "Departement"):
            await turn_context.send_activity("ceci est un domaine disponible chez nous pour e-learning")
        elif(intent == "domaine"):
            if(result.text.lower() in l):
                await turn_context.send_activity("ceci est un domaine disponible chez nous pour e-learning")
            elif(entity_list!=['$instance']):
                await turn_context.send_activity(f"{result.entities[entity_list[1]][0]} est un domaine du {entity_list[1]}")
            else:
                await turn_context.send_activity("Comment je peux vous aider ?")
        elif(intent == "services"):
            await turn_context.send_activity("on est une librairie en ligne , vente des livres , des formation à attendre et des cours à suivre dans plusieurs domaines . je suis votre assistant fidéle")
        elif(intent in i):
            test = getList(intent)
            url = "https://tutocamp/sites/library/SitePages/"+test+".aspx"
            await turn_context.send_activity(f"vous pouvez voir {intent} en visitant le lien suivant : "+url)
        elif(intent in a):
            if(entity_list==['$instance']):
                await turn_context.send_activity(f"c'est compris que vous voulez {intent} mais spécifiez plus un exemple du domaine du service s'il vous plait; i.e IT(java,cisco,security...) / Management(leading,RH) / Softskills(communication,gestion du stress...)")
            else:
                for i in entity_list:
                    if(i != '$instance'):
                        st = ' '.join([str(elem) for elem in result.entities[i]]).replace(' ','_')
                        if(st in l):
                            await turn_context.send_activity(f"c'est compris que vous voulez {intent} mais spécifiez plus un exemple du "+st)
                        else:
                            action = intent.split("_")
                            test = getData(intent,st)
                            if(len(test)!=1):
                                if(test[0]=="Livre"):
                                    image="https://i.pinimg.com/474x/9a/12/c8/9a12c8fe2d0755250f57da8aa2cd9787.jpg"
                                elif(test[0]=="Cours"):
                                    image="https://png.pngtree.com/png-vector/20190719/ourlarge/pngtree-e-learning-line-icon-online-internet-education-symbol-graduation-png-image_1550378.jpg"
                                elif(test[0]=="Formation"):
                                    image="https://png.pngtree.com/png-vector/20190719/ourlarge/pngtree-e-learning-line-icon-online-internet-education-symbol-graduation-png-image_1550378.jpg"
                                await turn_context.send_activity("voici les "+action[1]+" que vous cherchez :")
                                k = 1
                                while(k < len(test)):
                                    url = CONFIG.PRODUCT_URL+str(test[k]['id'])+"&type=SP.Data."+test[0]+"ListItem"
                                    reply =  self.create_adaptive_card_attachment(url,test[k]['Title'],image,test[k]['Type'],test[k]['Price'],test[k]['Description'],test[k]['Author'])
                                    response = MessageFactory.attachment(reply)
                                    await turn_context.send_activity(response)
                                    k=k+1
                            else:
                                if(action[1]=="formation"):
                                    await turn_context.send_activity("la "+action[1]+" que vous souhaitez commander n'est disponible chez nous maintenant")
                                else:
                                    await turn_context.send_activity("le "+action[1]+" que vous souhaitez commander n'est disponible chez nous maintenant")

    def create_adaptive_card_attachment(self,url: string,title: string,image: string,Type: string,price: string,description: string,author: string):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "./cards/Product.json")
        with open(path) as card_file:
            card = json.load(card_file)
            card["body"][0]["items"][0]["text"]=title
            card["body"][0]["items"][1]["columns"][0]["items"][0]["url"]=image
            card["body"][0]["items"][1]["columns"][1]["items"][0]["text"]=description
            card["body"][1]["items"][0]["facts"][0]["value"]=author
            card["body"][1]["items"][0]["facts"][1]["value"]=Type
            card["body"][1]["items"][0]["facts"][2]["value"]=price
            card["actions"][0]["url"]=url
            card["actions"][1]["url"]=url
        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )