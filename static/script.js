(function() {
	
    var ajax_get = function(url, callback) {

        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                
                document.getElementById('load').innerHTML = '<img src=\"/static/noun_Man_68200.png\" height=\"42\" width=\"42\">'

                console.log('responseText:' + xmlhttp.responseText); // afficher résultat dans la console

                try {
                    var data = JSON.parse(xmlhttp.responseText); // parse xml to json
                } catch(err) {
                    console.log(err.message + " in " + xmlhttp.responseText);
                    return;
                }
                callback(data);
            }
        };
        
        // on lance la requête définie plus haut et le gif de chargement
        document.getElementById('load').innerHTML = '<img src=\"/static/noun_Man_68200.gif\" height=\"42\" width=\"42\">'
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
    };
	

    var n_etape = 1
    var q = ''
	var ask = document.getElementById('ask');

    // réaction, fonction lancée à l'évènement click de la souris
	ask.addEventListener('click', function() {

        // on construie l'url de requête au python
		var url2 = '/ask?sentence=' + document.getElementById('sentence').value + '&n_etape=' + n_etape + '&q=' + q;

        // data = json
        // on utilise la méthode ajax_get définie plus haut, et on définie la function callback argument de ajax_get et avec l'url plus haut
        ajax_get(url2, function(data) {

            // traitement des données reçu par javascript, envoyé par python (le serveur)
            n_etape = data["n_etape"]
            if (n_etape == 6){
                // on affiche en plus de la réponse classique du chatbot : update carte + résumé de la page wiki
                document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+ 'Vous visualisez la carte à cet endroit: '+  data['lat'] + ', ' + data['lon']
                document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+  data['resume']

                document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+  "WikiChatbot: " + data['answer']
                update(data['lon'], data['lat'])

            }
            else{
                if(n_etape == 5){
                    // on affiche la liste des résultats de la requête

                    var resume = data['resume']
                    q = data['q']
                    var pas;
                    len = data['answer'].length;
                    for (pas = 0; pas < len; pas++) {
                         document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />' + data['answer'][pas]
                        }
                }

                else{
                    // comportement "classique", on affiche seulement la réponse du chatbot, pas de résumé ou de carte à mettre à jour
                    // dialogue simple avec le chatbot 
                    document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+  "WikiChatbot: "+ data['answer']
                }
            }
        });
        // on rajoute "You:"
        document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+ 'You: ' + document.getElementById('sentence').value
        // on efface le contenu de l'input/form
        document.getElementById('sentence').value = ""
    });

    // même chose mais lancé quand on appuie sur entré au clavier
    const input = document.getElementById('sentence');
    input.addEventListener('keyup', function(e) {

        // 13 code pour entrée
        if (e.keyCode === 13) {

        var url2 = '/ask?sentence=' + document.getElementById('sentence').value + '&n_etape=' + n_etape + '&q=' + q;
        ajax_get(url2, function(data) {
            n_etape = data["n_etape"]
            if (n_etape == 6){
                document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+ 'Vous visualisez la carte à cet endroit: '+  data['lat'] + ', ' + data['lon']
                document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+  data['resume']

                document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+  "WikiChatbot: " + data['answer']
                update(data['lon'], data['lat'])

            }
            else{
                if(n_etape == 5){
                    var resume = data['resume']
                    q = data['q']
                    var pas;
                    len = data['answer'].length;
                    for (pas = 0; pas < len; pas++) {
                         document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />' + data['answer'][pas]
                        }
                    //document.getElementById('resume').innerHTML = resume
                }

                else{
                    document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+  "WikiChatbot: "+ data['answer']
                }
            }
        });
        document.getElementById('answer').innerHTML = document.getElementById('answer').innerHTML + '<br /> <br />'+ 'You: ' + document.getElementById('sentence').value
        document.getElementById('sentence').value = ""
        }

    });

    // function utilisée au dessus qui met à jour la map avec les coordonnées lon, lat
	var update = function (lon, lat){
        document.getElementById('basicMap').innerHTML = "";
        map = new OpenLayers.Map("basicMap");
        var mapnik = new OpenLayers.Layer.OSM();
        map.addLayer(mapnik);
        map.setCenter(new OpenLayers.LonLat(lon,lat) // Centre de la carte
          .transform(
            new OpenLayers.Projection("EPSG:4326"), // transformation de WGS 1984
            new OpenLayers.Projection("EPSG:900913") // en projection Mercator sphérique
          ), 15 // Zoom level
        );
        var lonLat = new OpenLayers.LonLat(lon, lat)
          .transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            map.getProjectionObject() // to Spherical Mercator Projection
          );
    
    // définie le zoom de la map
    var zoom=16;

    // définie et instancie le marker
    var markers = new OpenLayers.Layer.Markers( "Markers" );
    map.addLayer(markers);
    markers.addMarker(new OpenLayers.Marker(lonLat));
      }

})()