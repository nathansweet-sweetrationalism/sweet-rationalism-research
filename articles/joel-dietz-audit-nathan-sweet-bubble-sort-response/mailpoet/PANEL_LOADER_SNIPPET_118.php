<?php
/** Browser-only loading of 14 Dietz article panels from 7 immutable GitHub templates.
 * The published WordPress post stores links; MailPoet sees no instruction payload.
 */
add_action('rest_api_init', static function () {
    register_rest_route('rcf/v1', '/dietz-panels', [
        'methods' => 'GET',
        'permission_callback' => '__return_true',
        'callback' => static function ($request) {
            $cache_key = 'sr_dietz_panels_20261112_v1';
            $data = get_transient($cache_key);
            if (!is_array($data)) {
                $source = 'https://raw.githubusercontent.com/nathansweet-sweetrationalism/sweet-rationalism-research/f39dea354d604d14a02fca178135420344b053da/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/mailpoet/COMPUTATIONAL_PANEL_TEMPLATES_2026-11-12.txt';
                $response = wp_safe_remote_get($source, ['timeout' => 18, 'redirection' => 2]);
                if (is_wp_error($response) || wp_remote_retrieve_response_code($response) !== 200) {
                    return new WP_Error('rcf_panels_unavailable', 'Computational instruction payload temporarily unavailable.', ['status' => 503]);
                }
                $body = wp_remote_retrieve_body($response);
                $data = json_decode($body, true);
                $names = ['doi', 'tadpole', 'xenobot', 'score', 'ports', 'validator', 'authorship'];
                if (!is_array($data)
                    || ($data['schema'] ?? '') !== 'rcf-computational-panels.v1'
                    || !isset($data['templates']) || !is_array($data['templates'])
                    || count($data['templates']) !== 7
                    || array_keys($data['templates']) !== $names
                    || strlen($body) > 200000
                ) {
                    return new WP_Error('rcf_panels_invalid', 'Instruction payload schema mismatch.', ['status' => 502]);
                }
                set_transient($cache_key, $data, 12 * HOUR_IN_SECONDS);
            }
            if ($request->get_param('probe') === '1') {
                return rest_ensure_response([
                    'ok' => true,
                    'schema' => $data['schema'],
                    'template_count' => count($data['templates']),
                    'template_keys' => array_keys($data['templates']),
                    'placeholder' => $data['placeholder'] ?? null,
                ]);
            }
            $result = rest_ensure_response($data);
            $result->header('Cache-Control', 'public, max-age=3600');
            return $result;
        },
    ]);
});
add_action('wp_footer', static function () {
    if ((int) get_queried_object_id() !== 218725796) { return; }
    echo <<<'SR_JS'
<script id="sr-dietz-js-panel-loader">
(function () {
  'use strict';
  var endpoint = '/wp-json/rcf/v1/dietz-panels';
  var panelPrefix = 'rcf-computational-';
  function reveal() {
    var hash = window.location.hash.slice(1);
    if (!/^rcf-computational-[a-z0-9-]+(?:-open)?$/.test(hash)) return;
    var node = document.getElementById(hash);
    if (!node) return;
    var details = node.matches('details.rcf-computational-test') ? node :
                  node.closest('details.rcf-computational-test');
    if (!details) return;
    details.open = true;
    window.requestAnimationFrame(function () { details.scrollIntoView({block:'start'}); });
  }
  function init() {
    var anchors = Array.from(document.querySelectorAll('a.rcf-computational-trigger[data-rcf-panel]'));
    if (anchors.length !== 14) return;
    fetch(endpoint, {credentials:'same-origin'}).then(function (r) {
      if (!r.ok) throw new Error('Panel asset unavailable: HTTP ' + r.status);
      return r.json();
    }).then(function (data) {
      if (!data || data.schema !== 'rcf-computational-panels.v1' || !data.templates) throw new Error('Panel schema mismatch');
      var replacements = [];
      anchors.forEach(function (anchor) {
        var id = anchor.getAttribute('data-rcf-panel');
        var match = /^rcf-computational-(doi|tadpole|xenobot|score|ports|validator|authorship)-(quick|analysis)$/.exec(id || '');
        if (!match || !data.templates[match[1]]) throw new Error('Missing panel ' + id);
        var html = data.templates[match[1]].split('__RCF_PANEL_ID__').join(id);
        var template = document.createElement('template');
        template.innerHTML = html.trim();
        var details = template.content.firstElementChild;
        if (!details || details.tagName !== 'DETAILS' || details.id !== id || !details.classList.contains('rcf-computational-test')) {
          throw new Error('Panel markup invalid: ' + id);
        }
        replacements.push([anchor, details]);
      });
      replacements.forEach(function (pair) { pair[0].replaceWith(pair[1]); });
      reveal();
    }).catch(function (err) {
      // Preserve source links if the external payload cannot be loaded.
      if (window.console && console.error) console.error('Computational instruction loader:', err);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true});
  else init();
  window.addEventListener('hashchange', reveal);
  window.addEventListener('pageshow', reveal);
})();
</script>
SR_JS;
}, 32);
