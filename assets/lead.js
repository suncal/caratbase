/* CaratBase — saving a valuation, and capturing the intent behind it.

   A lead is the asset. Everything else on this site depends on Google deciding to send
   traffic; a saved valuation with a stated intent does not, and it is the one thing that
   survives an algorithm change.

   The rule here is that we never ask for an email we cannot do anything with. The worker
   reports whether a mailer is configured (/api/capabilities -> {email:true|false}), and
   until it is, this module offers the thing that genuinely works today — saving to the
   vault on your own device — and does not collect an address under a promise we would
   not keep. The moment RESEND_API_KEY and MAIL_FROM exist on the worker, the email field
   appears on its own with no change here.

   Intent is captured either way, because "I want to sell this" next to a stone spec is
   the valuable half and costs the visitor nothing.
*/
const Lead = (function () {
  const EP = window.CB_ANALYTICS_ENDPOINT || '';
  let canEmail = null;                 // null = not yet known

  const INTENTS = [
    ['sell',    'Sell it',            'What it would fetch, and who pays most'],
    ['insure',  'Insure it',          'The replacement figure, and what cover costs'],
    ['appraise', 'Get it appraised',  'A document for insurance or probate'],
    ['curious', 'Just curious',       'No plans — I wanted the number'],
  ];

  function capabilities() {
    if (!EP) return Promise.resolve({ email: false });
    return fetch(EP + '/api/capabilities', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : { email: false }; })
      .catch(function () { return { email: false }; });
  }

  function valid(email) {
    return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(email || '').trim());
  }

  /* `spec` is whatever the page knows about the piece: carat, shape, color, clarity,
     origin, cert, est_low, est_high. All optional. */
  function render(el, spec, opts) {
    const node = typeof el === 'string' ? document.getElementById(el) : el;
    if (!node) return;
    const o = opts || {};

    capabilities().then(function (caps) {
      canEmail = !!caps.email;

      const emailField = canEmail
        ? '<div class="field" style="margin-top:12px">' +
            '<label for="ldEmail">Email the report to</label>' +
            '<input type="email" id="ldEmail" placeholder="you@example.com" autocomplete="email">' +
          '</div>'
        : '';

      const action = canEmail ? 'Send me this report' : 'Save this valuation';
      const sub = canEmail
        ? 'One email with the figures on this page. No list, no follow-up sequence, and you can say so if you would rather we did not keep it.'
        : 'Saved on this device only — it does not leave your browser. Tell us what you are planning and we will point you at the right next step.';

      node.innerHTML =
        '<div class="panel" style="border-color:var(--gold-2)">' +
          '<div class="eyebrow">' + (o.eyebrow || 'Keep this') + '</div>' +
          '<h3 style="font-size:21px;margin:6px 0 4px">' + (o.title || 'What are you planning to do with it?') + '</h3>' +
          '<p class="small" style="margin-bottom:14px">' + sub + '</p>' +
          '<div class="ld-intents" id="ldIntents">' +
            INTENTS.map(function (i) {
              return '<button type="button" class="btn btn-ghost ld-intent" data-intent="' + i[0] + '">' +
                     i[1] + '</button>';
            }).join('') +
          '</div>' +
          '<p class="small" id="ldHint" style="margin-top:10px;min-height:1.2em"></p>' +
          emailField +
          '<button type="button" class="btn btn-gold" id="ldGo" style="margin-top:12px">' + action + '</button>' +
          '<p class="small" id="ldOut" style="margin-top:10px"></p>' +
        '</div>';

      let intent = '';
      node.querySelectorAll('.ld-intent').forEach(function (b) {
        b.addEventListener('click', function () {
          intent = b.dataset.intent;
          node.querySelectorAll('.ld-intent').forEach(function (x) { x.classList.remove('on'); });
          b.classList.add('on');
          const found = INTENTS.filter(function (i) { return i[0] === intent; })[0];
          document.getElementById('ldHint').textContent = found ? found[2] : '';
        });
      });

      document.getElementById('ldGo').addEventListener('click', function () {
        const out = document.getElementById('ldOut');
        const field = document.getElementById('ldEmail');
        const email = field ? field.value.trim() : '';

        if (canEmail && !valid(email)) {
          out.textContent = 'That email does not look right — check it and try again.';
          return;
        }

        const payload = Object.assign({ intent: intent || 'curious' }, spec || {});
        if (email) payload.email = email;
        if (window.cbTrack) cbTrack('lead', payload);

        if (canEmail && email) {
          out.textContent = 'Sending…';
          fetch(EP + '/api/send-report', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ email: email, subject: o.subject || 'Your CaratBase valuation',
                                   html: (o.html && o.html()) || document.title })
          }).then(function (r) { return r.json().catch(function () { return {}; }); })
            .then(function (d) {
              out.textContent = d && d.ok
                ? 'Sent. Check your inbox — and your spam folder, just in case.'
                : 'We could not send it just now. Nothing was lost; try again shortly.';
            })
            .catch(function () {
              out.textContent = 'We could not send it just now. Nothing was lost; try again shortly.';
            });
          return;
        }

        /* No mailer: save locally, which is a promise we can actually keep — but only
           claim the save if it actually happened. Vault needs vault.js on the page, and
           localStorage throws in private mode. */
        let saved = false;
        if (typeof Vault !== 'undefined' && spec) {
          try { Vault.add(Object.assign({ intent: payload.intent }, spec)); saved = true; }
          catch (e) { saved = false; }
        }
        out.textContent = saved
          ? 'Saved to your vault on this device. ' + (o.after || 'The options below are the usual next step.')
          : 'Noted — thanks. ' + (o.after || 'The options below are the usual next step.');
      });
    });
  }

  return { render: render, intents: INTENTS };
})();

window.Lead = Lead;
