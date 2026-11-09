/* YK CROWN — shared site script: floating WhatsApp button + enquiry form handling. */
(function () {
  var WA_NUMBER = '351969058818';
  var EMAIL = 'info@ykcrown.com';
  // When the n8n lead webhook is ready, paste its Production URL here.
  // Until then, enquiries are handed over to WhatsApp so none are lost.
  var LEAD_ENDPOINT = '';

  function lang() {
    var l = (document.documentElement.lang || 'en').slice(0, 2);
    return l === 'pt' || l === 'zh' ? l : 'en';
  }
  var T = {
    en: { wa: 'Chat on WhatsApp', hello: 'Hello YK CROWN, I would like more information', about: 'about', sent: 'Thank you — we received your enquiry and will reply within one business day.', fallback: 'Opening WhatsApp to send your enquiry…' },
    pt: { wa: 'Falar no WhatsApp', hello: 'Olá YK CROWN, gostaria de receber mais informações', about: 'sobre', sent: 'Obrigado — recebemos o seu pedido e respondemos no prazo de um dia útil.', fallback: 'A abrir o WhatsApp para enviar o seu pedido…' },
    zh: { wa: 'WhatsApp 咨询', hello: '您好 YK CROWN，我想了解更多信息', about: '关于', sent: '谢谢，我们已收到您的咨询，将在一个工作日内回复。', fallback: '正在打开 WhatsApp 发送您的咨询…' }
  };
  function waLink(text) { return 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(text); }
  function track(name, params) {
    try { if (window.gtag) window.gtag('event', name, params || {}); } catch (e) {}
    try { if (window.fbq) window.fbq('track', name === 'generate_lead' ? 'Lead' : 'Contact'); } catch (e) {}
  }

  /* Floating WhatsApp button */
  var css = '.yk-wa{position:fixed;right:18px;bottom:18px;z-index:900;display:flex;align-items:center;gap:10px;background:#25d366;color:#fff;border-radius:999px;padding:12px 18px 12px 14px;font:600 14px/1 Arial,Helvetica,sans-serif;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.22)}.yk-wa svg{width:24px;height:24px;flex:none}.yk-wa:hover{filter:brightness(1.05)}@media(max-width:560px){.yk-wa span{display:none}.yk-wa{padding:14px}}.lightbox.open~.yk-wa{display:none}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var a = document.createElement('a');
  a.className = 'yk-wa'; a.target = '_blank'; a.rel = 'noopener';
  a.setAttribute('aria-label', 'WhatsApp');
  a.innerHTML = '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3.3 8.6 3.3 15.6c0 2.4.7 4.7 1.9 6.7L3 29l6.9-2.1c1.9 1 4 1.6 6.1 1.6 7 0 12.7-5.7 12.7-12.7S23 3 16 3zm0 23.2c-1.9 0-3.8-.5-5.4-1.5l-.4-.2-4.1 1.2 1.3-4-.3-.4c-1.1-1.7-1.6-3.6-1.6-5.6C5.5 9.8 10.2 5.2 16 5.2s10.5 4.6 10.5 10.4S21.8 26.2 16 26.2zm5.8-7.8c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.3-.5-2.5-1.6-.9-.8-1.6-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.3 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.9 1.1 3.4.9 4 .8.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg><span></span>';
  function refreshWa() {
    var t = T[lang()];
    a.querySelector('span').textContent = t.wa;
    var page = document.title.split('|')[1] ? document.title.split('|')[1].trim() : 'YK CROWN';
    a.href = waLink(t.hello + ' ' + t.about + ' ' + page + '.');
  }
  refreshWa();
  document.body.appendChild(a);
  new MutationObserver(refreshWa).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });

  /* Any link marked data-wa="Topic" gets a prefilled WhatsApp message */
  document.querySelectorAll('[data-wa]').forEach(function (el) {
    el.addEventListener('click', function () {
      var t = T[lang()];
      el.href = waLink(t.hello + ' ' + t.about + ' ' + el.getAttribute('data-wa') + '.');
    });
  });
  document.addEventListener('click', function (e) {
    var l = e.target.closest('a[href*="wa.me"]');
    if (l) track('contact_whatsapp', { location: l.className || 'link' });
  });

  /* Enquiry form */
  var form = document.getElementById('enquiry-form');
  if (!form) return;
  var params = new URLSearchParams(location.search);
  var interest = params.get('interest');
  if (interest) {
    var sel = form.querySelector('[name="interest"]');
    var norm = function (s) { return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); };
    var match = Array.prototype.find.call(sel.options, function (o) { return o.value && norm(o.value).indexOf(norm(interest)) === 0; });
    if (match) sel.value = match.value;
  }
  var status = document.getElementById('form-status');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.website && form.website.value) return; // spam trap
    var d = {};
    new FormData(form).forEach(function (v, k) { d[k] = String(v).trim(); });
    d.page = location.href;
    d.referrer = document.referrer || null;
    ['utm_source', 'utm_medium', 'utm_campaign'].forEach(function (k) { if (params.get(k)) d[k] = params.get(k); });
    d.submitted_at = new Date().toISOString();
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    function viaWhatsApp() {
      var t = T[lang()];
      var msg = t.hello + '.\n\n' +
        'Name: ' + d.name + '\nEmail: ' + d.email + (d.phone ? '\nPhone: ' + d.phone : '') +
        (d.country ? '\nCountry: ' + d.country : '') + '\nInterest: ' + (d.interest || '-') +
        (d.message ? '\n\n' + d.message : '');
      status.textContent = t.fallback;
      track('generate_lead', { method: 'whatsapp_fallback', interest: d.interest });
      window.location.href = waLink(msg);
      btn.disabled = false;
    }

    if (!LEAD_ENDPOINT) { viaWhatsApp(); return; }
    fetch(LEAD_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        form.reset();
        status.textContent = T[lang()].sent;
        track('generate_lead', { method: 'form', interest: d.interest });
        btn.disabled = false;
      })
      .catch(viaWhatsApp);
  });
})();
