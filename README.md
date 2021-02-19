# :fr: :phone: Peut on coder avec OCaml Python et C par SMS ?

Je souhaite répondre à la question suivante : peut on coder avec OCaml Python et C par SMS ?

## Quel objectif ?

Je souhaite pouvoir faire ça, depuis mon téléphone :

1. J'envoie un texto qui content « `pw:PASSWORD python: print("Hello world from Python!")` » à `0612345678` (un numéro spécifique), depuis mon téléphone (sans appli, sans Internet, sans rien d'autre que des vieux SMS en GSM) ;

2. Quelques secondes plus tard, je reçois de ce numéro `0612345678` un SMS qui content « `Python:Out[1] Hello world from Python!` » ;

3. Je veux que ça marche pour des *petits* programmes en *Python 3*, *OCaml 4.05+* et *C11* ;

4. Je veux les fonctionnalités suivantes :
   - qu'il y ait ce mot de passe ;
   - qu'il y ait un numéro incrémental de cellule sortie : trois requêtes de suite seront `Out[1]: ...`, `Out[2]: ...`, `Out[3]: ...`, etc.
   - que ça fonctionne sans problème pour ces trois langages (voir plus ?) ;
   - TODO: que l'exécution soit sécurisée, et isolée (voir [camisole](https://camisole.prologin.org/) ?) ;

5. Premières étapes :
   - que le code soit exécuté sur *ma machine* (ou sur un serveur distant quand ce sera prêt) ;
   - je veux devoir lancer manuellement le serveur, et afficher dans une console ce qui se passe ;

- Références : <https://www.fullstackpython.com/blog/respond-sms-text-messages-python-flask.html> en anglais (lu le 2021-02-19).

## Solution

Ce dépôt GitHub contient un petit script Python 3 (avec un serveur [Flask](https://flask.palletsprojects.com/)) pour expérimenter et essayer cela.

Quelques questions et réponse :

1. **Quel numéro de SMS ?**
  Avec un compte **payant** sur [Twilio](https://www.twilio.com/) (voir [les prix](https://www.twilio.com/sms/pricing/fr)) ;

2. **Quel architecture logicielle ?**

   - Localement sur mon ordinateur, je vais lancer une petite application Web écrite avec [Flask](https://flask.palletsprojects.com/).
   - Cette application écoute un *webhook* local (qui peut être ouvert sur l'Internet global avec [ngrok](https://ngrok.com/)).
   - Quand un message arrive sur ce *webhook*, l'application Flask répond en renvoyant un SMS avec le résultat de l'exécution du code soumis par la requête au webhook.
   - Avec l'API de Twilio, on peut connecter cette appli (ouverte avec ngrok) au numéro de téléphone (payant) fourni par le compte Twilio.
   - Avec tout ça, je peux exécuter (et voir la sortie et le code de retour) en envoyant un SMS à ce numéro.

3. **Où ça en est ?** Juste une idée pour l'instant. TODO: continuer!


TODO: la suite n'est pas terminée !

## Exemples

### Usage simple

1. [Installer ce projet](#Installation),
2. Créer un compte [Twilio](https://www.twilio.com/try-twilio),
3. Lancer le serveur avec `make local`, tester le,
4. Si ça marche, essayez le serveur distant avec `make ngrok` et allez ajouter l'adresse ngrok du webhook dans [le panneau de contrôle Twilio](https://www.twilio.com/console/phone-numbers),
5. Tester avec un exemple !
6. Soyez tout content :+1: ! Et ajouter une [petite étoile](https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS/stargazers) :star: à ce projet !

Cela va vous envoyer un texto contenant la réponse de l'exécution de ce programme, si tout est bien configuré.

![screenshots/example1.png](screenshots/example1.png)

### Aide

L'usage du script est le suivant :

```bash
python app.py --help|-h | TODO: [server] [port]
```

- Avec `-h` ou `--help`, affiche l'aide,
- TODO:

### Aide détaillée

```bash
$ ./app.py --help
TODO:
```

### Cas d'échec

Le script est traduit en français et anglais, et il affiche des messages d'erreurs clairs selon les causes d'échec.

----

## Installation

TODO: pour l'instant, pas assez stable pour être installé nulle part !

### Manuellement ?

Facile !
Cloner ce dépôt, aller dans le dossier, et utilisez le directement, sans le copier ailleurs.

```bash
cd /tmp/
git clone https://GitHub.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS
cd Peut-on-coder-avec-OCaml-Python-et-C-par-SMS/
make setupvenv
make local
# test it
make server
# add ngrok webhook to https://www.twilio.com/console/phone-numbers
# test it, using phone number!
```

> Si quelque chose ne fonctionne pas bien, merci [de signaler un problème](https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS/issues/new) :clap: !

### Avec `pip` ? :warning: TODO

Ce projet ne sera **pas** distribué sur [le dépôt de packet Pypi](https://pypi.org/), mais il peut être installé directement depuis GitHub avec [`pip`](http://pip.pypa.io/) et cette commande :

```bash
sudo pip install git+https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS
```

TODO: pas terminé, à faire !

Vérifiez que vous utilisez `pip3` et pas `pip2` selon la version de Python pour laquelle vous voulez installer cet outil. ([Python 2 n'est plus supporté](https://pythonclock.org/))

![PyPI implementation](https://img.shields.io/pypi/implementation/lempel_ziv_complexity.svg)
TODO:

----

## Comparaison à d'autres projets

- TODO: ?

----

## À propos :notebook:

### Langage et version(s) ?

Écrit en [Python v3.6+](https://www.python.org/3/) (version CPython).

### :scroll: Licence ? [![GitHub licence](https://img.shields.io/github/license/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.svg)](https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS/blob/master/LICENSE)

Ce script et cette documentation sont distribuées en accès libre selon les conditions de la [licence MIT](https://lbesson.mit-license.org/) (cf le fichier [LICENSE](LICENSE) en anglais).
© [Lilian Besson](https://GitHub.com/Naereen), 2021.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS/graphs/commit-activity)
[![Demandez moi n'importe quoi !](https://img.shields.io/badge/Demandez%20moi-n'%20importe%20quoi-1abc9c.svg)](https://GitHub.com/Naereen/ama.fr)
[![Analytics](https://ga-beacon.appspot.com/UA-38514290-17/github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS/README.md?pixel)](https://GitHub.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS/)

[![ForTheBadge uses-badges](http://ForTheBadge.com/images/badges/uses-badges.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-swag](http://ForTheBadge.com/images/badges/built-with-swag.svg)](https://GitHub.com/Naereen/)
