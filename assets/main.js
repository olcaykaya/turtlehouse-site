(function(){
  var d=document,root=d.documentElement,RM=matchMedia('(prefers-reduced-motion: reduce)').matches,FINE=matchMedia('(pointer: fine)').matches;
  var hasG=window.gsap&&window.ScrollTrigger;
  if(!hasG){root.classList.remove('js');return}
  gsap.registerPlugin(ScrollTrigger);
  var EASE='expo.out';

  /* smooth scroll (Lenis) */
  if(window.Lenis&&!RM){var lenis=window.lenis=new Lenis({lerp:.09});lenis.on('scroll',ScrollTrigger.update);gsap.ticker.add(function(t){lenis.raf(t*1000)});gsap.ticker.lagSmoothing(0)}

  /* nav hide/show */
  var nav=d.querySelector('.nav'),lastY=0;
  addEventListener('scroll',function(){var y=scrollY;nav.classList.toggle('scrolled',y>40);nav.classList.toggle('hide',y>lastY&&y>400&&!d.body.classList.contains('menu-open'));lastY=y},{passive:true});
  var bg=d.querySelector('.burger');if(bg)bg.addEventListener('click',function(){var o=d.body.classList.toggle('menu-open');d.querySelector('.menu').classList.toggle('open',o);bg.setAttribute('aria-expanded',o)});

  /* hero: film title card — lines in sequence */
  var D=.15,intro=d.querySelector('.intro');
  if(intro){if(RM){intro.remove()}else{D=1.75;var n=intro.querySelector('.intro-n'),o={v:0};
    gsap.to(o,{v:100,duration:1.2,ease:'power2.inOut',onUpdate:function(){n.textContent=(o.v<10?'0':'')+Math.round(o.v)}});
    gsap.from(intro.querySelector('.intro-t'),{yPercent:120,duration:.9,ease:EASE});
    gsap.to(intro,{clipPath:'inset(0% 0% 100% 0%)',duration:1.1,ease:'expo.inOut',delay:1.3,onComplete:function(){intro.remove()}})}}
  var lines=d.querySelectorAll('.hero2 h1 .ln>span, .page-hero h1 .ln>span');
  if(lines.length&&!RM){gsap.from(lines,{yPercent:110,duration:1.3,stagger:.09,ease:EASE,delay:D});
    gsap.from('.hero2-eyebrow, .hero2-row .lead, .hero2-row .cta-row, .hero2 .chip, .page-hero .lead, .page-hero .cta-row, .crumbs',{y:24,opacity:0,duration:1.1,stagger:.08,ease:EASE,delay:D+.4});
    }

  /* viewfinder timecode */
  var tc=d.querySelector('[data-tc]');
  if(tc){var t0=performance.now();(function tick(){var s=(performance.now()-t0)/1000,f=Math.floor((s%1)*24),p=function(n){return(n<10?'0':'')+n};tc.textContent='00:'+p(Math.floor(s/60)%60)+':'+p(Math.floor(s)%60)+':'+p(f);requestAnimationFrame(tick)})()}

  /* depth: pointer tilt + glow on viewfinder (desktop only) */
  var vf=d.querySelector('.vf');
  if(vf&&FINE&&!RM){var st=vf.parentElement;st.addEventListener('pointermove',function(e){var r=st.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;vf.style.setProperty('--rx',(x*10)+'deg');vf.style.setProperty('--ry',(-y*8)+'deg');vf.style.setProperty('--gx',((x+.5)*100)+'%');vf.style.setProperty('--gy',((y+.5)*100)+'%')});
    st.addEventListener('pointerleave',function(){vf.style.setProperty('--rx','0deg');vf.style.setProperty('--ry','0deg')})}

  /* statement: words light up with scroll */
  d.querySelectorAll('.statement p').forEach(function(p){
    p.innerHTML=p.innerHTML.split(/(\s+|<em>.*?<\/em>)/).map(function(w){return /^\s*$/.test(w)?w:'<span class="w">'+w+'</span>'}).join('');
    if(RM)return;gsap.to(p.querySelectorAll('.w'),{opacity:1,stagger:.1,ease:'none',scrollTrigger:{trigger:p,start:'top 80%',end:'bottom 45%',scrub:true}})});

  /* expanding film window */
  var ff=d.querySelector('.film-frame');
  if(ff&&!RM){var tl=gsap.timeline({scrollTrigger:{trigger:'.film',start:'top top',end:'bottom bottom',scrub:true}});
    var C0=innerWidth<=980?'inset(10% 6% 10% 6% round 18px)':'inset(18% 22% 18% 22% round 10px)';tl.fromTo(ff,{clipPath:C0},{clipPath:'inset(0% 0% 0% 0% round 0px)',ease:'none'},0).fromTo(ff.querySelector('video'),{scale:1.15},{scale:1,ease:'none'},0)}

  /* reveals */
  gsap.utils.toArray('.rv').forEach(function(el){gsap.to(el,{opacity:1,y:0,duration:1.2,ease:EASE,scrollTrigger:{trigger:el,start:'top 88%'}})});

  /* parallax image layers */
  if(!RM)gsap.utils.toArray('[data-par]').forEach(function(el){gsap.fromTo(el,{yPercent:-8},{yPercent:8,ease:'none',scrollTrigger:{trigger:el.parentElement,start:'top bottom',end:'bottom top',scrub:true}})});

  /* horizontal reel (desktop) */
  var tr=d.querySelector('.reel-track');
  if(tr&&innerWidth>980&&!RM){gsap.to(tr,{x:function(){return-(tr.scrollWidth-innerWidth)},ease:'none',scrollTrigger:{trigger:'.reel',start:'top top',end:function(){return'+='+(tr.scrollWidth-innerWidth)},pin:true,scrub:1,invalidateOnRefresh:true}})}

  /* service peek follows cursor */
  var pk=d.querySelector('.peek');
  if(pk&&FINE){var img=pk.querySelector('img'),xTo=gsap.quickTo(pk,'x',{duration:.6,ease:'power3'}),yTo=gsap.quickTo(pk,'y',{duration:.6,ease:'power3'});
    d.querySelectorAll('.svc-list a').forEach(function(a){a.addEventListener('mouseenter',function(){img.src=a.dataset.img;pk.classList.add('on')});a.addEventListener('mouseleave',function(){pk.classList.remove('on')})});
    addEventListener('pointermove',function(e){xTo(e.clientX+40);yTo(e.clientY)})}

  /* cursor */
  var cu=d.querySelector('.cursor');
  if(cu&&FINE&&!RM){var cx=gsap.quickTo(cu,'x',{duration:.25}),cy=gsap.quickTo(cu,'y',{duration:.25});addEventListener('pointermove',function(e){cu.style.opacity=1;cx(e.clientX);cy(e.clientY)});
    d.querySelectorAll('a,button,summary').forEach(function(a){a.addEventListener('mouseenter',function(){cu.classList.add('big')});a.addEventListener('mouseleave',function(){cu.classList.remove('big')})})}

  /* work filter */
  d.querySelectorAll('.filter button').forEach(function(b){b.addEventListener('click',function(){d.querySelectorAll('.filter button').forEach(function(x){x.classList.toggle('on',x===b)});var c=b.dataset.f;d.querySelectorAll('.masonry figure').forEach(function(f){f.style.display=(c==='all'||f.dataset.c===c)?'':'none'});ScrollTrigger.refresh()})});

  /* rack focus: frames pull into focus as they enter */
  if(!RM)gsap.utils.toArray('main img, main video').forEach(function(m){if(m.closest('.vf'))return;gsap.fromTo(m,{'--fb':'10px'},{'--fb':'0px',duration:1.4,ease:'power2.out',scrollTrigger:{trigger:m,start:'top 92%'}})});

  /* lens cursor over media */
  if(cu&&FINE&&!RM)d.querySelectorAll('[data-group]>*, .strip .m').forEach(function(m){m.addEventListener('mouseenter',function(){cu.classList.add('lens')});m.addEventListener('mouseleave',function(){cu.classList.remove('lens')})});

  /* reels: play only what's visible; on mobile the centered phone is active */
  var ph=d.querySelectorAll('.phone');
  if(ph.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target.querySelector('video');if(e.isIntersecting&&e.intersectionRatio>.55){if(!v.src)v.src=v.dataset.src;v.play().catch(function(){});e.target.classList.add('act')}else{v.pause();e.target.classList.remove('act')}})},{threshold:[0,.55,.9]});ph.forEach(function(p){io.observe(p)});
}

  /* photo stack: earlier cards sink back as the next one lands */
  if(!RM)gsap.utils.toArray('.card').forEach(function(c,i,a){if(i===a.length-1)return;gsap.to(c,{scale:.9,opacity:.5,ease:'none',scrollTrigger:{trigger:a[i+1],start:'top bottom',end:'top '+(96+(i+1)*18)+'px',scrub:true}})});

  /* mobile quick-contact bar appears after the hero */
  var mb=d.querySelector('.mbar');if(mb){var hz=d.querySelector('.hero2,.page-hero');addEventListener('scroll',function(){mb.classList.toggle('on',scrollY>(hz?hz.offsetHeight*.6:300)&&!d.body.classList.contains('menu-open'))},{passive:true})}

  /* reels carousel: drag + arrows */
  var rail=d.querySelector('.phones');
  if(rail){var down=false,sx=0,sl=0,moved=0;
    rail.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;down=true;moved=0;sx=e.clientX;sl=rail.scrollLeft;rail.classList.add('drag')});
    addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-sx;moved=Math.max(moved,Math.abs(dx));rail.scrollLeft=sl-dx});
    addEventListener('pointerup',function(){if(!down)return;down=false;rail.classList.remove('drag')});
    rail.addEventListener('click',function(e){if(moved>6){e.stopPropagation();e.preventDefault();moved=0}},true);
    d.querySelectorAll('.rbtn').forEach(function(b){b.addEventListener('click',function(){var w=rail.querySelector('.phone').offsetWidth+22;rail.scrollBy({left:w*2*b.dataset.dir,behavior:'smooth'})})})}

  /* lightbox with a camera shutter */
  var lb=d.querySelector('.lb'),stage=lb&&lb.querySelector('.lb-stage'),cap=lb&&lb.querySelector('.lb-cap'),items=[],idx=0;
  function srcOf(el){var v=el.querySelector('video');if(v)return{t:'v',s:v.dataset.src||v.currentSrc||v.src,p:v.poster};var im=el.querySelector('img')||(el.tagName==='IMG'?el:null);return im?{t:'i',s:im.currentSrc||im.src,a:im.alt}:null}
  function shutter(fn){var sh=d.querySelectorAll('.shutter i');if(RM){fn();return}gsap.timeline().to(sh,{scaleY:1,duration:.16,ease:'power2.in'}).add(fn).to(sh,{scaleY:0,duration:.32,ease:'power3.out'},'+=.05')}
  function show(i){idx=(i+items.length)%items.length;var m=srcOf(items[idx]);if(!m)return;stage.innerHTML=m.t==='v'?'<video src="'+m.s+'" poster="'+(m.p||'')+'" autoplay loop muted playsinline controls></video>':'<img src="'+m.s+'" alt="">';cap.textContent=(idx+1)+' / '+items.length}
  function openLb(list,i){items=list;shutter(function(){show(i);lb.hidden=false;if(window.lenis)window.lenis.stop()})}
  function closeLb(){shutter(function(){lb.hidden=true;stage.innerHTML='';if(window.lenis)window.lenis.start()})}
  if(lb){d.querySelectorAll('[data-group]').forEach(function(g){var list=[].slice.call(g.children);list.forEach(function(el,i){el.addEventListener('click',function(){openLb(list.filter(function(x){return x.offsetParent!==null}),list.filter(function(x){return x.offsetParent!==null}).indexOf(el))})})});
    d.querySelectorAll('.strip').forEach(function(g){var list=[].slice.call(g.children);list.forEach(function(el,i){el.addEventListener('click',function(){openLb(list,i)})})});
    lb.querySelector('.lb-x').onclick=closeLb;lb.querySelector('.lb-p').onclick=function(){show(idx-1)};lb.querySelector('.lb-n').onclick=function(){show(idx+1)};
    lb.addEventListener('click',function(e){if(e.target===lb)closeLb()});
    addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')closeLb();if(e.key==='ArrowRight')show(idx+1);if(e.key==='ArrowLeft')show(idx-1)});
    var tx=0;lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});lb.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)show(idx+(dx<0?1:-1))})}

  addEventListener('load',function(){ScrollTrigger.refresh()});

  /* HERO LENS — the video is drawn through a live WebGL lens that follows you */
  (function(){
    var hero=d.querySelector('.hero2');if(!hero)return;
    var vid=hero.querySelector('.hero-src'),cv=hero.querySelector('.lens-gl'),MOB=innerWidth<=980;
    vid.src=MOB?vid.dataset.m:vid.dataset.d;vid.play().catch(function(){});
    var gl=cv.getContext('webgl',{antialias:false,premultipliedAlpha:false});if(!gl||RM)return;
    var VS='attribute vec2 p;varying vec2 uv;void main(){uv=p*.5+.5;gl_Position=vec4(p,0.,1.);}';
    var FS='precision mediump float;varying vec2 uv;uniform sampler2D t;uniform vec2 res,tres,m;uniform float r,k,zoom,time;'+
    'vec2 cover(vec2 u){float ra=res.x/res.y,rt=tres.x/tres.y;vec2 s=ra>rt?vec2(1.,rt/ra):vec2(ra/rt,1.);return (u-.5)*s/zoom+.5;}'+
    'void main(){vec2 c=uv-.5;float e=dot(c,c);vec2 u=.5+c*(1.-.10*e);'+   /* subtle barrel of a wide lens */
    'vec2 px=u*res;vec2 dv=(px-m)/r;float l=length(dv);float inside=1.-smoothstep(.85,1.,l);'+
    'float f=1.-k*.45*(1.-l*l)*inside;vec2 q=(m+(px-m)*f)/res;'+               /* magnifying bulge */
    'vec2 off=(q-m/res)*(.012*k*inside+.004*e*4.);'+                          /* chromatic fringe */
    'float R=texture2D(t,cover(q+off)).r,G=texture2D(t,cover(q)).g,B=texture2D(t,cover(q-off)).b;vec3 col=vec3(R,G,B);'+
    'col*=1.-e*.9;col+=smoothstep(.03,0.,abs(l-1.))*.18;col*=mix(1.,1.08,inside);'+
    'float n=fract(sin(dot(uv*res+time,vec2(12.9898,78.233)))*43758.5453);col+=(n-.5)*.035;gl_FragColor=vec4(col,1.);}';
    function sh(type,src){var o=gl.createShader(type);gl.shaderSource(o,src);gl.compileShader(o);if(!gl.getShaderParameter(o,gl.COMPILE_STATUS)){console.warn(gl.getShaderInfoLog(o));return null}return o}
    var pr=gl.createProgram(),a=sh(gl.VERTEX_SHADER,VS),b=sh(gl.FRAGMENT_SHADER,FS);if(!a||!b)return;
    gl.attachShader(pr,a);gl.attachShader(pr,b);gl.linkProgram(pr);gl.useProgram(pr);
    var buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
    var loc=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
    var tex=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,tex);gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,true);
    [gl.TEXTURE_WRAP_S,gl.TEXTURE_WRAP_T].forEach(function(w){gl.texParameteri(gl.TEXTURE_2D,w,gl.CLAMP_TO_EDGE)});gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);
    var U={};['res','tres','m','r','k','zoom','time'].forEach(function(n){U[n]=gl.getUniformLocation(pr,n)});
    var DPR=Math.min(devicePixelRatio||1,MOB?1.5:1.75),W,H,st={x:.5,y:.45,k:.9,zoom:1,r:MOB?.3:.2},tg={x:.5,y:.45},auto=true,lastMove=0,vis=true,ready=false;
    function size(){W=cv.width=Math.round(hero.clientWidth*DPR);H=cv.height=Math.round(hero.clientHeight*DPR);gl.viewport(0,0,W,H)}size();addEventListener('resize',size);
    function aim(x,y){var r=hero.getBoundingClientRect();tg.x=(x-r.left)/r.width;tg.y=(y-r.top)/r.height;auto=false;lastMove=performance.now()}
    hero.addEventListener('pointermove',function(e){aim(e.clientX,e.clientY)});
    hero.addEventListener('touchmove',function(e){aim(e.touches[0].clientX,e.touches[0].clientY)},{passive:true});
    hero.addEventListener('pointerleave',function(){auto=true});
    hero.addEventListener('click',function(e){if(e.target.closest('a,button'))return;gsap.fromTo(st,{k:2.6,zoom:1.12},{k:.9,zoom:1,duration:1.4,ease:'elastic.out(1,.45)'});var h=hero.querySelector('.hint');if(h)h.style.opacity=0});
    if(cu&&FINE){hero.addEventListener('mouseenter',function(){cu.classList.add('hl')});hero.addEventListener('mouseleave',function(){cu.classList.remove('hl')});
      hero.addEventListener('pointermove',function(e){cu.style.setProperty('--rot',(e.clientX/innerWidth*180)+'deg')})}
    ScrollTrigger.create({trigger:hero,start:'top top',end:'bottom top',onUpdate:function(s){st.zoom=1+s.progress*.25;st.k=.9+s.progress*1.6},onToggle:function(s){vis=s.isActive||scrollY<hero.offsetHeight}});
    var dead=false;
    function loop(t){requestAnimationFrame(loop);if(dead||!vis||vid.readyState<2)return;
      if(auto||performance.now()-lastMove>4000){var s=t/1000;tg.x=.5+Math.sin(s*.35)*.28;tg.y=.48+Math.sin(s*.7)*.14}
      st.x+=(tg.x-st.x)*.08;st.y+=(tg.y-st.y)*.08;
      try{gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,vid)}catch(err){dead=true;d.documentElement.classList.remove('gl-on');return}
      gl.uniform2f(U.res,W,H);gl.uniform2f(U.tres,vid.videoWidth,vid.videoHeight);gl.uniform2f(U.m,st.x*W,(1-st.y)*H);
      gl.uniform1f(U.r,(MOB?hero.clientWidth*.4:150)*DPR);gl.uniform1f(U.k,st.k);gl.uniform1f(U.zoom,st.zoom);gl.uniform1f(U.time,t*.001%10);
      gl.drawArrays(gl.TRIANGLE_STRIP,0,4);if(!ready){ready=true;d.documentElement.classList.add('gl-on')}}
    requestAnimationFrame(loop);
  })();
})();
