const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../src/assets/cart.js'), 'utf8');
const item = (extra = {}) => ({v:'1001',h:'ring',t:'Ring',p:20,q:1,max:0,...extra});

function cartHarness(initial = [], analytics = true) {
  const listeners = {}, events = [];
  let saved = initial;
  const window = {NI_CART:{shop:'https://namastebookshop.com',domain:'namastejewelryshop.com',
    brand:'Namaste Jewelry Shop',ref:'namastejewelryshop',attr:'?attributes%5BStorefront%5D=Namaste%20Jewelry%20Shop'},addEventListener(){}};
  if (analytics) window.gtag = (...args) => events.push(args);
  vm.runInNewContext(source, {window,
    document:{querySelector:()=>null,querySelectorAll:()=>[],addEventListener:(event,cb)=>{listeners[event]=cb;}},
    localStorage:{getItem:()=>JSON.stringify(saved),setItem:(_,value)=>{saved=JSON.parse(value);}},
    fetch:()=>Promise.reject(new Error('offline test')),setTimeout:()=>0,console
  });
  function click(attributes, dataset = {}) {
    const target={dataset,disabled:false,textContent:'Add to cart',href:'',
      classList:{add(){},remove(){}},hasAttribute:key=>key in attributes,
      getAttribute:key=>attributes[key]??null,closest:()=>null};
    listeners.click({target:{closest:()=>target},preventDefault(){}});
    return target;
  }
  return {events,click,window,items:()=>saved};
}

test('add_to_cart records only quantity actually accepted below the limit', () => {
  const h=cartHarness([item({q:98,max:99})]);
  h.click({'data-atc':''},item({q:3}));
  assert.equal(h.items()[0].q,99);
  assert.equal(h.events.length,1);
  assert.equal(h.events[0][1],'add_to_cart');
  assert.equal(h.events[0][2].items[0].quantity,1);
  assert.equal(h.events[0][2].value,20);
});

test('clicking Add at the quantity limit does not report another cart addition', () => {
  const h=cartHarness([item({q:1,max:1})]);
  const button=h.click({'data-atc':''},item());
  assert.equal(h.items()[0].q,1);
  assert.equal(h.events.length,0);
  assert.equal(button.textContent,'Limit reached');
});

test('a partly capped bundle reports only the accepted items', () => {
  const h=cartHarness([item({max:1})]);
  h.click({'data-atc-items':JSON.stringify([item(),item({v:'1002',h:'chain',p:35})])});
  assert.equal(h.events.length,1);
  assert.equal(h.events[0][2].items.length,1);
  assert.equal(h.events[0][2].items[0].item_id,'1002');
  assert.equal(h.events[0][2].value,35);
});

test('checkout keeps the Shopify host, variants, quantities and source markers', () => {
  const h=cartHarness([item({q:2}),item({v:'1002',q:4,max:3}),item({v:'1003',out:true})]);
  const button=h.click({'data-checkout':''});
  const url=new URL(button.href);
  assert.equal(url.origin,'https://namastebookshop.com');
  assert.equal(url.pathname,'/cart/1001:2,1002:3');
  assert.equal(url.searchParams.get('attributes[Storefront]'),'Namaste Jewelry Shop');
  assert.equal(url.searchParams.get('attributes[Site]'),'namastejewelryshop.com');
  assert.equal(url.searchParams.get('ref'),'namastejewelryshop');
  assert.equal(url.searchParams.get('note'),'Ordered on Namaste Jewelry Shop (namastejewelryshop.com)');
  assert.equal(h.events.length,1);
  assert.equal(h.events[0][1],'begin_checkout');
  assert.equal(h.events[0][2].value,100);
  assert.deepEqual(Array.from(h.events[0][2].items,x=>x.quantity),[2,3]);
  assert.ok(h.events.every(event=>event[1]!=='purchase'));
});

test('empty and sold-out-only carts produce no checkout event or URL', () => {
  for (const items of [[],[item({out:true})]]) {
    const h=cartHarness(items);
    h.click({'data-checkout':''});
    assert.equal(h.window.NI_CART_URL(),'');
    assert.equal(h.events.length,0);
  }
});

test('cart and checkout remain usable with analytics blocked', () => {
  const h=cartHarness([],false);
  h.click({'data-atc':''},item());
  const checkout=h.click({'data-checkout':''});
  assert.equal(h.items().length,1);
  assert.match(checkout.href,/^https:\/\/namastebookshop.com\/cart\/1001:1\?/);
  assert.equal(h.events.length,0);
});
