import os
import ssl
import json
import urllib.request
import urllib.error
from flask import Flask, request, Response

app = Flask(__name__)

# ── HTML aplikacji ────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Model Studio</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;background:#0e0c0a;color:#f0ece6;min-height:100vh}
a{color:#c9a96e;text-decoration:none}a:hover{text-decoration:underline}
.hdr{display:flex;align-items:center;justify-content:space-between;padding:15px 28px;border-bottom:0.5px solid rgba(240,236,230,0.1);background:#0e0c0a;position:sticky;top:0;z-index:100}
.logo{font-family:'Playfair Display',serif;font-size:19px;letter-spacing:0.04em}.logo span{color:#c9a96e}
.layout{display:grid;grid-template-columns:440px 1fr;min-height:calc(100vh - 54px)}
@media(max-width:800px){.layout{grid-template-columns:1fr}.lpanel{max-height:none;border-right:none;border-bottom:0.5px solid rgba(240,236,230,0.1)}}
.lpanel{border-right:0.5px solid rgba(240,236,230,0.1);padding:22px 20px;display:flex;flex-direction:column;overflow-y:auto;max-height:calc(100vh - 54px)}
.rpanel{padding:22px 26px;display:flex;flex-direction:column;gap:16px;overflow-y:auto;max-height:calc(100vh - 54px)}
.section{padding:16px 0;border-bottom:0.5px solid rgba(240,236,230,0.07)}
.section:last-of-type{border-bottom:none;padding-bottom:0}
.sec-title{font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:#c9a96e;font-weight:500;margin-bottom:11px}
.field-lbl{font-size:10px;color:rgba(240,236,230,0.38);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px}
input[type=text],input[type=password],select{background:rgba(240,236,230,0.06);border:0.5px solid rgba(240,236,230,0.18);border-radius:8px;padding:10px 13px;color:#f0ece6;font-size:12px;font-family:'DM Sans',sans-serif;outline:none;width:100%;transition:border-color 0.2s}
input:focus,select:focus{border-color:rgba(201,169,110,0.65)}
input::placeholder{color:rgba(240,236,230,0.28)}
select{cursor:pointer}select option{background:#1a1714}
.api-row{display:flex;gap:8px}.api-row input{flex:1}
.iBtn{width:38px;height:38px;flex-shrink:0;border-radius:8px;border:0.5px solid rgba(240,236,230,0.18);background:rgba(240,236,230,0.04);color:rgba(240,236,230,0.55);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background 0.2s}
.iBtn:hover{background:rgba(240,236,230,0.1)}
.hint{font-size:10px;color:rgba(240,236,230,0.28);margin-top:6px;line-height:1.6;font-weight:300}
.upload-cols{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.upzone{border:1px dashed rgba(201,169,110,0.32);border-radius:10px;padding:18px 10px;text-align:center;cursor:pointer;transition:all 0.2s;background:rgba(201,169,110,0.025);position:relative;min-height:145px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.upzone:hover,.upzone.drag{border-color:rgba(201,169,110,0.7);background:rgba(201,169,110,0.07)}
.upzone input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;padding:0}
.upzone h4{font-size:11px;font-weight:500;margin:7px 0 3px;color:#f0ece6}
.upzone p{font-size:10px;color:rgba(240,236,230,0.38);font-weight:300;line-height:1.5}
.badge{font-size:9px;letter-spacing:0.08em;text-transform:uppercase;padding:2px 7px;border-radius:3px;margin-bottom:7px}
.bp{background:rgba(201,169,110,0.18);color:#c9a96e;border:0.5px solid rgba(201,169,110,0.35)}
.bm{background:rgba(56,138,221,0.15);color:rgba(183,212,244,0.9);border:0.5px solid rgba(56,138,221,0.3)}
.prevBox{display:none;position:relative;border-radius:9px;overflow:hidden;background:rgba(240,236,230,0.04);border:0.5px solid rgba(240,236,230,0.1)}
.prevBox.on{display:block}
.prevBox img{width:100%;max-height:185px;object-fit:contain;display:block}
.delBtn{position:absolute;top:6px;right:6px;width:22px;height:22px;border-radius:4px;background:rgba(14,12,10,0.85);border:0.5px solid rgba(240,236,230,0.2);color:#f0ece6;cursor:pointer;font-size:11px;display:flex;align-items:center;justify-content:center}
.prevLbl{position:absolute;bottom:0;left:0;right:0;padding:5px 8px;background:rgba(14,12,10,0.75);font-size:10px;color:rgba(240,236,230,0.6);font-weight:300}
.chip-row{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:11px;padding:5px 11px;border-radius:100px;border:0.5px solid rgba(240,236,230,0.18);background:transparent;color:rgba(240,236,230,0.58);cursor:pointer;transition:all 0.18s;font-family:'DM Sans',sans-serif;white-space:nowrap}
.chip:hover{border-color:rgba(201,169,110,0.5);color:#f0ece6}
.chip.on{background:rgba(201,169,110,0.15);border-color:#c9a96e;color:#c9a96e}
.preset-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:8px}
.preset{border-radius:7px;overflow:hidden;cursor:pointer;border:1.5px solid transparent;transition:all 0.2s;aspect-ratio:3/4;background:rgba(240,236,230,0.06);display:flex;align-items:center;justify-content:center;font-size:10px;color:rgba(240,236,230,0.4);text-align:center;padding:5px;position:relative}
.preset.on{border-color:#c9a96e}.preset:hover{border-color:rgba(201,169,110,0.5)}
.preset span{position:relative;z-index:1;font-size:9px;background:rgba(14,12,10,0.75);padding:2px 5px;border-radius:3px}
.gen-btn{width:100%;padding:15px;background:#c9a96e;border:none;border-radius:10px;color:#0e0c0a;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;letter-spacing:0.08em;text-transform:uppercase;cursor:pointer;transition:all 0.22s;margin-top:16px}
.gen-btn:hover:not(:disabled){background:#dbbf87;transform:translateY(-1px)}
.gen-btn:disabled{background:rgba(201,169,110,0.2);color:rgba(14,12,10,0.4);cursor:not-allowed}
.status{padding:11px 15px;border-radius:8px;font-size:12px;line-height:1.6;display:none}
.status.on{display:block}
.status.info{background:rgba(56,138,221,0.09);border:0.5px solid rgba(56,138,221,0.28);color:rgba(183,212,244,0.9)}
.status.err{background:rgba(226,75,74,0.09);border:0.5px solid rgba(226,75,74,0.28);color:rgba(240,193,193,0.9)}
.status.ok{background:rgba(29,158,117,0.09);border:0.5px solid rgba(29,158,117,0.28);color:rgba(159,225,203,0.9)}
.prog{display:none;align-items:center;gap:12px;font-size:11px;color:rgba(240,236,230,0.45)}
.prog.on{display:flex}
.prog-bar{flex:1;height:2px;background:rgba(240,236,230,0.1);border-radius:2px;overflow:hidden}
.prog-fill{height:100%;background:#c9a96e;border-radius:2px;transition:width 0.5s;width:0%}
.dot{width:7px;height:7px;border-radius:50%;background:#c9a96e;flex-shrink:0;animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.2}}
.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;opacity:0.28;min-height:340px;text-align:center}
.empty p{font-size:13px;line-height:1.8;max-width:220px;font-weight:300}
.results-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.img-card{position:relative;border-radius:12px;overflow:hidden;background:rgba(240,236,230,0.04);border:0.5px solid rgba(240,236,230,0.1);aspect-ratio:2/3;transition:all 0.22s}
.img-card:hover{border-color:rgba(201,169,110,0.45);transform:translateY(-3px)}
.img-card img{width:100%;height:100%;object-fit:cover;display:block}
.card-ov{position:absolute;bottom:0;left:0;right:0;padding:10px;background:linear-gradient(transparent,rgba(14,12,10,0.88));display:flex;gap:6px;opacity:0;transition:opacity 0.2s}
.img-card:hover .card-ov{opacity:1}
.cBtn{flex:1;padding:7px 5px;border-radius:6px;border:0.5px solid rgba(240,236,230,0.25);background:rgba(14,12,10,0.7);color:#f0ece6;font-size:11px;cursor:pointer;font-family:'DM Sans',sans-serif;transition:background 0.2s;text-align:center}
.cBtn:hover{background:rgba(201,169,110,0.3)}
.skel{border-radius:12px;aspect-ratio:2/3;background:rgba(240,236,230,0.06);position:relative;overflow:hidden}
.skel::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(240,236,230,0.05),transparent);animation:shim 1.6s infinite;transform:translateX(-100%)}
@keyframes shim{to{transform:translateX(100%)}}
.skel p{position:absolute;bottom:14px;left:0;right:0;text-align:center;font-size:10px;color:rgba(240,236,230,0.22);font-weight:300}
.info-box{background:rgba(201,169,110,0.05);border:0.5px solid rgba(201,169,110,0.2);border-radius:9px;padding:13px 16px;font-size:11px;color:rgba(240,236,230,0.5);line-height:1.75}
.info-box strong{color:#c9a96e;font-weight:500}
</style>
</head>
<body>
<div class="hdr">
  <div class="logo">AI MODEL <span>STUDIO</span></div>
  <div style="font-size:11px;color:rgba(240,236,230,0.3)">FASHN Virtual Try-On v1.6</div>
  <div style="font-size:10px;padding:3px 10px;border-radius:4px;background:rgba(29,158,117,0.15);border:0.5px solid rgba(29,158,117,0.3);color:rgba(159,225,203,0.9)">● online</div>
</div>
<div class="layout">
  <div class="lpanel">
    <div class="section">
      <div class="sec-title">Klucz API fal.ai</div>
      <div class="api-row">
        <input type="password" id="apiKey" placeholder="fal_xxxxxxxxxxxxxxxxxxxxxxxx">
        <button class="iBtn" onclick="var i=document.getElementById('apiKey');i.type=i.type==='password'?'text':'password'">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
        </button>
      </div>
      <div class="hint">Klucz: <a href="https://fal.ai/dashboard/keys" target="_blank">fal.ai/dashboard/keys</a> · ~$0.075/zdjęcie</div>
    </div>
    <div class="section">
      <div class="sec-title">Zdjęcia wejściowe</div>
      <div class="upload-cols">
        <div>
          <div class="upzone" id="pZone" ondragover="dg(event,'pZone',1)" ondragleave="dg(event,'pZone',0)" ondrop="dp(event,'p')">
            <input type="file" id="pFile" accept="image/*" onchange="li(this.files[0],'p')">
            <div class="badge bp">Produkt</div>
            <svg width="26" height="26" viewBox="0 0 32 32" fill="none" opacity="0.5"><rect x="4" y="6" width="24" height="22" rx="3" stroke="#c9a96e" stroke-width="1.2"/><rect x="9" y="12" width="14" height="10" rx="2" stroke="#c9a96e" stroke-width="1"/></svg>
            <h4>Ubranie</h4><p>Wieszak / podłoga<br>flat lay / manekin</p>
          </div>
          <div class="prevBox" id="pPrev"><img id="pImg" src="" alt=""><div class="prevLbl">Produkt</div><button class="delBtn" onclick="ci('p')">✕</button></div>
        </div>
        <div>
          <div class="upzone" id="mZone" ondragover="dg(event,'mZone',1)" ondragleave="dg(event,'mZone',0)" ondrop="dp(event,'m')">
            <input type="file" id="mFile" accept="image/*" onchange="li(this.files[0],'m')">
            <div class="badge bm">Modelka</div>
            <svg width="26" height="26" viewBox="0 0 32 32" fill="none" opacity="0.5"><circle cx="16" cy="10" r="5" stroke="#378add" stroke-width="1.2"/><path d="M6 28c0-5.52 4.48-10 10-10s10 4.48 10 10" stroke="#378add" stroke-width="1.2" stroke-linecap="round"/></svg>
            <h4>Modelka</h4><p>Pełna sylwetka<br>neutralne tło</p>
          </div>
          <div class="prevBox" id="mPrev"><img id="mImg" src="" alt=""><div class="prevLbl">Modelka</div><button class="delBtn" onclick="ci('m')">✕</button></div>
        </div>
      </div>
      <div style="margin-top:13px">
        <div class="field-lbl">Lub wybierz gotową modelkę</div>
        <div class="preset-grid">
          <div class="preset" onclick="sp(this,'https://storage.googleapis.com/falserverless/model_tests/leffa/person_image.jpg')"><span>Modelka 1</span></div>
          <div class="preset" onclick="sp(this,'https://images.unsplash.com/photo-1529139574466-a303027f1d1f?w=400&q=80')"><span>Modelka 2</span></div>
          <div class="preset" onclick="sp(this,'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&q=80')"><span>Modelka 3</span></div>
          <div class="preset" onclick="sp(this,'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400&q=80')"><span>Modelka 4</span></div>
        </div>
        <div class="hint">Najlepszy wynik: własne zdjęcie modelki stojącej prosto, neutralne tło.</div>
      </div>
    </div>
    <div class="section">
      <div class="sec-title">Typ ubrania</div>
      <div class="chip-row">
        <div class="chip on" data-g="cat" data-v="upper_body" onclick="sc(this)">Góra — bluzka / top / kurtka</div>
        <div class="chip" data-g="cat" data-v="lower_body" onclick="sc(this)">Dół — spodnie / spódnica</div>
        <div class="chip" data-g="cat" data-v="one-piece" onclick="sc(this)">Sukienka / kombinezon</div>
      </div>
    </div>
    <div class="section">
      <div class="sec-title">Tryb generowania</div>
      <div class="chip-row">
        <div class="chip on" data-g="mode" data-v="balanced" onclick="sc(this)">Balans (rekomendowany)</div>
        <div class="chip" data-g="mode" data-v="fast" onclick="sc(this)">Szybki (~10 sek.)</div>
        <div class="chip" data-g="mode" data-v="quality" onclick="sc(this)">Wysoka jakość (~30 sek.)</div>
      </div>
    </div>
    <div class="section">
      <div class="sec-title">Liczba zdjęć</div>
      <div style="display:flex;align-items:center;gap:12px">
        <input type="range" min="1" max="4" value="1" step="1" id="nShots" style="flex:1;-webkit-appearance:none;height:2px;background:rgba(240,236,230,0.15);border-radius:2px;outline:none;padding:0;accent-color:#c9a96e" oninput="document.getElementById('nVal').textContent=this.value">
        <span style="font-size:13px;color:#c9a96e;min-width:20px;text-align:right" id="nVal">1</span>
      </div>
      <div class="hint">Każde zdjęcie = osobne wywołanie · $0.075 × liczba</div>
    </div>
    <button class="gen-btn" id="genBtn" onclick="generate()">✦ Generuj zdjęcia produktowe</button>
  </div>
  <div class="rpanel">
    <div style="display:flex;align-items:center;justify-content:space-between">
      <div style="font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:#c9a96e;font-weight:500">Wyniki</div>
      <div style="font-size:11px;color:rgba(240,236,230,0.3)" id="rCount"></div>
    </div>
    <div class="info-box"><strong>FASHN Virtual Try-On v1.6</strong> — nakłada Twoje ubranie (wieszak/flat-lay) precyzyjnie na modelkę, zachowując kolory, wzory i tekstury. Wynik: 864×1296px.</div>
    <div class="status" id="statusBar"></div>
    <div class="prog" id="progEl"><div class="dot"></div><div class="prog-bar"><div class="prog-fill" id="pFill"></div></div><div id="pLbl" style="min-width:150px;text-align:right;font-size:11px"></div></div>
    <div id="qInfo" style="font-size:11px;color:rgba(240,236,230,0.32);text-align:center;display:none;padding:4px 0"></div>
    <div class="empty" id="emptyEl">
      <svg width="52" height="52" viewBox="0 0 52 52" fill="none"><rect x="6" y="8" width="20" height="36" rx="4" stroke="currentColor" stroke-width="1.2"/><path d="M10 16h12M10 22h8M10 28h10M10 34h6" stroke="currentColor" stroke-width="1" stroke-linecap="round" opacity="0.5"/><circle cx="37" cy="27" r="10" stroke="currentColor" stroke-width="1.2"/></svg>
      <p>Wgraj ubranie i modelkę, następnie kliknij Generuj</p>
    </div>
    <div id="skelWrap" style="display:none"><div class="results-grid" id="skelGrid"></div></div>
    <div class="results-grid" id="rGrid"></div>
  </div>
</div>
<script>
const S={cat:'upper_body',mode:'balanced'};
let pUri=null,mUri=null,busy=false;
document.querySelectorAll('.chip').forEach(c=>{c.addEventListener('click',()=>{document.querySelectorAll('[data-g="'+c.dataset.g+'"]').forEach(x=>x.classList.remove('on'));c.classList.add('on');S[c.dataset.g]=c.dataset.v})});
function dg(e,id,on){e.preventDefault();document.getElementById(id).classList.toggle('drag',!!on)}
function dp(e,t){e.preventDefault();dg(e,t==='p'?'pZone':'mZone',0);const f=e.dataTransfer.files[0];if(f&&f.type.startsWith('image/'))li(f,t)}
function li(file,t){if(!file)return;const r=new FileReader();r.onload=e=>{const u=e.target.result;if(t==='p'){pUri=u;document.getElementById('pImg').src=u;document.getElementById('pPrev').classList.add('on');document.getElementById('pZone').style.display='none'}else{mUri=u;document.getElementById('mImg').src=u;document.getElementById('mPrev').classList.add('on');document.getElementById('mZone').style.display='none';document.querySelectorAll('.preset').forEach(p=>p.classList.remove('on'))}};r.readAsDataURL(file)}
function ci(t){if(t==='p'){pUri=null;document.getElementById('pImg').src='';document.getElementById('pPrev').classList.remove('on');document.getElementById('pZone').style.display='';document.getElementById('pFile').value=''}else{mUri=null;document.getElementById('mImg').src='';document.getElementById('mPrev').classList.remove('on');document.getElementById('mZone').style.display='';document.getElementById('mFile').value='';document.querySelectorAll('.preset').forEach(p=>p.classList.remove('on'))}}
function sp(el,url){document.querySelectorAll('.preset').forEach(p=>p.classList.remove('on'));el.classList.add('on');mUri=url;document.getElementById('mImg').src=url;document.getElementById('mPrev').classList.add('on');document.getElementById('mZone').style.display='none'}
function ss(msg,type){const el=document.getElementById('statusBar');el.innerHTML=msg;el.className='status on '+(type||'info')}
function sp2(pct,lbl){const w=document.getElementById('progEl'),f=document.getElementById('pFill'),l=document.getElementById('pLbl');if(pct<0){w.classList.remove('on');return}w.classList.add('on');f.style.width=pct+'%';l.textContent=lbl||''}
async function apiFal(path,method,key,body){const res=await fetch('/proxy/'+path,{method:method||'GET',headers:{'Authorization':'Key '+key,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});if(!res.ok){const t=await res.text();let m='Błąd '+res.status;try{const j=JSON.parse(t);m+=': '+(j.detail||j.message||t.substring(0,200))}catch{m+=': '+t.substring(0,200)}throw new Error(m)}return res.json()}
async function poll(key,id){const start=Date.now();for(let i=0;i<80;i++){await new Promise(r=>setTimeout(r,2500));const e=Math.round((Date.now()-start)/1000);const d=await apiFal('fal-ai/fashn/tryon/v1.6/requests/'+id+'/status','GET',key);document.getElementById('qInfo').textContent='Status: '+d.status+' · '+e+'s';if(d.status==='COMPLETED')return apiFal('fal-ai/fashn/tryon/v1.6/requests/'+id,'GET',key);if(d.status==='FAILED')throw new Error('Generowanie nieudane')}throw new Error('Timeout')}
async function generate(){if(busy)return;const key=document.getElementById('apiKey').value.trim();if(!key){ss('Wpisz klucz API fal.ai','err');return}if(!pUri){ss('Wgraj zdjęcie ubrania','err');return}if(!mUri){ss('Wgraj zdjęcie modelki lub wybierz preset','err');return}const shots=parseInt(document.getElementById('nShots').value);busy=true;document.getElementById('genBtn').disabled=true;document.getElementById('emptyEl').style.display='none';document.getElementById('rGrid').innerHTML='';document.getElementById('statusBar').className='status';document.getElementById('skelWrap').style.display='block';const sg=document.getElementById('skelGrid');sg.innerHTML='';for(let i=0;i<shots;i++){const s=document.createElement('div');s.className='skel';s.innerHTML='<p>Generowanie '+(i+1)+'/'+shots+'...</p>';sg.appendChild(s)}sp2(10,'Wysyłanie...');ss('Wysyłanie do fal.ai...','info');document.getElementById('qInfo').style.display='block';const results=[];try{for(let i=0;i<shots;i++){sp2(15+i*20,'Zdjęcie '+(i+1)+'/'+shots+'...');const sub=await apiFal('fal-ai/fashn/tryon/v1.6','POST',key,{model_image:mUri,garment_image:pUri,category:S.cat,mode:S.mode,garment_photo_type:'auto',adjust_hands:true,restore_background:false,restore_clothes:false});results.push(await poll(key,sub.request_id))}document.getElementById('skelWrap').style.display='none';document.getElementById('qInfo').style.display='none';const grid=document.getElementById('rGrid');grid.innerHTML='';let tot=0;results.forEach(res=>{const imgs=res.images||(res.image?[res.image]:[]);imgs.forEach(img=>{const url=typeof img==='string'?img:(img.url||'');if(!url)return;const c=document.createElement('div');c.className='img-card';c.innerHTML='<img src="'+url+'" loading="lazy"><div class="card-ov"><button class="cBtn" onclick="dl(\''+url+'\','+(tot+1)+')">↓ Pobierz</button><button class="cBtn" onclick="window.open(\''+url+'\',\'_blank\')">Pełny</button></div>';grid.appendChild(c);tot++})});document.getElementById('rCount').textContent=tot+' zdjęć';sp2(-1);ss('Gotowe! Wygenerowano '+tot+' zdjęć.','ok')}catch(err){document.getElementById('skelWrap').style.display='none';document.getElementById('qInfo').style.display='none';sp2(-1);ss('<strong>Błąd:</strong> '+(err.message||'Nieznany błąd'),'err');document.getElementById('emptyEl').style.display='flex'}finally{busy=false;document.getElementById('genBtn').disabled=false}}
function dl(url,n){const a=document.createElement('a');a.href=url;a.download='modelka_'+n+'.jpg';a.target='_blank';document.body.appendChild(a);a.click();document.body.removeChild(a)}
</script>
</body>
</html>"""


@app.route('/')
def index():
    return HTML, 200, {'Content-Type': 'text/html; charset=utf-8'}


@app.route('/proxy/<path:fal_path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy(fal_path):
    if request.method == 'OPTIONS':
        return '', 204, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        }

    target = f'https://queue.fal.run/{fal_path}'
    auth = request.headers.get('Authorization', '')
    body = request.get_data() if request.method == 'POST' else None

    req = urllib.request.Request(
        target,
        data=body,
        method=request.method,
        headers={
            'Authorization': auth,
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Model-Studio/1.0',
        }
    )

    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
            data = r.read()
            return Response(data, status=r.status,
                            content_type='application/json',
                            headers={'Access-Control-Allow-Origin': '*'})
    except urllib.error.HTTPError as e:
        data = e.read()
        return Response(data, status=e.code,
                        content_type='application/json',
                        headers={'Access-Control-Allow-Origin': '*'})
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=502,
                        content_type='application/json',
                        headers={'Access-Control-Allow-Origin': '*'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3333))
    app.run(host='0.0.0.0', port=port)
