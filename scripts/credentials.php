<?php
if (PHP_SAPI !== 'cli') exit;
// Only outputs hashes. Supply the secret via stdin, never command arguments.
$mode = $argv[1] ?? '';
if (!in_array($mode, ['admin','api'], true)) exit("Usage : php scripts/credentials.php admin|api < secret.txt\n");
$secret = trim(stream_get_contents(STDIN));
if (strlen($secret) < 24) exit("Utilisez un secret aléatoire d’au moins 24 caractères.\n");
echo ($mode === 'admin' ? password_hash($secret, PASSWORD_DEFAULT) : hash('sha256', $secret)) . PHP_EOL;
