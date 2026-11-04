# Reprendre le site et le SEO depuis un autre appareil

Ce fichier est le prompt de reprise. Depuis un PC ou un iPhone, ouvrez une conversation avec un assistant disposant d’un accès en lecture et en écriture à ce dépôt GitHub. Collez le bloc ci-dessous. Un assistant sans accès au dépôt ne pourra pas y enregistrer les modifications.

GitHub conserve le code et les contenus sources. Il n’exécute pas automatiquement ce prompt et ne déploie pas automatiquement le site sur Hostinger.

## Prompt à copier-coller

```text
Tu reprends le développement et le SEO local de mon site d’électricien.
Dépôt de référence : https://github.com/psmcbat-debug/Mendel
Lis d’abord README.md et CONTINUER-LE-PROJET.md dans leur dernière version sur GitHub, puis inspecte les fichiers et les derniers commits. Ne te base pas sur une ancienne copie locale.

OBJECTIF
Améliorer concrètement le site et le SEO pour générer des appels qualifiés autour de Nogent-sur-Marne et du Perreux-sur-Marne. Conserve PHP, PDO/MySQL, le rendu serveur et l’identité visuelle actuelle. Travaille sur l’existant.

MÉTHODE
1. Vérifie les accès au dépôt et récupère la dernière version. Lis les instructions du dépôt si elles existent.
2. Détermine ce qui a réellement été terminé et ce qui reste à faire. Les notes ci-dessous sont un état initial, à confronter au code et au site.
3. Si je fournis une demande précise, exécute-la. Sinon, choisis la prochaine amélioration utile et réalisable, annonce brièvement ton choix et réalise-la jusqu’à un résultat vérifiable.
4. Effectue les vérifications pertinentes et indique précisément celles que tu as exécutées, celles qui ont échoué et celles qui restent impossibles dans ton environnement.
5. Enregistre les changements dans GitHub. Privilégie une branche de travail et une pull request lorsqu’un travail existe déjà sur main. Ne force pas l’historique et ne remplace pas les modifications d’une autre session.
6. Actualise l’état et les prochaines étapes dans README.md. Termine par les liens du commit ou de la pull request, les résultats des tests et ce qui attend encore des informations de ma part.
7. Si un accès manque, progresse sur les tâches indépendantes puis indique le blocage exact. Ne prétends jamais avoir envoyé ou publié sans confirmation du service.

PRIORITÉS À AUDITER
- Fonctionnement des 15 pages, exactitude des quartiers et codes postaux, qualité et différenciation des contenus.
- Appels téléphoniques : liens tel:, visibilité mobile, accessibilité et parcours de conversion.
- Titles, descriptions, H1, canonical, redirections, maillage interne, robots et sitemap.
- Données structurées décrivant exclusivement l’entreprise et les zones réellement confirmées.
- Sécurité de l’administration et de l’API, maintien des contenus en base et sauvegardes.
- Compatibilité Hostinger, vérification MySQL, HTTPS et réécriture des URL.
- Performances réelles sur ordinateur et mobile ; mesurer avant d’annoncer des Core Web Vitals.
- Articles utiles répondant aux questions des clients, sans multiplication artificielle de pages.

INFORMATIONS À RESPECTER
Le nom commercial, le téléphone, le logo, le domaine, les horaires, les délais, les tarifs, les qualifications, les assurances et les zones desservies ne doivent jamais être inventés.
Les informations absentes restent à compléter. Ne coche pas les validations commerciales ou de couverture pour contourner les contrôles.
Ne crée ni faux avis, ni fausses réalisations, ni faux bureaux locaux. Distingue une illustration d’une photo réelle.
Vérifie les repères géographiques dans des sources fiables et conserve leurs liens. Ne déduis pas la desserte de l’entreprise de l’existence d’un quartier.
Ne promets ni classement Google, ni disponibilité 24 h/24, ni délai d’arrivée non vérifié.
Les conseils électriques doivent rester prudents ; ne guide pas un particulier dans une manipulation dangereuse.
Saint-Maur-des-Fossés : cette page cible le 94100 ; La Varenne-Saint-Hilaire en 94210 exige une confirmation distincte.

CONTENUS ET BASE
content/cities.json contient les contenus initiaux. Après installation, les données de la base sont la source des contenus du site en fonctionnement.
Modifier un fichier JSON sur GitHub ne met pas à jour automatiquement une base Hostinger déjà initialisée. scripts/init.php ajoute les pages absentes et conserve les pages existantes.
Pour modifier les contenus en production, utilise l’administration ou une procédure de migration adaptée avec sauvegarde. L’API d’articles ne doit pas être détournée pour modifier les pages locales.
Pour un nouvel article, pars de content/article.example.json et conserve-le en brouillon jusqu’à sa relecture. Ne publie en production que si ma demande le prévoit et si les informations requises sont validées.
Le script scripts/publish_article.py utilise une URL HTTPS et un jeton fournis par un canal sécurisé. Un commit GitHub et une publication Hostinger sont deux actions distinctes.

SÉCURITÉ ET DÉPLOIEMENT
Ne versionne jamais config/local.php, .runtime/, une base réelle, des mots de passe ou des jetons.
Ne demande pas de coller un secret dans un fichier public ou dans la conversation : utilise les paramètres sécurisés disponibles.
Ne déploie pas sur un site Hostinger existant sans identifier le domaine réellement destiné à ce projet.
Prépare et vérifie les changements avant un déploiement. Préserve la base et les contenus existants ; sauvegarde avant toute migration.
N’annonce le raccordement Hostinger ou une publication que si le service en confirme le résultat.

MA DEMANDE POUR CETTE SESSION
Continue à améliorer le site et le SEO à partir de son état actuel. Commence par la prochaine priorité réalisable ; si je donne une consigne supplémentaire, elle définit le périmètre de cette session.
```

## État initial à vérifier lors de chaque reprise

- Site PHP 8.3+, administration, API sécurisée d’articles, sitemap dynamique.
- 15 pages locales initialement livrées en brouillon, avec environ 700 à 730 mots de contenu principal chacune.
- Identité et coordonnées de l’entreprise, couverture, tarifs et horaires encore à confirmer au moment de la création.
- 196 contrôles d’intégration SQLite avaient passé. Le rapport historique figure dans docs/test-report.json ; il ne remplace pas les tests après de nouvelles modifications.
- Le banc tests/integration.py utilisait un runtime PHP et un php.ini dans .runtime/ sur Windows. Ce runtime privé n’est pas dans GitHub : adapter le lancement et les extensions à l’environnement disponible avant d’exécuter les tests.
- La connexion au compte Hostinger a été consultée, mais le nouveau site n’avait pas encore été créé ni déployé.
- Le dépôt contient le code et les contenus sources, pas les secrets ni la base locale.

## Reprise sur PC

Cloner le dépôt, ou récupérer ses dernières modifications avant de travailler. Installer PHP et les extensions nécessaires selon README.md. Ouvrir le dossier dans son outil de développement et utiliser le prompt ci-dessus. Vérifier les changements non enregistrés avant de changer de branche ou de récupérer le travail d’une autre session.

## Reprise sur iPhone

Ouvrir ce fichier sur GitHub et copier le prompt dans une conversation avec un assistant ayant accès au dépôt. Vérifier que cette conversation peut réellement lire et écrire dans Mendel. L’iPhone sert à donner les consignes ; l’exécution de PHP et des tests nécessite un environnement de développement accessible à cet assistant.

Pour une demande ciblée, remplacer la dernière rubrique du prompt par exemple par : « Améliore les différences entre les pages locales, conserve les brouillons et ouvre une pull request », ou « Prépare un article utile en brouillon sur les coupures de courant et ajoute-le au dépôt ».

## Suivi entre les appareils

La dernière version GitHub et les notes du README servent de référence commune. Éviter de lancer deux sessions qui modifient simultanément les mêmes fichiers. Avant chaque reprise, consulter les branches et pull requests ouvertes.
