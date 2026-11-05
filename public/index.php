<?php
declare(strict_types=1);
require dirname(__DIR__) . '/app/bootstrap.php';
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: strict-origin-when-cross-origin');
header("Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'");
header('Permissions-Policy: camera=(), microphone=(), geolocation=()');
header('Cache-Control: no-store');
if (secure_request()) header('Strict-Transport-Security: max-age=31536000');
if (!local_mode() && !secure_request()) { http_response_code(400); exit('HTTPS requis. Activez le certificat SSL et la redirection HTTPS dans Hostinger.'); }
if (!empty($_COOKIE['electricien_admin'])) start_session();
$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
try {
    if (str_starts_with($path,'/api/')) { require ROOT.'/app/api.php'; exit; }
    if ($path === '/admin' || str_starts_with($path,'/admin/')) { require ROOT.'/app/admin.php'; exit; }
    $c = company();
    require ROOT.'/app/view.php';
    if ($path === '/robots.txt') {
        header('Content-Type: text/plain; charset=utf-8');
        if (local_mode() || company_errors($c)) { echo "User-agent: *\nDisallow: /\n"; exit; }
        echo "User-agent: *\nDisallow: /admin/\nDisallow: /api/\nSitemap: ".rtrim($c['site_url'],'/')."/sitemap.xml\n"; exit;
    }
    if ($path === '/sitemap.xml') {
        header('Content-Type: application/xml; charset=utf-8');
        echo '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
        if (!local_mode() && !company_errors($c)) {
            $base = rtrim($c['site_url'],'/');
            foreach (['/','/electricien/','/conseils/'] as $url) echo '<url><loc>'.e($base.$url).'</loc></url>';
            foreach (array_merge(pages('city'),pages('article')) as $p) if (live($p,$c)) echo '<url><loc>'.e($base.page_url($p)).'</loc><lastmod>'.e($p['updated_at']).'</lastmod></url>';
        }
        echo '</urlset>'; exit;
    }
    if (!in_array($_SERVER['REQUEST_METHOD'],['GET','HEAD'],true)) { header('Allow: GET, HEAD'); http_response_code(405); exit; }
    if (!preview_allowed() && company_errors($c)) {
        http_response_code(503); header('Retry-After: 86400'); header('X-Robots-Tag: noindex, nofollow');
        echo '<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Site en préparation</title><link rel="stylesheet" href="/assets/site.css"><main class="wrap prose"><div class="page-title"><span class="eyebrow">BIENTÔT EN LIGNE</span><h1>Le site est en préparation.</h1><p>Les informations de l’entreprise seront disponibles prochainement.</p></div></main></html>'; exit;
    }
    if ($path !== '/' && !str_ends_with($path,'/') && preg_match('~^/(electricien|conseils|mentions-legales|confidentialite)(/[a-z0-9-]+)?$~D',$path)) { header('Location: '.$path.'/',true,301); exit; }
    if ($path === '/') { home_page($c); exit; }
    if ($path === '/electricien/') {
        head($c,'Électricien par ville | Nogent et alentours','Retrouvez votre ville et les informations utiles pour un dépannage électrique dans l’Est parisien.',$path,company_errors($c)===[]);
        echo '<main id="main"><div class="wrap page-title"><span class="eyebrow">L’ÉLECTRICITÉ PRÈS DE CHEZ VOUS</span><h1>Votre ville, votre électricien.</h1><p>Les informations utiles pour préparer votre demande de dépannage.</p></div><section class="wrap city-section">'; city_grid($c); echo '</section></main>'; foot($c); exit;
    }
    if ($path === '/conseils/') {
        head($c,'Conseils électricité | Diagnostic et dépannage','Les conseils pour comprendre une panne et préparer une intervention électrique.',$path,company_errors($c)===[]);
        echo '<main id="main"><div class="wrap page-title"><span class="eyebrow">COMPRENDRE AVANT D’AGIR</span><h1>Les conseils électriques.</h1></div><div class="wrap article-grid">';
        $articles=available_pages('article',$c);
        if (!$articles) echo '<p class="empty">Les premiers conseils seront disponibles prochainement.</p>';
        foreach ($articles as $p) echo '<article class="article-card"><h2><a href="'.e(page_url($p)).'">'.e($p['title']).'</a></h2><p>'.e($p['intro']).'</p><a href="'.e(page_url($p)).'">Lire le conseil →</a></article>';
        echo '</div></main>'; foot($c); exit;
    }
    if (preg_match('~^/(electricien|conseils)/([a-z0-9-]+)/$~D',$path,$m)) {
        $p=page($m[2]);
        if ($p && page_url($p)===$path && (preview_allowed() || live($p,$c))) {
            if ($p['kind']==='city') { city_page($p,$c); exit; }
            $schema = live($p,$c)?['@context'=>'https://schema.org','@type'=>'Article','headline'=>$p['title'],'dateModified'=>$p['updated_at'],'mainEntityOfPage'=>rtrim($c['site_url'],'/').$path,'publisher'=>['@type'=>'Organization','name'=>$c['name']]]:[];
            head($c,$p['meta_title'],$p['description'],$path,live($p,$c),$schema);
            echo '<main id="main"><div class="wrap page-title"><span class="eyebrow">CONSEILS ÉLECTRICITÉ</span><h1>'.e($p['title']).'</h1><p>'.e($p['intro']).'</p></div><article class="wrap prose">';
            foreach ($p['sections'] as $s) { echo '<h2>'.e($s['title']).'</h2>'; foreach ($s['paragraphs'] as $para) echo '<p>'.e($para).'</p>'; }
            echo '</article>';
            if (!empty($p['faq'])) {
                echo '<section class="faq wrap"><div><span class="eyebrow">POUR ALLER PLUS LOIN</span><h2>Vos questions.</h2></div><div>';
                foreach ($p['faq'] as $q) echo '<details><summary>'.e($q['question']).'<span aria-hidden="true">+</span></summary><p>'.e($q['answer']).'</p></details>';
                echo '</div></section>';
            }
            echo '</main>'; foot($c); exit;
        }
    }
    if (in_array($path,['/mentions-legales/','/confidentialite/'],true)) {
        $legal=$path==='/mentions-legales/'; $title=$legal?'Mentions légales':'Confidentialité';
        head($c,$title,$title,$path,false);
        echo '<main id="main" class="wrap prose"><div class="page-title"><h1>'.$title.'</h1></div>';
        echo $legal ? '<p>'.nl2br(e($c['legal_text'] ?: 'Informations de l’éditeur à compléter avant publication.')).'</p>' : '<p>Ce site ne dépose aucun cookie publicitaire et ne charge aucun outil de mesure d’audience. Les liens téléphoniques ouvrent l’application d’appel de votre appareil.</p><p>Un cookie de session strictement nécessaire est utilisé dans l’espace d’administration. Les tentatives de connexion sont temporairement conservées sous forme d’une empreinte de l’adresse IP pour protéger cet espace.</p><p>Les informations sur le responsable du site et le contact pour exercer vos droits figurent dans les mentions légales. L’hébergeur peut conserver des journaux techniques conformément à ses propres conditions.</p>';
        echo '</main>'; foot($c); exit;
    }
    http_response_code(404); head($c,'Page introuvable','Cette page est indisponible.',$path,false);
    echo '<main id="main" class="wrap prose"><div class="page-title"><span class="eyebrow">404</span><h1>Cette page n’est pas disponible.</h1><p><a href="/">Revenir à l’accueil</a></p></div></main>'; foot($c);
} catch (Throwable $error) {
    error_log(get_class($error).': '.$error->getMessage());
    http_response_code(503); header('X-Robots-Tag: noindex');
    echo 'Le site est temporairement indisponible. Merci de réessayer plus tard.';
}
