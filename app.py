import os, ssl, json, urllib.request, urllib.error
from flask import Flask, request, Response

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Model Studio · fal.ai</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;background:#0e0c0a;color:#f0ece6;min-height:100vh}
a{color:#c9a96e;text-decoration:none}a:hover{text-decoration:underline}
.hdr{display:flex;align-items:center;justify-content:space-between;padding:14px 26px;border-bottom:0.5px solid rgba(240,236,230,0.1);background:#0e0c0a;position:sticky;top:0;z-index:100}
.logo{font-family:'Playfair Display',serif;font-size:18px;letter-spacing:0.04em}.logo span{color:#c9a96e}
.online{font-size:10px;padding:3px 10px;border-radius:4px;background:rgba(29,158,117,0.15);border:0.5px solid rgba(29,158,117,0.3);color:rgba(159,225,203,0.9)}
.layout{display:grid;grid-template-columns:480px 1fr;min-height:calc(100vh - 52px)}
@media(max-width:900px){.layout{grid-template-columns:1fr}}
.lpanel{border-right:0.5px solid rgba(240,236,230,0.1);padding:20px;display:flex;flex-direction:column;overflow-y:auto;max-height:calc(100vh - 52px)}
.rpanel{padding:20px 24px;display:flex;flex-direction:column;gap:14px;overflow-y:auto;max-height:calc(100vh - 52px)}
.sec{padding:13px 0;border-bottom:0.5px solid rgba(240,236,230,0.07)}
.sec:last-of-type{border-bottom:none;padding-bottom:0}
.stitle{font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:#c9a96e;font-weight:500;margin-bottom:10px}
.flbl{font-size:10px;color:rgba(240,236,230,0.38);letter-spacing:0.06em;text-transform:uppercase;margin-bottom:5px}
input,select,textarea{background:rgba(240,236,230,0.06);border:0.5px solid rgba(240,236,230,0.18);border-radius:8px;padding:9px 12px;color:#f0ece6;font-size:12px;font-family:'DM Sans',sans-serif;outline:none;width:100%;transition:border-color 0.2s}
input:focus,select:focus,textarea:focus{border-color:rgba(201,169,110,0.65)}
input::placeholder,textarea::placeholder{color:rgba(240,236,230,0.28)}
select{cursor:pointer}select option{background:#1a1714}
textarea{resize:vertical;min-height:72px;line-height:1.55}
.row{display:flex;gap:8px;align-items:center}.row input{flex:1}
.iBtn{width:36px;height:36px;flex-shrink:0;border-radius:8px;border:0.5px solid rgba(240,236,230,0.18);background:rgba(240,236,230,0.04);color:rgba(240,236,230,0.5);cursor:pointer;display:flex;align-items:center;justify-content:center}
.iBtn:hover{background:rgba(240,236,230,0.1)}
.hint{font-size:10px;color:rgba(240,236,230,0.28);margin-top:5px;line-height:1.6;font-weight:300}

/* MODEL SELECTOR */
.model-selector{display:flex;flex-direction:column;gap:6px}
.model-select-row{display:flex;gap:8px;align-items:center}
.model-select-row select{flex:1}
.model-custom-row{display:flex;gap:8px;align-items:center;margin-top:6px}
.model-custom-row input{flex:1;font-family:'DM Sans',monospace;font-size:11px}
.model-pill{display:inline-flex;align-items:center;gap:5px;font-size:10px;padding:3px 9px;border-radius:4px;background:rgba(201,169,110,0.1);border:0.5px solid rgba(201,169,110,0.25);color:#c9a96e;margin-top:6px}

/* POPULAR MODELS */
.popular-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:8px}
.pcard{border:0.5px solid rgba(240,236,230,0.1);border-radius:8px;padding:8px 10px;cursor:pointer;transition:all 0.18s;background:rgba(240,236,230,0.02)}
.pcard:hover{border-color:rgba(201,169,110,0.4);background:rgba(201,169,110,0.05)}
.pcard.on{border-color:#c9a96e;background:rgba(201,169,110,0.08)}
.pcard-name{font-size:11px;font-weight:500;color:#f0ece6;margin-bottom:2px}
.pcard-id{font-size:9px;color:rgba(240,236,230,0.35);font-family:monospace;margin-bottom:4px;word-break:break-all}
.pcard-price{font-size:9px;color:#c9a96e}
.pcard-tag{font-size:8px;padding:1px 5px;border-radius:3px;display:inline-block;margin-top:3px}
.t-tryon{background:rgba(29,158,117,0.15);color:rgba(159,225,203,0.9)}
.t-edit{background:rgba(56,138,221,0.15);color:rgba(183,212,244,0.9)}
.t-gen{background:rgba(201,169,110,0.15);color:#c9a96e}

/* UPLOAD */
.upcols{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.upzone{border:1px dashed rgba(201,169,110,0.3);border-radius:10px;padding:14px 10px;text-align:center;cursor:pointer;transition:all 0.2s;background:rgba(201,169,110,0.02);position:relative;min-height:120px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.upzone:hover,.upzone.drag{border-color:rgba(201,169,110,0.7);background:rgba(201,169,110,0.07)}
.upzone input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;padding:0}
.upzone h4{font-size:11px;font-weight:500;margin:5px 0 2px}
.upzone p{font-size:10px;color:rgba(240,236,230,0.35);font-weight:300;line-height:1.4}
.badge{font-size:9px;letter-spacing:0.07em;text-transform:uppercase;padding:2px 6px;border-radius:3px;margin-bottom:5px}
.bp{background:rgba(201,169,110,0.15);color:#c9a96e;border:0.5px solid rgba(201,169,110,0.3)}
.bm{background:rgba(56,138,221,0.12);color:rgba(183,212,244,0.9);border:0.5px solid rgba(56,138,221,0.25)}
.prev{display:none;position:relative;border-radius:8px;overflow:hidden;background:rgba(240,236,230,0.04);border:0.5px solid rgba(240,236,230,0.1)}
.prev.on{display:block}
.prev img{width:100%;max-height:150px;object-fit:contain;display:block}
.dBtn{position:absolute;top:5px;right:5px;width:20px;height:20px;border-radius:4px;background:rgba(14,12,10,0.85);border:0.5px solid rgba(240,236,230,0.2);color:#f0ece6;cursor:pointer;font-size:10px;display:flex;align-items:center;justify-content:center}
.plbl{position:absolute;bottom:0;left:0;right:0;padding:4px 8px;background:rgba(14,12,10,0.75);font-size:10px;color:rgba(240,236,230,0.6)}

/* CHIPS */
.chips{display:flex;flex-wrap:wrap;gap:5px}
.chip{font-size:11px;padding:4px 10px;border-radius:100px;border:0.5px solid rgba(240,236,230,0.16);background:transparent;color:rgba(240,236,230,0.55);cursor:pointer;transition:all 0.18s;font-family:'DM Sans',sans-serif;white-space:nowrap}
.chip:hover{border-color:rgba(201,169,110,0.45);color:#f0ece6}
.chip.on{background:rgba(201,169,110,0.13);border-color:#c9a96e;color:#c9a96e}

/* PRESET MODELS */
.pmodels{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:7px}
.pmod{border-radius:7px;overflow:hidden;cursor:pointer;border:1.5px solid transparent;transition:all 0.2s;aspect-ratio:3/4;background:rgba(240,236,230,0.05);display:flex;align-items:center;justify-content:center;font-size:10px;color:rgba(240,236,230,0.35);text-align:center;position:relative;padding:4px}
.pmod.on{border-color:#c9a96e}.pmod:hover{border-color:rgba(201,169,110,0.45)}
.pmod span{position:relative;z-index:1;font-size:9px;background:rgba(14,12,10,0.75);padding:2px 4px;border-radius:3px}

/* MISC */
.gen-btn{width:100%;padding:14px;background:#c9a96e;border:none;border-radius:10px;color:#0e0c0a;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;letter-spacing:0.08em;text-transform:uppercase;cursor:pointer;transition:all 0.22s;margin-top:14px}
.gen-btn:hover:not(:disabled){background:#dbbf87;transform:translateY(-1px)}
.gen-btn:disabled{background:rgba(201,169,110,0.18);color:rgba(14,12,10,0.4);cursor:not-allowed}
.status{padding:10px 14px;border-radius:8px;font-size:12px;line-height:1.6;display:none}
.status.on{display:block}
.status.info{background:rgba(56,138,221,0.09);border:0.5px solid rgba(56,138,221,0.25);color:rgba(183,212,244,0.9)}
.status.err{background:rgba(226,75,74,0.09);border:0.5px solid rgba(226,75,74,0.25);color:rgba(240,193,193,0.9)}
.status.ok{background:rgba(29,158,117,0.09);border:0.5px solid rgba(29,158,117,0.25);color:rgba(159,225,203,0.9)}
.prog{display:none;align-items:center;gap:12px;font-size:11px;color:rgba(240,236,230,0.4)}
.prog.on{display:flex}
.prog-bar{flex:1;height:2px;background:rgba(240,236,230,0.1);border-radius:2px;overflow:hidden}
.prog-fill{height:100%;background:#c9a96e;border-radius:2px;transition:width 0.5s;width:0%}
.dot{width:7px;height:7px;border-radius:50%;background:#c9a96e;flex-shrink:0;animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.2}}
.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;opacity:0.25;min-height:300px;text-align:center}
.empty p{font-size:13px;line-height:1.8;max-width:220px;font-weight:300}
.rgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}
.icard{position:relative;border-radius:12px;overflow:hidden;background:rgba(240,236,230,0.04);border:0.5px solid rgba(240,236,230,0.1);aspect-ratio:3/4;transition:all 0.22s}
.icard:hover{border-color:rgba(201,169,110,0.4);transform:translateY(-2px)}
.icard img{width:100%;height:100%;object-fit:cover;display:block}
.iov{position:absolute;bottom:0;left:0;right:0;padding:9px;background:linear-gradient(transparent,rgba(14,12,10,0.88));display:flex;gap:5px;opacity:0;transition:opacity 0.2s}
.icard:hover .iov{opacity:1}
.ibtn{flex:1;padding:6px 4px;border-radius:6px;border:0.5px solid rgba(240,236,230,0.22);background:rgba(14,12,10,0.7);color:#f0ece6;font-size:11px;cursor:pointer;font-family:'DM Sans',sans-serif;text-align:center}
.ibtn:hover{background:rgba(201,169,110,0.28)}
.skel{border-radius:12px;aspect-ratio:3/4;background:rgba(240,236,230,0.05);position:relative;overflow:hidden}
.skel::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(240,236,230,0.04),transparent);animation:shim 1.6s infinite;transform:translateX(-100%)}
@keyframes shim{to{transform:translateX(100%)}}
.skel p{position:absolute;bottom:12px;left:0;right:0;text-align:center;font-size:10px;color:rgba(240,236,230,0.2)}
</style>
</head>
<body>

<div class="hdr">
  <div class="logo">AI MODEL <span>STUDIO</span></div>
  <div style="font-size:11px;color:rgba(240,236,230,0.3)">fal.ai · 600+ modeli</div>
  <div class="online">● online</div>
</div>

<div class="layout">
<div class="lpanel">

  <!-- API KEY -->
  <div class="sec">
    <div class="stitle">Klucz API fal.ai</div>
    <div class="row">
      <input type="password" id="apiKey" placeholder="fal_xxxxxxxxxxxxxxxxxxxxxxxx">
      <button class="iBtn" onclick="var i=document.getElementById('apiKey');i.type=i.type==='password'?'text':'password'">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
      </button>
    </div>
    <div class="hint"><a href="https://fal.ai/dashboard/keys" target="_blank">fal.ai/dashboard/keys</a> &nbsp;·&nbsp; <a href="https://fal.ai/dashboard/billing" target="_blank">doładowanie</a></div>
  </div>

  <!-- WYBÓR MODELU -->
  <div class="sec">
    <div class="stitle">Model AI</div>

    <!-- POPULARNE MODELE -->
    <div class="flbl">Popularne modele do mody</div>
    <div class="popular-grid" id="popularGrid">

      <div class="pcard on" data-endpoint="fal-ai/fashn/tryon/v1.6" data-type="tryon" onclick="selectPopular(this)">
        <div class="pcard-name">FASHN Try-On</div>
        <div class="pcard-id">fal-ai/fashn/tryon/v1.6</div>
        <div class="pcard-price">$0.075/zdjęcie</div>
        <div class="pcard-tag t-tryon">try-on</div>
      </div>

      <div class="pcard" data-endpoint="fal-ai/nano-banana-2/edit" data-type="edit" onclick="selectPopular(this)">
        <div class="pcard-name">Nano Banana 2</div>
        <div class="pcard-id">fal-ai/nano-banana-2/edit</div>
        <div class="pcard-price">$0.039/zdjęcie</div>
        <div class="pcard-tag t-edit">Gemini 3.1</div>
      </div>

      <div class="pcard" data-endpoint="fal-ai/gemini-3-pro-image-preview" data-type="edit" onclick="selectPopular(this)">
        <div class="pcard-name">Nano Banana Pro</div>
        <div class="pcard-id">fal-ai/gemini-3-pro-image-preview</div>
        <div class="pcard-price">$0.15/zdjęcie</div>
        <div class="pcard-tag t-edit">Gemini 3 Pro</div>
      </div>

      <div class="pcard" data-endpoint="fal-ai/flux-2/edit" data-type="edit" onclick="selectPopular(this)">
        <div class="pcard-name">FLUX.2 Edit</div>
        <div class="pcard-id">fal-ai/flux-2/edit</div>
        <div class="pcard-price">$0.05/zdjęcie</div>
        <div class="pcard-tag t-edit">image edit</div>
      </div>

      <div class="pcard" data-endpoint="fal-ai/flux/dev/image-to-image" data-type="edit" onclick="selectPopular(this)">
        <div class="pcard-name">FLUX img2img</div>
        <div class="pcard-id">fal-ai/flux/dev/image-to-image</div>
        <div class="pcard-price">$0.025/zdjęcie</div>
        <div class="pcard-tag t-edit">img2img</div>
      </div>

      <div class="pcard" data-endpoint="fal-ai/flux/dev" data-type="gen" onclick="selectPopular(this)">
        <div class="pcard-name">FLUX Dev</div>
        <div class="pcard-id">fal-ai/flux/dev</div>
        <div class="pcard-price">$0.025/zdjęcie</div>
        <div class="pcard-tag t-gen">text→image</div>
      </div>

      <div class="pcard" data-endpoint="fal-ai/flux/schnell" data-type="gen" onclick="selectPopular(this)">
        <div class="pcard-name">FLUX Schnell</div>
        <div class="pcard-id">fal-ai/flux/schnell</div>
        <div class="pcard-price">$0.003/zdjęcie</div>
        <div class="pcard-tag t-gen">szybki</div>
      </div>

      <div class="pcard" data-endpoint="fal-ai/recraft-v3" data-type="gen" onclick="selectPopular(this)">
        <div class="pcard-name">Recraft V3</div>
        <div class="pcard-id">fal-ai/recraft-v3</div>
        <div class="pcard-price">$0.04/zdjęcie</div>
        <div class="pcard-tag t-gen">wektory/foto</div>
      </div>

      <div class="pcard" data-endpoint="fal-ai/ideogram/v3" data-type="gen" onclick="selectPopular(this)">
        <div class="pcard-name">Ideogram V3</div>
        <div class="pcard-id">fal-ai/ideogram/v3</div>
        <div class="pcard-price">$0.08/zdjęcie</div>
        <div class="pcard-tag t-gen">tekst w obrazie</div>
      </div>

    </div>

    <!-- LUB WPISZ WŁASNY -->
    <div style="margin-top:12px">
      <div class="flbl">Lub wpisz własny endpoint ID z fal.ai</div>
      <div class="row">
        <input type="text" id="customEndpoint" placeholder="np. fal-ai/flux-pro/v1.1-ultra" style="font-family:monospace;font-size:11px" oninput="onCustomEndpoint()">
        <a href="https://fal.ai/explore/models" target="_blank" style="flex-shrink:0">
          <button class="iBtn" title="Przeglądaj modele na fal.ai">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
          </button>
        </a>
      </div>
      <div class="hint">Znajdź endpoint na <a href="https://fal.ai/explore/models" target="_blank">fal.ai/explore/models</a> i wklej ID tutaj</div>
    </div>

    <!-- AKTYWNY MODEL -->
    <div class="model-pill" id="activePill">✦ fal-ai/fashn/tryon/v1.6</div>
  </div>

  <!-- ZDJĘCIA -->
  <div class="sec" id="uploadSec">
    <div class="stitle">Zdjęcia wejściowe</div>
    <div class="upcols">
      <div>
        <div class="upzone" id="pZone" ondragover="dg(event,'pZone',1)" ondragleave="dg(event,'pZone',0)" ondrop="dp(event,'p')">
          <input type="file" id="pFile" accept="image/*" onchange="li(this.files[0],'p')">
          <div class="badge bp">Produkt</div>
          <svg width="22" height="22" viewBox="0 0 32 32" fill="none" opacity="0.5"><rect x="4" y="6" width="24" height="22" rx="3" stroke="#c9a96e" stroke-width="1.2"/><rect x="9" y="12" width="14" height="10" rx="2" stroke="#c9a96e" stroke-width="1"/></svg>
          <h4>Ubranie</h4><p>Wieszak / flat-lay</p>
        </div>
        <div class="prev" id="pPrev"><img id="pImg" src="" alt=""><div class="plbl">Produkt</div><button class="dBtn" onclick="ci('p')">✕</button></div>
      </div>
      <div id="modelCol">
        <div class="upzone" id="mZone" ondragover="dg(event,'mZone',1)" ondragleave="dg(event,'mZone',0)" ondrop="dp(event,'m')">
          <input type="file" id="mFile" accept="image/*" onchange="li(this.files[0],'m')">
          <div class="badge bm">Modelka</div>
          <svg width="22" height="22" viewBox="0 0 32 32" fill="none" opacity="0.5"><circle cx="16" cy="10" r="5" stroke="#378add" stroke-width="1.2"/><path d="M6 28c0-5.52 4.48-10 10-10s10 4.48 10 10" stroke="#378add" stroke-width="1.2" stroke-linecap="round"/></svg>
          <h4>Modelka</h4><p>Pełna sylwetka</p>
        </div>
        <div class="prev" id="mPrev"><img id="mImg" src="" alt=""><div class="plbl">Modelka</div><button class="dBtn" onclick="ci('m')">✕</button></div>
      </div>
    </div>

    <!-- PRESETY MODELEK -->
    <div id="presetWrap" style="margin-top:10px">
      <div class="flbl">Gotowe modelki</div>
      <div class="pmodels">
        <div class="pmod" onclick="sp(this,'https://storage.googleapis.com/falserverless/model_tests/leffa/person_image.jpg')"><span>Modelka 1</span></div>
        <div class="pmod" onclick="sp(this,'https://images.unsplash.com/photo-1529139574466-a303027f1d1f?w=400&q=80')"><span>Modelka 2</span></div>
        <div class="pmod" onclick="sp(this,'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&q=80')"><span>Modelka 3</span></div>
        <div class="pmod" onclick="sp(this,'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400&q=80')"><span>Modelka 4</span></div>
      </div>
    </div>
  </div>

  <!-- FASHN OPCJE -->
  <div class="sec" id="trypnOpts">
    <div class="stitle">Opcje try-on</div>
    <div style="margin-bottom:10px">
      <div class="flbl">Typ ubrania</div>
      <div class="chips">
        <div class="chip on" data-g="cat" data-v="upper_body" onclick="sc(this)">Góra — bluzka / top</div>
        <div class="chip" data-g="cat" data-v="lower_body" onclick="sc(this)">Dół — spodnie / spódnica</div>
        <div class="chip" data-g="cat" data-v="one-piece" onclick="sc(this)">Sukienka / kombinezon</div>
      </div>
    </div>
    <div>
      <div class="flbl">Tryb</div>
      <div class="chips">
        <div class="chip on" data-g="mode" data-v="balanced" onclick="sc(this)">Balans</div>
        <div class="chip" data-g="mode" data-v="fast" onclick="sc(this)">Szybki</div>
        <div class="chip" data-g="mode" data-v="quality" onclick="sc(this)">Wysoka jakość</div>
      </div>
    </div>
  </div>

  <!-- PROMPT -->
  <div class="sec" id="promptSec">
    <div class="stitle">Prompt / opis</div>
    <textarea id="promptTxt" placeholder="Opisz co chcesz wygenerować..."></textarea>
    <div class="hint" id="promptHint"></div>
  </div>

  <!-- LICZBA ZDJĘĆ -->
  <div class="sec">
    <div class="stitle">Liczba zdjęć</div>
    <div style="display:flex;align-items:center;gap:12px">
      <input type="range" min="1" max="4" value="1" step="1" id="nShots" style="flex:1;-webkit-appearance:none;height:2px;background:rgba(240,236,230,0.15);border-radius:2px;outline:none;padding:0;accent-color:#c9a96e" oninput="document.getElementById('nVal').textContent=this.value">
      <span style="font-size:13px;color:#c9a96e;min-width:20px;text-align:right" id="nVal">1</span>
    </div>
    <div class="hint" id="costHint">~$0.075 za 1 zdjęcie</div>
  </div>

  <button class="gen-btn" id="genBtn" onclick="generate()">✦ Generuj zdjęcia</button>
</div>

<!-- RIGHT -->
<div class="rpanel">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <div style="font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:#c9a96e;font-weight:500">Wyniki</div>
    <div style="font-size:11px;color:rgba(240,236,230,0.3)" id="rCount"></div>
  </div>
  <div class="status" id="statusBar"></div>
  <div class="prog" id="progEl"><div class="dot"></div><div class="prog-bar"><div class="prog-fill" id="pFill"></div></div><div id="pLbl" style="min-width:150px;text-align:right;font-size:11px"></div></div>
  <div id="qInfo" style="font-size:11px;color:rgba(240,236,230,0.3);text-align:center;display:none;padding:4px 0"></div>
  <div class="empty" id="emptyEl">
    <svg width="50" height="50" viewBox="0 0 50 50" fill="none"><rect x="5" y="7" width="20" height="36" rx="4" stroke="currentColor" stroke-width="1.2"/><path d="M9 15h12M9 21h8M9 27h10M9 33h6" stroke="currentColor" stroke-width="1" stroke-linecap="round" opacity="0.5"/><circle cx="36" cy="26" r="10" stroke="currentColor" stroke-width="1.2"/></svg>
    <p>Wybierz model, skonfiguruj i kliknij Generuj</p>
  </div>
  <div id="skelWrap" style="display:none"><div class="rgrid" id="skelGrid"></div></div>
  <div class="rgrid" id="rGrid"></div>
</div>
</div>

<script>
const S={cat:'upper_body',mode:'balanced'};
let pUri=null,mUri=null,busy=false;
let activeEndpoint='fal-ai/fashn/tryon/v1.6';
let activeType='tryon'; // tryon | edit | gen

// model info
const MODEL_INFO={
  'fal-ai/fashn/tryon/v1.6':{price:0.075,type:'tryon',prompt:'',hint:'Wgraj ubranie + modelkę. FASHN precyzyjnie nakłada produkt zachowując kolory i wzory.'},
  'fal-ai/nano-banana-2/edit':{price:0.039,type:'edit',prompt:'Put this clothing item on a professional fashion model, white studio background, full body shot, photorealistic',hint:'Gemini 3.1 Flash — edytuje zdjęcie produktu wg opisu. Wgraj ubranie i opisz sesję.'},
  'fal-ai/gemini-3-pro-image-preview':{price:0.15,type:'edit',prompt:'Create a luxury fashion editorial photo featuring this garment on an elegant model, dramatic lighting, Vogue magazine style',hint:'Gemini 3 Pro — najwyższa jakość do klientów premium. Rozumie złożone instrukcje.'},
  'fal-ai/flux-2/edit':{price:0.05,type:'edit',prompt:'Professional fashion model wearing this clothing item, clean white studio background, full body, commercial photography',hint:'FLUX.2 Edit — edycja wieloma referencjami. Wgraj zdjęcie produktu + opisz efekt.'},
  'fal-ai/flux/dev/image-to-image':{price:0.025,type:'edit',prompt:'Fashion model wearing this clothing, white studio background, professional product photography',hint:'FLUX Dev img2img — transformuje zdjęcie produktu. Ustaw strength 0.7-0.85 dla dobrych wyników.'},
  'fal-ai/flux/dev':{price:0.025,type:'gen',prompt:'Professional fashion model wearing elegant clothing, white studio background, full body shot, commercial photography, 8K',hint:'FLUX Dev — generuje z opisu tekstowego. Nie wymaga zdjęcia produktu.'},
  'fal-ai/flux/schnell':{price:0.003,type:'gen',prompt:'Fashion model in elegant outfit, white background, professional photo',hint:'FLUX Schnell — bardzo szybki (~3 sek), tani. Idealny do szybkich podglądów.'},
  'fal-ai/recraft-v3':{price:0.04,type:'gen',prompt:'Professional fashion model in stylish clothing, clean studio background, editorial photography',hint:'Recraft V3 — świetny do fotografii produktowej i wektorów.'},
  'fal-ai/ideogram/v3':{price:0.08,type:'gen',prompt:'Professional fashion model wearing stylish clothes, studio background, commercial photography',hint:'Ideogram V3 — najlepszy do obrazów z tekstem (np. etykiety, napisy na ubraniach).'},
};

function selectPopular(el){
  document.querySelectorAll('.pcard').forEach(c=>c.classList.remove('on'));
  el.classList.add('on');
  activeEndpoint=el.dataset.endpoint;
  activeType=el.dataset.type;
  document.getElementById('customEndpoint').value='';
  updateUI();
}

function onCustomEndpoint(){
  const val=document.getElementById('customEndpoint').value.trim();
  if(!val)return;
  document.querySelectorAll('.pcard').forEach(c=>c.classList.remove('on'));
  activeEndpoint=val;
  // guess type from endpoint
  if(val.includes('tryon'))activeType='tryon';
  else if(val.includes('edit')||val.includes('nano-banana')||val.includes('gemini')||val.includes('image-to-image'))activeType='edit';
  else activeType='gen';
  updateUI();
}

function updateUI(){
  document.getElementById('activePill').textContent='✦ '+activeEndpoint;
  const info=MODEL_INFO[activeEndpoint];
  const price=info?info.price:0.05;
  const type=info?info.type:activeType;
  const shots=parseInt(document.getElementById('nShots').value);
  document.getElementById('costHint').textContent='~$'+(price*shots).toFixed(3)+' za '+shots+' zdjęcie'+(shots>1?'a':'');

  // show/hide model column
  const needsModel=type==='tryon';
  document.getElementById('modelCol').style.display=needsModel?'block':'none';
  document.getElementById('presetWrap').style.display=needsModel?'block':'none';
  document.getElementById('trypnOpts').style.display=type==='tryon'?'block':'none';

  // prompt
  const needsPrompt=type!=='tryon';
  document.getElementById('promptSec').style.display=needsPrompt?'block':'none';
  if(info&&info.prompt)document.getElementById('promptTxt').placeholder=info.prompt;
  if(info&&info.hint)document.getElementById('promptHint').textContent=info.hint;
  else document.getElementById('promptHint').textContent='Wklej endpoint ID z fal.ai/explore/models. Aplikacja automatycznie dobierze parametry.';
}

document.querySelectorAll('.chip').forEach(c=>{c.addEventListener('click',()=>{document.querySelectorAll('[data-g="'+c.dataset.g+'"]').forEach(x=>x.classList.remove('on'));c.classList.add('on');S[c.dataset.g]=c.dataset.v})});
function dg(e,id,on){e.preventDefault();document.getElementById(id).classList.toggle('drag',!!on)}
function dp(e,t){e.preventDefault();dg(e,t==='p'?'pZone':'mZone',0);const f=e.dataTransfer.files[0];if(f&&f.type.startsWith('image/'))li(f,t)}
function li(file,t){if(!file)return;const r=new FileReader();r.onload=e=>{const u=e.target.result;if(t==='p'){pUri=u;document.getElementById('pImg').src=u;document.getElementById('pPrev').classList.add('on');document.getElementById('pZone').style.display='none'}else{mUri=u;document.getElementById('mImg').src=u;document.getElementById('mPrev').classList.add('on');document.getElementById('mZone').style.display='none';document.querySelectorAll('.pmod').forEach(p=>p.classList.remove('on'))}};r.readAsDataURL(file)}
function ci(t){if(t==='p'){pUri=null;document.getElementById('pImg').src='';document.getElementById('pPrev').classList.remove('on');document.getElementById('pZone').style.display='';document.getElementById('pFile').value=''}else{mUri=null;document.getElementById('mImg').src='';document.getElementById('mPrev').classList.remove('on');document.getElementById('mZone').style.display='';document.getElementById('mFile').value='';document.querySelectorAll('.pmod').forEach(p=>p.classList.remove('on'))}}
function sp(el,url){document.querySelectorAll('.pmod').forEach(p=>p.classList.remove('on'));el.classList.add('on');mUri=url;document.getElementById('mImg').src=url;document.getElementById('mPrev').classList.add('on');document.getElementById('mZone').style.display='none'}

function ss(msg,type){const el=document.getElementById('statusBar');el.innerHTML=msg;el.className='status on '+(type||'info')}
function sp2(pct,lbl){const w=document.getElementById('progEl'),f=document.getElementById('pFill'),l=document.getElementById('pLbl');if(pct<0){w.classList.remove('on');return}w.classList.add('on');f.style.width=pct+'%';l.textContent=lbl||''}

async function falFetch(path,method,key,body){
  const res=await fetch('/proxy/'+path,{method:method||'GET',headers:{'Authorization':'Key '+key,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});
  if(!res.ok){const t=await res.text();let m='Błąd '+res.status;try{const j=JSON.parse(t);m+=': '+(j.detail||j.message||t.substring(0,250))}catch{m+=': '+t.substring(0,250)}throw new Error(m)}return res.json()
}

async function pollQueue(key,endpoint,reqId){
  const start=Date.now();
  for(let i=0;i<80;i++){
    await new Promise(r=>setTimeout(r,2500));
    const e=Math.round((Date.now()-start)/1000);
    const d=await falFetch(endpoint+'/requests/'+reqId+'/status','GET',key);
    document.getElementById('qInfo').textContent='Status: '+d.status+' · '+e+'s';
    if(d.status==='COMPLETED')return falFetch(endpoint+'/requests/'+reqId,'GET',key);
    if(d.status==='FAILED')throw new Error('Generowanie nieudane. Spróbuj ponownie.');
  }
  throw new Error('Timeout')
}

function buildPayload(){
  const prompt=document.getElementById('promptTxt').value.trim()||(MODEL_INFO[activeEndpoint]?MODEL_INFO[activeEndpoint].prompt:'');
  const type=MODEL_INFO[activeEndpoint]?MODEL_INFO[activeEndpoint].type:activeType;
  if(type==='tryon')return{model_image:mUri,garment_image:pUri,category:S.cat,mode:S.mode,garment_photo_type:'auto',adjust_hands:true,restore_background:false,restore_clothes:false};
  if(activeEndpoint.includes('image-to-image'))return{image_url:pUri,prompt:prompt,strength:0.8,num_inference_steps:28};
  if(activeEndpoint.includes('nano-banana')||activeEndpoint.includes('gemini'))return{prompt:prompt,image_urls:pUri?[pUri]:[]};
  if(activeEndpoint.includes('flux-2/edit'))return{prompt:prompt,image_url:pUri};
  // generic text-to-image
  return{prompt:prompt,image_size:{width:768,height:1024},num_inference_steps:28,enable_safety_checker:false};
}

function extractImgs(res){
  if(res.images)return res.images.map(i=>typeof i==='string'?i:i.url).filter(Boolean);
  if(res.image)return[typeof res.image==='string'?res.image:res.image.url];
  return[];
}

async function generate(){
  if(busy)return;
  const key=document.getElementById('apiKey').value.trim();
  const type=MODEL_INFO[activeEndpoint]?MODEL_INFO[activeEndpoint].type:activeType;
  if(!key){ss('Wpisz klucz API fal.ai','err');return}
  if(type==='tryon'&&!pUri){ss('Wgraj zdjęcie ubrania','err');return}
  if(type==='tryon'&&!mUri){ss('Wgraj zdjęcie modelki lub wybierz preset','err');return}
  if(type==='edit'&&!pUri&&!activeEndpoint.includes('nano-banana')&&!activeEndpoint.includes('gemini')){ss('Wgraj zdjęcie produktu','err');return}

  const shots=parseInt(document.getElementById('nShots').value);
  busy=true;document.getElementById('genBtn').disabled=true;
  document.getElementById('emptyEl').style.display='none';
  document.getElementById('rGrid').innerHTML='';
  document.getElementById('statusBar').className='status';
  document.getElementById('skelWrap').style.display='block';
  const sg=document.getElementById('skelGrid');sg.innerHTML='';
  for(let i=0;i<shots;i++){const s=document.createElement('div');s.className='skel';s.innerHTML='<p>Generowanie '+(i+1)+'/'+shots+'...</p>';sg.appendChild(s)}
  sp2(10,'Wysyłanie...');
  ss('Wysyłanie do <strong>'+activeEndpoint+'</strong>...','info');
  document.getElementById('qInfo').style.display='block';

  const results=[];
  try{
    for(let i=0;i<shots;i++){
      sp2(15+i*20,'Zdjęcie '+(i+1)+'/'+shots+'...');
      const payload=buildPayload();
      // Fast models run sync
      const isSync=activeEndpoint.includes('schnell');
      if(isSync){
        const res=await falFetch(activeEndpoint,'POST',key,{...payload,sync_mode:true});
        results.push(res);
      }else{
        const sub=await falFetch(activeEndpoint,'POST',key,payload);
        if(sub.request_id){
          results.push(await pollQueue(key,activeEndpoint,sub.request_id));
        }else{
          results.push(sub);
        }
      }
    }
    document.getElementById('skelWrap').style.display='none';
    document.getElementById('qInfo').style.display='none';
    const grid=document.getElementById('rGrid');grid.innerHTML='';
    let tot=0;
    results.forEach(res=>{
      extractImgs(res).forEach(url=>{
        const c=document.createElement('div');c.className='icard';
        c.innerHTML='<img src="'+url+'" loading="lazy"><div class="iov"><button class="ibtn" onclick="dl(\''+url+'\','+(tot+1)+')">↓ Pobierz</button><button class="ibtn" onclick="window.open(\''+url+'\',\'_blank\')">Pełny</button></div>';
        grid.appendChild(c);tot++;
      });
    });
    document.getElementById('rCount').textContent=tot+' zdjęć · '+activeEndpoint;
    sp2(-1);ss('Gotowe! <strong>'+tot+'</strong> zdjęć · '+activeEndpoint,'ok');
  }catch(err){
    document.getElementById('skelWrap').style.display='none';
    document.getElementById('qInfo').style.display='none';
    sp2(-1);ss('<strong>Błąd:</strong> '+(err.message||'Nieznany błąd'),'err');
    document.getElementById('emptyEl').style.display='flex';
  }finally{busy=false;document.getElementById('genBtn').disabled=false}
}

function dl(url,n){const a=document.createElement('a');a.href=url;a.download='zdjecie_'+n+'.jpg';a.target='_blank';document.body.appendChild(a);a.click();document.body.removeChild(a)}

// Init
updateUI();
</script>
</body>
</html>"""


@app.route('/')
def index():
    return HTML, 200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Security-Policy': "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;"
    }

@app.route('/proxy/<path:fal_path>', methods=['GET','POST','OPTIONS'])
def proxy(fal_path):
    if request.method == 'OPTIONS':
        return '', 204, {'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'GET, POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type, Authorization'}
    target = f'https://queue.fal.run/{fal_path}'
    auth = request.headers.get('Authorization','')
    body = request.get_data() if request.method == 'POST' else None
    req = urllib.request.Request(target, data=body, method=request.method,
        headers={'Authorization':auth,'Content-Type':'application/json','User-Agent':'AI-Model-Studio/1.0'})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
            data = r.read()
            return Response(data, status=r.status, content_type='application/json', headers={'Access-Control-Allow-Origin':'*'})
    except urllib.error.HTTPError as e:
        data = e.read()
        return Response(data, status=e.code, content_type='application/json', headers={'Access-Control-Allow-Origin':'*'})
    except Exception as e:
        return Response(json.dumps({'error':str(e)}), status=502, content_type='application/json', headers={'Access-Control-Allow-Origin':'*'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3333))
    app.run(host='0.0.0.0', port=port)
