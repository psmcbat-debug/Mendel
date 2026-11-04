<?php
function words(string $text): int { return preg_match_all('/[\p{L}\p{N}]+(?:[’\x27-][\p{L}\p{N}]+)*/u', $text); }
function content_text(array $p): string {
    $text = ($p['intro'] ?? '') . ' ';
    foreach ($p['sections'] ?? [] as $s) $text .= ($s['title'] ?? '') . ' ' . implode(' ', $s['paragraphs'] ?? []) . ' ';
    foreach ($p['faq'] ?? [] as $q) $text .= ($q['question'] ?? '') . ' ' . ($q['answer'] ?? '') . ' ';
    return $text;
}
function company_errors(array $c): array {
    $errors = [];
    if (($c['identity_verified'] ?? false) !== true || trim($c['name'] ?? '') === '') $errors[] = 'Identité de l’entreprise non validée.';
    if (!preg_match('/^\+[1-9][0-9]{7,14}$/', $c['phone'] ?? '')) $errors[] = 'Téléphone international manquant ou invalide.';
    if (!http_url($c['site_url'] ?? '') || parse_url($c['site_url'], PHP_URL_QUERY) || !in_array(parse_url($c['site_url'], PHP_URL_PATH), [null, '', '/'], true)) $errors[] = 'Domaine HTTPS définitif requis (sans sous-dossier).';
    if (($c['services_verified'] ?? false) !== true) $errors[] = 'Prestations à confirmer.';
    if (($c['pricing_verified'] ?? false) !== true || trim($c['pricing_text'] ?? '') === '') $errors[] = 'Informations tarifaires réelles à renseigner et valider.';
    if (($c['hours_verified'] ?? false) !== true || trim($c['hours_text'] ?? '') === '') $errors[] = 'Horaires à renseigner et valider.';
    if (($c['legal_verified'] ?? false) !== true || trim($c['legal_text'] ?? '') === '') $errors[] = 'Mentions légales à compléter et valider.';
    return $errors;
}
function page_errors(array $p): array {
    $errors = [];
    if (!is_string($p['slug'] ?? null) || !preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*$/D', $p['slug']) || strlen($p['slug']) > 120) $errors[] = 'Slug invalide.';
    if (!in_array($p['kind'] ?? '', ['city','article'], true)) $errors[] = 'Type de contenu invalide.';
    if (!in_array($p['status'] ?? '', ['draft','published'], true)) $errors[] = 'Statut invalide.';
    foreach (['title','meta_title','description','intro'] as $key) if (!is_string($p[$key] ?? null) || trim($p[$key]) === '') $errors[] = "Champ requis : $key.";
    if (is_string($p['meta_title']??null) && mb_strlen($p['meta_title'])>100) $errors[] = 'Titre SEO trop long (100 caractères maximum).';
    if (is_string($p['description']??null) && mb_strlen($p['description'])>200) $errors[] = 'Description trop longue (200 caractères maximum).';
    if (!is_array($p['sections'] ?? null) || count($p['sections']) < 1) return array_merge($errors,['Sections requises.']);
    if (!is_array($p['faq'] ?? [])) return array_merge($errors,['FAQ invalide.']);
    foreach ($p['sections'] ?? [] as $s) {
        if (!is_array($s) || !is_string($s['title'] ?? null) || !is_array($s['paragraphs'] ?? null)) { $errors[] = 'Section invalide.'; continue; }
        foreach ($s['paragraphs'] as $v) if (!is_string($v)) $errors[] = 'Paragraphe invalide.';
    }
    foreach ($p['faq'] ?? [] as $q) if (!is_array($q) || !is_string($q['question'] ?? null) || !is_string($q['answer'] ?? null)) $errors[] = 'FAQ invalide.';
    if (($p['kind'] ?? '') === 'city') {
        if (!is_string($p['city'] ?? null) || !is_string($p['postal_code']??null) || !preg_match('/^\d{5}$/D', $p['postal_code'])) $errors[] = 'Ville et code postal requis.';
        if (count($p['faq'] ?? []) < 4 || count($p['faq'] ?? []) > 6) $errors[] = 'La FAQ doit comporter de 4 à 6 questions.';
        foreach (['districts','verified_districts','neighbors','sources'] as $key) if (!is_array($p[$key]??null)) $errors[] = "Liste requise : $key.";
        foreach (['districts','verified_districts','neighbors'] as $key) if (is_array($p[$key]??null)) foreach ($p[$key] as $value) if (!is_string($value)) $errors[] = "Valeur invalide : $key.";
        foreach (['local_note','coverage_evidence'] as $key) if (!is_string($p[$key]??null)) $errors[] = "Texte requis : $key.";
        if (is_array($p['sources']??null)) foreach ($p['sources'] as $s) if (!is_array($s) || !is_string($s['label']??null) || !is_string($s['url']??null) || !http_url($s['url'])) $errors[] = 'Source HTTPS invalide.';
        foreach (['review','photo'] as $key) if (isset($p[$key]) && !is_array($p[$key])) $errors[] = "Objet invalide : $key.";
        foreach (['review'=>['city','author','text','source'],'photo'=>['path','alt','caption']] as $key=>$fields) {
            if (!is_array($p[$key]??null)) continue;
            foreach ($fields as $field) if (!is_string($p[$key][$field]??'')) $errors[] = "Texte invalide : $key.$field.";
        }
    }
    return $errors;
}
function publication_errors(array $p, array $c): array {
    $errors = array_merge(company_errors($c), page_errors($p));
    if (page_errors($p)) return $errors;
    if (($p['editorial_verified']??false) !== true) $errors[] = 'Relecture éditoriale à valider.';
    if ($p['kind'] === 'city') {
        if (($p['coverage_verified']??false) !== true || empty($p['verified_districts'])) $errors[] = 'Ville et quartiers réellement desservis à confirmer.';
        if (empty($p['coverage_evidence'])) $errors[] = 'Consigner la confirmation de couverture (responsable et date).';
        if (array_diff($p['verified_districts'] ?? [], $p['districts'] ?? [])) $errors[] = 'Un quartier confirmé est absent des repères géographiques.';
        $count = words(content_text($p));
        if ($count < 600 || $count > 1000) $errors[] = "Le contenu doit contenir 600 à 1 000 mots ($count).";
    }
    return array_unique($errors);
}
