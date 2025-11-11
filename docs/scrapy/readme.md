# **Le framework Scrapy**<a href="../../"><img align="right" src="../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
1. Le moteur Scrapy (Engine) contrôle le flux de données et la communication entre les composants.
1. Un ou plusieurs Spider·s (classes définies par l'utilisateur) indiquent à Scrapy quelles URLs visiter et comment extraire les données.
1. Les requêtes (Requests) générées par les Spiders sont envoyées au Scheduler, qui les met en file d'attente.
1. Le Scheduler transmet les requêtes au Downloader, qui télécharge le contenu HTML des pages web.
1. Le Downloader renvoie les réponses (Responses) au moteur. Le moteur les transmet aux Spiders pour extraction des données (c'est le parsing).
1. Le·s Spider·s extraient les données et peuvent générer de nouvelles requêtes à suivre.
1. Les données extraites passent ensuite dans la Item Pipeline. C'est un ensemble de traitements qui nettoient, valident et stockent les informations (e.g. base de données, fichiers).

Le cycle se termine quand les requêtes sont traitées.

<img src="https://docs.scrapy.org/en/latest/_images/scrapy_architecture_02.png" alt="Fonctionnement de Scrapy" align="center"><br><br>

Dans ce framework, le spider a un roôle central.  
Cette classe Python hérite de `scrapy.Spider` et définit les comportements spécifiques pour le scraping d'un site web.
___
Cf.  
[Archigtecture de Scrpy](https://docs.scrapy.org/en/latest/topics/architecture.html)  
[Documentation officielle de Scrapy](https://docs.scrapy.org/en/latest/)