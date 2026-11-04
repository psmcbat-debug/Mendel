<?php
declare(strict_types=1);

define('ROOT', dirname(__DIR__));
$config = is_file(ROOT . '/config/local.php') ? require ROOT . '/config/local.php' : [];
$config += [
    'environment' => 'production',
    'dsn' => 'sqlite:' . ROOT . '/var/site.sqlite',
    'db_user' => null, 'db_password' => null,
    'admin_password_hash' => '', 'api_token_hash' => '',
];
date_default_timezone_set('Europe/Paris');
require __DIR__ . '/store.php';
require __DIR__ . '/validation.php';

function e(mixed $value): string { return htmlspecialchars((string)$value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function json_read(string $path): array { return json_decode(file_get_contents($path), true, 64, JSON_THROW_ON_ERROR); }
function local_mode(): bool { return $GLOBALS['config']['environment'] === 'local'; }
function secure_request(): bool { return ($_SERVER['HTTPS'] ?? '') === 'on'; }
function start_session(): void {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    session_name('electricien_admin');
    session_set_cookie_params(['httponly' => true, 'secure' => !local_mode(), 'samesite' => 'Strict', 'path' => '/']);
    ini_set('session.use_strict_mode', '1');
    session_start();
    if (isset($_SESSION['last']) && time() - $_SESSION['last'] > 1800) $_SESSION = [];
}
function admin(): bool { return !empty($_SESSION['admin']) && time() - ($_SESSION['last'] ?? 0) <= 1800; }
function csrf(): string { return $_SESSION['csrf'] ??= bin2hex(random_bytes(32)); }
function require_csrf(): void {
    if (!hash_equals(csrf(), (string)($_POST['csrf'] ?? ''))) { http_response_code(403); exit('Session expirée. Rechargez la page.'); }
}
function send_json(array $data, int $status = 200): never {
    http_response_code($status); header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR); exit;
}
function page_url(array $page): string { return '/' . ($page['kind'] === 'city' ? 'electricien' : 'conseils') . '/' . $page['slug'] . '/'; }
function live(array $page, array $company): bool { return $page['status'] === 'published' && publication_errors($page, $company) === []; }
function preview_allowed(): bool { return local_mode() || admin(); }
function available_pages(string $kind, array $company): array {
    return array_values(array_filter(pages($kind), fn($p) => preview_allowed() || live($p, $company)));
}
function phone_link(array $company): ?string {
    return !empty($company['identity_verified']) && preg_match('/^\+[1-9][0-9]{7,14}$/', $company['phone'] ?? '') ? 'tel:' . $company['phone'] : null;
}
function asset_path(string $value): bool { return (bool)preg_match('~^/assets/[a-zA-Z0-9_/-]+\.(webp|avif)$~D', $value) && !str_contains($value, '..'); }
function http_url(string $value): bool { return filter_var($value, FILTER_VALIDATE_URL) && parse_url($value, PHP_URL_SCHEME) === 'https'; }
