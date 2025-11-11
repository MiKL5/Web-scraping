# **Quels outils utilisent des navigateurs sans tête ?**<a href="../../../../"><img align="right" src="../../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Les "_headless browsers_" sont des navigateurs web qui fonctionnent sans interface graphique.
---
Ils sont couramment utilisés pour le web scraping, les tests automatisés et d'autres tâches nécessitant l'interaction avec des pages web de manière programmatique.
1. **Puppeteer**  
C'est une bibliothèque JavaScript contrôlant Chrome ou Chromium en mode sans tête.  
Elle permet l'exécution de code JavaScript, faire des captures d'écran, générer des PDF, et interagir avec les pages web comme un utilisateur réel.
2. **Selenium**  
Cet outil populaire pour l'automatisation des tests de navigateurs.  
Il fonctionne avec Chrome, Firefox, ... sans tête.  
Il sert à simuler des interactions complexes comme les clics, le défilement ou la saisie de texte.
3. **Playwright**
Cette bibliothèque JavaScript prend aussi en charge Chrome, Firefox, WebKit sans tête.  
Pour les tests automatisés et le scraping avancé.
4. **Headless Chrome** 
Cette version de Google Chrome n'a pas d'interface graphique.  
Contrôlable directement par des outils comme Puppeteer ou des scripts personnalisés.
5. **PhantomJS**
Ce headless browser est basé sur WebKit.  
Bien qu'il soit moins utilisé aujourd'hui, il reste une option pour le web scraping et les tests automatisés.

Ces outils sont particulièrement adaptés pour le scraping de sites dynamiques qui utilisent JavaScript pour charger du contenu. ​ 
___
⚠️ Nonobstant, leur utilisation doit respecter les règles d'éthique et les conditions d'utilisation des sites web.  
Il est crucial de vérifier la légalité du scraping dans la juridiction concernée et d'éviter de surcharger les serveurs des sites web ciblés.