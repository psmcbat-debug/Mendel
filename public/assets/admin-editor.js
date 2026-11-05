// Progressive enhancement: the form also saves without JavaScript.
for (const button of document.querySelectorAll('[data-add]')) {
  button.hidden = false;
  const kind = button.dataset.add;
  const container = document.querySelector(`[data-editor-rows="${kind}"]`);
  let next = container.children.length;
  button.addEventListener('click', () => {
    const max = kind === 'sections' ? 30 : 10;
    if (container.children.length >= max) return;
    const row = document.querySelector(kind === 'sections' ? '#section-template' : '#faq-template').content.firstElementChild.cloneNode(true);
    for (const field of row.querySelectorAll('[name]')) {
      const oldId = field.id;
      field.name = field.name.replace('[0]', `[${next}]`);
      field.id = `${oldId}-${next}`;
      const label = row.querySelector(`label[for="${oldId}"]`);
      if (label) label.htmlFor = field.id;
      const help = row.querySelector(`#${oldId}-help`);
      if (help) { help.id = `${field.id}-help`; field.setAttribute('aria-describedby', help.id); }
    }
    row.querySelector('legend').textContent = `${kind === 'sections' ? 'Section' : 'Question'} ${next + 1}`;
    next++;
    enableRemoval(row);
    container.append(row);
    row.querySelector('input,textarea').focus();
  });
}
function enableRemoval(row) {
  const button = row.querySelector('.remove-row');
  button.hidden = false;
  button.addEventListener('click', () => {
    const hasText = [...row.querySelectorAll('input,textarea')].some(field => field.value.trim());
    if (hasText && !window.confirm('Retirer cette rubrique du formulaire ? Le changement sera appliqué uniquement après enregistrement.')) return;
    const container = row.parentElement;
    row.remove();
    document.querySelector(`[data-add="${container.dataset.editorRows}"]`).focus();
  });
}
document.querySelectorAll('[data-editor-rows] > .editor-row').forEach(enableRemoval);
