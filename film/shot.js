// Quick stills of the film at given times (seconds).  usage: node shot.js 5.5 12 28
const {chromium}=require('playwright');const path=require('path');
(async()=>{
  const times=process.argv.slice(2).map(Number);
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
  p.on('pageerror',e=>console.log('ERR',e.message));
  await p.goto('file://'+path.join(__dirname,'index.html'));await p.evaluate(()=>window.ready);
  for(const t of times){await p.evaluate(t=>render(t),t);await p.screenshot({path:path.join(__dirname,`still_${t}.png`)});}
  await b.close();
})();
