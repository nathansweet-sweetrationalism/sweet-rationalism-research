# Private evidence index

Names and SHA-256 only. The files are held locally for the owner, outside this repository.

- `wp_get_post_raw.txt`  d4779e9bdd249a8ea6e67bd01d15d5768d4e746d54b4a381cde45ea76b9d4493
- `article_raw.html`  034280325838f1cd563709772311e2de3556f56931b9229538ef944c70c51a98
- `article.json`  ff81f932cc1a5d76795f77d6f6e67f0e8cecd8b079406441e4ba9d0f9c03a416
- `links.json`  13af79806585af6a8c1c79af6c89f9529b0e0e56203dd0d1f11fc25ad16d8579
- `link_results.json`  359fb23d05430b83aa80913671d84ff32639d4e199dfaf9246929c931e91e08c
- `panel_inventory.json`  1399d939db41e417dc172b57146e0ba99354fa416d79725e6dcfef5f8fe28991
- `patch/article_patched.html`  f4d791fda72274f5e310ffcf8c36453cb068153bfa65080f0cbb4aef3de16734
- `patch/prompt_patch.diff`  abd7ccde4221e73c85e8eb195458205411a67eca394eacdcaf90dfa8e4e9ea8a
- `gate_bottom_line.json`  75bc1b9b8b5b06aaf01efff7e2a5760b1e57e45182ba239ece33d5050fa8268e
- `gate_framework.txt`  2831b31d894c4d8385e8a33bb4b4509ec8ae6212c43236c0263957f5d26bc0e6
- `gate_prose.json`  3a02971e6f4f3369647e6fd8332526aff47ab256081a9b239dcb152daf7e22a3

`article_raw.html` is the exact draft content at the snapshot. `patch/` holds the proposed three-substitution panel repair (full patched HTML and unified diff). `links.json` and `link_results.json` list every link in the draft with its signed-out status. `gate_*` are outputs of the repository editorial gate scripts.
