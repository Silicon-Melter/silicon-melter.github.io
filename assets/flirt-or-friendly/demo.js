(function(){
  var M=window.FF_MODEL, root=document.getElementById('ff'); if(!M||!root) return;
  var clean=makeCleaner(M), $=function(s){return root.querySelector(s)};
  var N=M.docs[0]+M.docs[1], LP=[Math.log(M.docs[0]/N),Math.log(M.docs[1]/N)];
  function p(w,c){var n=M.counts[w]?M.counts[w][c]:0;return (n+1)/(M.total[c]+M.V)}
  function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function run(){
    var r=clean($('#ff-in').value), tk=r.tokens, s=[LP[0],LP[1]], known=[];
    tk.forEach(function(w){ if(M.counts.hasOwnProperty(w)){ s[0]+=Math.log(p(w,0)); s[1]+=Math.log(p(w,1)); known.push(w) } });
    var pf=1/(1+Math.exp(s[0]-s[1]));
    $('.ff-needle').style.left=(4+92*pf)+'%';
    $('.ff-pct').textContent=tk.length?(pf>=.5?'flirty ':'friendly ')+(100*Math.max(pf,1-pf)).toFixed(pf>.995||pf<.005?1:0)+'%':'';
    $('.ff-score').innerHTML='Log score: flirty <b>'+s[1].toFixed(2)+'</b> vs friendly <b>'+s[0].toFixed(2)+'</b> (prior '+LP[1].toFixed(3)+' vs '+LP[0].toFixed(3)+' plus each word\'s log likelihood). The higher one wins.';
    $('.ff-toks').innerHTML=tk.map(function(w){return '<code>'+esc(w)+'</code>'}).join(' ')||'<em>nothing yet</em>';
    $('.ff-steps').innerHTML=r.steps.map(function(x){return '<li><span class="k">'+x[0]+'</span><code>'+esc(x[1]||' ')+'</code></li>'}).join('');
    var mx=0; known.forEach(function(w){mx=Math.max(mx,p(w,0),p(w,1))});
    var box=$('.ff-bars'); box.innerHTML='';
    tk.forEach(function(w,i){
      var d=document.createElement('div'); d.style.animationDelay=(i*70)+'ms';
      if(!M.counts.hasOwnProperty(w)){ d.className='ff-row skip'; d.innerHTML='<div class="ff-w">'+esc(w)+'</div><div class="ff-pair">never seen in training, so it is skipped</div>'; box.appendChild(d); return }
      var a=p(w,1),b=p(w,0),ratio=a/b, c=M.counts[w];
      d.className='ff-row';
      d.innerHTML='<div class="ff-w">'+esc(w)+'</div><div class="ff-pair" title="seen '+c[1]+'&times; in flirty and '+c[0]+'&times; in friendly training messages">'+
        '<div class="ff-b fl"><i data-w="'+(100*a/mx*0.82)+'"></i><span>'+(1000*a).toFixed(1)+'</span></div>'+
        '<div class="ff-b fr"><i data-w="'+(100*b/mx*0.82)+'"></i><span>'+(1000*b).toFixed(1)+'</span></div></div>'+
        '<div class="ff-push '+(ratio>=1?'fl':'fr')+'">&times;'+(ratio>=1?ratio:1/ratio).toFixed(ratio>9.95||1/ratio>9.95?0:1)+'<br>'+(ratio>=1?'more flirty':'more friendly')+'</div>';
      box.appendChild(d);
      setTimeout(function(){d.querySelectorAll('i').forEach(function(x){x.style.width=x.dataset.w+'%'})},60+i*70);
    });
  }
  var t=null; $('#ff-in').addEventListener('input',function(){clearTimeout(t);t=setTimeout(run,220)});
  root.querySelectorAll('.ff-ex button').forEach(function(b){b.onclick=function(){$('#ff-in').value=b.textContent;run()}});
  run();
})();
