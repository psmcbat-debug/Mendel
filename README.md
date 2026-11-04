# Électricien — 15 pages locales

Site PHP 8.3+, rendu serveur, sans dépendances front-end, compatible MySQL via PDO. Prévisualisation locale sur SQLite.

## État du projet

15 pages locales rédigées (environ 700 à 730 mots chacune), administration, API d’articles et sitemap dynamique. Toutes les pages sont livrées en brouillon. Le nom, le téléphone, les horaires, les tarifs, les mentions légales et les zones desservies restent à confirmer. Aucun avis ni chantier fictif.

196 contrôles d’intégration ont passé sur SQLite, notamment les routes, les métadonnées, les appels, les données structurées, la protection des brouillons, l’API et les sessions. MySQL, HTTPS, les réécritures et les performances réelles doivent encore être vérifiés sur Hostinger.

## Installation Hostinger

1. Créer un site PHP et une base MySQL avec un utilisateur dédié dans hPanel. Activer HTTPS et sa redirection.
2. Placer `app/`, `config/`, `content/`, `scripts/` et `var/` dans le dossier du domaine, **en dehors de `public_html`**. Copier le contenu de `public/` (y compris `.htaccess`) dans `public_html/`.
3. Copier `config/example.php` vers `config/local.php`. Renseigner le DSN MySQL, l’utilisateur et le mot de passe. Garder `environment` à `production`.
4. Activer PHP 8.3 ou plus et les extensions PDO, pdo_mysql et mbstring. Donner à PHP l’accès aux fichiers nécessaires, sans permissions publiques excessives.
5. Choisir deux secrets aléatoires distincts d’au moins 24 caractères. Générer le hash administrateur avec `php scripts/credentials.php admin` et celui du jeton API avec `php scripts/credentials.php api`, en transmettant chaque secret via l’entrée standard. Ne pas mettre les secrets dans les arguments de commande ou Git.
6. En SSH depuis le dossier du domaine, lancer `php scripts/init.php`. Cette commande crée les tables et ajoute les pages absentes ; elle conserve les contenus déjà enregistrés.
7. Ouvrir `/admin/`, compléter l’entreprise, puis chaque page. Confirmer les quartiers réellement desservis, consigner la confirmation dans `coverage_evidence`, renseigner `verified_districts`, puis valider `coverage_verified` et `editorial_verified` avant publication.
8. Tester les appels, la connexion, une publication de brouillon, les canonical, `/robots.txt` et `/sitemap.xml`. Soumettre le sitemap à Search Console après publication.

Sans validation de l’entreprise, le site de production présente une page de préparation avec réponse 503 et noindex. Les pages non validées restent privées ; un administrateur connecté peut les prévisualiser. Le sitemap ne contient que les pages effectivement publiables. Ne pas publier `config/`, `var/` ou `.runtime/` dans le répertoire web.

## Articles et publication à distance

Les articles et pages sont stockés dans la table `pages`, les paramètres dans `settings`. Les modifications de contenu alimentent `audit_log`. Les tentatives de connexion sont limitées et conservées temporairement dans `login_attempts`.

L’API exige HTTPS et `Authorization: Bearer JETON` :

- `GET /api/v1/status` : vérifier le raccordement.
- `GET /api/v1/articles` : lister les articles.
- `GET /api/v1/articles?slug=...` : lire un article.
- `POST /api/v1/articles` : créer ou mettre à jour un article par son slug.

Le format est illustré dans `content/article.example.json`. Le contenu est du texte structuré, sans HTML exécutable. Les publications nécessitent `status: published`, `editorial_verified: true` et les paramètres d’entreprise validés. Un article publié rejoint automatiquement le sitemap. L’API ne peut pas écraser une page locale.

Le script `python scripts/publish_article.py content/article.example.json` envoie un brouillon. Fournir `ELECTRICIEN_SITE_URL` et `ELECTRICIEN_API_TOKEN` dans l’environnement sécurisé de la session ; ajouter `--publish` uniquement pour publier un article relu. Le jeton n’est jamais envoyé dans l’URL et les redirections sont refusées.

Le connecteur Hostinger a été consulté, mais **ce nouveau site n’existe pas encore**. Aucun site existant n’a été modifié. Le raccordement opérationnel de cette API au domaine reste à faire après création du site.

## Prévisualisation et maintenance

Copier la configuration d’exemple et utiliser `environment: local` avec un DSN SQLite et les extensions pdo_sqlite et mbstring. Lancer `php scripts/init.php`, puis `php -S 127.0.0.1:8088 -t public scripts/router.php`.

`php scripts/setup-local.php` génère un accès de test local conservé dans `.runtime/acces-local.json`, jamais versionné. La production doit avoir ses propres secrets.

`content/cities.json` contient les contenus initiaux et leurs sources géographiques. Après initialisation, l’administration modifie la base. Le générateur éditorial `scripts/build_content.py` reconstruit uniquement les fichiers sources, sans écraser la base. `scripts/sync-local.php` est réservé à la maquette et remplace les brouillons non validés : ne pas l’utiliser sur des contenus locaux personnalisés.

Les avis et photos sont facultatifs et masqués tant qu’ils ne sont pas vérifiés. Les photos réelles autorisées se placent dans `public/assets/` au format WebP ou AVIF ; renseigner ensuite les champs `photo` de la page. Le logo utilise également WebP ou AVIF. L’illustration actuelle du tableau est réalisée en CSS et clairement identifiée comme illustration.

Sauvegarder la base MySQL avant toute mise à jour de production. Ne jamais remplacer une base réelle par la base SQLite de prévisualisation.
