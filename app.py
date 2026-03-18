import os, ssl, json, urllib.request, urllib.error
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

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
.hdr{display:flex;align-items:center;justify-content:space-between;padding:14px 26px;border-bottom:0.5px solid rgba(240,236,230,0.1);background:#0e0c0a;position:sticky;top:0;z-index:100}
.logo{font-family:'Playfair Display',serif;font-size:18px;letter-spacing:0.04em}.logo span{color:#c9a96e}
.online{font-size:10px;padding:3px 10px;border-radius:4px;background:rgba(29,158,117,0.15);border:0.5px solid rgba(29,158,117,0.3);color:rgba(159,225,203,0.9)}
.layout{display:grid;grid-template-columns:460px 1fr;min-height:calc(100vh - 52px)}
@media(max-width:900px){.layout{grid-template-columns:1fr}}
.lpanel{border-right:0.5px solid rgba(240,236,230,0.1);padding:20px;display:flex;flex-direction:column;overflow-y:auto;max-height:calc(100vh - 52px)}
.rpanel{padding:20px 24px;display:flex;flex-direction:column;gap:14px;overflow-y:auto;max-height:calc(100vh - 52px)}
.sec{padding:12px 0;border-bottom:0.5px solid rgba(240,236,230,0.07)}
.sec:last-of-type{border-bottom:none;padding-bottom:0}
.stitle{font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:#c9a96e;font-weight:500;margin-bottom:9px}
.flbl{font-size:10px;color:rgba(240,236,230,0.38);letter-spacing:0.06em;text-transform:uppercase;margin-bottom:5px}
input,select,textarea{background:rgba(240,236,230,0.06);border:0.5px solid rgba(240,236,230,0.18);border-radius:8px;padding:9px 12px;color:#f0ece6;font-size:12px;font-family:'DM Sans',sans-serif;outline:none;width:100%;transition:border-color 0.2s}
input:focus,select:focus,textarea:focus{border-color:rgba(201,169,110,0.65)}
input::placeholder,textarea::placeholder{color:rgba(240,236,230,0.28)}
select{cursor:pointer}select option{background:#1a1714}
textarea{resize:vertical;min-height:70px;line-height:1.55}
.row{display:flex;gap:8px;align-items:center}.row input{flex:1}
.ib{width:36px;height:36px;flex-shrink:0;border-radius:8px;border:0.5px solid rgba(240,236,230,0.18);background:rgba(240,236,230,0.04);color:rgba(240,236,230,0.5);cursor:pointer;display:flex;align-items:center;justify-content:center}
.ib:hover{background:rgba(240,236,230,0.1)}
.hint{font-size:10px;color:rgba(240,236,230,0.28);margin-top:5px;line-height:1.6;font-weight:300}
.pgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;margin-top:7px}
.pc{border:0.5px solid rgba(240,236,230,0.1);border-radius:8px;padding:7px 9px;cursor:pointer;transition:all 0.18s;background:rgba(240,236,230,0.02)}
.pc:hover{border-color:rgba(201,169,110,0.4)}.pc.on{border-color:#c9a96e;background:rgba(201,169,110,0.08)}
.pc-name{font-size:11px;font-weight:500;color:#f0ece6;margin-bottom:1px}
.pc-id{font-size:8px;color:rgba(240,236,230,0.3);font-family:monospace;margin-bottom:3px;word-break:break-all}
.pc-price{font-size:9px;color:#c9a96e}
.pc-tag{font-size:8px;padding:1px 5px;border-radius:3px;display:inline-block;margin-top:2px}
.tt{background:rgba(29,158,117,0.15);color:rgba(159,225,203,0.9)}
.te{background:rgba(56,138,221,0.15);color:rgba(183,212,244,0.9)}
.tg{background:rgba(201,169,110,0.15);color:#c9a96e}
.ucols{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.uz{border:1px dashed rgba(201,169,110,0.3);border-radius:10px;padding:13px 10px;text-align:center;cursor:pointer;transition:all 0.2s;background:rgba(201,169,110,0.02);position:relative;min-height:115px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.uz:hover{border-color:rgba(201,169,110,0.7);background:rgba(201,169,110,0.07)}
.uz input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.uz h4{font-size:11px;font-weight:500;margin:5px 0 2px}.uz p{font-size:10px;color:rgba(240,236,230,0.35);font-weight:300;line-height:1.4}
.badge{font-size:9px;letter-spacing:0.07em;text-transform:uppercase;padding:2px 6px;border-radius:3px;margin-bottom:4px}
.bp{background:rgba(201,169,110,0.15);color:#c9a96e;border:0.5px solid rgba(201,169,110,0.3)}
.bm{background:rgba(56,138,221,0.12);color:rgba(183,212,244,0.9);border:0.5px solid rgba(56,138,221,0.25)}
.pv{display:none;position:relative;border-radius:8px;overflow:hidden;background:rgba(240,236,230,0.04);border:0.5px solid rgba(240,236,230,0.1)}
.pv.on{display:block}.pv img{width:100%;max-height:140px;object-fit:contain;display:block}
.db{position:absolute;top:5px;right:5px;width:20px;height:20px;border-radius:4px;background:rgba(14,12,10,0.85);border:0.5px solid rgba(240,236,230,0.2);color:#f0ece6;cursor:pointer;font-size:10px;display:flex;align-items:center;justify-content:center}
.pl{position:absolute;bottom:0;left:0;right:0;padding:4px 8px;background:rgba(14,12,10,0.75);font-size:10px;color:rgba(240,236,230,0.6)}
.chips{display:flex;flex-wrap:wrap;gap:5px}
.chip{font-size:11px;padding:4px 10px;border-radius:100px;border:0.5px solid rgba(240,236,230,0.16);background:transparent;color:rgba(240,236,230,0.55);cursor:pointer;transition:all 0.18s;font-family:'DM Sans',sans-serif;white-space:nowrap}
.chip:hover{border-color:rgba(201,169,110,0.45);color:#f0ece6}.chip.on{background:rgba(201,169,110,0.13);border-color:#c9a96e;color:#c9a96e}
.pmods{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:7px}
.pm{border-radius:7px;cursor:pointer;border:1.5px solid transparent;transition:all 0.2s;aspect-ratio:3/4;background:rgba(240,236,230,0.05);display:flex;align-items:center;justify-content:center;font-size:10px;color:rgba(240,236,230,0.35);text-align:center;position:relative;padding:4px}
.pm.on{border-color:#c9a96e}.pm:hover{border-color:rgba(201,169,110,0.45)}
.pm span{position:relative;z-index:1;font-size:9px;background:rgba(14,12,10,0.75);padding:2px 4px;border-radius:3px}
.mpill{display:inline-flex;font-size:10px;padding:3px 9px;border-radius:4px;background:rgba(201,169,110,0.1);border:0.5px solid rgba(201,169,110,0.25);color:#c9a96e;margin-top:6px;word-break:break-all}
.gb{width:100%;padding:14px;background:#c9a96e;border:none;border-radius:10px;color:#0e0c0a;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;letter-spacing:0.08em;text-transform:uppercase;cursor:pointer;transition:all 0.22s;margin-top:14px}
.gb:hover:not(:disabled){background:#dbbf87;transform:translateY(-1px)}.gb:disabled{background:rgba(201,169,110,0.18);color:rgba(14,12,10,0.4);cursor:not-allowed}
.sb{padding:10px 14px;border-radius:8px;font-size:12px;line-height:1.6;display:none}
.sb.on{display:block}.sb.info{background:rgba(56,138,221,0.09);border:0.5px solid rgba(56,138,221,0.25);color:rgba(183,212,244,0.9)}
.sb.err{background:rgba(226,75,74,0.09);border:0.5px solid rgba(226,75,74,0.25);color:rgba(240,193,193,0.9)}
.sb.ok{background:rgba(29,158,117,0.09);border:0.5px solid rgba(29,158,117,0.25);color:rgba(159,225,203,0.9)}
.prog{display:none;align-items:center;gap:12px;font-size:11px;color:rgba(240,236,230,0.4)}.prog.on{display:flex}
.pb{flex:1;height:2px;background:rgba(240,236,230,0.1);border-radius:2px;overflow:hidden}
.pf{height:100%;background:#c9a96e;border-radius:2px;transition:width 0.5s;width:0%}
.dot{width:7px;height:7px;border-radius:50%;background:#c9a96e;flex-shrink:0;animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.2}}
.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;opacity:0.25;min-height:300px;text-align:center}
.empty p{font-size:13px;line-height:1.8;max-width:220px;font-weight:300}
.rg{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}
.ic{position:relative;border-radius:12px;overflow:hidden;background:rgba(240,236,230,0.04);border:0.5px solid rgba(240,236,230,0.1);aspect-ratio:3/4;transition:all 0.22s}
.ic:hover{border-color:rgba(201,169,110,0.4);transform:translateY(-2px)}.ic img{width:100%;height:100%;object-fit:cover;display:block}
.io{position:absolute;bottom:0;left:0;right:0;padding:9px;background:linear-gradient(transparent,rgba(14,12,10,0.88));display:flex;gap:5px;opacity:0;transition:opacity 0.2s}
.ic:hover .io{opacity:1}
.ib2{flex:1;padding:6px 4px;border-radius:6px;border:0.5px solid rgba(240,236,230,0.22);background:rgba(14,12,10,0.7);color:#f0ece6;font-size:11px;cursor:pointer;font-family:'DM Sans',sans-serif;text-align:center}
.ib2:hover{background:rgba(201,169,110,0.28)}
.sk{border-radius:12px;aspect-ratio:3/4;background:rgba(240,236,230,0.05);position:relative;overflow:hidden}
.sk::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(240,236,230,0.04),transparent);animation:shim 1.6s infinite;transform:translateX(-100%)}
@keyframes shim{to{transform:translateX(100%)}}
.sk p{position:absolute;bottom:12px;left:0;right:0;text-align:center;font-size:10px;color:rgba(240,236,230,0.2)}
</style>
</head>
<body>
<div class="hdr">
  <div class="logo">AI MODEL <span>STUDIO</span></div>
  <div style="font-size:11px;color:rgba(240,236,230,0.3)">fal.ai</div>
  <div class="online">online</div>
</div>
<div class="layout">
<div class="lpanel">
  <div class="sec">
    <div class="stitle">Klucz API fal.ai</div>
    <div class="row">
      <input type="password" id="apiKey" placeholder="fal_xxxxxxxxxxxxxxxxxxxxxxxx">
      <button class="ib" id="toggleKey">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
      </button>
    </div>
    <div class="hint"><a href="https://fal.ai/dashboard/keys" target="_blank">fal.ai/dashboard/keys</a> | <a href="https://fal.ai/dashboard/billing" target="_blank">doladowanie</a></div>
  </div>
  <div class="sec">
    <div class="stitle">Model AI</div>
    <div class="pgrid" id="pgrid">
      <div class="pc on" data-ep="fal-ai/fashn/tryon/v1.6" data-t="tryon"><div class="pc-name">FASHN Try-On</div><div class="pc-id">fal-ai/fashn/tryon/v1.6</div><div class="pc-price">$0.075</div><div class="pc-tag tt">try-on</div></div>
      <div class="pc" data-ep="fal-ai/nano-banana-2/edit" data-t="edit"><div class="pc-name">Nano Banana 2</div><div class="pc-id">fal-ai/nano-banana-2/edit</div><div class="pc-price">$0.039</div><div class="pc-tag te">Gemini 3.1</div></div>
      <div class="pc" data-ep="fal-ai/gemini-3-pro-image-preview" data-t="edit"><div class="pc-name">Nano Banana Pro</div><div class="pc-id">fal-ai/gemini-3-pro-image-preview</div><div class="pc-price">$0.15</div><div class="pc-tag te">Gemini 3 Pro</div></div>
      <div class="pc" data-ep="fal-ai/flux-2/edit" data-t="edit"><div class="pc-name">FLUX.2 Edit</div><div class="pc-id">fal-ai/flux-2/edit</div><div class="pc-price">$0.05</div><div class="pc-tag te">img edit</div></div>
      <div class="pc" data-ep="fal-ai/flux/dev/image-to-image" data-t="edit"><div class="pc-name">FLUX img2img</div><div class="pc-id">fal-ai/flux/dev/image-to-image</div><div class="pc-price">$0.025</div><div class="pc-tag te">img2img</div></div>
      <div class="pc" data-ep="fal-ai/flux/dev" data-t="gen"><div class="pc-name">FLUX Dev</div><div class="pc-id">fal-ai/flux/dev</div><div class="pc-price">$0.025</div><div class="pc-tag tg">text2img</div></div>
      <div class="pc" data-ep="fal-ai/flux/schnell" data-t="gen"><div class="pc-name">FLUX Schnell</div><div class="pc-id">fal-ai/flux/schnell</div><div class="pc-price">$0.003</div><div class="pc-tag tg">szybki</div></div>
      <div class="pc" data-ep="fal-ai/recraft-v3" data-t="gen"><div class="pc-name">Recraft V3</div><div class="pc-id">fal-ai/recraft-v3</div><div class="pc-price">$0.04</div><div class="pc-tag tg">foto</div></div>
      <div class="pc" data-ep="fal-ai/ideogram/v3" data-t="gen"><div class="pc-name">Ideogram V3</div><div class="pc-id">fal-ai/ideogram/v3</div><div class="pc-price">$0.08</div><div class="pc-tag tg">tekst</div></div>
    </div>
    <div style="margin-top:10px">
      <div class="flbl">Lub wpisz wlasny endpoint</div>
      <div class="row">
        <input type="text" id="customEp" placeholder="np. fal-ai/flux-pro/v1.1-ultra" style="font-family:monospace;font-size:11px">
        <a href="https://fal.ai/explore/models" target="_blank"><button class="ib"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg></button></a>
      </div>
    </div>
    <div class="mpill" id="mpill">fal-ai/fashn/tryon/v1.6</div>
  </div>
  <div class="sec" id="uploadSec">
    <div class="stitle">Zdjecia wejsciowe</div>
    <div class="ucols">
      <div>
        <div class="uz" id="pZone"><input type="file" id="pFile" accept="image/jpeg,image/png,image/webp"><div class="badge bp">Produkt</div><svg width="20" height="20" viewBox="0 0 32 32" fill="none" opacity="0.5"><rect x="4" y="6" width="24" height="22" rx="3" stroke="#c9a96e" stroke-width="1.2"/><rect x="9" y="12" width="14" height="10" rx="2" stroke="#c9a96e" stroke-width="1"/></svg><h4>Ubranie</h4><p>Wieszak / flat-lay</p></div>
        <div class="pv" id="pPrev"><img id="pImg" src="" alt=""><div class="pl">Produkt</div><button class="db" id="delP">x</button></div>
      </div>
      <div id="modelCol">
        <div class="uz" id="mZone"><input type="file" id="mFile" accept="image/jpeg,image/png,image/webp"><div class="badge bm">Modelka</div><svg width="20" height="20" viewBox="0 0 32 32" fill="none" opacity="0.5"><circle cx="16" cy="10" r="5" stroke="#378add" stroke-width="1.2"/><path d="M6 28c0-5.52 4.48-10 10-10s10 4.48 10 10" stroke="#378add" stroke-width="1.2" stroke-linecap="round"/></svg><h4>Modelka</h4><p>Pelna sylwetka</p></div>
        <div class="pv" id="mPrev"><img id="mImg" src="" alt=""><div class="pl">Modelka</div><button class="db" id="delM">x</button></div>
      </div>
    </div>
    <div id="presetWrap" style="margin-top:8px">
      <div class="flbl">Gotowe modelki</div>
      <div class="pmods">
        <div class="pm" data-url="https://storage.googleapis.com/falserverless/model_tests/leffa/person_image.jpg"><span>M1</span></div>
        <div class="pm" data-url="https://images.unsplash.com/photo-1529139574466-a303027f1d1f?w=400&q=80"><span>M2</span></div>
        <div class="pm" data-url="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&q=80"><span>M3</span></div>
        <div class="pm" data-url="https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400&q=80"><span>M4</span></div>
      </div>
    </div>
  </div>
  <div class="sec" id="tryonOpts">
    <div class="stitle">Opcje try-on</div>
    <div style="margin-bottom:9px"><div class="flbl">Typ ubrania</div>
      <div class="chips">
        <div class="chip on" data-g="cat" data-v="tops">Gora</div>
        <div class="chip" data-g="cat" data-v="bottoms">Dol</div>
        <div class="chip" data-g="cat" data-v="one-pieces">Sukienka</div>
      </div>
    </div>
    <div><div class="flbl">Tryb</div>
      <div class="chips">
        <div class="chip on" data-g="mode" data-v="balanced">Balans</div>
        <div class="chip" data-g="mode" data-v="performance">Szybki</div>
        <div class="chip" data-g="mode" data-v="quality">Jakosc</div>
      </div>
    </div>
  </div>
  <div class="sec" id="promptSec" style="display:none">
    <div class="stitle">Prompt</div>
    <textarea id="promptTxt" placeholder="Opisz co chcesz wygenerowac..."></textarea>
    <div class="hint" id="promptHint"></div>
  </div>
  <div class="sec">
    <div class="stitle">Liczba zdiec</div>
    <div style="display:flex;align-items:center;gap:12px">
      <input type="range" min="1" max="4" value="1" step="1" id="nShots" style="flex:1;-webkit-appearance:none;height:2px;background:rgba(240,236,230,0.15);border-radius:2px;outline:none;padding:0;accent-color:#c9a96e">
      <span style="font-size:13px;color:#c9a96e;min-width:20px;text-align:right" id="nVal">1</span>
    </div>
    <div class="hint" id="costHint">~$0.075 za 1 zdjecie</div>
  </div>
  <button class="gb" id="genBtn">Generuj zdjecia</button>
</div>
<div class="rpanel">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <div style="font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:#c9a96e;font-weight:500">Wyniki</div>
    <div style="font-size:11px;color:rgba(240,236,230,0.3)" id="rCount"></div>
  </div>
  <div class="sb" id="sb"></div>
  <div class="prog" id="prog"><div class="dot"></div><div class="pb"><div class="pf" id="pf"></div></div><div id="pl" style="min-width:150px;text-align:right;font-size:11px"></div></div>
  <div id="qi" style="font-size:11px;color:rgba(240,236,230,0.3);text-align:center;display:none;padding:4px 0"></div>
  <div class="empty" id="emptyEl"><svg width="50" height="50" viewBox="0 0 50 50" fill="none"><rect x="5" y="7" width="20" height="36" rx="4" stroke="currentColor" stroke-width="1.2"/><circle cx="36" cy="26" r="10" stroke="currentColor" stroke-width="1.2"/></svg><p>Wybierz model i kliknij Generuj</p></div>
  <div id="skelWrap" style="display:none"><div class="rg" id="skelGrid"></div></div>
  <div class="rg" id="rGrid"></div>
</div>
</div>
<script>
(function(){
'use strict';
var S={cat:'tops',mode:'balanced'};
var pUri=null,mUri=null,busy=false;
var ep='fal-ai/fashn/tryon/v1.6',et='tryon';
var MI={
  'fal-ai/fashn/tryon/v1.6':{p:0.075,t:'tryon',ph:'',h:'Wgraj ubranie i modelke.'},
  'fal-ai/nano-banana-2/edit':{p:0.039,t:'edit',ph:'Put this clothing on a professional fashion model, white studio background, full body, photorealistic',h:'Gemini 3.1 - edytuje zdjecie wg opisu.'},
  'fal-ai/gemini-3-pro-image-preview':{p:0.15,t:'edit',ph:'Luxury fashion editorial photo, elegant model, dramatic lighting, Vogue style',h:'Gemini 3 Pro - najwyzsza jakosc.'},
  'fal-ai/flux-2/edit':{p:0.05,t:'edit',ph:'Professional fashion model wearing this clothing, white studio background, full body',h:'FLUX.2 Edit.'},
  'fal-ai/flux/dev/image-to-image':{p:0.025,t:'edit',ph:'Fashion model wearing this clothing, white studio, professional photography',h:'FLUX Dev img2img.'},
  'fal-ai/flux/dev':{p:0.025,t:'gen',ph:'Professional fashion model, white studio background, full body, 8K commercial photography',h:'FLUX Dev - z opisu tekstowego.'},
  'fal-ai/flux/schnell':{p:0.003,t:'gen',ph:'Fashion model, elegant outfit, white background, professional photo',h:'FLUX Schnell - szybki ~3 sek.'},
  'fal-ai/recraft-v3':{p:0.04,t:'gen',ph:'Fashion model in stylish clothing, clean studio background, editorial photography',h:'Recraft V3.'},
  'fal-ai/ideogram/v3':{p:0.08,t:'gen',ph:'Fashion model wearing stylish clothes, studio background',h:'Ideogram V3.'}
};
function ui(){
  document.getElementById('mpill').textContent=ep;
  var info=MI[ep],price=info?info.p:0.05,type=info?info.t:et;
  var shots=parseInt(document.getElementById('nShots').value);
  document.getElementById('costHint').textContent='~$'+(price*shots).toFixed(3)+' za '+shots+' zdjecie';
  document.getElementById('modelCol').style.display=type==='tryon'?'block':'none';
  document.getElementById('presetWrap').style.display=type==='tryon'?'block':'none';
  document.getElementById('tryonOpts').style.display=type==='tryon'?'block':'none';
  document.getElementById('promptSec').style.display=type!=='tryon'?'block':'none';
  if(info&&info.ph)document.getElementById('promptTxt').placeholder=info.ph;
  if(info&&info.h)document.getElementById('promptHint').textContent=info.h;
}
document.querySelectorAll('.pc').forEach(function(c){c.addEventListener('click',function(){document.querySelectorAll('.pc').forEach(function(x){x.classList.remove('on');});c.classList.add('on');ep=c.dataset.ep;et=c.dataset.t;document.getElementById('customEp').value='';ui();});});
document.getElementById('customEp').addEventListener('input',function(){var v=this.value.trim();if(!v)return;document.querySelectorAll('.pc').forEach(function(x){x.classList.remove('on');});ep=v;et=v.indexOf('tryon')!==-1?'tryon':v.indexOf('edit')!==-1||v.indexOf('nano-banana')!==-1||v.indexOf('gemini')!==-1||v.indexOf('image-to-image')!==-1?'edit':'gen';ui();});
document.getElementById('toggleKey').addEventListener('click',function(){var i=document.getElementById('apiKey');i.type=i.type==='password'?'text':'password';});
document.getElementById('nShots').addEventListener('input',function(){document.getElementById('nVal').textContent=this.value;ui();});
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){document.querySelectorAll('[data-g="'+c.dataset.g+'"]').forEach(function(x){x.classList.remove('on');});c.classList.add('on');S[c.dataset.g]=c.dataset.v;});});
document.getElementById('pFile').addEventListener('change',function(){if(this.files&&this.files[0])lf(this.files[0],'p');});
document.getElementById('mFile').addEventListener('change',function(){if(this.files&&this.files[0])lf(this.files[0],'m');});
function lf(file,t){var r=new FileReader();r.onload=function(e){if(t==='p'){pUri=e.target.result;document.getElementById('pImg').src=pUri;document.getElementById('pPrev').classList.add('on');document.getElementById('pZone').style.display='none';}else{mUri=e.target.result;document.getElementById('mImg').src=mUri;document.getElementById('mPrev').classList.add('on');document.getElementById('mZone').style.display='none';document.querySelectorAll('.pm').forEach(function(p){p.classList.remove('on');});}};r.readAsDataURL(file);}
document.getElementById('delP').addEventListener('click',function(){pUri=null;document.getElementById('pImg').src='';document.getElementById('pPrev').classList.remove('on');document.getElementById('pZone').style.display='';document.getElementById('pFile').value='';});
document.getElementById('delM').addEventListener('click',function(){mUri=null;document.getElementById('mImg').src='';document.getElementById('mPrev').classList.remove('on');document.getElementById('mZone').style.display='';document.getElementById('mFile').value='';document.querySelectorAll('.pm').forEach(function(p){p.classList.remove('on');});});
document.querySelectorAll('.pm').forEach(function(el){el.addEventListener('click',function(){document.querySelectorAll('.pm').forEach(function(p){p.classList.remove('on');});el.classList.add('on');mUri=el.dataset.url;document.getElementById('mImg').src=mUri;document.getElementById('mPrev').classList.add('on');document.getElementById('mZone').style.display='none';});});
document.getElementById('rGrid').addEventListener('click',function(e){var btn=e.target.closest('.ib2');if(!btn)return;var card=btn.closest('.ic');if(!card)return;var url=card.dataset.url;if(!url)return;if(btn.dataset.a==='dl'){var a=document.createElement('a');a.href=url;a.download='zdjecie.jpg';a.target='_blank';document.body.appendChild(a);a.click();document.body.removeChild(a);}else{window.open(url,'_blank');}});
function ss(msg,type){var el=document.getElementById('sb');el.textContent=msg;el.className='sb on '+(type||'info');}
function sp(pct,lbl){var w=document.getElementById('prog'),f=document.getElementById('pf'),l=document.getElementById('pl');if(pct<0){w.classList.remove('on');return;}w.classList.add('on');f.style.width=pct+'%';l.textContent=lbl||'';}
function api(data){return fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(function(res){return res.json().then(function(j){if(!res.ok)throw new Error(j.error||j.detail||j.message||'Blad '+res.status);return j;});});}
function poll(key,reqId,endpoint){var start=Date.now(),attempts=0;function attempt(){return new Promise(function(r){setTimeout(r,2500);}).then(function(){attempts++;var e=Math.round((Date.now()-start)/1000);return api({action:'status',auth:'Key '+key,endpoint:endpoint,request_id:reqId}).then(function(d){document.getElementById('qi').textContent='Status: '+d.status+' - '+e+'s';if(d.status==='COMPLETED')return api({action:'result',auth:'Key '+key,endpoint:endpoint,request_id:reqId});if(d.status==='FAILED')throw new Error('Generowanie nieudane.');if(attempts>=80)throw new Error('Timeout');return attempt();});})}return attempt();}
function payload(){var prompt=document.getElementById('promptTxt').value.trim();var info=MI[ep];if(!prompt&&info&&info.ph)prompt=info.ph;var type=info?info.t:et;if(type==='tryon')return{model_image:mUri,garment_image:pUri,category:S.cat,mode:S.mode,garment_photo_type:'auto'};if(ep.indexOf('image-to-image')!==-1)return{image_url:pUri,prompt:prompt,strength:0.8,num_inference_steps:28};if(ep.indexOf('nano-banana')!==-1||ep.indexOf('gemini')!==-1)return{prompt:prompt,image_urls:pUri?[pUri]:[]};if(ep.indexOf('flux-2/edit')!==-1)return{prompt:prompt,image_url:pUri};return{prompt:prompt,image_size:{width:768,height:1024},num_inference_steps:28,enable_safety_checker:false};}
function imgs(res){if(res.images)return res.images.map(function(i){return typeof i==='string'?i:i.url;}).filter(Boolean);if(res.image)return[typeof res.image==='string'?res.image:res.image.url];return[];}
function addCard(url){var card=document.createElement('div');card.className='ic';card.dataset.url=url;var img=document.createElement('img');img.src=url;img.loading='lazy';var ov=document.createElement('div');ov.className='io';var b1=document.createElement('button');b1.className='ib2';b1.dataset.a='dl';b1.textContent='Pobierz';var b2=document.createElement('button');b2.className='ib2';b2.dataset.a='open';b2.textContent='Pelny';ov.appendChild(b1);ov.appendChild(b2);card.appendChild(img);card.appendChild(ov);document.getElementById('rGrid').appendChild(card);}
document.getElementById('genBtn').addEventListener('click',function(){
  if(busy)return;
  var key=document.getElementById('apiKey').value.trim();
  var info=MI[ep],type=info?info.t:et;
  if(!key){ss('Wpisz klucz API fal.ai','err');return;}
  if(type==='tryon'&&!pUri){ss('Wgraj zdjecie ubrania','err');return;}
  if(type==='tryon'&&!mUri){ss('Wgraj zdjecie modelki lub wybierz preset','err');return;}
  var shots=parseInt(document.getElementById('nShots').value);
  busy=true;document.getElementById('genBtn').disabled=true;
  document.getElementById('emptyEl').style.display='none';document.getElementById('rGrid').innerHTML='';document.getElementById('sb').className='sb';
  document.getElementById('skelWrap').style.display='block';
  var sg=document.getElementById('skelGrid');sg.innerHTML='';
  for(var i=0;i<shots;i++){var sk=document.createElement('div');sk.className='sk';var skp=document.createElement('p');skp.textContent='Generowanie '+(i+1)+'/'+shots+'...';sk.appendChild(skp);sg.appendChild(sk);}
  sp(10,'Wysylanie...');ss('Wysylanie do '+ep+'...','info');document.getElementById('qi').style.display='block';
  var results=[],tot=0;
  function doShot(idx){
    if(idx>=shots){document.getElementById('skelWrap').style.display='none';document.getElementById('qi').style.display='none';results.forEach(function(res){imgs(res).forEach(function(url){addCard(url);tot++;});});document.getElementById('rCount').textContent=tot+' zdiec';sp(-1);ss('Gotowe! '+tot+' zdiec wygenerowanych.','ok');busy=false;document.getElementById('genBtn').disabled=false;return;}
    sp(15+idx*20,'Zdjecie '+(idx+1)+'/'+shots+'...');
    api({action:'submit',auth:'Key '+key,endpoint:ep,payload:payload()}).then(function(sub){if(sub.request_id)return poll(key,sub.request_id,ep);return sub;}).then(function(res){results.push(res);doShot(idx+1);}).catch(function(err){document.getElementById('skelWrap').style.display='none';document.getElementById('qi').style.display='none';sp(-1);ss('Blad: '+(err.message||'Nieznany blad'),'err');document.getElementById('emptyEl').style.display='flex';busy=false;document.getElementById('genBtn').disabled=false;});
  }
  doShot(0);
});
ui();
})();
</script>
</body>
</html>"""


def fal_request(method, path, auth, body=None):
    target = 'https://queue.fal.run/' + path
    headers = {'Authorization': auth, 'User-Agent': 'AI-Model-Studio/2.0'}
    if body:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(target, data=body, method=method, headers=headers)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return 502, json.dumps({'error': str(e)}).encode()


@app.route('/')
def index():
    return HTML, 200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Security-Policy': "default-src * data: blob:; script-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com; style-src * 'unsafe-inline'; img-src * data: blob:;"
    }


@app.route('/api', methods=['POST', 'OPTIONS'])
def api():
    if request.method == 'OPTIONS':
        return '', 204, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    action = data.get('action', '')
    auth = data.get('auth', '')
    endpoint = data.get('endpoint', '')

    if action == 'submit':
        body = json.dumps(data.get('payload', {})).encode()
        status, resp = fal_request('POST', endpoint, auth, body)
    elif action == 'status':
        req_id = data.get('request_id', '')
        status, resp = fal_request('GET', endpoint + '/requests/' + req_id + '/status', auth)
    elif action == 'result':
        req_id = data.get('request_id', '')
        status, resp = fal_request('GET', endpoint + '/requests/' + req_id, auth)
    else:
        return jsonify({'error': 'unknown action: ' + action}), 400

    try:
        result = json.loads(resp)
    except Exception:
        result = {'raw': resp.decode('utf-8', errors='replace')}

    return Response(
        json.dumps(result),
        status=status,
        content_type='application/json',
        headers={'Access-Control-Allow-Origin': '*'}
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3333))
    app.run(host='0.0.0.0', port=port)
