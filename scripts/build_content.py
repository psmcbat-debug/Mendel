"""One-time editorial seed builder. Does not overwrite the database."""
import json
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
records = []

def add(city, slug, postal, districts, neighbors, source, local_title, local, case_title, case, question, answer, note):
    records.append(dict(city=city, slug=slug, postal_code=postal, districts=districts.split('|'), neighbors=neighbors.split('|'), source=source, local_title=local_title, local=local.split('\n\n'), case_title=case_title, case=case.split('\n\n'), question=question, answer=answer, local_note=note))

add('Nogent-sur-Marne','nogent-sur-marne','94130',
'Le Bois-Baltard|Les Viselets|Village|Marne-Beauté|Plaisance-Mairie',
'le-perreux-sur-marne|fontenay-sous-bois|joinville-le-pont',
'https://ville-nogentsurmarne.com/democratie-locale/perimetre-des-quartiers/',
'À Nogent, une adresse précise pour préparer le dépannage',
'''La commune distingue cinq quartiers : Le Bois-Baltard, Les Viselets, Village, Marne-Beauté et Plaisance-Mairie. Ces noms permettent de situer une demande, mais ne remplacent pas une adresse complète. Pour un logement près de la gare de Nogent-sur-Marne ou dans le secteur du port, indiquez la rue, le numéro et l’entrée réellement utilisée. Une entrée de résidence peut être différente de l’adresse postale figurant sur le courrier.

Dans un appartement du Village comme dans une maison des Viselets, la première information utile est l’étendue de la coupure. Le logement entier est-il privé de courant, ou seulement une cuisine, un étage ou une prise ? Si vous habitez en copropriété, demandez si les voisins sont également touchés, sans accéder aux locaux techniques. Cette distinction aide à orienter votre demande entre installation privative, équipement collectif et incident du réseau.

Le quartier Marne-Beauté comprend notamment des voies proches de la Marne. Si votre demande concerne une cave, un garage ou un local ayant subi une entrée d’eau, signalez-le dès le premier échange. N’approchez pas un équipement électrique humide. La proximité du fleuve ne permet pas, à elle seule, de conclure à un défaut : seul l’examen de l’installation peut en déterminer la cause.''',
'Tableau ancien : décrire le défaut plutôt que tout remplacer',
'''Un tableau électrique dont vous ignorez l’âge n’impose pas automatiquement un remplacement complet. Notez ce qui s’est produit avant la panne : utilisation d’un four, démarrage du chauffage ou coupure sans appareil nouveau. Ces éléments guident le diagnostic, sans démonter le coffret ni toucher à ses connexions.

La réparation d’un élément et la mise en sécurité globale répondent à des besoins différents. Demandez que le devis distingue la recherche de panne, la réparation proposée et les améliorations éventuelles. Pour une résidence avec gardien, vérifiez simplement qui peut autoriser l’accès aux espaces communs si cela devient nécessaire.''',
'La gare de Nogent-sur-Marne suffit-elle pour donner mon adresse ?',
'Non. Précisez la rue et le numéro, puis le quartier. Nogent-sur-Marne et Nogent–Le Perreux sont deux repères distincts ; une adresse complète évite une confusion lors de la préparation du déplacement.',
'Cinq quartiers municipaux, du Bois-Baltard à Plaisance-Mairie. La page concerne Nogent-sur-Marne, code postal 94130.')

add('Le Perreux-sur-Marne','le-perreux-sur-marne','94170',
'Secteur Ouest|Secteur Est|Secteur Nord',
'nogent-sur-marne|bry-sur-marne|neuilly-plaisance',
'https://www.leperreux94.fr/page/reunions-de-quartiers',
'Se repérer au Perreux, entre les secteurs Ouest, Est et Nord',
'''Pour ses réunions de quartier, Le Perreux-sur-Marne utilise trois secteurs géographiques : Ouest, Est et Nord. Cette répartition officielle donne un repère simple sans attribuer de limites arbitraires aux quartiers. Lors d’une demande de dépannage, indiquez surtout l’adresse exacte en 94170 et le type de logement. La mention « près de Nogent » est insuffisante pour confirmer la desserte et préparer un déplacement.

Dans le secteur de la gare de Nogent–Le Perreux, prenez soin de préciser la commune de votre adresse. Le nom de la gare réunit deux villes, alors que votre logement dépend d’une adresse bien déterminée. Si le bâtiment possède une entrée côté cour, un portail ou un interphone collectif, préparez ces indications pour le professionnel, sans les publier dans un avis ou sur une page accessible à tous.

Pour une maison comportant plusieurs niveaux, localisez les pièces privées de courant avant l’appel. Une panne au rez-de-chaussée avec un étage encore alimenté ne se décrit pas comme une coupure totale. Signalez également l’existence d’une dépendance ou d’un garage concernés, uniquement si vous le constatez. Cela permet de préparer une recherche ciblée plutôt que de supposer que tout le logement est en défaut.''',
'Une coupure liée au chauffage ou aux appareils de cuisine',
'''Lorsque la coupure survient pendant l’utilisation simultanée de plusieurs appareils, relevez cette circonstance. Une puissance appelée importante, un appareil défectueux ou un défaut du circuit peuvent produire des symptômes proches. Ne remplacez pas vous-même une protection par un modèle plus puissant pour empêcher le déclenchement.

Pour votre dépannage électrique au Perreux, décrivez les équipements qui fonctionnaient et ceux qui restent utilisables. Conservez les références des appareils si elles sont accessibles sans déplacement dangereux. Un diagnostic peut ensuite distinguer la réparation de l’installation d’une question liée à votre contrat d’électricité, qui relève de votre fournisseur.''',
'Mon adresse est près de Nogent–Le Perreux : quel code postal indiquer ?',
'Indiquez 94170 si votre adresse se trouve au Perreux-sur-Marne, puis la rue et le numéro. Le nom de la gare ne permet pas à lui seul de déterminer la commune ni l’entrée du bâtiment.',
'La municipalité regroupe les réunions de quartier en secteurs Ouest, Est et Nord. La couverture de chacun sera validée par l’entreprise.')

add('Bry-sur-Marne','bry-sur-marne','94360',
'La Pépinière|Centre-ville',
'le-perreux-sur-marne|villiers-sur-marne|champigny-sur-marne',
'https://www.brysurmarne.fr/app/uploads/2025/07/CM-du-30-juin-2025-2025DELIB0073-Approbation-du-Projet-Educatif-Territorial-PEDT-2024-2027-et-de-la-convention-relative-au-Projet-Educatif-territorial-et-au-Plan-mercredi.pdf',
'À Bry-sur-Marne, préciser le logement et ses annexes',
'''Le quartier de la Pépinière se situe au nord du pont de Bry. Le document éducatif territorial de la ville y décrit notamment des maisons individuelles. Ce repère géographique ne permet toutefois pas de présumer l’état de leur installation électrique. Pour votre demande, indiquez l’adresse en 94360 et précisez si la panne concerne l’habitation principale, un garage ou une autre partie de la propriété.

Au centre-ville, la préparation d’un dépannage dans un appartement peut demander d’autres renseignements : étage, numéro de bâtiment et présence d’un interlocuteur sur place. Si un local commercial occupe le rez-de-chaussée, vérifiez seulement si votre logement et ce local semblent touchés au même moment. Leurs alimentations peuvent être distinctes ; leur proximité ne prouve pas une origine commune de la panne.

Dans le secteur de la Pépinière, un éclairage extérieur ou une prise de garage peut être concerné sans que les pièces de vie soient privées de courant. Notez cette différence et signalez toute exposition à l’eau. Ne manipulez pas un appareillage humide pour tenter de le tester. Un électricien doit pouvoir examiner le circuit en sécurité avant de proposer une réparation ou un remplacement adapté.''',
'Une prise extérieure qui ne fonctionne plus',
'''Une prise inutilisable peut présenter un défaut de connexion, être liée à un circuit coupé ou dépendre d’une protection déclenchée. L’aspect extérieur ne suffit pas à conclure. Si vous observez une trace noire, un boîtier cassé ou une odeur inhabituelle, cessez d’utiliser l’équipement et tenez les occupants à distance.

Pour préparer le remplacement d’une prise électrique à Bry-sur-Marne, indiquez son emplacement et l’appareil habituellement branché. Le choix du matériel dépend de son environnement et de l’installation existante. Un remplacement à l’identique n’est pas nécessairement la solution correcte si l’origine du problème se trouve ailleurs sur le circuit.''',
'Puis-je demander un diagnostic pour un garage à la Pépinière ?',
'Précisez que la demande concerne un garage, son accès et les symptômes constatés. La desserte exacte et le périmètre du diagnostic doivent être confirmés lors de l’appel ; le nom du quartier ne vaut pas confirmation d’intervention.',
'La Pépinière, au nord du pont de Bry, et le centre-ville servent de repères. L’adresse exacte reste nécessaire pour confirmer une intervention.')

add('Champigny-sur-Marne','champigny-sur-marne','94500',
'Coeuilly|Le Plant|Le Plateau|Les Mordacs|Le Tremblay|Polangis|Centre-ville - Coteaux',
'joinville-le-pont|saint-maur-des-fosses|villiers-sur-marne',
'https://www.champignysurmarne.fr/connaitre-champigny/ma-mairie/la-ville-et-ses-quartiers',
'Des repères distincts, de Coeuilly au Tremblay',
'''Champigny-sur-Marne comprend des quartiers aux noms bien identifiés par la municipalité, notamment Coeuilly, Le Plant, Le Plateau, Les Mordacs et Le Tremblay. Leur nom aide à situer votre logement, mais une demande de dépannage électrique doit conserver la rue et le numéro en 94500. Le secteur annoncé ne permet pas de déduire un délai d’arrivée : celui-ci dépend de la disponibilité réelle et des conditions du déplacement.

Un point mérite une attention particulière : Polangis se répartit sur Champigny-sur-Marne et Joinville-le-Pont. Pour un logement dans ce secteur, vérifiez la commune indiquée sur votre adresse. Dire seulement « Polangis » peut orienter la demande vers la mauvaise ville. Ce détail est également utile pour établir correctement un devis et identifier le lieu exact des travaux.

Dans une résidence du Plateau ou des Mordacs, indiquez le bâtiment concerné et la présence éventuelle d’une panne des parties communes. Dans une maison de Coeuilly, décrivez plutôt les niveaux et les équipements touchés. Ces renseignements sont des indications pratiques : ils ne supposent ni une panne particulière dans un quartier ni une intervention déjà réalisée par l’entreprise.''',
'Distinguer une panne de logement d’un équipement collectif',
'''Si l’éclairage de la cage d’escalier ne fonctionne plus alors que votre appartement reste alimenté, prévenez le gestionnaire de l’immeuble. Une recherche de panne dans les parties communes ne se commande pas comme le remplacement d’une prise de votre logement. L’accès au local électrique et l’accord de l’interlocuteur compétent peuvent être nécessaires.

À l’inverse, une pièce seule privée de courant peut relever de votre installation intérieure. Pour le diagnostic, notez si les prises et l’éclairage de cette pièce sont tous concernés. Évitez de multiplier les essais : des symptômes précis sont plus utiles qu’une succession de réarmements du disjoncteur.''',
'Polangis est-il à Champigny ou à Joinville ?',
'Le quartier se répartit sur les deux communes. Pour une adresse à Champigny-sur-Marne, indiquez 94500 avec la rue et le numéro. L’entreprise confirmera ensuite si l’adresse fait partie de sa zone réelle.',
'La page cible le 94500. Polangis étant partagé avec Joinville-le-Pont, la commune doit toujours être précisée.')

add('Joinville-le-Pont','joinville-le-pont','94340',
'Polangis|Palissy|Île Fanac',
'champigny-sur-marne|nogent-sur-marne|saint-maur-des-fosses',
'https://www.joinville-le-pont.fr/vie-municipale/territoire/les-differents-quartiers/',
'À Joinville, tenir compte de l’accès réel au logement',
'''La ville présente Polangis, Palissy et l’Île Fanac parmi les quartiers du bas de Joinville, en relation avec la Marne. Pour un dépannage électrique, ces repères permettent de situer l’adresse sans remplacer la préparation de l’accès. Indiquez votre rue, le numéro et le code postal 94340, puis l’entrée utilisée par les visiteurs. Un accès piéton ou un passage particulier doit être signalé avant le déplacement.

Pour une adresse sur l’Île Fanac, décrivez concrètement comment rejoindre le bâtiment et convenez d’un point de rencontre si nécessaire. Ne supposez pas qu’un véhicule puisse accéder jusqu’au logement. Cette information peut influencer l’organisation du transport du matériel ; elle ne justifie aucune promesse de délai tant que le professionnel n’a pas étudié la demande.

À Polangis, la limite avec Champigny-sur-Marne rend la commune particulièrement importante. La municipalité de Joinville décrit son quartier, tandis que le nom Polangis est aussi utilisé côté Champigny. Reprenez l’adresse figurant sur vos documents. Pour un immeuble de Palissy, ajoutez le bâtiment et l’étage afin que l’examen de la panne puisse commencer au bon endroit.''',
'Après une entrée d’eau, éviter la remise sous tension',
'''Si une pièce ou un équipement a été mouillé, indiquez-le avant toute demande de remise en service. Une installation qui paraît sèche en surface peut nécessiter un contrôle. Ne touchez pas les prises, interrupteurs ou appareils atteints et n’entrez pas dans une zone inondée pour atteindre le tableau.

Le dépannage après une coupure d’électricité doit alors commencer par l’évaluation de la situation et la mise en sécurité nécessaire. Une réparation immédiate n’est pas toujours possible. Décrivez les pièces concernées et la chronologie de l’événement ; le professionnel pourra préciser les vérifications utiles sans tirer de conclusion à distance.''',
'Quelles informations préparer pour une adresse sur l’Île Fanac ?',
'Préparez l’adresse complète, l’accès piéton et les coordonnées de la personne présente. Le transport du matériel et la faisabilité du déplacement doivent être discutés ; aucune durée d’arrivée ne peut être déduite du seul quartier.',
'Polangis, Palissy et l’Île Fanac sont des repères municipaux. Les conditions d’accès et la couverture restent à confirmer adresse par adresse.')

add('Fontenay-sous-Bois','fontenay-sous-bois','94120',
'Rigollots|Roublot|Carrières',
'vincennes|nogent-sur-marne|rosny-sous-bois',
'https://www.fontenay.fr/citoyennete-vie-associative/vie-des-quartiers/rigollots-roublot-carrieres-2156.html',
'Rigollots, Roublot, Carrières : préciser le secteur et le circuit',
'''À Fontenay-sous-Bois, le conseil de quartier Rigollots–Roublot–Carrières regroupe des repères utilisés par les habitants. La Ville cite notamment la Halle Roublot et l’Éco-parc des Carrières René-Dumont parmi ses équipements. Ces lieux servent à situer une adresse ; ils ne désignent pas un lieu d’implantation de l’entreprise ni un chantier réalisé. Votre demande doit donc préciser la rue et le numéro en 94120.

Si votre appartement se trouve dans un bâtiment accessible depuis une cour, indiquez l’entrée concernée et l’étage. Un commerce ou un équipement municipal voisin peut aider à reconnaître la rue, mais ne doit pas remplacer l’adresse. Pour confirmer la possibilité d’un dépannage dans un autre secteur de Fontenay, communiquez directement l’adresse : la présence d’une page locale ne signifie pas que tous les quartiers ont déjà été validés.

Avant l’appel, distinguez une panne d’éclairage d’une panne de prises. Dans une même pièce, ces équipements peuvent être alimentés par des circuits différents. Si seule une commande murale ne répond plus, décrivez également les autres interrupteurs qui commandent le même éclairage. Cette observation permet de préparer le diagnostic sans retirer une plaque ni accéder aux conducteurs.''',
'Un interrupteur défaillant n’implique pas toujours un luminaire à changer',
'''Un éclairage qui reste éteint peut avoir plusieurs origines : lampe, alimentation, commande ou connexion. Précisez si la panne est permanente, intermittente ou apparue après un changement de luminaire. Ne cherchez pas à resserrer des fils vous-même et n’utilisez plus une commande présentant un échauffement ou une trace inhabituelle.

Pour une réparation d’interrupteur à Fontenay-sous-Bois, indiquez s’il existe plusieurs points de commande, un variateur ou un détecteur. Le matériel doit être compatible avec le circuit et l’usage. Demandez que le devis identifie l’équipement remplacé et la vérification effectuée, plutôt qu’un simple intitulé trop général.''',
'La Halle Roublot suffit-elle pour localiser mon dépannage ?',
'C’est un repère du quartier, mais il faut donner l’adresse de votre logement en 94120. Indiquez aussi l’entrée et l’étage ; la desserte sera confirmée pour cette adresse, et non pour le seul monument voisin.',
'Repères vérifiés : le secteur Rigollots–Roublot–Carrières et ses équipements municipaux. Aucun bureau de l’entreprise n’y est revendiqué.')

add('Vincennes','vincennes','94300',
'Vignerons|Saint-Louis-Bérault|Daumesnil|Centre-ville|Diderot - Domaine du Bois',
'saint-mande|fontenay-sous-bois|nogent-sur-marne',
'https://www.vincennes.fr/rencontre-de-quartier',
'Cinq quartiers pour situer votre demande à Vincennes',
'''Vincennes distingue cinq quartiers : Vignerons, Saint-Louis-Bérault, Daumesnil, Centre-ville et Diderot–Domaine du Bois. Le découpage municipal permet de nommer votre secteur avec précision. Pour obtenir un dépannage électrique, ajoutez toujours le numéro et la rue en 94300. Une adresse proche de la limite de Saint-Mandé ou de Fontenay-sous-Bois doit conserver sa commune exacte, même si un repère voisin est plus connu.

Dans un immeuble, une panne peut concerner un appartement, un palier ou plusieurs étages. Demandez à votre entourage ce qui est touché, sans intervenir sur l’armoire collective. Si votre logement fonctionne mais que le hall est éteint, le syndic ou le gardien est un interlocuteur utile. Si une seule prise de votre appartement pose problème, décrivez plutôt son emplacement et l’usage habituel.

Pour un local professionnel du centre-ville, précisez l’horaire d’accès et les équipements dont l’arrêt gêne l’activité. Une demande urgente ne permet pas de promettre une arrivée immédiate. La disponibilité, les conditions du déplacement et la nature de la réparation doivent être convenues au téléphone. Les quartiers cités servent à préparer la confirmation de desserte, sans prétendre à des interventions déjà réalisées.''',
'En copropriété, faire préciser le périmètre du diagnostic',
'''Avant la venue d’un électricien à Vincennes, identifiez la personne qui autorise les travaux. Une réparation dans votre logement et une intervention sur un équipement commun n’engagent pas nécessairement le même interlocuteur. Conservez les coordonnées de votre gestionnaire si un accès partagé doit être organisé.

Lorsque le disjoncteur saute dans votre appartement, notez les pièces affectées et le moment du déclenchement. Évitez de conclure que le tableau entier est hors service. Le devis doit permettre de comprendre ce qui est contrôlé et ce qui serait remplacé. Une demande d’amélioration générale peut faire l’objet d’un échange séparé du dépannage initial.''',
'Dans quel quartier se trouve mon adresse de Vincennes ?',
'La Ville distingue Vignerons, Saint-Louis-Bérault, Daumesnil, Centre-ville et Diderot–Domaine du Bois. Si vous hésitez, donnez simplement votre adresse complète en 94300 ; elle est plus utile qu’un nom de quartier approximatif.',
'Les cinq quartiers proviennent du découpage municipal. Chaque desserte doit être confirmée avant la publication commerciale de la page.')

add('Saint-Mandé','saint-mande','94160',
'Secteur avenue du Général-de-Gaulle|Secteur avenue Victor-Hugo|Secteur rue Sacrot',
'vincennes|charenton-le-pont|fontenay-sous-bois',
'https://www.saintmande.fr/pratique/stationnement-et-mobilite/stationnement',
'Des repères de rue pour votre dépannage à Saint-Mandé',
'''À Saint-Mandé, l’avenue du Général-de-Gaulle, l’avenue Victor-Hugo et la rue Sacrot constituent des repères vérifiables dans les informations municipales de stationnement. Nous les utilisons ici comme secteurs de rue, sans les présenter comme un découpage officiel en quartiers. Pour préparer un déplacement, l’adresse complète en 94160 reste la référence, accompagnée de l’entrée du bâtiment et de l’étage.

Le stationnement fait l’objet de règles locales qui peuvent évoluer. Ne garantissez pas une place sur la voie publique à un professionnel sans savoir si elle est autorisée. Si votre immeuble dispose d’un accès particulier ou d’un emplacement utilisable avec accord, indiquez-le au moment de la prise de rendez-vous. Ces précisions facilitent l’organisation, mais ne remplacent pas la confirmation du créneau.

Dans un appartement, décrivez si le défaut concerne la lumière, une prise isolée ou l’ensemble du logement. Pour une panne qui apparaît seulement certains soirs, notez les appareils utilisés et l’heure approximative. Le professionnel pourra examiner ces indices lors du diagnostic. Le nom d’une avenue ne permet jamais de déduire l’âge de votre installation ni de recommander automatiquement une rénovation complète.''',
'Une panne intermittente : conserver des observations utiles',
'''Un défaut qui disparaît puis revient peut être difficile à reproduire lors de la visite. Relevez ce qui change : appareil mis en route, bruit anormal, coupure limitée à une pièce ou déclenchement au tableau. Une courte description datée aide davantage qu’une photographie prise en démontant un équipement.

Pour un diagnostic d’installation électrique à Saint-Mandé, demandez ce qui sera recherché et comment les résultats seront expliqués. Ne maintenez pas en service un appareil qui chauffe anormalement ou produit des étincelles pour « montrer la panne ». La sécurité des occupants passe avant la reproduction du défaut.''',
'Les secteurs cités sont-ils des quartiers officiels de Saint-Mandé ?',
'Non : il s’agit ici de repères de rue tirés des informations municipales. La rue et le numéro en 94160 permettent de confirmer la zone d’intervention sans inventer un découpage administratif.',
'Les repères correspondent à des axes réels. Ils ne constituent pas une liste officielle de quartiers ni une couverture déjà validée.')

add('Saint-Maur-des-Fossés','saint-maur-des-fosses','94100',
'Adamville|Le Vieux Saint-Maur|Saint-Maur Créteil|La Pie|Le Parc',
'joinville-le-pont|champigny-sur-marne|maisons-alfort',
'https://www.saint-maur.com/ma-mairie/decouvrir-saint-maur/la-ville-de-saint-maur',
'Saint-Maur : distinguer le 94100 de La Varenne en 94210',
'''Saint-Maur-des-Fossés comprend huit quartiers, dont Adamville, Le Vieux Saint-Maur, Saint-Maur Créteil, La Pie et Le Parc. Cette page cible les demandes en 94100. La Varenne-Saint-Hilaire utilise le code postal 94210 : il ne faut donc pas attribuer automatiquement 94100 à toutes les adresses de la commune. Le code postal figurant sur votre adresse permet de préparer correctement le devis et la confirmation de desserte.

Pour une maison d’Adamville ou de La Pie, précisez si les circuits concernés alimentent l’habitation, un garage ou un espace extérieur. Pour un appartement près de Saint-Maur Créteil, indiquez le bâtiment et l’accès réel. Ces indications sont utiles à l’organisation, sans supposer que les installations d’un quartier présentent toutes les mêmes caractéristiques.

Le nom « Saint-Maur » est parfois utilisé seul dans une conversation. Lors d’un appel de dépannage, donnez le quartier puis l’adresse complète. Si votre logement est en 94210, faites confirmer séparément cette couverture : une page ciblant 94100 ne constitue pas une validation pour La Varenne. Cette distinction évite une extension implicite de la zone annoncée et facilite une réponse adaptée à votre situation.''',
'Un circuit de dépendance peut demander une recherche séparée',
'''Lorsque la maison reste alimentée et que seul le garage est privé de courant, décrivez cette différence. Ne supposez pas que la panne provient du compteur. Un professionnel doit identifier le circuit et les protections concernés avant de déterminer si une réparation de connexion, un remplacement d’équipement ou une autre opération est nécessaire.

Si vous préparez également une amélioration de l’installation, distinguez ce projet de l’urgence du jour. Le dépannage vise à traiter le défaut constaté ; une mise en sécurité plus large nécessite un périmètre explicite. Demandez que ces deux besoins soient clairement séparés dans l’explication et, si nécessaire, dans le devis.''',
'Cette page couvre-t-elle automatiquement La Varenne-Saint-Hilaire ?',
'Non. La page cible Saint-Maur-des-Fossés en 94100. Pour La Varenne-Saint-Hilaire en 94210, indiquez votre adresse et demandez une confirmation spécifique de la desserte avant d’organiser une intervention.',
'Cible principale : 94100. La Varenne-Saint-Hilaire (94210) nécessite une confirmation distincte et n’est pas incluse par défaut.')

add('Maisons-Alfort','maisons-alfort','94700',
'Centre-ville|Alfort|Charentonneau|Les Juilliottes',
'charenton-le-pont|saint-maur-des-fosses|joinville-le-pont',
'https://maisons-alfort.fr/votre-ville-votre-mairie/decouvrir-maisons-alfort/portrait-en-images/',
'À Maisons-Alfort, ne pas confondre commune et repère de quartier',
'''La Ville présente notamment le Centre-ville, Alfort, Charentonneau et Les Juilliottes dans son portrait du territoire. Ces repères aident à situer une demande de dépannage électrique en 94700. Le quartier d’Alfort appartient à Maisons-Alfort : son nom ne doit pas être confondu avec la commune voisine d’Alfortville. Reprendre votre adresse complète évite ce type d’erreur lors du premier appel.

Dans une résidence des Juilliottes, précisez le bâtiment, l’entrée et la pièce touchée par la panne. Si votre demande concerne une maison de Charentonneau, indiquez si l’installation comprend un garage ou un autre volume concerné. Il s’agit de renseignements à adapter au logement réel, sans généraliser l’état électrique à partir du quartier.

Une coupure après le branchement d’un nouvel appareil ne signifie pas nécessairement que cet appareil est seul en cause. Notez ce qui fonctionnait auparavant et si d’autres équipements se sont arrêtés au même moment. Les symptômes, l’adresse et les possibilités d’accès constituent les informations les plus utiles pour confirmer la demande. Le tarif et le créneau devront être précisés par l’entreprise, en fonction du besoin constaté.''',
'Prise de cuisine : expliquer l’usage avant le remplacement',
'''Pour une prise utilisée par un lave-vaisselle, un four ou un autre équipement de cuisine, précisez l’appareil concerné sans le déplacer si l’accès est difficile. Une prise défectueuse ne doit pas être remplacée au hasard par un modèle choisi uniquement pour son apparence. Le professionnel doit vérifier les conditions du circuit et la compatibilité du matériel.

Signalez tout échauffement, faux contact ou trace visible. N’ajoutez pas une multiprise pour contourner durablement le problème. Le dépannage doit rechercher la cause, puis expliquer la réparation retenue. Si l’appareil lui-même semble défaillant, un réparateur d’électroménager peut être nécessaire après identification de l’origine.''',
'Alfort et Alfortville désignent-ils la même adresse ?',
'Non. Alfort est un quartier de Maisons-Alfort, tandis qu’Alfortville est une autre commune. Pour cette page, donnez l’adresse complète à Maisons-Alfort et le code postal 94700, puis votre quartier si vous le connaissez.',
'Centre-ville, Alfort, Charentonneau et Les Juilliottes sont des repères municipaux. Le code postal ciblé est 94700.')

add('Charenton-le-Pont','charenton-le-pont','94220',
'Bercy|Valmy|Conflans|Plateau de Gravelle|Les Carrières|Centre ancien|Quartier du Pont',
'maisons-alfort|saint-mande|vincennes',
'https://www.val-de-marne.gouv.fr/content/download/21037/140381/file/Partie%202-1.pdf',
'À Charenton, identifier le bon côté du bâtiment',
'''Les documents d’urbanisme de Charenton-le-Pont identifient notamment Bercy, Valmy, Conflans, le Plateau de Gravelle, Les Carrières, le Centre ancien et le Quartier du Pont. Pour une demande en 94220, ces noms donnent un contexte géographique. Ils ne prouvent pas une présence permanente de l’entreprise dans chacun de ces secteurs : la desserte doit être confirmée à partir de votre adresse.

Le nom Bercy peut désigner un secteur parisien ou charentonnais selon le contexte. Indiquez donc explicitement Charenton-le-Pont et le code postal de votre logement. Pour un immeuble dont l’accès se fait par une cour ou une autre rue, précisez l’entrée utilisée. Cette information est particulièrement utile lorsque l’adresse administrative ne correspond pas à l’endroit où un intervenant doit se présenter.

Si le défaut concerne un local commercial, un bureau ou une partie commune, expliquez l’usage du lieu et indiquez qui peut autoriser les travaux. Un diagnostic d’installation privative ne couvre pas automatiquement l’ensemble des équipements du bâtiment. Préparer ce périmètre permet de demander une prestation adaptée et d’éviter une incompréhension sur le déplacement ou les accès nécessaires.''',
'Tableau électrique : isoler le besoin de réparation',
'''Une odeur anormale, un déclenchement répété ou un circuit indisponible doivent être décrits avec précision. Ne retirez pas le capot du tableau pour rechercher l’origine. Si l’équipement présente un signe de danger, éloignez-vous et faites prendre en charge la situation par un professionnel ou les secours selon l’urgence.

La réparation d’un tableau électrique à Charenton peut concerner un composant ou demander une analyse plus large. Aucun remplacement complet ne doit être déduit d’une simple conversation. Demandez quelles observations justifient la solution proposée et quelles vérifications sont prévues après les travaux, puis examinez le devis avant d’accepter.''',
'Une demande « à Bercy » suffit-elle pour Charenton-le-Pont ?',
'Non. Le nom peut aussi évoquer Paris. Donnez Charenton-le-Pont, 94220, la rue et le numéro. Ajoutez l’accès réel au bâtiment pour que la desserte et les conditions du déplacement soient confirmées sans ambiguïté.',
'Les secteurs cités figurent dans les documents d’urbanisme. La page concerne Charenton-le-Pont en 94220, et non Paris-Bercy.')

add('Neuilly-Plaisance','neuilly-plaisance','93360',
'Plateau d’Avron|Centre-ville|Secteur des bords de Marne',
'rosny-sous-bois|neuilly-sur-marne|le-perreux-sur-marne',
'https://www.mairie-neuillyplaisance.com/images/pdf/GUIDE_NP_2021_Rogne.pdf',
'Du Plateau d’Avron aux bords de Marne : l’adresse avant l’itinéraire',
'''Le guide municipal de Neuilly-Plaisance décrit la voie Lamarque comme un cheminement entre les bords de Marne, le centre-ville et les coteaux d’Avron. Ce repère permet de comprendre les différents secteurs de la commune. Il s’agit d’un itinéraire de promenade, pas d’un accès automobile à proposer pour un dépannage. Donnez plutôt la rue effectivement accessible et l’entrée de votre logement en 93360.

Le Plateau d’Avron est un repère connu, mais le nom du secteur ne suffit pas pour organiser un déplacement. Précisez le numéro, le portail et les éventuelles modalités d’accès privé. Pour une adresse près de la gare, indiquez également la commune : Neuilly-Plaisance, Neuilly-sur-Marne et Neuilly-sur-Seine sont des villes distinctes, malgré la proximité de leurs noms.

Si votre panne touche une maison et une annexe, décrivez séparément ce qui fonctionne dans chaque espace. Une dépendance privée de courant n’implique pas nécessairement une panne du réseau public. À l’inverse, plusieurs habitations touchées simultanément justifient de consulter les incidents du réseau avant de demander un déplacement pour votre seule installation intérieure.''',
'Préparer un dépannage sans improviser un raccordement provisoire',
'''En attendant un diagnostic, ne tirez pas une rallonge depuis une zone humide ni depuis un voisin pour alimenter durablement un circuit défaillant. Cela peut créer d’autres risques et ne résout pas le défaut initial. Notez les équipements essentiels devenus indisponibles pour expliquer votre besoin lors de l’appel.

Le professionnel pourra distinguer la recherche de panne de la réparation et préciser les limites d’une éventuelle remise en service. Pour un circuit extérieur, donnez son usage et les circonstances du défaut. La mise en sécurité peut être prioritaire même si elle ne permet pas de rétablir immédiatement tous les équipements.''',
'La voie Lamarque peut-elle servir d’accès à un véhicule de dépannage ?',
'Ne la proposez pas comme accès automobile : le guide municipal la décrit comme un cheminement de promenade soumis à des restrictions. Communiquez la rue d’accès réelle et demandez au professionnel de confirmer l’organisation du déplacement.',
'Plateau d’Avron, centre-ville et bords de Marne : trois repères à distinguer. Neuilly-Plaisance correspond au code postal 93360.')

add('Neuilly-sur-Marne','neuilly-sur-marne','93330',
'Maison Blanche|Les Fauvettes|Centre ancien|Primevères - Maltournée',
'neuilly-plaisance|bry-sur-marne|le-perreux-sur-marne',
'https://www.neuillysurmarne.fr/conseil-de-quartier/',
'À Neuilly-sur-Marne, une entrée précise dans les résidences',
'''Maison Blanche figure parmi les secteurs des conseils de quartier de Neuilly-sur-Marne. Les documents d’aménagement municipaux identifient aussi le centre ancien, Les Fauvettes et Primevères–Maltournée. Ces repères situent votre demande en 93330 ; ils n’indiquent pas que chaque résidence est déjà desservie. La couverture réelle doit être confirmée avant de publier une affirmation commerciale sur l’intervention dans un secteur.

Pour une résidence de Maison Blanche ou des Fauvettes, préparez le nom du bâtiment, le numéro d’entrée et l’étage. Le nom de la résidence peut regrouper plusieurs accès. Indiquez celui qui mène au logement concerné, puis vérifiez qu’une personne pourra accueillir le professionnel. Les codes d’entrée se communiquent directement au moment utile et ne doivent pas apparaître dans un avis public.

Si votre demande concerne les parties communes, signalez-le dès le départ. Une panne du hall, du portail ou d’un équipement partagé peut nécessiter l’accord et l’organisation du gestionnaire. Ne cherchez pas à ouvrir une armoire technique pour identifier vous-même le circuit. Dans un logement, limitez vos observations aux symptômes visibles et aux pièces qui restent alimentées.''',
'Un logement récent peut aussi nécessiter une recherche de panne',
'''L’âge supposé d’un bâtiment ne permet pas de diagnostiquer un défaut. Une protection qui déclenche peut être liée à un appareil, à une connexion ou à un autre problème électrique. Décrivez ce qui s’est passé avant la coupure et indiquez si des travaux ou un nouvel équipement l’ont précédée.

Conservez les documents de votre installation si vous en disposez, sans conclure vous-même à la responsabilité d’un intervenant. Le diagnostic doit établir des observations. Pour une réparation proposée, demandez une explication claire du périmètre et des contrôles prévus ; l’urgence ne dispense pas de comprendre le devis.''',
'Maison Blanche désigne-t-il une adresse suffisante pour intervenir ?',
'Non. Ce secteur comprend plusieurs lieux et accès. Indiquez Neuilly-sur-Marne, 93330, la rue, le numéro et le bâtiment. Ces détails permettent de confirmer la desserte et de préparer l’arrivée à la bonne entrée.',
'Repères : Maison Blanche, Les Fauvettes, centre ancien et Primevères–Maltournée. À ne pas confondre avec Neuilly-Plaisance (93360).')

add('Villiers-sur-Marne','villiers-sur-marne','94350',
'Les Hautes-Noues',
'bry-sur-marne|champigny-sur-marne|le-perreux-sur-marne',
'https://www.villiers94.fr/decouvrir-villiers/grands-projets/le-pru-des-hautes-noues/',
'Aux Hautes-Noues et à Villiers, décrire l’accès actuel',
'''La Ville de Villiers-sur-Marne présente le renouvellement urbain des Hautes-Noues parmi ses projets de quartier, avec un travail sur les rues et les accès. Cette information invite à communiquer l’entrée réellement utilisée aujourd’hui, plutôt qu’un ancien repère. Nous ne présumons pas de travaux ou de restrictions encore en cours : pour votre demande, décrivez simplement ce que vous constatez sur place.

Dans une résidence, notez la rue, le numéro du bâtiment et le code postal 94350. Si un nom de résidence figure sur les documents mais pas sur l’interphone, précisez cette différence lors de l’appel. La couverture des Hautes-Noues et des autres adresses de Villiers doit être confirmée par l’entreprise avant publication ; une commune ciblée pour le référencement n’est pas une preuve de desserte.

Pour un logement récemment aménagé, indiquez si la panne est apparue après un déplacement d’appareil, des travaux ou une remise en service. Ces circonstances aident à préparer le diagnostic sans préjuger de l’origine du problème. Conservez les informations déjà disponibles sur les circuits, mais n’enlevez aucune protection pour compléter votre description. L’accès aux conducteurs relève du professionnel.''',
'Après des travaux, distinguer coïncidence et défaut constaté',
'''Une coupure survenue après une intervention dans le logement mérite d’être décrite précisément. Notez la date, les pièces concernées et les équipements qui fonctionnaient avant. Le lien chronologique est utile, mais il ne prouve pas à lui seul la cause de la panne ni la responsabilité d’une personne.

Pour un dépannage électrique à Villiers-sur-Marne, rassemblez le devis ou les schémas dont vous disposez si cela aide à comprendre l’installation. Demandez ensuite au professionnel de détailler ses observations et la réparation proposée. Une prise, un interrupteur et un tableau ne se remplacent pas tous selon le même diagnostic.''',
'Que préciser pour une intervention aux Hautes-Noues ?',
'L’adresse en 94350, le bâtiment, l’entrée actuelle et la personne présente sur place. Si un accès a changé, décrivez-le. La page municipale sur le quartier ne renseigne ni la disponibilité de l’électricien ni son temps d’arrivée.',
'Les Hautes-Noues constituent un repère documenté. Les autres quartiers pourront être ajoutés après vérification géographique et confirmation de leur desserte.')

add('Rosny-sous-Bois','rosny-sous-bois','93110',
'Centre-ville|Plateau d’Avron|Beauséjour|La Boissière|Bois-Perrier',
'neuilly-plaisance|fontenay-sous-bois|neuilly-sur-marne',
'https://www.rosnysousbois.fr/minformer-sur-ma-ville/ma-ville/vie-democratique/democratie-de-proximite/',
'À Rosny, préciser la commune au-delà du Plateau d’Avron',
'''Les informations municipales de démocratie de proximité regroupent notamment Centre-ville, Plateau d’Avron et Beauséjour, et identifient La Boissière. Bois-Perrier est également un repère de la ville. Lors d’un appel, indiquez Rosny-sous-Bois et 93110 avant de préciser votre secteur. Le Plateau d’Avron est aussi associé à Neuilly-Plaisance : son nom seul ne permet pas de déterminer l’adresse d’intervention.

Dans une résidence de Bois-Perrier ou de La Boissière, ajoutez le bâtiment et l’accès du logement concerné. Si plusieurs halls portent des numéros proches, précisez celui à utiliser. Pour une maison du secteur de Beauséjour, indiquez si le défaut touche aussi un garage ou une installation extérieure. Ces détails décrivent la situation réelle, sans supposer un type de panne propre à chaque quartier.

Une panne annoncée « près de Rosny » doit être localisée avant de confirmer le déplacement. Donnez la commune de votre adresse, même si votre repère habituel se trouve dans une ville voisine. Les modalités de desserte, de disponibilité et de tarification seront alors examinées pour le bon lieu. Aucun temps d’arrivée ne peut être déduit de la distance apparente sur une carte.''',
'Une coupure complète ne relève pas toujours du tableau',
'''Si tout le logement est privé d’électricité, vérifiez d’abord si d’autres logements sont concernés, sans toucher aux équipements collectifs. Un incident du réseau public et une panne intérieure ne demandent pas la même prise en charge. Le service d’information d’Enedis aide à rechercher un incident annoncé à votre adresse.

Lorsque le courant revient mais qu’un circuit reste inutilisable, notez cette évolution. Le dépannage après coupure peut porter sur ce défaut résiduel. Ne forcez pas une protection à rester en position marche. Décrivez ce qui est revenu et ce qui reste indisponible afin de préparer un diagnostic ciblé.''',
'Le Plateau d’Avron permet-il de distinguer Rosny de Neuilly-Plaisance ?',
'Non. Précisez Rosny-sous-Bois et 93110, puis la rue et le numéro. Ce repère géographique est associé à plusieurs secteurs ; la commune exacte évite de confirmer une intervention sur la mauvaise adresse.',
'La page vise Rosny-sous-Bois en 93110. Le Plateau d’Avron ne doit pas être utilisé seul pour identifier la commune.')

services = [
    'Le dépannage électrique d’urgence commence par la description de la panne et la confirmation de la disponibilité. La recherche et réparation de panne de courant vise à identifier le circuit ou l’équipement en défaut. Un disjoncteur qui saute peut signaler des causes différentes ; un court-circuit ne se confirme pas sur une simple impression. Ne bloquez jamais une protection et ne répétez pas les réarmements si le défaut revient.',
    'La réparation de tableau électrique, le remplacement de prises électriques et les problèmes d’interrupteurs demandent un examen de l’installation concernée. Le diagnostic d’installation électrique permet de préciser les anomalies observées. La mise en sécurité électrique traite les risques identifiés selon le périmètre convenu. Elle ne doit pas être confondue avec une rénovation complète ou un diagnostic immobilier réglementaire.',
    'Le dépannage après une coupure d’électricité concerne l’installation intérieure lorsqu’un défaut y subsiste. Une panne du réseau public relève du gestionnaire de réseau. En présence de fumée, d’étincelles ou d’un équipement humide, restez à distance et demandez une prise en charge adaptée à l’urgence. Ne démontez ni prise ni tableau pour tenter une réparation.'
]

def build(r):
    city = r['city']
    place = 'au '+city[3:] if city.startswith('Le ') else 'à '+city
    source_list = [dict(label='Source locale — quartiers et repères géographiques',url=r['source'])]
    extras = {
      'le-perreux-sur-marne':['https://www.leperreux94.fr/page/orientations-damenagement-et-de-programmation-oap'],
      'neuilly-sur-marne':['https://www.neuillysurmarne.fr/wp-content/uploads/2024/07/2-PADD.pdf'],
      'rosny-sous-bois':['https://www.rosnysousbois.fr/patrimoine-et-histoire/carte-didentite-de-la-ville/'],
      'saint-maur-des-fosses':['https://fr.wikipedia.org/wiki/Saint-Maur-des-Foss%C3%A9s'],
      'nogent-sur-marne':['https://ville-nogentsurmarne.com/cadre-de-vie/cinq-quartiers/quartier-nogent-baltard/'],
      'champigny-sur-marne':['https://www.joinville-le-pont.fr/vie-municipale/territoire/les-differents-quartiers/']
    }
    source_list += [dict(label='Repère local complémentaire',url=u) for u in extras.get(r['slug'],[])]
    source_list += [dict(label='Enedis — panne et interruption du réseau',url='https://www.enedis.fr/panne-et-interruption'),dict(label='Service Public — dépannage à domicile et devis',url='https://www.service-public.gouv.fr/particuliers/vosdroits/F38350')]
    return {
      'kind':'city','slug':r['slug'],'status':'draft','city':city,'postal_code':r['postal_code'],
      'title':f'Électricien à {city} – Dépannage électrique rapide',
      'meta_title':f'Électricien {city} ({r["postal_code"]}) | Dépannage',
      'description':f'Panne électrique à {city} ? Préparez votre dépannage : tableau, prises, disjoncteur et mise en sécurité. Repères locaux en {r["postal_code"]}.',
      'intro':f'Une panne électrique {place} ? Retrouvez les informations utiles pour décrire le problème, préparer un diagnostic et organiser une réparation. La disponibilité et la desserte de votre adresse sont à confirmer lors de l’appel.',
      'local_note':r['local_note'],'districts':r['districts'],'verified_districts':[],
      'coverage_verified':False,'coverage_evidence':'','editorial_verified':False,
      'sections':[
        dict(title=r['local_title'],paragraphs=r['local']),
        dict(title=r['case_title'],paragraphs=r['case']),
        dict(title=f'Les besoins de dépannage électrique {place}',paragraphs=services)
      ],
      'faq':[
        dict(question=r['question'],answer=r['answer']),
        dict(question=f'Comment demander un électricien en urgence {place} ?',answer=f'Préparez votre adresse en {r["postal_code"]}, les symptômes et les pièces concernées. Faites confirmer la disponibilité, la couverture et les conditions tarifaires. Aucun délai d’arrivée n’est garanti par cette page.'),
        dict(question='Que faire si le disjoncteur saute à nouveau ?',answer='Ne forcez pas son maintien en marche. Notez les appareils utilisés et les circuits touchés, puis demandez un diagnostic. En cas d’odeur, de fumée ou d’eau près d’un équipement, restez à distance.'),
        dict(question=f'Quels secteurs de {city} sont desservis ?',answer='Seuls les secteurs confirmés par l’entreprise seront annoncés comme desservis. Les noms présentés dans les repères locaux décrivent la géographie ; donnez votre adresse pour vérifier la couverture effective.'),
        dict(question='Quel tarif prévoir et comment se passe l’intervention ?',answer='Demandez le prix du déplacement, du diagnostic, de la main-d’œuvre et des pièces, ainsi que les éventuelles majorations. Le périmètre des travaux doit être expliqué et chiffré dans un devis avant votre accord.')
      ],
      'neighbors':r['neighbors'],'sources':source_list,
      'review':{'verified':False,'city':city,'author':'','text':'','source':''},
      'photo':{'verified':False,'permission':False,'path':'','alt':'','caption':''}
    }

if __name__ == '__main__':
    result = [build(r) for r in records]
    (ROOT/'content/cities.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for p in result:
        text = p['intro']+' '+' '.join(s['title']+' '+' '.join(s['paragraphs']) for s in p['sections'])+' '+' '.join(q['question']+' '+q['answer'] for q in p['faq'])
        count = len(re.findall(r"[\w]+(?:[’'-][\w]+)*",text))
        print(p['slug'],count)
