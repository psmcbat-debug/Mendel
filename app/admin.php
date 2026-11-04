<?php
start_session();
header('X-Robots-Tag: noindex, nofollow');
require ROOT.'/app/view.php';
$message=''; $error='';
if ($_SERVER['REQUEST_METHOD']==='POST') {
    require_csrf();
    $action=$_POST['action']??'';
    if ($action==='login') {
        $ip=hash('sha256',($_SERVER['REMOTE_ADDR']??'unknown'));
        $s=db()->prepare('DELETE FROM login_attempts WHERE attempted_at < ?'); $s->execute([time()-900]);
        $s=db()->prepare('SELECT COUNT(*) FROM login_attempts WHERE ip_hash=?'); $s->execute([$ip]);
        if ((int)$s->fetchColumn()>=5) { http_response_code(429); $error='Trop de tentatives. Réessayez dans 15 minutes.'; }
        else {
            $s=db()->prepare('INSERT INTO login_attempts (ip_hash,attempted_at) VALUES (?,?)'); $s->execute([$ip,time()]);
            if ($config['admin_password_hash'] && password_verify((string)($_POST['password']??''),$config['admin_password_hash'])) {
                session_regenerate_id(true); $_SESSION=['admin'=>true,'last'=>time(),'csrf'=>bin2hex(random_bytes(32))];
                header('Location: /admin/',true,303); exit;
            }
            $error='Connexion impossible. Vérifiez le mot de passe et la configuration.';
        }
    } elseif (admin()) {
        $_SESSION['last']=time();
        try {
            if ($action==='logout') { $_SESSION=[]; session_destroy(); header('Location: /admin/',true,303); exit; }
            if ($action==='company') {
                $c=company();
                foreach (['name','phone','phone_display','site_url','logo','description','hours_text','response_time_text','pricing_text','experience_text','insurance_text','legal_text'] as $key) $c[$key]=trim((string)($_POST[$key]??''));
                $c['site_url']=rtrim($c['site_url'],'/');
                if ($c['logo'] && !asset_path($c['logo'])) throw new RuntimeException('Le logo doit être un fichier WebP ou AVIF dans /assets/.');
                foreach (['identity_verified','services_verified','hours_verified','response_time_verified','pricing_verified','experience_verified','insurance_verified','legal_verified'] as $key) $c[$key]=isset($_POST[$key]);
                save_company($c); $message='Paramètres enregistrés. Les pages non conformes restent hors publication.';
            }
            if ($action==='save_page') {
                if (strlen($_POST['payload']??'')>131072) throw new RuntimeException('Contenu trop volumineux.');
                $p=json_decode($_POST['payload']??'',true,32,JSON_THROW_ON_ERROR);
                if (!is_array($p)) throw new RuntimeException('Objet JSON requis.');
                $p['status']=($_POST['status']??'draft')==='published'?'published':'draft';
                $errors=page_errors($p);
                if ($errors) throw new RuntimeException(implode(' ',$errors));
                $original=(string)($_POST['original_slug']??'');
                if ($original && $original!==$p['slug']) throw new RuntimeException('Le slug d’un contenu existant ne doit pas être modifié.');
                $existing=page($p['slug']);
                if (!$original && $existing) throw new RuntimeException('Ce slug existe déjà. Ouvrez sa fiche pour le modifier.');
                if ($existing && $existing['kind']!==$p['kind']) throw new RuntimeException('Le type du contenu ne doit pas être modifié.');
                if ($p['status']==='published' && ($errors=publication_errors($p,company()))) throw new RuntimeException(implode(' ',$errors));
                save_page($p); header('Location: /admin/?edit='.rawurlencode($p['slug']).'&saved=1',true,303); exit;
            }
        } catch (Throwable $e) { $error=$e instanceof JsonException?'JSON invalide : vérifiez les virgules et guillemets.':$e->getMessage(); }
    } else { http_response_code(403); $error='Session expirée. Reconnectez-vous.'; }
}
if (admin()) $_SESSION['last']=time();
?><!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Administration · Électricien</title><link rel="stylesheet" href="/assets/site.css"></head><body><main class="admin" id="main">
<?php if (!admin()): ?><div class="admin-card login"><span class="eyebrow">ESPACE PRIVÉ</span><h1>Votre site,<br>simplement.</h1><p>Connectez-vous pour gérer les pages et les informations de l’entreprise.</p><?php if ($error): ?><p class="notice error" role="alert"><?= e($error) ?></p><?php endif ?><?php if (!$config['admin_password_hash']): ?><p class="notice">Accès non configuré. Définissez le mot de passe administrateur dans le fichier privé de configuration. Consultez le guide d’installation.</p><?php else: ?><form method="post"><input type="hidden" name="csrf" value="<?= e(csrf()) ?>"><input type="hidden" name="action" value="login"><label for="password">Mot de passe</label><input type="password" id="password" name="password" autocomplete="current-password" required><button class="button" type="submit">Se connecter →</button></form><?php endif ?><p><a href="/">Retour au site</a></p></div>
<?php else: $c=company(); ?><span class="eyebrow">ADMINISTRATION</span><h1>Votre présence locale.</h1><nav><a href="/admin/">Tableau de bord</a><a href="/admin/?settings=1">Entreprise</a><a href="/admin/?new=article">Nouvel article</a><a href="/admin/?new=city">Nouvelle ville</a><a href="/">Voir le site ↗</a></nav>
<?php if ($message || isset($_GET['saved'])): ?><p class="notice" role="status"><?= e($message ?: 'Contenu enregistré en base de données.') ?></p><?php endif ?><?php if ($error): ?><p class="notice error" role="alert"><?= e($error) ?></p><?php endif ?>
<?php if (isset($_GET['settings'])): ?><form method="post" class="admin-card"><h2>L’entreprise</h2><p>Ne cochez une validation qu’après vérification réelle. Le changement d’un paramètre peut suspendre l’indexation des pages.</p><input type="hidden" name="csrf" value="<?= e(csrf()) ?>"><input type="hidden" name="action" value="company">
<?php $labels=['name'=>'Nom commercial réel','phone'=>'Téléphone international, ex. +33…','phone_display'=>'Numéro affiché','site_url'=>'Domaine définitif HTTPS','logo'=>'Chemin du logo WebP ou AVIF, ex. /assets/logo.webp','description'=>'Présentation courte','hours_text'=>'Horaires réels','response_time_text'=>'Délais (facultatif, sans promesse non vérifiée)','pricing_text'=>'Tarifs : déplacement, main-d’œuvre, forfaits, majorations, TVA et coût du devis','experience_text'=>'Expérience (facultatif)','insurance_text'=>'Assurance réelle (facultatif)','legal_text'=>'Mentions légales : éditeur, adresse, immatriculation, directeur de publication, hébergeur, contact, médiateur applicable'];
foreach ($labels as $key=>$label): ?><label for="<?= e($key) ?>"><?= e($label) ?></label><?php if (str_ends_with($key,'_text') || $key==='description'): ?><textarea id="<?= e($key) ?>" name="<?= e($key) ?>"><?= e($c[$key]) ?></textarea><?php else: ?><input id="<?= e($key) ?>" name="<?= e($key) ?>" value="<?= e($c[$key]) ?>"><?php endif ?><?php endforeach ?>
<?php foreach (['identity_verified'=>'Identité et téléphone vérifiés','services_verified'=>'Toutes les prestations présentées sont réellement proposées','hours_verified'=>'Horaires vérifiés','response_time_verified'=>'Délais vérifiés','pricing_verified'=>'Conditions tarifaires vérifiées','experience_verified'=>'Expérience vérifiée','insurance_verified'=>'Assurance vérifiée','legal_verified'=>'Mentions légales vérifiées'] as $key=>$label): ?><label class="checkbox"><input type="checkbox" name="<?= e($key) ?>" <?= !empty($c[$key])?'checked':'' ?>><?= e($label) ?></label><?php endforeach ?><button class="button">Enregistrer les paramètres</button></form>
<?php elseif (isset($_GET['edit']) || isset($_GET['new'])):
$p=isset($_GET['edit'])?page((string)$_GET['edit']):null;
if (!$p) $p=['kind'=>($_GET['new']??'article')==='city'?'city':'article','slug'=>'nouveau-conseil','status'=>'draft','title'=>'Titre du conseil','meta_title'=>'Titre SEO du conseil','description'=>'Description utile pour les résultats de recherche.','intro'=>'Introduction du conseil.','sections'=>[['title'=>'Première section','paragraphs'=>['Rédigez votre contenu ici.']]],'faq'=>[],'editorial_verified'=>false];
if ($p['kind']==='city' && !isset($p['city'])) $p+=['city'=>'Ville','postal_code'=>'00000','districts'=>[],'verified_districts'=>[],'coverage_verified'=>false,'coverage_evidence'=>'','neighbors'=>[],'local_note'=>'','sources'=>[]];
$problems=publication_errors($p,$c);
?><form method="post" class="admin-card"><h2><?= e($p['title']) ?></h2><p><?= $p['kind']==='city'?words(content_text($p)).' mots · objectif : 600 à 1 000 mots.':'Article stocké dans la base de données.' ?></p><?php if ($problems): ?><div class="notice"><strong>À compléter avant publication</strong><ul><?php foreach ($problems as $problem): ?><li><?= e($problem) ?></li><?php endforeach ?></ul></div><?php endif ?><p>Éditez le contenu structuré ci-dessous. Aucun HTML n’est exécuté. Pour une ville, renseignez <code>verified_districts</code>, <code>coverage_evidence</code> et les validations. Les emplacements <code>review</code> et <code>photo</code> sont prévus pour des preuves authentiques.</p><input type="hidden" name="csrf" value="<?= e(csrf()) ?>"><input type="hidden" name="action" value="save_page"><input type="hidden" name="original_slug" value="<?= e($_GET['edit']??'') ?>"><label for="payload">Contenu JSON</label><textarea class="code" id="payload" name="payload" spellcheck="false" required><?= e($error && isset($_POST['payload'])?$_POST['payload']:json_encode($p,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)) ?></textarea><label for="status">Statut</label><select id="status" name="status"><option value="draft">Brouillon — privé</option><option value="published" <?= $p['status']==='published'?'selected':'' ?>>Publié — sous réserve de validation</option></select><div class="admin-actions"><button class="button">Enregistrer</button><?php if (isset($_GET['edit'])): ?><a href="<?= e(page_url($p)) ?>">Prévisualiser ↗</a><?php endif ?></div></form>
<?php else: ?><div class="admin-card"><h2>Préparation de la publication</h2><?php $errors=company_errors($c); if ($errors): ?><ul><?php foreach ($errors as $item): ?><li><?= e($item) ?></li><?php endforeach ?></ul><a href="/admin/?settings=1">Compléter l’entreprise →</a><?php else: ?><p>Les informations générales sont validées. Confirmez la couverture et la relecture de chaque page avant publication.</p><?php endif ?></div>
<?php foreach (['city'=>'Pages locales','article'=>'Articles'] as $kind=>$label): ?><section class="admin-card"><h2><?= e($label) ?></h2><div class="table-scroll"><table><thead><tr><th>Contenu</th><th>État effectif</th><th>Mots</th><th>Actions</th></tr></thead><tbody><?php foreach (pages($kind) as $p): ?><tr><td><?= e($p['title']) ?></td><td><span class="badge"><?= live($p,$c)?'Publié':($p['status']==='published'?'Publication suspendue':'Brouillon') ?></span></td><td><?= words(content_text($p)) ?></td><td><a href="/admin/?edit=<?= e($p['slug']) ?>">Modifier</a> · <a href="<?= e(page_url($p)) ?>">Voir</a></td></tr><?php endforeach ?></tbody></table></div></section><?php endforeach ?><div class="admin-card"><h2>Publication à distance</h2><p>API : <code>POST /api/v1/articles</code>. Le jeton privé se configure côté serveur ; il n’apparaît jamais ici. Les articles arrivent en brouillon sauf demande explicite de publication avec validation éditoriale.</p></div><?php endif ?>
<form method="post"><input type="hidden" name="csrf" value="<?= e(csrf()) ?>"><input type="hidden" name="action" value="logout"><button class="button">Se déconnecter</button></form><?php endif ?></main></body></html>
