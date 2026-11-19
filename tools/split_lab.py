# -*- coding: utf-8 -*-
"""Split the portal: settings leave the public page and move to a private lab.

NOTE: this script predates the lab moving off GitHub Pages. Re-running it would
recreate a PUBLIC lab.html in this repo — do not run it now. The lab lives on the
Cloudflare Worker (sliding-in-backend/portal-lab.html); see tools/build_lab_js.py.

- index.html keeps reading localStorage['articulate-tune'] and applying it, but
  loses the tuner section, its CSS, the DNA loading helix and the loader schema.
- lab.html is a standalone page carrying the tuner. Saving there writes the same
  localStorage key on the same origin, so the main site picks it up.

Run:  python tools/split_lab.py
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IDX = os.path.join(ROOT, "index.html")

html = io.open(IDX, "r", encoding="utf-8", newline="").read().replace("\r\n", "\n")


def cut(start_marker, end_marker, keep_end=False):
    """Remove html[start:end_marker] (or up to and including it)."""
    global html
    i = html.index(start_marker)
    j = html.index(end_marker, i) + (len(end_marker) if keep_end else 0)
    removed = html[i:j]
    html = html[:i] + html[j:]
    return removed


def sub_once(old, new):
    global html
    n = html.count(old)
    assert n == 1, "anchor count %d for %r" % (n, old[:70])
    html = html.replace(old, new)


# ── 1. pull the CSS blocks we want to reuse ────────────────────────────────
loader_css = cut("/* ── LOADER ── */", "/* ── TUNER ── */")
tuner_css = cut("/* ── TUNER ── */", "/* ── A11Y ── */")

# light-theme rules for tuner/loader/preview
for rule in [
    'html[data-theme="light"] .tuner{background:var(--bg);border-top-color:rgba(76,29,149,.2)}\n',
    'html[data-theme="light"] .tune-tab{background:#fff;border-color:rgba(76,29,149,.25);color:var(--text-cream)}\n',
    'html[data-theme="light"] .tune-tab.is-active{background:#7c3aed;border-color:#7c3aed;color:#fff}\n',
    'html[data-theme="light"] .tune-preview{background:#fff;border-color:rgba(76,29,149,.2)}\n',
    'html[data-theme="light"] .tune-field input[type=range]::-webkit-slider-runnable-track{background:rgba(76,29,149,.25)}\n',
    'html[data-theme="light"] .tune-save{background:#7c3aed}\n',
    'html[data-theme="light"] .tune-reset{background:#fff;border-color:rgba(76,29,149,.25)}\n',
    'html[data-theme="light"] .pv-card{background:#f5f3ff;border-color:rgba(76,29,149,.25)}\n',
    'html[data-theme="light"] .pv-card span{color:var(--text-cream)}\n',
    'html[data-theme="light"] .dna-bar{background-color:#cfc6f5}\n',
]:
    sub_once(rule, "")

# ── 2. replace the loading helix with a quiet scroll cue ──────────────────
sub_once(
    '    <div class="loading-screen" id="loader">\n'
    '      <div class="label-sm">keep scrolling down</div>\n'
    '      <div class="dna-helix" id="dnaHelix"></div>\n'
    '    </div>',
    '    <div class="loading-screen" id="loader">\n'
    '      <div class="label-sm">keep scrolling down</div>\n'
    '      <div class="scroll-cue" aria-hidden="true"></div>\n'
    '    </div>',
)

# ── 3. drop the public tuner section ──────────────────────────────────────
cut('<section class="tuner" id="tuner">', '<script src="https://cdn.jsdelivr.net')

# ── 4. loader out of the tune model ───────────────────────────────────────
sub_once(
    "  loader:{bars:13,barW:12,barH:110,gap:14,glowOp:.7,glowScale:1,glowSoft:72,spin:12,tilt:25},\n",
    "",
)
i = html.index("  loader:[\n")
j = html.index("  particles:[", i)
html = html[:i] + html[j:]

sub_once("function applyTune(){\n  rebuildDna();\n", "function applyTune(){\n")

# ── 5. drop the DNA loader code ───────────────────────────────────────────
cut("/* ═══ DNA LOADER (tuner-driven) ═══ */", "rebuildDna();\n")

# ── 6. drop the tuner UI block ────────────────────────────────────────────
cut("/* ═══ TUNER UI — live preview + sliders + save ═══ */", "/* ═══ TICK")

# ── 7. tick(): no helix, just fade the cue ────────────────────────────────
sub_once(
    "  var helixP=rp[0],loader=document.getElementById('loader');\n"
    "  if(dna&&helixP>0&&helixP<1)dna.apply(helixP);\n"
    "  loader.style.opacity=helixP>=.98?'0':'1';\n",
    "  var helixP=rp[0],loaderEl=document.getElementById('loader');\n"
    "  if(loaderEl)loaderEl.style.opacity=helixP>=.98?'0':'1';\n",
)

# ── 8. scroll cue styling (added where the loader css used to be) ─────────
sub_once(
    "/* ── A11Y ── */",
    "/* ── SCROLL CUE ── */\n"
    ".scroll-cue{width:26px;height:26px;border-right:2px solid var(--purple);\n"
    "  border-bottom:2px solid var(--purple);transform:rotate(45deg);\n"
    "  animation:cueBob 2.2s ease-in-out infinite}\n"
    "@keyframes cueBob{0%,100%{transform:rotate(45deg) translate(0,0);opacity:.5}\n"
    "  50%{transform:rotate(45deg) translate(6px,6px);opacity:1}}\n\n"
    "/* ── A11Y ── */",
)

io.open(IDX, "w", encoding="utf-8", newline="").write(html)
print("index.html: %d bytes, tuner section present: %s, dna present: %s"
      % (len(html), 'class="tuner"' in html, "dnaHelix" in html))

# ── 9. build the lab page ─────────────────────────────────────────────────
LAB = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self';">
<title>Articulate English — Site Lab</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--purple:#8b5cf6;--accent2:#22d3ee;--text-cream:#f4f1ea;--text-dim:rgba(244,241,234,.5);--bg:#000}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text-cream);font-family:'Inter',sans-serif;line-height:1.6;
     -webkit-font-smoothing:antialiased;min-height:100vh;padding:3.5rem 1.5rem 6rem}
.lab-head{max-width:1080px;margin:0 auto 2.5rem;display:flex;align-items:flex-end;justify-content:space-between;gap:1.5rem;flex-wrap:wrap}
.lab-head h1{font-family:'Oswald',sans-serif;font-size:clamp(1.8rem,4vw,2.6rem);text-transform:uppercase;letter-spacing:.05em}
.lab-head p{color:var(--text-dim);font-size:1rem;max-width:560px}
.lab-badge{font-family:'Oswald',sans-serif;font-size:.85rem;letter-spacing:.14em;text-transform:uppercase;
  color:#c4b5fd;border:1px solid rgba(139,92,246,.4);border-radius:999px;padding:.5rem 1rem;white-space:nowrap}
.lab-link{font-family:'Inter',sans-serif;font-size:.95rem;color:var(--accent2);text-decoration:none;
  border:1px solid rgba(34,211,238,.35);border-radius:999px;padding:.6rem 1.2rem;min-height:44px;
  display:inline-flex;align-items:center;transition:border-color .2s}
.lab-link:hover{border-color:var(--accent2)}
__TUNER_CSS__
@media(prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;transition-duration:.01ms!important}}
</style>
</head>
<body>

<div class="lab-head">
  <div>
    <h1>Site Lab</h1>
    <p>Private tuning page. Move a slider and the preview updates live; press Save to write the
       settings, then open the main site — it reads the same settings and applies them.</p>
  </div>
  <div style="display:flex;gap:.8rem;align-items:center;flex-wrap:wrap">
    <span class="lab-badge">Private — noindex</span>
    <a class="lab-link" href="index.html">Open the main site →</a>
  </div>
</div>

<section class="tuner" id="tuner">
  <div class="tuner-head">
    <h2>Tune the site</h2>
    <p>Changes are stored on this device only, and the public site never shows this panel.</p>
  </div>
  <div class="tuner-tabs" id="tuneTabs" role="group" aria-label="Element to tune">
    <button class="tune-tab is-active" data-target="particles" type="button" aria-pressed="true">Particles</button>
    <button class="tune-tab" data-target="gallery" type="button" aria-pressed="false">Gallery cards</button>
  </div>
  <div class="tuner-body">
    <div class="tune-preview" id="tunePreview" aria-label="Live preview of the selected element"></div>
    <div class="tune-controls" id="tuneControls"></div>
  </div>
  <div class="tuner-foot">
    <button class="tune-save" id="tuneSave" type="button">Save</button>
    <button class="tune-reset" id="tuneReset" type="button">Reset</button>
    <span class="tune-status" id="tuneStatus" role="status" aria-live="polite"></span>
  </div>
</section>

<script>
(function(){
'use strict';
var clamp01=function(v){return Math.max(0,Math.min(1,v));};

var TUNE_KEY='articulate-tune';
var TUNE_DEFAULTS={
  particles:{pCount:200,bCount:250,pSize:.65,bSize:.7,pOp:.9,bOp:.8,ring:7,bgRing:10,repelRadius:12,repelStrength:20,swellRadius:.22,swellStrength:2},
  gallery:{cardW:420,cardH:280,spread:370,depth:120,backZ:-130,farSpread:550,farZ:-230,farZ2:-400,reflect:150,capSize:16.8}
};
var TUNE_SCHEMA={
  particles:[
    {k:'pCount',l:'Front count',min:0,max:500,step:10,u:''},
    {k:'bCount',l:'Back count',min:0,max:500,step:10,u:''},
    {k:'pSize',l:'Sphere size (front)',min:.2,max:1.6,step:.05,u:''},
    {k:'bSize',l:'Sphere size (back)',min:.2,max:1.6,step:.05,u:''},
    {k:'pOp',l:'Front opacity',min:0,max:1,step:.01,u:''},
    {k:'bOp',l:'Back opacity',min:0,max:1,step:.01,u:''},
    {k:'ring',l:'Ring radius',min:3,max:14,step:.5,u:''},
    {k:'bgRing',l:'Back ring radius',min:3,max:18,step:.5,u:''},
    {k:'repelRadius',l:'Hover radius',min:0,max:40,step:1,u:''},
    {k:'repelStrength',l:'Hover push',min:0,max:40,step:1,u:''},
    {k:'swellRadius',l:'Swell radius',min:.05,max:.6,step:.01,u:''},
    {k:'swellStrength',l:'Swell amount',min:0,max:5,step:.1,u:'×'}
  ],
  gallery:[
    {k:'cardW',l:'Card width',min:240,max:560,step:4,u:'px'},
    {k:'cardH',l:'Card height',min:160,max:400,step:4,u:'px'},
    {k:'spread',l:'Side spread',min:120,max:700,step:10,u:'px'},
    {k:'depth',l:'Front depth',min:0,max:400,step:10,u:'px'},
    {k:'backZ',l:'Side depth',min:-400,max:0,step:10,u:'px'},
    {k:'farSpread',l:'Outer spread',min:200,max:900,step:10,u:'px'},
    {k:'farZ2',l:'Outer depth',min:-700,max:-100,step:10,u:'px'},
    {k:'reflect',l:'Reflection gap',min:0,max:300,step:10,u:'px'},
    {k:'capSize',l:'Caption size',min:12,max:26,step:.2,u:'px'}
  ]
};
var TUNE=(function(){
  var raw=null;
  try{raw=JSON.parse(localStorage.getItem(TUNE_KEY)||'null');}catch(e){}
  function field(group,key){var f=null;(TUNE_SCHEMA[group]||[]).forEach(function(x){if(x.k===key)f=x;});return f;}
  function clampVal(group,key,v){var f=field(group,key);return f?Math.min(f.max,Math.max(f.min,v)):v;}
  function merge(base,over,group){
    var o={};
    Object.keys(base).forEach(function(k){
      var bv=base[k],ov=over?over[k]:undefined;
      if(bv&&typeof bv==='object'&&!Array.isArray(bv))o[k]=merge(bv,(ov&&typeof ov==='object')?ov:{},k);
      else{var ok=(ov!==undefined&&ov!==null&&typeof ov==='number'&&isFinite(ov));o[k]=ok?clampVal(group,k,ov):bv;}
    });
    return o;
  }
  return merge(TUNE_DEFAULTS,raw||{},'');
})();

/* Writing the key is what updates the main site — index.html reads the same key. */
function applyTune(){ return true; }

var host=document.getElementById('tuner');
var tabsEl=document.getElementById('tuneTabs'),
    controlsEl=document.getElementById('tuneControls'),
    previewEl=document.getElementById('tunePreview'),
    saveEl=document.getElementById('tuneSave'),
    resetEl=document.getElementById('tuneReset'),
    statusEl=document.getElementById('tuneStatus');

var target='particles';
var draft=JSON.parse(JSON.stringify(TUNE));
var pvCanvas=null;
var LABELS={particles:'particle ring',gallery:'cover-flow cards'};

function fmt(v,f){return (f.step<1?v.toFixed(2):Math.round(v))+(f.u?' '+f.u:'');}

function renderTabs(){
  tabsEl.querySelectorAll('.tune-tab').forEach(function(b){
    var on=b.getAttribute('data-target')===target;
    b.classList.toggle('is-active',on);
    b.setAttribute('aria-pressed',on?'true':'false');
  });
}

function sizePvCards(){
  previewEl.querySelectorAll('.pv-card').forEach(function(c){
    c.style.width=(draft.gallery.cardW*.42)+'px';
    c.style.height=(draft.gallery.cardH*.42)+'px';
    var sp=c.querySelector('span');
    if(sp)sp.style.fontSize=Math.max(10,draft.gallery.capSize*.42)+'px';
  });
}

function drawPvParticles(){
  if(!pvCanvas)return;
  var ctx=pvCanvas.getContext('2d'),w=pvCanvas.width,h=pvCanvas.height,q=draft.particles;
  ctx.clearRect(0,0,w,h);
  ctx.fillStyle='#05060f';ctx.fillRect(0,0,w,h);
  var cx=w/2,cy=h/2,i,a,R;
  R=Math.min(w,h)*.42*(q.bgRing/10);
  for(i=0;i<q.bCount;i++){
    a=(i/q.bCount)*Math.PI*2;
    ctx.beginPath();
    ctx.arc(cx+Math.cos(a)*R,cy+Math.sin(a)*R*.5,Math.max(.6,q.bSize*7),0,Math.PI*2);
    ctx.fillStyle='rgba(200,75,255,'+(q.bOp*.7).toFixed(3)+')';
    ctx.fill();
  }
  R=Math.min(w,h)*.30*(q.ring/7);
  for(i=0;i<q.pCount;i++){
    a=(i/q.pCount)*Math.PI*2;
    ctx.beginPath();
    ctx.arc(cx+Math.cos(a)*R,cy+Math.sin(a)*R*.5,Math.max(.6,q.pSize*7),0,Math.PI*2);
    ctx.fillStyle='rgba(34,211,238,'+(q.pOp*.85).toFixed(3)+')';
    ctx.fill();
  }
}

function renderPreview(){
  previewEl.innerHTML='';
  pvCanvas=null;
  var lab=document.createElement('div');
  lab.className='pv-label';
  lab.textContent=LABELS[target]+' — live preview';
  previewEl.appendChild(lab);
  var stage=document.createElement('div');
  stage.setAttribute('aria-hidden','true');
  stage.style.cssText='display:flex;align-items:center;justify-content:center;width:100%;height:100%';
  previewEl.appendChild(stage);

  if(target==='particles'){
    pvCanvas=document.createElement('canvas');
    pvCanvas.className='pv-canvas';
    pvCanvas.width=Math.max(320,Math.round(previewEl.clientWidth||600));
    pvCanvas.height=340;
    stage.appendChild(pvCanvas);
    drawPvParticles();
    var note=document.createElement('div');
    note.className='pv-note';
    note.textContent='Representative view — the live ring is a 3D particle cloud.';
    stage.appendChild(note);
  }else{
    var row=document.createElement('div'); row.className='pv-cards';
    ['Product one','Product two','Product three'].forEach(function(t){
      var c=document.createElement('div'); c.className='pv-card';
      var sp=document.createElement('span'); sp.textContent=t;
      c.appendChild(sp); row.appendChild(c);
    });
    stage.appendChild(row);
    sizePvCards();
  }
}

function renderControls(){
  controlsEl.innerHTML='';
  TUNE_SCHEMA[target].forEach(function(f){
    var wrap=document.createElement('div'); wrap.className='tune-field';
    var top=document.createElement('div'); top.className='tune-field-top';
    var lab=document.createElement('label');
    lab.setAttribute('for','tf-'+target+'-'+f.k); lab.textContent=f.l;
    var out=document.createElement('output');
    out.setAttribute('for','tf-'+target+'-'+f.k);
    var v=draft[target][f.k];
    out.textContent=fmt(v,f);
    var inp=document.createElement('input');
    inp.type='range'; inp.id='tf-'+target+'-'+f.k;
    inp.min=f.min; inp.max=f.max; inp.step=f.step; inp.value=v;
    inp.addEventListener('input',function(){
      var nv=parseFloat(inp.value);
      draft[target][f.k]=nv;
      out.textContent=fmt(nv,f);
      if(target==='particles')drawPvParticles(); else sizePvCards();
    });
    top.appendChild(lab); top.appendChild(out);
    wrap.appendChild(top); wrap.appendChild(inp);
    controlsEl.appendChild(wrap);
  });
}

tabsEl.addEventListener('click',function(e){
  var b=e.target.closest('.tune-tab');
  if(!b)return;
  target=b.getAttribute('data-target');
  renderTabs(); renderPreview(); renderControls();
  statusEl.textContent='';
});

saveEl.addEventListener('click',function(){
  TUNE=JSON.parse(JSON.stringify(draft));
  var stored=false;
  try{localStorage.setItem(TUNE_KEY,JSON.stringify(TUNE));stored=true;}catch(e){}
  statusEl.textContent=stored
    ?'Saved — open the main site to see it applied.'
    :'Could not be saved (storage unavailable).';
});

resetEl.addEventListener('click',function(){
  draft=JSON.parse(JSON.stringify(TUNE_DEFAULTS));
  TUNE=JSON.parse(JSON.stringify(TUNE_DEFAULTS));
  try{localStorage.removeItem(TUNE_KEY);}catch(e){}
  renderTabs(); renderPreview(); renderControls();
  statusEl.textContent='Reset to defaults.';
});

renderTabs(); renderPreview(); renderControls();
})();
</script>
</body>
</html>
"""
LAB = LAB.replace("__TUNER_CSS__", tuner_css)
io.open(os.path.join(ROOT, "lab.html"), "w", encoding="utf-8", newline="").write(LAB)
print("lab.html: %d bytes" % len(LAB))
