// Port of the repo's CleanText pipeline (main.py apply_clean), for the browser.
function makeCleaner(M){
  var PUNC="!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
  var EMO=[[";)","_wink"],[";-)","_wink"],["😉","_wink"],[":)","_smile"],[":-)","_smile"],["😊","_smile"],[":p","_tongue"],[":d","_laugh"],["😂","_laugh"],["<3","_heart"],["❤","_heart"],["😍","_heart"],["🥰","_heart"],[":*","_kiss"],["😘","_kiss"],["😏","_smirk"]];
  var LEFT=Object.keys(M.leftovers).filter(function(k){return /^['’]/.test(k)}).sort(function(a,b){return b.length-a.length});
  function fixToken(t){ return fixRaw(t).toLowerCase(); }
  function fixRaw(t){
    var k=t.toLowerCase();
    if(M.contractions.hasOwnProperty(k)) return M.contractions[k];
    if(M.leftovers.hasOwnProperty(k)) return M.leftovers[k];
    if(M.slangc.hasOwnProperty(k)) return M.slangc[k];
    for(var i=0;i<LEFT.length;i++){var s=LEFT[i]; if(k.length>s.length&&k.endsWith(s)) return t.slice(0,t.length-s.length)+M.leftovers[s];}
    return t;
  }
  function lemma(w){
    if(M.lemma.hasOwnProperty(w)) return M.lemma[w];
    if(M.counts.hasOwnProperty(w)||w.indexOf("NOT_")===0) return w;
    var rules=[["ed","e"],["ed",""],["ing","e"],["ing",""]];
    for(var i=0;i<rules.length;i++){var r=rules[i]; if(w.length>r[0].length+1&&w.endsWith(r[0])){var c=w.slice(0,-r[0].length)+r[1]; if(M.counts.hasOwnProperty(c)) return c;}}
    return w;
  }
  return function(text){
    var steps=[]; var t=text.toLowerCase(); steps.push(["lower case",t]);
    t=t.replace(/[A-Za-z0-9_'’]+/g,fixToken); steps.push(["expand contractions",t]);
    EMO.forEach(function(e){t=t.split(e[0]).join(" "+e[1]+" ")}); steps.push(["flag emoticons",t]);
    t=Array.from(t).filter(function(ch){return PUNC.indexOf(ch)<0}).join(""); steps.push(["remove punctuation",t]);
    var w=t.split(/\s+/).filter(Boolean),o=[];
    for(var i=0;i<w.length;i++){ if((w[i]==="not"||w[i]==="no"||w[i]==="never")&&i+1<w.length){o.push("NOT_"+w[i+1]);i++} else o.push(w[i]) }
    steps.push(["join negations",o.join(" ")]);
    o=o.map(function(x){return /(.)\1{2,}/u.test(x)? x.replace(/(.)\1{2,}/gu,"$1")+" _elongated":x}).join(" ").split(/\s+/).filter(Boolean);
    steps.push(["flag stretched words",o.join(" ")]);
    o=o.map(function(x){return M.slang.hasOwnProperty(x)?M.slang[x]+" _slang":x}).join(" ").split(/\s+/).filter(Boolean);
    steps.push(["translate slang",o.join(" ")]);
    o=o.map(function(x){return x.charAt(0)==="_"?x:lemma(x)});
    steps.push(["lemmatise",o.join(" ")]);
    return {tokens:o,steps:steps};
  };
}
