import os, ssl, json, urllib.request, urllib.error
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FASHN Studio — AI Virtual Try-On</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#09080A;--bg1:#111013;--bg2:#161419;--bg3:#1d1b21;
  --gold:#C9A96E;--gold2:#dbbf87;--gold-dim:rgba(201,169,110,0.15);
  --text:#F0ECE6;--text2:rgba(240,236,230,0.55);--text3:rgba(240,236,230,0.28);
  --border:rgba(240,236,230,0.08);--border2:rgba(240,236,230,0.14);
  --green:rgba(29,158,117,0.9);--green-bg:rgba(29,158,117,0.1);--green-border:rgba(29,158,117,0.25);
  --blue:rgba(100,160,240,0.9);--blue-bg:rgba(100,160,240,0.1);--blue-border:rgba(100,160,240,0.25);
  --red:rgba(220,80,80,0.9);--red-bg:rgba(220,80,80,0.08);--red-border:rgba(220,80,80,0.25);
}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;line-height:1.5}
a{color:var(--gold);text-decoration:none}a:hover{text-decoration:underline}

/* ─── Header ─── */
.hdr{display:flex;align-items:center;justify-content:space-between;padding:0 28px;height:54px;border-bottom:0.5px solid var(--border);background:rgba(9,8,10,0.95);backdrop-filter:blur(12px);position:sticky;top:0;z-index:200}
.logo{font-family:'Cormorant Garamond',serif;font-size:20px;letter-spacing:0.06em;font-weight:400}.logo em{color:var(--gold);font-style:normal}
.hdr-right{display:flex;align-items:center;gap:12px}
.badge-live{font-size:10px;padding:3px 9px;border-radius:100px;background:var(--green-bg);border:0.5px solid var(--green-border);color:var(--green);letter-spacing:0.06em}
.hdr-link{font-size:11px;color:var(--text3);letter-spacing:0.04em}

/* ─── Layout ─── */
.layout{display:grid;grid-template-columns:400px 1fr;min-height:calc(100vh - 54px)}
@media(max-width:860px){.layout{grid-template-columns:1fr}}
.lpanel{border-right:0.5px solid var(--border);overflow-y:auto;max-height:calc(100vh - 54px);display:flex;flex-direction:column}
.rpanel{overflow-y:auto;max-height:calc(100vh - 54px);padding:24px;display:flex;flex-direction:column;gap:16px}

/* ─── Panel sections ─── */
.sec{padding:18px 20px;border-bottom:0.5px solid var(--border)}
.sec:last-child{border-bottom:none;padding-bottom:24px}
.stitle{font-size:9px;letter-spacing:0.18em;text-transform:uppercase;color:var(--gold);font-weight:500;margin-bottom:12px}
.flbl{font-size:10px;color:var(--text3);letter-spacing:0.07em;text-transform:uppercase;margin-bottom:6px}

/* ─── Inputs ─── */
input[type=text],input[type=password],select,textarea{
  background:var(--bg3);border:0.5px solid var(--border2);border-radius:8px;
  padding:9px 12px;color:var(--text);font-size:12px;font-family:'Inter',sans-serif;
  outline:none;width:100%;transition:border-color 0.18s
}
input[type=text]:focus,input[type=password]:focus,select:focus,textarea:focus{border-color:rgba(201,169,110,0.5)}
input::placeholder,textarea::placeholder{color:var(--text3)}
select{cursor:pointer;appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M1 1l4 4 4-4' stroke='rgba(240,236,230,0.3)' stroke-width='1.2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;padding-right:28px}
select option{background:var(--bg2)}
textarea{resize:vertical;min-height:72px;line-height:1.6}
.row{display:flex;gap:8px;align-items:stretch}.row input{flex:1}
.icon-btn{width:36px;flex-shrink:0;border-radius:8px;border:0.5px solid var(--border2);background:var(--bg3);color:var(--text2);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.18s}
.icon-btn:hover{background:var(--bg2);border-color:rgba(201,169,110,0.35)}

/* ─── API pill ─── */
.api-pill{font-size:10px;padding:3px 10px;border-radius:100px;background:var(--gold-dim);border:0.5px solid rgba(201,169,110,0.25);color:var(--gold);margin-top:8px;display:inline-block;font-family:monospace;letter-spacing:0.03em}

/* ─── Model selector tabs ─── */
.model-tabs{display:flex;gap:6px;flex-wrap:wrap}
.mtab{padding:7px 14px;border-radius:8px;border:0.5px solid var(--border2);background:var(--bg3);color:var(--text2);cursor:pointer;font-size:11px;font-family:'Inter',sans-serif;transition:all 0.18s;letter-spacing:0.03em}
.mtab:hover{border-color:rgba(201,169,110,0.35);color:var(--text)}
.mtab.on{background:var(--gold-dim);border-color:rgba(201,169,110,0.5);color:var(--gold)}
.mtab .tag{font-size:9px;padding:1px 5px;border-radius:3px;margin-left:5px;vertical-align:middle}
.tag-try{background:rgba(29,158,117,0.15);color:var(--green)}
.tag-gen{background:rgba(100,160,240,0.12);color:var(--blue)}

/* ─── Image upload zones ─── */
.upload-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.upload-zone{border:1px dashed rgba(201,169,110,0.25);border-radius:10px;min-height:130px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:all 0.2s;position:relative;background:var(--bg2);text-align:center;padding:14px 10px}
.upload-zone:hover{border-color:rgba(201,169,110,0.6);background:rgba(201,169,110,0.04)}
.upload-zone input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.upload-zone .uz-badge{font-size:9px;letter-spacing:0.1em;text-transform:uppercase;padding:2px 7px;border-radius:100px;margin-bottom:7px;font-weight:500}
.uz-badge.garment{background:var(--gold-dim);color:var(--gold);border:0.5px solid rgba(201,169,110,0.25)}
.uz-badge.model{background:var(--blue-bg);color:var(--blue);border:0.5px solid var(--blue-border)}
.upload-zone h4{font-size:11px;font-weight:500;color:var(--text);margin-bottom:2px}
.upload-zone p{font-size:10px;color:var(--text3);font-weight:300}

/* ─── Image preview ─── */
.img-prev{display:none;position:relative;border-radius:10px;overflow:hidden;border:0.5px solid var(--border2);background:var(--bg2)}
.img-prev.on{display:block}
.img-prev img{width:100%;max-height:150px;object-fit:contain;display:block}
.img-prev-label{position:absolute;bottom:0;left:0;right:0;padding:5px 8px;background:rgba(9,8,10,0.8);font-size:10px;color:var(--text2)}
.img-del{position:absolute;top:5px;right:5px;width:22px;height:22px;border-radius:5px;background:rgba(9,8,10,0.85);border:0.5px solid var(--border2);color:var(--text);cursor:pointer;font-size:11px;display:flex;align-items:center;justify-content:center;transition:all 0.15s}
.img-del:hover{background:rgba(220,80,80,0.25);border-color:var(--red-border)}

/* ─── Preset models ─── */
.preset-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:8px}
.preset-item{border-radius:8px;aspect-ratio:3/4;border:1.5px solid transparent;cursor:pointer;overflow:hidden;background:var(--bg3);transition:all 0.2s;position:relative}
.preset-item img{width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;transition:opacity 0.2s}
.preset-item:hover img,.preset-item.on img{opacity:1}
.preset-item.on{border-color:var(--gold)}
.preset-item:hover{border-color:rgba(201,169,110,0.45)}
.preset-item .plabel{position:absolute;bottom:3px;left:0;right:0;text-align:center;font-size:8px;color:rgba(240,236,230,0.5);background:rgba(9,8,10,0.6);padding:2px}

/* ─── Options chips ─── */
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.chip{font-size:11px;padding:5px 12px;border-radius:100px;border:0.5px solid var(--border2);background:transparent;color:var(--text2);cursor:pointer;transition:all 0.18s;font-family:'Inter',sans-serif}
.chip:hover{border-color:rgba(201,169,110,0.4);color:var(--text)}
.chip.on{background:var(--gold-dim);border-color:rgba(201,169,110,0.5);color:var(--gold)}

/* ─── Number input ─── */
.num-row{display:flex;align-items:center;gap:12px}
.num-row input[type=range]{flex:1;-webkit-appearance:none;height:2px;background:var(--bg3);border:none;border-radius:2px;outline:none;padding:0;accent-color:var(--gold)}
.num-val{font-size:14px;color:var(--gold);min-width:24px;text-align:right;font-weight:500}

/* ─── Generate button ─── */
.gen-btn{width:100%;padding:15px;background:var(--gold);border:none;border-radius:10px;color:#0e0c0a;font-family:'Inter',sans-serif;font-size:12px;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;cursor:pointer;transition:all 0.22s;margin-top:6px}
.gen-btn:hover:not(:disabled){background:var(--gold2);transform:translateY(-1px)}
.gen-btn:disabled{background:rgba(201,169,110,0.15);color:rgba(14,12,10,0.35);cursor:not-allowed}

/* ─── Status bar ─── */
.sbar{padding:11px 14px;border-radius:9px;font-size:12px;line-height:1.6;display:none}
.sbar.on{display:block}
.sbar.info{background:var(--blue-bg);border:0.5px solid var(--blue-border);color:var(--blue)}
.sbar.err{background:var(--red-bg);border:0.5px solid var(--red-border);color:var(--red)}
.sbar.ok{background:var(--green-bg);border:0.5px solid var(--green-border);color:var(--green)}

/* ─── Progress ─── */
.progress-wrap{display:none;align-items:center;gap:12px;font-size:11px;color:var(--text3)}
.progress-wrap.on{display:flex}
.progress-bar{flex:1;height:1.5px;background:var(--bg3);border-radius:2px;overflow:hidden}
.progress-fill{height:100%;background:var(--gold);border-radius:2px;transition:width 0.6s}
.pulse-dot{width:6px;height:6px;border-radius:50%;background:var(--gold);flex-shrink:0;animation:pulse 1.2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.3;transform:scale(0.7)}}
.status-txt{font-size:10px;color:var(--text3);text-align:center;padding:2px 0}

/* ─── Results ─── */
.results-header{display:flex;align-items:center;justify-content:space-between}
.results-label{font-size:9px;letter-spacing:0.18em;text-transform:uppercase;color:var(--gold);font-weight:500}
.results-count{font-size:11px;color:var(--text3)}
.results-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px}
.result-card{position:relative;border-radius:12px;overflow:hidden;background:var(--bg2);border:0.5px solid var(--border);aspect-ratio:3/4;transition:all 0.22s}
.result-card:hover{border-color:rgba(201,169,110,0.35);transform:translateY(-3px);box-shadow:0 8px 32px rgba(0,0,0,0.5)}
.result-card img{width:100%;height:100%;object-fit:cover;display:block}
.result-overlay{position:absolute;bottom:0;left:0;right:0;padding:12px 10px;background:linear-gradient(transparent,rgba(9,8,10,0.9));display:flex;gap:6px;opacity:0;transition:opacity 0.2s}
.result-card:hover .result-overlay{opacity:1}
.result-btn{flex:1;padding:7px 5px;border-radius:7px;border:0.5px solid rgba(240,236,230,0.2);background:rgba(9,8,10,0.7);color:var(--text);font-size:11px;cursor:pointer;font-family:'Inter',sans-serif;text-align:center;transition:all 0.15s}
.result-btn:hover{background:rgba(201,169,110,0.25);border-color:rgba(201,169,110,0.4)}

/* ─── Skeletons ─── */
.skeleton{border-radius:12px;aspect-ratio:3/4;background:var(--bg2);position:relative;overflow:hidden;border:0.5px solid var(--border)}
.skeleton::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(240,236,230,0.03),transparent);animation:shimmer 1.8s infinite;transform:translateX(-100%)}
@keyframes shimmer{to{transform:translateX(100%)}}
.skeleton p{position:absolute;bottom:14px;left:0;right:0;text-align:center;font-size:10px;color:var(--text3)}

/* ─── Empty state ─── */
.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;opacity:0.2;min-height:360px;text-align:center}
.empty svg{opacity:0.7}
.empty h3{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:400;letter-spacing:0.04em}
.empty p{font-size:12px;line-height:1.9;max-width:240px;font-weight:300}

/* ─── Hint ─── */
.hint{font-size:10px;color:var(--text3);margin-top:5px;line-height:1.6;font-weight:300}

/* ─── Cost hint ─── */
.cost-hint{font-size:10px;color:rgba(201,169,110,0.6);margin-top:5px}
</style>
</head>
<body>
<div class="hdr">
  <div class="logo">FASHN <em>STUDIO</em></div>
  <div class="hdr-right">
    <div class="hdr-link">fashn.ai API</div>
    <div class="badge-live">LIVE</div>
  </div>
</div>

<div class="layout">
<!-- ══════════ LEFT PANEL ══════════ -->
<div class="lpanel">

  <!-- API KEY -->
  <div class="sec">
    <div class="stitle">Klucz API FASHN.ai</div>
    <div class="row">
      <input type="password" id="apiKey" placeholder="fa-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx">
      <button class="icon-btn" id="toggleKey" title="Pokaż/ukryj">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
      </button>
    </div>
    <div class="hint">Utwórz klucz na <a href="https://fashn.ai/dashboard/api-keys" target="_blank">fashn.ai/dashboard</a></div>
    <div class="api-pill" id="endpointPill">api.fashn.ai/v1</div>
  </div>

  <!-- MODEL SELECTION -->
  <div class="sec">
    <div class="stitle">Model AI</div>
    <div class="model-tabs">
      <div class="mtab on" data-m="tryon-v1.6" data-t="tryon">Try-On v1.6 <span class="tag tag-try">try-on</span></div>
      <div class="mtab" data-m="product-to-model" data-t="product">Produkt→Model <span class="tag tag-gen">gen</span></div>
      <div class="mtab" data-m="background-remove" data-t="bg">Usuń tło <span class="tag tag-gen">bg</span></div>
    </div>
    <div class="hint" id="modelHint">Wirtualna przymierzalnia — nałóż ubranie na model. ~$0.075/zdjęcie</div>
  </div>

  <!-- UPLOAD IMAGES -->
  <div class="sec" id="uploadSec">
    <div class="stitle">Zdjęcia wejściowe</div>
    <div class="upload-grid">
      <!-- GARMENT -->
      <div>
        <div class="upload-zone" id="garmentZone">
          <input type="file" id="garmentFile" accept="image/jpeg,image/png,image/webp">
          <div class="uz-badge garment">Ubranie</div>
          <svg width="22" height="22" viewBox="0 0 32 32" fill="none" opacity="0.45" style="margin-bottom:6px">
            <path d="M10 6L6 12h4v14h12V12h4l-4-6" stroke="#C9A96E" stroke-width="1.2" stroke-linejoin="round"/>
            <path d="M10 6c0 2 6 4 6 4s6-2 6-4" stroke="#C9A96E" stroke-width="1.2"/>
          </svg>
          <h4>Wgraj ubranie</h4>
          <p>Flat-lay / na modelu / manekin</p>
        </div>
        <div class="img-prev" id="garmentPrev">
          <img id="garmentImg" src="" alt="">
          <div class="img-prev-label">Ubranie</div>
          <button class="img-del" id="delGarment">✕</button>
        </div>
      </div>
      <!-- MODEL (for tryon) -->
      <div id="modelUploadCol">
        <div class="upload-zone" id="modelZone">
          <input type="file" id="modelFile" accept="image/jpeg,image/png,image/webp">
          <div class="uz-badge model">Modelka</div>
          <svg width="22" height="22" viewBox="0 0 32 32" fill="none" opacity="0.45" style="margin-bottom:6px">
            <circle cx="16" cy="10" r="5" stroke="#64A0F0" stroke-width="1.2"/>
            <path d="M6 29c0-5.52 4.48-10 10-10s10 4.48 10 10" stroke="#64A0F0" stroke-width="1.2" stroke-linecap="round"/>
          </svg>
          <h4>Wgraj modelkę</h4>
          <p>Pełna sylwetka</p>
        </div>
        <div class="img-prev" id="modelPrev">
          <img id="modelImg" src="" alt="">
          <div class="img-prev-label">Modelka</div>
          <button class="img-del" id="delModel">✕</button>
        </div>
      </div>
    </div>

    <!-- PRESET MODELS -->
    <div id="presetSection" style="margin-top:12px">
      <div class="flbl">Przykładowe modelki</div>
      <div class="preset-grid" id="presetGrid">
        <div class="preset-item" data-url="https://storage.googleapis.com/falserverless/model_tests/leffa/person_image.jpg">
          <img src="https://storage.googleapis.com/falserverless/model_tests/leffa/person_image.jpg" alt="" loading="lazy">
          <div class="plabel">M1</div>
        </div>
        <div class="preset-item" data-url="https://images.unsplash.com/photo-1529139574466-a303027f1d1f?w=400&q=80">
          <img src="https://images.unsplash.com/photo-1529139574466-a303027f1d1f?w=400&q=80" alt="" loading="lazy">
          <div class="plabel">M2</div>
        </div>
        <div class="preset-item" data-url="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&q=80">
          <img src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&q=80" alt="" loading="lazy">
          <div class="plabel">M3</div>
        </div>
        <div class="preset-item" data-url="https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400&q=80">
          <img src="https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400&q=80" alt="" loading="lazy">
          <div class="plabel">M4</div>
        </div>
      </div>
    </div>
  </div>

  <!-- TRY-ON OPTIONS -->
  <div class="sec" id="tryonOptions">
    <div class="stitle">Parametry try-on</div>
    <div style="margin-bottom:14px">
      <div class="flbl">Kategoria ubrania</div>
      <div class="chips">
        <div class="chip on" data-g="cat" data-v="auto">Auto</div>
        <div class="chip" data-g="cat" data-v="tops">Góra</div>
        <div class="chip" data-g="cat" data-v="bottoms">Dół</div>
        <div class="chip" data-g="cat" data-v="one-pieces">Sukienka</div>
      </div>
    </div>
    <div style="margin-bottom:14px">
      <div class="flbl">Tryb generowania</div>
      <div class="chips">
        <div class="chip on" data-g="mode" data-v="balanced">Balans</div>
        <div class="chip" data-g="mode" data-v="performance">Szybki</div>
        <div class="chip" data-g="mode" data-v="quality">Jakość HD</div>
      </div>
    </div>
    <div>
      <div class="flbl">Typ zdjęcia ubrania</div>
      <div class="chips">
        <div class="chip on" data-g="gtype" data-v="auto">Auto-detect</div>
        <div class="chip" data-g="gtype" data-v="flat-lay">Flat-lay</div>
        <div class="chip" data-g="gtype" data-v="model">Na modelu</div>
      </div>
    </div>
  </div>

  <!-- PRODUCT-TO-MODEL OPTIONS -->
  <div class="sec" id="prodOptions" style="display:none">
    <div class="stitle">Parametry Product→Model</div>
    <div style="margin-bottom:12px">
      <div class="flbl">Opis sceny (opcjonalnie)</div>
      <textarea id="prodPrompt" placeholder="np. professional fashion model, white studio, editorial photography"></textarea>
    </div>
    <div>
      <div class="flbl">Tryb</div>
      <div class="chips">
        <div class="chip on" data-g="pmode" data-v="balanced">Balans</div>
        <div class="chip" data-g="pmode" data-v="performance">Szybki</div>
        <div class="chip" data-g="pmode" data-v="quality">Jakość</div>
      </div>
    </div>
  </div>

  <!-- SHOTS -->
  <div class="sec">
    <div class="stitle">Liczba zdjęć</div>
    <div class="num-row">
      <input type="range" min="1" max="4" value="1" step="1" id="nShots">
      <span class="num-val" id="nVal">1</span>
    </div>
    <div class="cost-hint" id="costHint">~$0.075 za 1 zdjęcie</div>
  </div>

  <!-- GENERATE BUTTON -->
  <div class="sec">
    <button class="gen-btn" id="genBtn">Generuj</button>
  </div>

</div><!-- /lpanel -->

<!-- ══════════ RIGHT PANEL ══════════ -->
<div class="rpanel">
  <div class="results-header">
    <div class="results-label">Wyniki</div>
    <div class="results-count" id="rCount"></div>
  </div>
  <div class="sbar" id="sbar"></div>
  <div class="progress-wrap" id="progWrap">
    <div class="pulse-dot"></div>
    <div class="progress-bar"><div class="progress-fill" id="progFill"></div></div>
    <div style="min-width:130px;text-align:right;font-size:11px" id="progLabel"></div>
  </div>
  <div class="status-txt" id="statusTxt"></div>
  <div class="empty" id="emptyEl">
    <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
      <rect x="8" y="6" width="22" height="48" rx="5" stroke="currentColor" stroke-width="1.2"/>
      <path d="M8 14h22M8 46h22" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
      <circle cx="44" cy="34" r="12" stroke="currentColor" stroke-width="1.2"/>
      <path d="M44 30v4l3 2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
    </svg>
    <h3>FASHN Studio</h3>
    <p>Wybierz model, wgraj zdjęcia i kliknij Generuj</p>
  </div>
  <div id="skelWrap" style="display:none"><div class="results-grid" id="skelGrid"></div></div>
  <div class="results-grid" id="rGrid"></div>
</div>
</div>

<script>
(function(){
'use strict';

/* ── State ── */
var S = {cat:'auto', mode:'balanced', gtype:'auto', pmode:'balanced'};
var garmentUri=null, modelUri=null, busy=false;
var currentModel='tryon-v1.6', currentType='tryon';

var FASHN_API = '/fashn';
var MODELS = {
  'tryon-v1.6':     {price:0.075, type:'tryon',   hint:'Virtual try-on v1.6 — idealne kolory i wzory. ~$0.075/zdjęcie'},
  'product-to-model':{price:0.10,  type:'product', hint:'Przekształca zdjęcie produktu w zdjęcie na modelu. ~$0.10/zdjęcie'},
  'background-remove':{price:0.02, type:'bg',      hint:'Usuwa tło ze zdjęcia produktu. ~$0.02/zdjęcie'}
};

/* ── UI update ── */
function updateUI(){
  var info = MODELS[currentModel] || {price:0.075, type:'tryon'};
  var shots = parseInt(document.getElementById('nShots').value);
  document.getElementById('costHint').textContent = '~$'+(info.price*shots).toFixed(3)+' za '+shots+' zdjęcie';
  document.getElementById('modelHint').textContent = info.hint;
  // show/hide sections
  var isTryon = currentType==='tryon';
  var isProd = currentType==='product';
  document.getElementById('modelUploadCol').style.display = isTryon?'':'none';
  document.getElementById('presetSection').style.display = isTryon?'':'none';
  document.getElementById('tryonOptions').style.display = isTryon?'':'none';
  document.getElementById('prodOptions').style.display = isProd?'':'none';
  // bg-remove: only garment upload needed
  var garmentLabel = currentType==='bg'?'Zdjęcie produktu':'Ubranie';
  document.querySelector('#garmentZone h4').textContent = 'Wgraj '+(currentType==='bg'?'zdjęcie':'ubranie');
}

/* ── Model tabs ── */
document.querySelectorAll('.mtab').forEach(function(tab){
  tab.addEventListener('click', function(){
    document.querySelectorAll('.mtab').forEach(function(t){t.classList.remove('on');});
    tab.classList.add('on');
    currentModel = tab.dataset.m;
    currentType = tab.dataset.t;
    updateUI();
  });
});

/* ── Toggle key visibility ── */
document.getElementById('toggleKey').addEventListener('click', function(){
  var inp = document.getElementById('apiKey');
  inp.type = inp.type==='password'?'text':'password';
});

/* ── Shots slider ── */
document.getElementById('nShots').addEventListener('input', function(){
  document.getElementById('nVal').textContent = this.value;
  updateUI();
});

/* ── Chips ── */
document.querySelectorAll('.chip').forEach(function(c){
  c.addEventListener('click', function(){
    document.querySelectorAll('[data-g="'+c.dataset.g+'"]').forEach(function(x){x.classList.remove('on');});
    c.classList.add('on');
    S[c.dataset.g] = c.dataset.v;
  });
});

/* ── File readers ── */
function loadFile(file, type){
  var r = new FileReader();
  r.onload = function(e){ setImage(e.target.result, type); };
  r.readAsDataURL(file);
}
function setImage(uri, type){
  if(type==='garment'){
    garmentUri=uri;
    document.getElementById('garmentImg').src=uri;
    document.getElementById('garmentPrev').classList.add('on');
    document.getElementById('garmentZone').style.display='none';
  } else {
    modelUri=uri;
    document.getElementById('modelImg').src=uri;
    document.getElementById('modelPrev').classList.add('on');
    document.getElementById('modelZone').style.display='none';
    document.querySelectorAll('.preset-item').forEach(function(p){p.classList.remove('on');});
  }
}
document.getElementById('garmentFile').addEventListener('change', function(){
  if(this.files&&this.files[0]) loadFile(this.files[0],'garment');
});
document.getElementById('modelFile').addEventListener('change', function(){
  if(this.files&&this.files[0]) loadFile(this.files[0],'model');
});

/* ── Delete images ── */
document.getElementById('delGarment').addEventListener('click', function(){
  garmentUri=null;
  document.getElementById('garmentImg').src='';
  document.getElementById('garmentPrev').classList.remove('on');
  document.getElementById('garmentZone').style.display='';
  document.getElementById('garmentFile').value='';
});
document.getElementById('delModel').addEventListener('click', function(){
  modelUri=null;
  document.getElementById('modelImg').src='';
  document.getElementById('modelPrev').classList.remove('on');
  document.getElementById('modelZone').style.display='';
  document.getElementById('modelFile').value='';
  document.querySelectorAll('.preset-item').forEach(function(p){p.classList.remove('on');});
});

/* ── Presets ── */
document.querySelectorAll('.preset-item').forEach(function(el){
  el.addEventListener('click', function(){
    document.querySelectorAll('.preset-item').forEach(function(p){p.classList.remove('on');});
    el.classList.add('on');
    setImage(el.dataset.url,'model');
  });
});

/* ── Drag and drop ── */
['garmentZone','modelZone'].forEach(function(id){
  var zone=document.getElementById(id);
  zone.addEventListener('dragover',function(e){e.preventDefault();zone.style.borderColor='rgba(201,169,110,0.7)';});
  zone.addEventListener('dragleave',function(){zone.style.borderColor='';});
  zone.addEventListener('drop',function(e){
    e.preventDefault();zone.style.borderColor='';
    var file=e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files[0];
    if(file&&file.type.startsWith('image/')) loadFile(file,id==='garmentZone'?'garment':'model');
  });
});

/* ── Status helpers ── */
function showStatus(msg,type){
  var el=document.getElementById('sbar');
  el.textContent=msg;
  el.className='sbar on '+(type||'info');
}
function setProgress(pct,label){
  var w=document.getElementById('progWrap');
  var f=document.getElementById('progFill');
  var l=document.getElementById('progLabel');
  if(pct<0){w.classList.remove('on');return;}
  w.classList.add('on');
  f.style.width=pct+'%';
  l.textContent=label||'';
}
function setStatusTxt(txt){document.getElementById('statusTxt').textContent=txt||'';}

/* ── FASHN API calls ── */
function fashnRequest(action, payload){
  return fetch(FASHN_API, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({action:action, payload:payload})
  }).then(function(res){
    return res.json().then(function(j){
      if(!res.ok) throw new Error(j.error||j.detail||('HTTP '+res.status));
      return j;
    });
  });
}

/* ── Poll until done ── */
function pollStatus(predictionId, apiKey){
  var start=Date.now(), attempts=0;
  function attempt(){
    return new Promise(function(r){setTimeout(r,2500);}).then(function(){
      attempts++;
      var elapsed=Math.round((Date.now()-start)/1000);
      setStatusTxt('Status: polling... '+elapsed+'s');
      return fashnRequest('status',{id:predictionId, api_key:apiKey}).then(function(d){
        var status=d.status||'';
        if(status==='completed') return d;
        if(status==='failed') throw new Error('Generowanie nieudane: '+(d.error||'Nieznany błąd'));
        if(attempts>=80) throw new Error('Timeout — za długo czekamy');
        return attempt();
      });
    });
  }
  return attempt();
}

/* ── Build payload ── */
function buildPayload(gUri, mUri){
  var key=document.getElementById('apiKey').value.trim();
  if(currentType==='tryon'){
    return {
      api_key:key, model_name:'tryon-v1.6',
      inputs:{
        model_image:mUri, garment_image:gUri,
        category:S.cat, mode:S.mode, garment_photo_type:S.gtype,
        moderation_level:'permissive', num_samples:1, output_format:'png'
      }
    };
  }
  if(currentType==='product'){
    var payload={api_key:key, model_name:'product-to-model', inputs:{garment_image:gUri, mode:S.pmode}};
    var prompt=document.getElementById('prodPrompt').value.trim();
    if(prompt) payload.inputs.prompt=prompt;
    return payload;
  }
  // bg-remove
  return {api_key:key, model_name:'background-remove', inputs:{image:gUri}};
}

/* ── Extract image URLs from response ── */
function extractUrls(res){
  if(res.output&&Array.isArray(res.output)) return res.output.filter(Boolean);
  if(res.output&&typeof res.output==='string') return[res.output];
  if(res.images) return res.images.map(function(i){return typeof i==='string'?i:i.url;}).filter(Boolean);
  if(res.image) return[typeof res.image==='string'?res.image:res.image.url];
  return[];
}

/* ── Add result card ── */
function addCard(url){
  document.getElementById('emptyEl').style.display='none';
  var card=document.createElement('div');
  card.className='result-card';card.dataset.url=url;
  var img=document.createElement('img');img.src=url;img.loading='lazy';
  var ov=document.createElement('div');ov.className='result-overlay';
  var b1=document.createElement('button');b1.className='result-btn';b1.textContent='Pobierz';b1.dataset.a='dl';
  var b2=document.createElement('button');b2.className='result-btn';b2.textContent='Pełny';b2.dataset.a='open';
  ov.appendChild(b1);ov.appendChild(b2);
  card.appendChild(img);card.appendChild(ov);
  document.getElementById('rGrid').appendChild(card);
}
document.getElementById('rGrid').addEventListener('click',function(e){
  var btn=e.target.closest('.result-btn');if(!btn)return;
  var url=btn.closest('.result-card').dataset.url;if(!url)return;
  if(btn.dataset.a==='dl'){var a=document.createElement('a');a.href=url;a.download='fashn-output.png';a.target='_blank';document.body.appendChild(a);a.click();document.body.removeChild(a);}
  else window.open(url,'_blank');
});

/* ── Generate ── */
document.getElementById('genBtn').addEventListener('click', function(){
  if(busy) return;
  var key=document.getElementById('apiKey').value.trim();
  if(!key){showStatus('Wpisz klucz API FASHN.ai','err');return;}
  if(!garmentUri){showStatus(currentType==='bg'?'Wgraj zdjęcie produktu':'Wgraj zdjęcie ubrania','err');return;}
  if(currentType==='tryon'&&!modelUri){showStatus('Wgraj zdjęcie modelki lub wybierz preset','err');return;}

  var shots=parseInt(document.getElementById('nShots').value);
  busy=true;
  document.getElementById('genBtn').disabled=true;
  document.getElementById('emptyEl').style.display='none';
  document.getElementById('rGrid').innerHTML='';
  document.getElementById('sbar').className='sbar';

  // Skeletons
  var sg=document.getElementById('skelGrid');
  sg.innerHTML='';
  for(var i=0;i<shots;i++){
    var sk=document.createElement('div');sk.className='skeleton';
    var skp=document.createElement('p');skp.textContent='Generowanie '+(i+1)+'/'+shots+'...';
    sk.appendChild(skp);sg.appendChild(sk);
  }
  document.getElementById('skelWrap').style.display='block';
  setProgress(8,'Wysyłanie...');
  showStatus('Łączenie z FASHN.ai...','info');

  var results=[],total=0;
  var _g=garmentUri,_m=modelUri;

  function doShot(idx){
    if(idx>=shots){
      document.getElementById('skelWrap').style.display='none';
      setProgress(-1);setStatusTxt('');
      results.forEach(function(res){
        extractUrls(res).forEach(function(url){addCard(url);total++;});
      });
      document.getElementById('rCount').textContent=total+' zdjęć';
      showStatus('Gotowe! Wygenerowano '+total+' zdjęć.','ok');
      busy=false;document.getElementById('genBtn').disabled=false;
      return;
    }
    setProgress(15+idx*20,'Zdjęcie '+(idx+1)+'/'+shots+'...');
    showStatus('Wysyłanie żądania '+(idx+1)+'/'+shots+'...','info');
    var payload=buildPayload(_g,_m);
    fashnRequest('run', payload).then(function(sub){
      var predId=sub.id;
      if(!predId) throw new Error('Brak ID predykcji w odpowiedzi');
      showStatus('Generowanie '+(idx+1)+'/'+shots+'... (ID: '+predId.substring(0,12)+'...)','info');
      return pollStatus(predId, payload.api_key);
    }).then(function(res){
      results.push(res);
      doShot(idx+1);
    }).catch(function(err){
      document.getElementById('skelWrap').style.display='none';
      setProgress(-1);setStatusTxt('');
      showStatus('Błąd: '+(err.message||'Nieznany błąd'),'err');
      document.getElementById('emptyEl').style.display='flex';
      busy=false;document.getElementById('genBtn').disabled=false;
    });
  }
  doShot(0);
});

updateUI();
})();
</script>
</body>
</html>"""


def fashn_request(method, path, api_key, body=None):
    """Proxy request to FASHN.ai API"""
    target = 'https://api.fashn.ai/v1/' + path
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json',
        'User-Agent': 'FASHN-Studio/1.0'
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(target, data=data, method=method, headers=headers)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        body_bytes = e.read()
        try:
            return e.code, json.loads(body_bytes)
        except Exception:
            return e.code, {'error': body_bytes.decode('utf-8', errors='replace')}
    except Exception as e:
        return 502, {'error': str(e)}


@app.route('/')
def index():
    return HTML, 200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-store',
        'Content-Security-Policy': (
            "default-src * data: blob:; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src * 'unsafe-inline'; "
            "img-src * data: blob:; "
            "connect-src * data: blob:;"
        )
    }


@app.route('/fashn', methods=['POST', 'OPTIONS'])
def fashn_proxy():
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
    payload = data.get('payload', {})
    api_key = payload.get('api_key', '')

    if not api_key:
        return jsonify({'error': 'Brak klucza API'}), 400

    if action == 'run':
        # Submit a new prediction
        body = {
            'model_name': payload.get('model_name', 'tryon-v1.6'),
            'inputs': payload.get('inputs', {})
        }
        status, result = fashn_request('POST', 'run', api_key, body)

    elif action == 'status':
        # Poll prediction status
        pred_id = payload.get('id', '')
        if not pred_id:
            return jsonify({'error': 'Missing prediction id'}), 400
        status, result = fashn_request('GET', 'status/' + pred_id, api_key)

    else:
        return jsonify({'error': 'Unknown action: ' + action}), 400

    return Response(
        json.dumps(result),
        status=status,
        content_type='application/json',
        headers={'Access-Control-Allow-Origin': '*'}
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3333))
    app.run(host='0.0.0.0', port=port)
