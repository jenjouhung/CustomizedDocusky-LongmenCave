import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const html=fs.readFileSync(new URL('../web/index.html',import.meta.url),'utf8');
const app=fs.readFileSync(new URL('../web/app.js',import.meta.url),'utf8');

test('後分類使用固定中文分段控制與緊湊工具列',()=>{
 assert.match(html,/role="tab" data-type="Metadata"[^>]*>後設資料<\/button>/);
 assert.match(html,/role="tab" data-type="Tag"[^>]*>內文標籤<\/button>/);
 assert.match(html,/class="facet-tools"/);
 assert.match(html,/id="clear-facets">清除全部<\/button>/);
 assert.match(html,/同欄多選採 OR/);
 assert.doesNotMatch(html,/>Metadata<\/option>|>Tag<\/option>/);
});

test('分段控制支援選取狀態、方向鍵及中文條件來源',()=>{
 assert.match(app,/setAttribute\('aria-selected'/);
 assert.match(app,/ArrowLeft','ArrowRight/);
 assert.match(app,/內文標籤':'後設資料/);
});
