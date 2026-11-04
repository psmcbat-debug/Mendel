<?php
header('X-Robots-Tag: noindex, nofollow');
$stored = $config['api_token_hash'];
$auth = $_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
if (!preg_match('/^Bearer ([A-Za-z0-9_-]{24,256})$/D',$auth,$match) || strlen($stored)!==64 || !hash_equals($stored,hash('sha256',$match[1]))) send_json(['error'=>'Authentification requise.'],401);
if ($path === '/api/v1/status' && $_SERVER['REQUEST_METHOD']==='GET') send_json(['connected'=>true,'publication_ready'=>company_errors(company())===[],'articles'=>count(pages('article'))]);
if ($path !== '/api/v1/articles') send_json(['error'=>'Route inconnue.'],404);
if ($_SERVER['REQUEST_METHOD']==='GET') {
    $slug=(string)($_GET['slug']??'');
    if ($slug) { $p=page($slug); if (!$p || $p['kind']!=='article') send_json(['error'=>'Article introuvable.'],404); send_json(['article'=>$p]); }
    send_json(['articles'=>array_map(fn($p)=>['slug'=>$p['slug'],'title'=>$p['title'],'status'=>$p['status'],'updated_at'=>$p['updated_at']],pages('article'))]);
}
if ($_SERVER['REQUEST_METHOD']!=='POST') { header('Allow: GET, POST'); send_json(['error'=>'Méthode non autorisée.'],405); }
if (!str_starts_with($_SERVER['CONTENT_TYPE']??'','application/json')) send_json(['error'=>'Content-Type application/json requis.'],415);
$body=file_get_contents('php://input',false,null,0,131073);
if (strlen($body)>131072) send_json(['error'=>'Article trop volumineux (128 Ko maximum).'],413);
try { $p=json_decode($body,true,32,JSON_THROW_ON_ERROR); } catch (JsonException $e) { send_json(['error'=>'JSON invalide.'],400); }
if (!is_array($p) || array_is_list($p)) send_json(['error'=>'Objet JSON requis.'],400);
$p['kind']='article'; $p['status']=$p['status']??'draft';
$errors=page_errors($p);
if ($errors) send_json(['errors'=>array_values($errors)],422);
$existing=page($p['slug']);
if ($existing && $existing['kind']!=='article') send_json(['error'=>'Ce slug appartient à une page locale.'],409);
if ($p['status']==='published') {
    $errors=publication_errors($p,company());
    if ($errors) send_json(['errors'=>array_values($errors)],422);
}
save_page($p,'api');
send_json(['saved'=>true,'slug'=>$p['slug'],'status'=>$p['status'],'path'=>page_url($p),'updated_at'=>page($p['slug'])['updated_at']],$existing?200:201);
