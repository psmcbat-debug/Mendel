<?php
// PHP development server router, not used by Hostinger.
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$file = realpath(dirname(__DIR__) . '/public' . $path);
$assets = realpath(dirname(__DIR__) . '/public/assets');
if ($file && $assets && str_starts_with($file, $assets . DIRECTORY_SEPARATOR) && is_file($file)) return false;
require dirname(__DIR__) . '/public/index.php';
