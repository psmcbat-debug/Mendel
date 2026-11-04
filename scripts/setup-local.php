<?php
if (PHP_SAPI!=='cli') exit;
require dirname(__DIR__).'/app/bootstrap.php';
if (!local_mode()) exit("Réservé à la prévisualisation locale.\n");
if ($config['admin_password_hash']) exit("Accès déjà configuré, conservé.\n");
$password=bin2hex(random_bytes(18));
$token=bin2hex(random_bytes(32));
$config['admin_password_hash']=password_hash($password,PASSWORD_DEFAULT);
$config['api_token_hash']=hash('sha256',$token);
file_put_contents(ROOT.'/config/local.php',"<?php\nreturn ".var_export($config,true).";\n");
if (!is_dir(ROOT.'/.runtime')) mkdir(ROOT.'/.runtime',0700,true);
file_put_contents(ROOT.'/.runtime/acces-local.json',json_encode(['usage'=>'LOCAL UNIQUEMENT — ne pas déployer','admin_url'=>'http://127.0.0.1:8088/admin/','admin_password'=>$password,'api_token'=>$token],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
echo "Accès local créé. Secrets conservés dans .runtime/acces-local.json (exclu de la livraison).\n";
