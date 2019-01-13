# -*- coding: cp1252 -*-
#We import useful librairies
# on importe les librairies nécessaires
from flask import Flask, jsonify, render_template, request
import time
import random
from functions2 import * # from lib import * => importer toutes les fonctions de lib

#we instantiate the app
# on l'instance l'app flask
app = Flask(__name__)



# on définie des routes
#we define routes

@app.route("/")
def main():
    return render_template('main.html', reload = time.time())

			

@app.route("/ask")
# ask renvoie un json qui correspond �  la r�ponse �  la sentence �  l'étape n_etape du chatbot
#ask send a json which is the answer to the sentence at the n step
def ask():

	sentence = request.args.get('sentence', 0)
	n_etape = request.args.get('n_etape', 0)
	q = request.args.get('q', 0)
	#answer, n_etape, resume = chat(sentence, int(n_etape))
	answer, n_etape, q = chat_json(sentence, int(n_etape), q)
	
	#etape de recherche
	if int(n_etape) == 6: 
		# �  cette étape on renvoie le r�sum� et  les coordonn�es, en plus de la réponse du chatbot et du numéro de l'étape
		# At this step we get the sumup and the coordinates
		return jsonify({
                "answer" : answer,
                "n_etape": n_etape,
                "lat": q[0][0],
                "lon": q[0][1],
                "resume" : q[1]
            })

	# etape du choix de l'utilisateur parmi les lieux proposés
	#user's choice step  for places
	elif int(n_etape) == 5:


		return jsonify({
                "answer" : answer,
                "n_etape": n_etape,
                "q":q,
            })

	# etape classique
	return jsonify({
                "answer" : answer,
                "n_etape": n_etape,
            })
    
    
    
#we launch the app
# on lance l'application
if __name__ == '__main__':
    app.run()