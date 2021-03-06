# Szientikon
Frei zugängliche wissenschaftliche Textsorten verschiedener Fachbereiche solle akquirieret werden und mit Methoden des Text Mining verglichen werden

### Allgemeine Installationsvorraussetzungen:

Die Anwendung erfordert [Python3](https://www.python.org/downloads/) (Version 3.7) und eine lokale [MongoDB](https://docs.mongodb.com/manual/administration/install-community/) Installation.

### Empfohlener Editor:
* [Pycharm](https://www.jetbrains.com/pycharm/)

### Verwendete Bibliotheken:

* [requests](http://docs.python-requests.org/en/master/) (sudo pip(3) install requests)
* [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) (sudo pip(3) install bs4)
* [django](https://www.djangoproject.com) (sudo pip(3) install django==2.1.4) 
* [mongoengine](http://docs.mongoengine.org) (sudo pip(3) install mongoengine)
* [NLTK](https://www.nltk.org/install.html) pip(3) install nltk
* [jsonschema](https://pypi.org/project/jsonschema/) pip(3) install jsonschema

alternativ Bibliotheken auch über Pycharm Package-Manager installieren


(Dann eine neue RunConfiguration "djangoServer" über + hinzufügen. Als "Environment Variables" ->
Name: "DJANGO_SETTINGS_MODULE" 
Wert: "DjangoTextMining.settings"
hinzufügen
PyCharm fragt beim ersten Run nach einem Root-Folder. Dieser ist der gesamte Ordner in dem die 3 django-Ordner enthalten sind.)

### Start der Anwendung: 
Schritt1: MongoDB mit dem Befehl "mongod" im Terminal starten \
Schritt2: Django starten im Projektordner mit dem Befehl "python(3) manage.py runserver 8000" \
Schritt3: im Browser url: http://127.0.0.1:8000/ öffnen


### Crawler und Parser
Zum erneuten crawlen der Daten die Datei `crawler.py` ausführen. Die gecrawlten Dateien befinden sich im CorpusRaw-Ordner.
Zum parsen dieser Ergebnisse die Datei `HTMLtoJSON.py` ausführen. Die geparsten JSON-Dateien befinden sich im OutputJSON-Ordner.
Ein bereits geparster Ordner mit JSON-Dateien liegt der Abgabe im Google-Drive bei.