<?php
if (PHP_SAPI!=='cli') exit;
require dirname(__DIR__).'/app/bootstrap.php';
if (!local_mode()) exit("Cette commande est réservée à la maquette locale.\n");
foreach (json_read(ROOT.'/content/cities.json') as $p) {
    $existing=page($p['slug']);
    if (!$existing || ($existing['status']==='draft' && !$existing['coverage_verified'] && !$existing['editorial_verified'])) save_page($p,'local-seed');
}
echo "Brouillons de prévisualisation synchronisés.\n";
