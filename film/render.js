// Renders film/index.html to numbered JPEG frames, then encode with ffmpeg (see README).
// usage: node render.js [workers=4] [outDir=./frames]
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const FPS=30,DUR=40,N=FPS*DUR,W=+process.argv[2]||4;
const out=path.resolve(process.argv[3]||path.join(__dirname,'frames'));fs.mkdirSync(out,{recursive:true});
const page_url='file://'+path.join(__dirname,'index.html');
(async()=>{
  const b=await chromium.launch();
  await Promise.all([...Array(W).keys()].map(async w=>{
    const p=await b.newPage({viewport:{width:1920,height:1080}});
    await p.goto(page_url);await p.evaluate(()=>window.ready);
    for(let f=w;f<N;f+=W){await p.evaluate(t=>render(t),f/FPS);
      await p.screenshot({path:`${out}/f_${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});}
    await p.close();
  }));
  await b.close();console.log('done ->',out);
})();
