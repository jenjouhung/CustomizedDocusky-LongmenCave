const {chromium}=require('/Users/joey/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');

(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.goto('http://127.0.0.1:4180');
  await page.locator('.record').first().waitFor();
  await page.getByRole('button',{name:/^視覺化：/}).click();
  await page.getByRole('tab',{name:'資料表格'}).click();
  await page.locator('.viz-data-table tbody tr').first().waitFor();
  assert.equal(await page.locator('.viz-data-table thead th').allTextContents().then(x=>x.join('|')),'序號|類別名稱|文件數|比例|累積比例');
  const rows=await page.locator('.viz-data-table tbody tr').count();assert(rows>0);
  const percentages=await page.locator('.viz-data-table tbody tr').first().locator('td').nth(3).textContent();assert.match(percentages,/%/);
  const firstLabel=await page.locator('.viz-table-label').first().textContent();await page.locator('#viz-search').fill(firstLabel.slice(0,1));assert(await page.locator('.viz-data-table tbody tr.is-unmatched').count()<rows);
  await page.locator('#viz-search').fill('不存在的項目');
  assert.equal(await page.locator('.viz-data-table tbody tr').count(),rows);
  assert.equal(await page.locator('.viz-data-table tbody tr.is-unmatched').count(),rows);
  await page.locator('.viz-data-table tbody tr').first().click();
  assert(await page.locator('.viz-data-table tbody tr.is-selected').count()===1);
  await page.locator('#viz-zoom').fill('70');assert.equal(await page.locator('#viz-zoom-value').textContent(),'70%');
  const downloadPromise=page.waitForEvent('download');await page.locator('#viz-export').click();const download=await downloadPromise;assert.match(download.suggestedFilename(),/\.csv$/);
  await page.getByRole('tab',{name:'長條圖'}).click();assert(await page.locator('.viz-bar-row').count()===rows);
  assert.deepEqual(errors,[]);
  console.log('Visualization table flows passed; rows:',rows);
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exit(1)});
