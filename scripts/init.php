<?php
if (PHP_SAPI !== 'cli') exit;
require dirname(__DIR__) . '/app/bootstrap.php';
migrate();
$s = db()->prepare('SELECT id FROM settings WHERE id=?'); $s->execute(['company']);
if (!$s->fetch()) {
    $s = db()->prepare('INSERT INTO settings (id,payload) VALUES (?,?)');
    $s->execute(['company', json_encode(json_read(ROOT . '/content/company.json'), JSON_UNESCAPED_UNICODE)]);
}
$n = 0;
foreach (json_read(ROOT . '/content/cities.json') as $p) {
    $errors = page_errors($p); if ($errors) throw new RuntimeException(implode(' ', $errors));
    if (!page($p['slug'])) { save_page($p, 'seed'); $n++; }
}
echo "$n pages ajoutées. Les contenus existants ont été conservés.\n";
