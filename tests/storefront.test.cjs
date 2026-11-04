const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../src/assets/site.js'), 'utf8');
const css = fs.readFileSync(path.join(__dirname, '../src/assets/site.css'), 'utf8');
const settle = () => new Promise(resolve => setImmediate(resolve));

function productHarness(result, fail = false) {
  const stockLabel = {textContent: 'In stock'};
  const stock = {classList: {toggle() {}}, querySelector: () => stockLabel};
  const buy = {dataset: {}, disabled: false, textContent: 'Add to cart', setAttribute(k,v) {this[k]=v;}};
  const price = {textContent: '$29.00'}, cmp = {hidden: true};
  const nodes = {'#buy':buy, '#price':price, '#stock':stock, '#cmp':cmp};
  vm.runInNewContext(source, {
    document: {querySelector:s=>nodes[s]||null, querySelectorAll:()=>[]},
    window: {NI_PRODUCT:{shop:'https://example.test',handle:'ring'}},
    fetch:()=>fail ? Promise.reject(new Error('network unavailable')) : Promise.resolve({ok:true,json:async()=>result})
  });
  return {buy,price,stockLabel};
}

test('failed live stock check does not claim an item is in stock', async () => {
  const p = productHarness(null, true); await settle();
  assert.equal(p.stockLabel.textContent, 'Availability checked at checkout');
  assert.equal(p.buy.disabled, false);
  assert.equal(p.price.textContent, '$29.00');
});
test('available variant still updates price and enables add to cart', async () => {
  const p = productHarness({variants:[{id:1,price:3500,available:true}]}); await settle();
  assert.equal(p.stockLabel.textContent,'In stock'); assert.equal(p.price.textContent,'$35.00');
  assert.equal(p.buy.disabled,false); assert.equal(p.buy.dataset.v,1);
});
test('sold-out variant still disables add to cart', async () => {
  const p = productHarness({variants:[{id:1,price:3500,available:false}]}); await settle();
  assert.equal(p.stockLabel.textContent,'Sold out'); assert.equal(p.buy.disabled,true);
});

async function shopHarness(n) {
  const grid={innerHTML:'',insertAdjacentHTML(_,html){this.innerHTML+=html;}}, more={hidden:false}, count={textContent:''};
  const nodes={'.shop':{dataset:{}}, '#grid':grid,'#more':more,'#count':count,'#q':{},'#sort':{},'#sort option[value=best]':{}};
  const data=Array.from({length:n},(_,i)=>({h:'p'+i,t:'Product '+i,i:'image.jpg',c:'rings',p:20,r:i,d:'2026-11-03'}));
  const meta={aisles:{rings:{name:'Rings',color:'#000'}}};
  vm.runInNewContext(source, {
    document:{querySelector:s=>nodes[s]||null,querySelectorAll:()=>[]}, window:{},
    fetch:url=>Promise.resolve({json:async()=>url.includes('catalog')?data:meta}),
    location:{pathname:'/shop/',search:''},history:{replaceState(){}},URLSearchParams
  });
  await settle(); return {grid,more,count};
}
for (const n of [0,3,48]) {
  test(`pagination is marked hidden with ${n} results`, async () => {
    const {more,count}=await shopHarness(n);assert.equal(more.hidden,true);assert.equal(count.textContent,`${n} items`);
  });
}
for (const n of [49,96]) {
  test(`pagination remains available until final page for ${n} results`, async () => {
    const {more,grid}=await shopHarness(n);assert.equal(more.hidden,false);
    assert.equal((grid.innerHTML.match(/<h3>/g)||[]).length,48);
    more.onclick();assert.equal(more.hidden,true);
    assert.equal((grid.innerHTML.match(/<h3>/g)||[]).length,n);
  });
}
test('hidden pagination selector overrides generic button display', () => {
  assert.match(css,/\.btn\{display:inline-flex/);
  assert.match(css,/#more\[hidden\]\{display:none\}/);
});

test('search suggests only gemstone landing pages present in the build', async () => {
  let scheduled;
  const hq={value:'Angelite',setAttribute(){} ,addEventListener(){}},sg={innerHTML:'',hidden:true};
  const meta={fams:{angelite:'Angelite',amethyst:'Amethyst'},stone_pages:{amethyst:'Amethyst'},brands:{}};
  vm.runInNewContext(source, {
    document:{querySelector:s=>({'#hq':hq,'#sugg':sg}[s]||null),querySelectorAll:()=>[],addEventListener(){}},
    window:{},fetch:url=>Promise.resolve({json:async()=>url.includes('catalog')?[]:meta}),
    setTimeout:cb=>{scheduled=cb;},clearTimeout(){}
  });
  hq.oninput();await scheduled();
  assert.doesNotMatch(sg.innerHTML,/\/stones\/angelite\//);
  assert.match(sg.innerHTML,/\/shop\/\?q=Angelite/);
  hq.value='Amethyst';hq.oninput();await scheduled();
  assert.match(sg.innerHTML,/\/stones\/amethyst\//);
});
