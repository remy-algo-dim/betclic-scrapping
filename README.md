# betclic-scrapping

### Objectif
Le projet permet de se connecter sur la page des matchs de foot Europeeans
puis de scrapper les paris dans la section Ecarts de buts de chaque match
On récupère les cotes les plus faibles (paris les plus surs) pour en faire une etude data derriere


### Vérification des paris
Il faudrait faire un second script qui permet d'aller verifier les cotes qui sont passées
et celles qui le sont pas (NLP ?).

Pour l'instant je remplie les resultats à la main

Output:
dataframe en CSV

# Environnements
- création des environnements en local et en prod via virtualenv
- pip install requirements.txt
- creation d'un .env en local avec les variables d'environnements associées au path
du chromedriver et du mode (local ou production)
- création d'un .env en prod également


# Deploiement
Machine AWS ai-leads:
* cd Dump (car le fichier .pem se trouve ici)
* ssh -i remy_key.pem ubuntu@ec2-13-38-119-82.eu-west-3.compute.amazonaws.com
* crontab tous les jours à 2 h du matin (heure où il n'y a pas de matchs, sinon le script ne fonctionne pas, je dois régler cela)

# Installations
- penser à installer chromedriver (en CLI) sur la machine de déploiement
* wget <URL_to_download>
* unzip <file_name_downloaded>.zip
* sudo mv chromedriver /usr/local/bin/    (chromedriver se trouve dans le folder telecharge)
  * cette commande sert à mettre chromedriver dans un repertoire accessible par le système
* sudo chmod +x /usr/local/bin/chromedriver
* chromedriver --version


- penser à installer google chrome sur la machine:
* wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
* sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
* sudo apt update
* sudo apt install google-chrome-stable
