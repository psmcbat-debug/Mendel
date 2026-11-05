# Électricien — 15 pages locales

Site PHP 8.3+, rendu serveur, sans dépendances front-end, compatible MySQL via PDO. Prévisualisation locale sur SQLite.

## Continuer le projet depuis un PC ou un iPhone

Le prompt de reprise se trouve à la racine du dépôt : **[CONTINUER-LE-PROJET.md](CONTINUER-LE-PROJET.md)**.

Ouvrez ce fichier et copiez le bloc « Prompt à copier-coller » dans une nouvelle conversation avec un assistant ayant accès en lecture et en écriture à ce dépôt GitHub. Il décrit le projet, les priorités SEO, les vérifications et les règles de publication.

Sur PC, vous pouvez aussi cloner le dépôt et ouvrir le dossier dans votre outil de développement. Sur iPhone, utilisez une conversation disposant d’un environnement de travail et de l’accès GitHub ; le téléphone seul n’exécute pas les tests PHP.

GitHub conserve les fichiers : **ajouter un prompt ne déclenche aucun travail automatique**. Une modification sur GitHub ne met pas automatiquement à jour le site ou la base Hostinger. Le déploiement et la publication de contenus sont des étapes distinctes.

## État du projet

15 pages locales rédigées (environ 700 à 730 mots chacune), administration, API d’articles et sitemap dynamique. Toutes les pages sont livrées en brouillon. Le nom, le téléphone, les horaires, les tarifs, les mentions légales et les zones desservies restent à confirmer. Aucun avis ni chantier fictif.

210 contrôles d’intégration ont passé sur SQLite, notamment les routes, les métadonnées, les appels, les données structurées, la protection des brouillons, l’API, les sessions et l’éditeur simple. MySQL, HTTPS, les réécritures et les performances réelles doivent encore être vérifiés sur Hostinger.

### Administration : éditeur simple (5 novembre 2026)

Les pages et articles s’éditent avec des champs pour le titre, l’adresse, les métadonnées SEO, l’introduction, les sections et les FAQ. Les rubriques peuvent être ajoutées ou retirées avec JavaScript ; des rubriques vides permettent aussi de compléter le formulaire sans JavaScript. Les FAQ d’articles sont affichées sur leur page publique.

Pour une ville, le formulaire permet de renseigner les repères, les quartiers réellement desservis et la confirmation de couverture. Les validations de relecture, de couverture et d’entreprise restent obligatoires pour publier. Le formulaire conserve les sources, avis et photos existants. Le lien « Mode avancé (JSON) » permet toujours de modifier ces informations complémentaires. Enregistrez avant de changer de mode : ce changement recharge le contenu enregistré.

Validation de cette évolution : 210 contrôles HTTP avec base isolée SQLite et validation de syntaxe PHP et JavaScript. Essai navigateur effectué : connexion, ajout/retrait de sections, ajout d’une FAQ, sauvegarde, déconnexion et affichage à 390 et 1366 pixels de largeur sans débordement horizontal. Les données de recette sont restées dans une base locale isolée.

Prochaines étapes : ajout des coordonnées réelles de l’entreprise, puis création du site Hostinger et vérifications MySQL/HTTPS avant publication. L’ajout des sources et des preuves pourrait ensuite bénéficier de champs dédiés dans l’éditeur simple.

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

Tests : `python tests/integration.py /chemin/vers/php` utilise le `php.ini` placé à côté de l’exécutable s’il existe. Un second argument permet de fournir un autre `php.ini`. Sans argument, le script recherche PHP dans le PATH puis le runtime local Windows. Les extensions PDO SQLite et mbstring doivent être activées. Les données de test sont créées dans un sous-dossier privé de `var/`.

`content/cities.json` contient les contenus initiaux et leurs sources géographiques. Après initialisation, l’administration modifie la base. Le générateur éditorial `scripts/build_content.py` reconstruit uniquement les fichiers sources, sans écraser la base. `scripts/sync-local.php` est réservé à la maquette et remplace les brouillons non validés : ne pas l’utiliser sur des contenus locaux personnalisés.

Les avis et photos sont facultatifs et masqués tant qu’ils ne sont pas vérifiés. Les photos réelles autorisées se placent dans `public/assets/` au format WebP ou AVIF ; renseigner ensuite les champs `photo` de la page. Le logo utilise également WebP ou AVIF. L’illustration actuelle du tableau est réalisée en CSS et clairement identifiée comme illustration.

Sauvegarder la base MySQL avant toute mise à jour de production. Ne jamais remplacer une base réelle par la base SQLite de prévisualisation.
