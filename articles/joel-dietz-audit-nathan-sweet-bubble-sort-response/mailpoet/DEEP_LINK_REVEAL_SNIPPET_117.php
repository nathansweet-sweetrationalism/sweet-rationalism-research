<?php
/** Scoped URL-fragment reveal for the 14 computational panels of article #218725796. */
add_action('wp_footer', static function () {
    if (!is_singular('post') || (int) get_queried_object_id() !== 218725796) {
        return;
    }
    echo <<<'SCRIPT'
<script id="sr-computational-deep-link-reveal">
(function () {
  'use strict';
  function openTarget() {
    var hash = window.location.hash || '';
    if (!/^#rcf-computational-[a-z0-9-]+$/.test(hash)) return;
    var target = document.getElementById(hash.slice(1));
    if (!target) return;
    var details = target.matches('details.rcf-computational-test')
      ? target : target.closest('details.rcf-computational-test');
    if (!details) return;
    details.open = true;
    var summary = details.querySelector('summary');
    if (summary) {
      window.requestAnimationFrame(function () {
        summary.scrollIntoView({ behavior: 'auto', block: 'start' });
      });
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', openTarget, { once: true });
  } else {
    openTarget();
  }
  window.addEventListener('hashchange', openTarget);
  window.addEventListener('pageshow', openTarget);
})();
</script>
SCRIPT;
}, 30);
