<?php
// Copy to config/local.php, outside public_html. Never commit real credentials.
return [
    'environment' => 'production',
    'dsn' => 'mysql:host=localhost;dbname=YOUR_DATABASE;charset=utf8mb4',
    'db_user' => 'YOUR_DATABASE_USER',
    'db_password' => '',
    'admin_password_hash' => '', // Generate with scripts/credentials.php
    'api_token_hash' => '',      // SHA-256 of a separate random API token
];
