<?php
// Human-readable editor; advanced JSON remains available for evidence and extra fields.
function editor_string(array $input, string $key): string {
    if (!is_string($input[$key] ?? '')) throw new RuntimeException('Valeur de formulaire invalide : '.$key);
    return trim($input[$key] ?? '');
}
function editor_lines(string $value): array {
    return array_values(array_unique(array_filter(array_map('trim', preg_split('/\R/u', $value)), fn($s)=>$s!=='')));
}
function editor_page(array $input, array $base): array {
    $p=$base;
    foreach (['slug','title','meta_title','description','intro'] as $key) $p[$key]=editor_string($input,$key);
    $p['editorial_verified']=isset($input['editorial_verified']);
    $p['sections']=[]; $p['faq']=[];
    foreach (['sections'=>30,'faq'=>10] as $key=>$max) {
        $rows=$input[$key]??[];
        if (!is_array($rows) || count($rows)>$max) throw new RuntimeException('Nombre de rubriques invalide.');
        foreach ($rows as $row) {
            if (!is_array($row)) throw new RuntimeException('Rubrique invalide.');
            if ($key==='sections') {
                $title=editor_string($row,'title'); $body=editor_string($row,'body');
                if ($title==='' && $body==='') continue;
                $paragraphs=array_values(array_filter(array_map('trim',preg_split('/\R\h*\R/u',$body)),fn($s)=>$s!==''));
                $p['sections'][]=['title'=>$title,'paragraphs'=>$paragraphs];
            } else {
                $question=editor_string($row,'question'); $answer=editor_string($row,'answer');
                if ($question==='' && $answer==='') continue;
                $p['faq'][]=['question'=>$question,'answer'=>$answer];
            }
        }
    }
    if ($p['kind']==='city') {
        foreach (['city','postal_code','local_note','coverage_evidence'] as $key) $p[$key]=editor_string($input,$key);
        foreach (['districts','verified_districts','neighbors'] as $key) $p[$key]=editor_lines(editor_string($input,$key));
        $p['coverage_verified']=isset($input['coverage_verified']);
        // Sources, review and photo are retained from the stored page, never replaced by hidden inputs.
    }
    return $p;
}
function editor_field(string $name,string $label,string $value,bool $multiline=false,string $help=''): void {
    $id='field-'.preg_replace('/[^a-zA-Z0-9-]/','-',$name);
    ?><label for="<?= e($id) ?>"><?= e($label) ?></label><?php if ($multiline): ?><textarea id="<?= e($id) ?>" name="<?= e($name) ?>" <?= $help?'aria-describedby="'.e($id).'-help"':'' ?>><?= e($value) ?></textarea><?php else: ?><input id="<?= e($id) ?>" name="<?= e($name) ?>" value="<?= e($value) ?>" <?= $help?'aria-describedby="'.e($id).'-help"':'' ?>><?php endif ?><?php if ($help): ?><p class="field-help" id="<?= e($id) ?>-help"><?= e($help) ?></p><?php endif ?><?php
}
function editor_row(string $kind,int $i,array $row): void {
    ?><fieldset class="editor-row"><legend><?= $kind==='sections'?'Section':'Question' ?> <?= $i+1 ?></legend><?php
    if ($kind==='sections') {
        editor_field("sections[$i][title]",'Titre de la section',$row['title']??'');
        editor_field("sections[$i][body]",'Texte',implode("\n\n",$row['paragraphs']??[]),true,'Séparez les paragraphes par une ligne vide.');
    } else {
        editor_field("faq[$i][question]",'Question',$row['question']??'');
        editor_field("faq[$i][answer]",'Réponse',$row['answer']??'',true);
    }
    ?><button type="button" class="remove-row" hidden>Retirer cette rubrique</button></fieldset><?php
}
function editor_fields(array $p): void {
    ?><input type="hidden" name="editor_mode" value="simple"><input type="hidden" name="kind" value="<?= e($p['kind']) ?>"><div class="editor-columns"><div><?php
    editor_field('title','Titre principal (H1)',$p['title']);
    editor_field('slug','Adresse de la page (slug)',$p['slug'],false,'Minuscules et tirets. Une adresse existante ne peut pas être modifiée ici.');
    ?></div><div><?php
    editor_field('meta_title','Titre pour Google',$p['meta_title'],false,'Un titre précis et propre à cette page. Maximum : 100 caractères.');
    editor_field('description','Description pour Google',$p['description'],true,'Résumé utile, sans promesse non vérifiée. Maximum : 200 caractères.');
    ?></div></div><?php
    editor_field('intro','Introduction',$p['intro'],true);
    ?><h3 class="editor-heading">Le contenu</h3><p>Rédigez du texte simple. Les titres de section sont affichés en H2 sur le site.</p><div data-editor-rows="sections"><?php foreach ($p['sections'] as $i=>$row) editor_row('sections',$i,$row); if (count($p['sections'])<30) editor_row('sections',count($p['sections']),[]); ?></div><button type="button" class="add-row" data-add="sections" hidden>Ajouter une section</button>
    <h3 class="editor-heading">Questions fréquentes</h3><p><?= $p['kind']==='city'?'Conservez de 4 à 6 questions utiles pour cette ville.':'Les questions sont facultatives pour un article.' ?></p><div data-editor-rows="faq"><?php foreach ($p['faq']??[] as $i=>$row) editor_row('faq',$i,$row); if (count($p['faq']??[])<6) editor_row('faq',count($p['faq']??[]),[]); ?></div><button type="button" class="add-row" data-add="faq" hidden>Ajouter une question</button>
    <?php if ($p['kind']==='city'): ?><h3 class="editor-heading">Ville et zone d’intervention</h3><div class="editor-columns"><div><?php editor_field('city','Ville',$p['city']); editor_field('postal_code','Code postal',$p['postal_code']); editor_field('districts','Quartiers et repères géographiques',implode("\n",$p['districts']),true,'Un nom par ligne. Vérifiez les sources avant tout ajout.'); ?></div><div><?php editor_field('verified_districts','Quartiers réellement desservis et confirmés',implode("\n",$p['verified_districts']),true,'Un nom par ligne, repris exactement dans la liste des quartiers.'); editor_field('coverage_evidence','Confirmation de desserte',$p['coverage_evidence'],true,'Consignez la personne ayant confirmé la couverture et la date.'); ?></div></div><?php editor_field('local_note','Présentation du secteur',$p['local_note'],true); editor_field('neighbors','Liens vers les villes proches',implode("\n",$p['neighbors']),true,'Un slug existant par ligne, par exemple : nogent-sur-marne.'); ?><label class="checkbox"><input type="checkbox" name="coverage_verified" <?= ($p['coverage_verified']??false)===true?'checked':'' ?>>La desserte de cette ville et des quartiers annoncés a été confirmée.</label><?php endif ?>
    <label class="checkbox"><input type="checkbox" name="editorial_verified" <?= ($p['editorial_verified']??false)===true?'checked':'' ?>>J’ai relu le contenu et vérifié les informations présentées.</label>
    <p class="field-help">Les avis, photos, sources et autres données complémentaires existants sont conservés. Leur édition est disponible en mode avancé.</p>
    <template id="section-template"><?php editor_row('sections',0,[]); ?></template><template id="faq-template"><?php editor_row('faq',0,[]); ?></template>
    <?php
}
