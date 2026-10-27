(function(){
  var WA = "917617017384";
  function waLink(text){ return "https://wa.me/" + WA + "?text=" + encodeURIComponent(text); }

  // Home slideshow: advances every 3.5s, pauses on hover/focus, when hidden, or on request
  var show = document.querySelector(".show");
  if (show) {
    var slides = show.querySelectorAll(".slide"), dots = show.querySelectorAll(".dot"),
        bar = show.querySelector(".show-bar i"), pb = show.querySelector(".pause"),
        DUR = 3500, cur = 0, timer = null, hover = false, stopped = false;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) stopped = true;
    var go = function(n){
      slides[cur].classList.remove("is-on"); slides[cur].setAttribute("aria-hidden","true");
      slides[cur].querySelector("a").tabIndex = -1; dots[cur].setAttribute("aria-pressed","false");
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add("is-on"); slides[cur].setAttribute("aria-hidden","false");
      slides[cur].querySelector("a").tabIndex = 0; dots[cur].setAttribute("aria-pressed","true");
      var nx = slides[(cur + 1) % slides.length].querySelector("img"); if (nx) nx.loading = "eager";
      schedule();
    };
    var schedule = function(){
      clearTimeout(timer); bar.classList.remove("run");
      if (stopped || hover || document.hidden || slides.length < 2) return;
      void bar.offsetWidth; bar.style.setProperty("--dur", DUR + "ms"); bar.classList.add("run");
      timer = setTimeout(function(){ go(cur + 1); }, DUR);
    };
    dots.forEach(function(d){ d.addEventListener("click", function(){ go(+d.getAttribute("data-i")); }); });
    show.addEventListener("mouseenter", function(){ hover = true; schedule(); });
    show.addEventListener("mouseleave", function(){ hover = false; schedule(); });
    show.addEventListener("focusin", function(){ hover = true; schedule(); });
    show.addEventListener("focusout", function(){ hover = false; schedule(); });
    document.addEventListener("visibilitychange", schedule);
    pb.textContent = stopped ? "Play" : "Pause";
    pb.addEventListener("click", function(){ stopped = !stopped; pb.textContent = stopped ? "Play" : "Pause"; pb.setAttribute("aria-label", stopped ? "Play slideshow" : "Pause slideshow"); schedule(); });
    var x0 = null;
    show.addEventListener("touchstart", function(ev){ x0 = ev.touches[0].clientX; }, {passive:true});
    show.addEventListener("touchend", function(ev){ if (x0 === null) return; var dx = ev.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1)); x0 = null; });
    schedule();
  }

  // Mobile menu
  var mb = document.querySelector(".menu-btn"), nav = document.querySelector(".nav");
  if (mb && nav) mb.addEventListener("click", function(){
    var open = nav.classList.toggle("open");
    mb.setAttribute("aria-expanded", open ? "true" : "false");
    mb.textContent = open ? "Close" : "Menu";
  });

  // Copy buttons
  document.querySelectorAll("[data-copy]").forEach(function(b){
    b.addEventListener("click", function(){
      var t = b.getAttribute("data-copy");
      var done = function(){ var o=b.textContent; b.textContent="Copied"; setTimeout(function(){b.textContent=o;},1400); };
      try { navigator.clipboard.writeText(t).then(done, function(){}); } catch(e) {}
    });
  });

  // Collection search
  var q = document.getElementById("q");
  if (q) q.addEventListener("input", function(){
    var v = q.value.trim().toLowerCase(), any = false;
    document.querySelectorAll(".cat").forEach(function(sec){
      var shown = 0;
      sec.querySelectorAll(".card").forEach(function(c){
        var hit = !v || c.getAttribute("data-k").indexOf(v) > -1;
        c.hidden = !hit; if (hit) shown++;
      });
      sec.hidden = shown === 0; if (shown) any = true;
    });
    var e = document.getElementById("noresults"); if (e) e.hidden = any;
  });

  // Enquiry form -> WhatsApp message
  var f = document.getElementById("enquiry");
  if (f) f.addEventListener("submit", function(ev){
    ev.preventDefault();
    var g = function(id){ var el=document.getElementById(id); return el ? el.value.trim() : ""; };
    var msg = "Hello Optiluxx,\n\nName: " + g("f-name") + "\nPhone: " + g("f-phone") +
      (g("f-city") ? "\nCity: " + g("f-city") : "") + "\nProject type: " + g("f-type") +
      "\n\n" + g("f-msg");
    var a = document.getElementById("wa-out");
    a.href = waLink(msg); a.hidden = false; a.focus();
  });

  // Product page
  var root = document.getElementById("product-root");
  if (root && window.OPX) {
    var render = function(){
      var slug = (location.hash || "").replace(/^#/, "");
      var P = window.OPX.products, C = window.OPX.cats;
      var p = P.filter(function(x){ return x.slug === slug; })[0];
      if (!p) {
        root.innerHTML = '<div class="wrap" style="padding-block:80px"><p class="eyebrow">Product</p><h1 style="font-size:2.4rem;margin-top:16px">Choose a product</h1><p class="muted" style="margin-top:14px">This product link is incomplete. Browse the <a href="indoor.html">indoor</a> or <a href="outdoor.html">outdoor</a> collection.</p></div>';
        return;
      }
      var c = C.filter(function(x){ return x.slug === p.cat; })[0];
      var coll = p.side === "indoor" ? "indoor.html" : "outdoor.html";
      var collName = p.side === "indoor" ? "Indoor · Aura" : "Outdoor · Nocturne";
      document.title = p.name + " · Optiluxx";
      var esc = function(s){ return String(s).replace(/[&<>"]/g, function(m){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]; }); };
      var rows = [];
      var s = p.specs;
      if (s.watt.length) rows.push(["Wattage", s.watt.join(" · ")]);
      if (s.beam.length) rows.push(["Beam angle", s.beam.join(" · ")]);
      if (s.ip.length) rows.push(["Protection", s.ip.join(" · ")]);
      if (s.cct.length) rows.push(["Colour temp.", s.cct.join(" · ")]);
      if (s.features.length) rows.push(["Options", s.features.join(" · ")]);
      rows.push(["Catalogue", (p.side === "indoor" ? "Aura Indoor, Oct 2026" : "Nocturne Outdoor, Sept 2026")]);
      var imgs = p.img.map(function(k,i){ return '<button type="button" aria-pressed="'+(i===0)+'" data-i="'+i+'" aria-label="Catalogue page '+(i+1)+'"><img src="assets/img/p/'+k+'.webp" alt="" loading="lazy"></button>'; }).join("");
      var related = P.filter(function(x){ return x.cat === p.cat && x.slug !== p.slug; }).slice(0, 4);
      var msg = "Hello Optiluxx, I'd like details and pricing for " + p.name + " (" + (c ? c.name : "") + ").";
      root.innerHTML =
        '<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="'+coll+'">'+collName+'</a><span>/</span><a href="'+coll+'#'+p.cat+'">'+esc(c ? c.name : "")+'</a></nav>' +
        '<div class="prod"><div class="gallery"><div class="main"><img id="pmain" src="assets/img/p/'+p.img[0]+'.webp" alt="'+esc(p.name)+' catalogue page" width="909" height="1286"></div>' +
        (p.img.length > 1 ? '<div class="thumbs">'+imgs+'</div>' : '') + '</div>' +
        '<div class="pinfo"><p class="eyebrow">'+esc(c ? c.name : "")+'</p><h1>'+esc(p.name)+'</h1><hr class="kelvin">' +
        (p.desc ? '<p class="desc">'+esc(p.desc)+'</p>' : '') +
        '<dl class="specs">' + rows.map(function(r){ return '<div><dt>'+r[0]+'</dt><dd>'+esc(r[1])+'</dd></div>'; }).join("") + '</dl>' +
        '<p class="note">Cut-outs, dimensions and finishes are on the catalogue page. Most models come in multiple finishes and beam options; ask us for the exact variant for your space.</p>' +
        '<div class="enq"><a class="btn solid" href="'+waLink(msg)+'" target="_blank" rel="noopener">Enquire on WhatsApp</a><a class="btn ghost" href="contact.html">Contact us</a></div></div></div>' +
        (related.length ? '<section class="section" style="padding-top:48px"><div class="cat-head"><div><p class="eyebrow">More in this family</p><h2 style="margin-top:12px">'+esc(c.name)+'</h2></div><a class="btn ghost" href="'+coll+'#'+p.cat+'">View all</a></div><div class="grid">' +
          related.map(function(r){ return '<a class="card" href="product.html#'+r.slug+'"><div class="im"><img src="assets/img/p/'+r.img[0]+'.webp" alt="" loading="lazy"></div><div class="tx"><b>'+esc(r.name)+'</b><span>'+esc(r.specs.watt.length ? r.specs.watt[0] + (r.specs.watt.length>1 ? " – " + r.specs.watt[r.specs.watt.length-1] : "") : "")+'</span></div></a>'; }).join("") +
          '</div></section>' : '') + '</div>';
      root.querySelectorAll(".thumbs button").forEach(function(b){
        b.addEventListener("click", function(){
          document.getElementById("pmain").src = "assets/img/p/" + p.img[+b.getAttribute("data-i")] + ".webp";
          root.querySelectorAll(".thumbs button").forEach(function(o){ o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
        });
      });
      window.scrollTo(0, 0);
    };
    render();
    window.addEventListener("hashchange", render);
  }
})();
