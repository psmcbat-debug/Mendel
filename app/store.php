<?php
function db(): PDO {
    static $db;
    if (!$db) {
        $c = $GLOBALS['config'];
        $db = new PDO($c['dsn'], $c['db_user'], $c['db_password'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
        if ($db->getAttribute(PDO::ATTR_DRIVER_NAME) === 'sqlite') $db->exec('PRAGMA busy_timeout=5000');
    }
    return $db;
}
function migrate(): void {
    $text = db()->getAttribute(PDO::ATTR_DRIVER_NAME) === 'mysql' ? 'LONGTEXT' : 'TEXT';
    db()->exec('CREATE TABLE IF NOT EXISTS settings (id VARCHAR(50) PRIMARY KEY, payload TEXT NOT NULL)');
    db()->exec('CREATE TABLE IF NOT EXISTS pages (slug VARCHAR(120) PRIMARY KEY, kind VARCHAR(20) NOT NULL, status VARCHAR(20) NOT NULL, payload '.$text.' NOT NULL, updated_at VARCHAR(30) NOT NULL)');
    db()->exec('CREATE TABLE IF NOT EXISTS login_attempts (ip_hash VARCHAR(64) NOT NULL, attempted_at BIGINT NOT NULL)');
    db()->exec('CREATE TABLE IF NOT EXISTS audit_log (event_id VARCHAR(40) PRIMARY KEY, action VARCHAR(50) NOT NULL, slug VARCHAR(120) NOT NULL, created_at VARCHAR(30) NOT NULL)');
}
function company(): array {
    $s = db()->prepare('SELECT payload FROM settings WHERE id = ?'); $s->execute(['company']);
    $v = $s->fetchColumn();
    if (!$v) throw new RuntimeException('Initialisez la base de données avec scripts/init.php.');
    return json_decode($v, true, 64, JSON_THROW_ON_ERROR);
}
function save_company(array $company): void {
    $s = db()->prepare('UPDATE settings SET payload = ? WHERE id = ?');
    $s->execute([json_encode($company, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR), 'company']);
}
function page(string $slug): ?array {
    $s = db()->prepare('SELECT * FROM pages WHERE slug = ?'); $s->execute([$slug]);
    $row = $s->fetch(); return $row ? hydrate($row) : null;
}
function hydrate(array $row): array {
    return array_merge(json_decode($row['payload'], true, 64, JSON_THROW_ON_ERROR), ['slug'=>$row['slug'], 'kind'=>$row['kind'], 'status'=>$row['status'], 'updated_at'=>$row['updated_at']]);
}
function pages(string $kind): array {
    $s = db()->prepare('SELECT * FROM pages WHERE kind = ? ORDER BY slug'); $s->execute([$kind]);
    return array_map('hydrate', $s->fetchAll());
}
function save_page(array $page, string $actor = 'admin'): void {
    $pdo = db(); $pdo->beginTransaction();
    try {
        $stamp = gmdate('Y-m-d\TH:i:s\Z');
        $payload = json_encode($page, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
        if (page($page['slug'])) {
            $s = $pdo->prepare('UPDATE pages SET kind=?, status=?, payload=?, updated_at=? WHERE slug=?');
            $s->execute([$page['kind'], $page['status'], $payload, $stamp, $page['slug']]);
        } else {
            $s = $pdo->prepare('INSERT INTO pages (kind,status,payload,updated_at,slug) VALUES (?,?,?,?,?)');
            $s->execute([$page['kind'], $page['status'], $payload, $stamp, $page['slug']]);
        }
        $s = $pdo->prepare('INSERT INTO audit_log (event_id,action,slug,created_at) VALUES (?,?,?,?)');
        $s->execute([bin2hex(random_bytes(16)), $actor . ':' . $page['status'], $page['slug'], $stamp]);
        $pdo->commit();
    } catch (Throwable $e) { $pdo->rollBack(); throw $e; }
}
