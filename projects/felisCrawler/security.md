# Security Policy
## **🔒 Politique de sécurité**
FelisCrawler est un projet **pédagogique** conçu pour l'apprentissage du web scraping. Il n'est pas destiné à un usage en production ou à grande échelle.
## **🛡️ Vulnérabilités connues**
### Aucune vulnérabilité critique
À ce jour, aucune vulnérabilité de sécurité critique n'a été identifiée dans le code du projet.
### **Limitations par design**
* **Pas d'authentification** : L'application Streamlit est locale et non sécurisée
* **Pas de validation d'entrée stricte** : Les paramètres de scraping ne sont pas validés côté serveur
* **Pas de rate limiting applicatif** : Le rate limiting dépend uniquement de Scrapy

Ces limitations sont **acceptables** pour un projet pédagogique local.
## **⚠️ Bonnes pratiques implémentées**
✅ **Respect de robots.txt** : `ROBOTSTXT_OBEY=True` activé par défaut  
✅ **Rate limiting** : Délai configurable entre requêtes (min 0.5s)  
✅ **User-Agent** : User-Agent identifiable pour respecter les serveurs  
✅ **Pas de données sensibles** : Aucune collecte de données personnelles  
✅ **Dépendances à jour** : Requirements.txt maintenu  
## **🐛 Signaler une vulnérabilité**
Si vous découvrez une vulnérabilité de sécurité :
1. **NE PAS** créer une issue publique
2. **Ouvrir une issue** avec le titre "[SECURITY]" sans détails sensibles
3. **Décrire** le problème de manière générale
4. **Attendre** une réponse avant de divulguer publiquement
### Délai de réponse
* Première réponse : **7 jours maximum**
* Correction : **30 jours maximum** (selon la criticité)
## **🚀 Utilisation sécurisée**
### **Recommandations**
* ✅ Utiliser uniquement en **local** (pas d'exposition publique)
* ✅ Respecter les **délais minimum** entre requêtes (≥ 1 seconde)
* ✅ Limiter la **profondeur de crawl** (≤ 5 niveaux)
* ✅ Surveiller la **consommation réseau**
* ❌ Ne **jamais** scraper massivement des sites tiers
* ❌ Ne **jamais** ignorer robots.txt (`ROBOTSTXT_OBEY=False`)
### **Responsabilité**
L'utilisateur est **entièrement responsable** de l'usage qu'il fait de FelisCrawler. Le projet ne peut être tenu responsable :
* D'un bannissement IP par Wikipedia
* D'une violation du RGPD
* D'une utilisation contraire aux CGU de sites tiers
## **📚 Ressources**
[Scrapy Security](https://docs.scrapy.org/en/latest/topics/security.html)  
[Wikipédia - Robots.txt](https://fr.wikipedia.org/robots.txt)  
[OWASP - Web Scraping](https://owasp.org/www-community/attacks/Web_Scraping)
___
<!-- **Version** : 1.0   -->
**Dernière mise à jour** : 2025-11-25