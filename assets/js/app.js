(function(){
  var S=window.SITE||{};
  var AR=document.documentElement.lang!=='en';
  var ROOT=document.documentElement.getAttribute('data-root')||'';
  var T=function(ar,en){return AR?ar:en};
  var $=function(s,r){return (r||document).querySelector(s)};
  var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};

  // قائمة الجوال
  var btn=$('.menu-btn'),nav=$('.nav');
  if(btn&&nav){btn.addEventListener('click',function(){
    var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o);btn.textContent=o?'✕':'☰';
  });}

  // السنة
  $$('[data-year]').forEach(function(e){e.textContent=new Date().getFullYear()});

  // رابط واتساب
  function wa(text){return 'https://wa.me/'+S.whatsapp+'?text='+encodeURIComponent(text)}
  $$('[data-wa]').forEach(function(a){a.href=wa(a.getAttribute('data-wa')||T('السلام عليكم، أود الاستفسار','Hello, I would like to ask a question'))});

  // نسخ الأرقام
  $$('[data-copy]').forEach(function(b){
    var label=b.textContent;
    b.addEventListener('click',function(){
      var v=b.getAttribute('data-copy');
      var done=function(){b.textContent=b.getAttribute('data-done')||'OK';setTimeout(function(){b.textContent=label},1800)};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(v).then(done,function(){sel(b,v);done()})}
      else{sel(b,v);done()}
    });
  });
  function sel(b,v){
    var n=b.previousElementSibling&&b.previousElementSibling.querySelector('.num');
    if(n&&window.getSelection){var r=document.createRange();r.selectNodeContents(n);var s=window.getSelection();s.removeAllRanges();s.addRange(r)}
  }

  // مكوّن صفحة فيسبوك (مخفي افتراضيًا)
  var fb=$('#fb-frame');
  if(fb&&!S.fbPlugin){
    var wrap=fb.closest('.fbwrap');if(wrap){var sb=wrap.closest('.social-box');if(sb)sb.classList.add('single');wrap.remove()}
    fb=null;
  }
  if(fb){
    var load=function(){
      var w=Math.min(500,fb.parentNode.clientWidth-24)||340;
      fb.src='https://www.facebook.com/plugins/page.php?href='+encodeURIComponent(S.facebook)+
        '&tabs=timeline&width='+w+'&height=640&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false&locale='+(AR?'ar_AR':'en_US');
    };
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){load();io.disconnect()}},{rootMargin:'300px'});io.observe(fb);
    }else load();
  }

  // منشورات من data/posts.json
  var box=$('#posts');
  if(box&&window.fetch){
    fetch(ROOT+'data/posts.json',{cache:'no-cache'}).then(function(r){return r.ok?r.json():[]}).then(function(list){
      list.slice(0,6).forEach(function(p){
        if(p.embed){
          var w=document.createElement('div');w.className='post post-embed';
          var f=document.createElement('iframe');
          f.title=T('منشور من صفحة منظمة بناة العراق على فيسبوك','Post from the Iraq Builders Facebook page');f.loading='lazy';f.allow='encrypted-media';
          f.src='https://www.facebook.com/plugins/post.php?href='+encodeURIComponent(p.embed)+'&show_text=true&width=500&locale='+(AR?'ar_AR':'en_US');
          w.appendChild(f);box.appendChild(w);return;
        }
        var a=document.createElement('article');a.className='post';
        var img=p.image?(/^https?:/.test(p.image)?p.image:ROOT+p.image):'';
        var h='';
        if(img)h+='<img loading="lazy" alt="" src="'+encodeURI(img)+'">';
        h+='<div>';
        if(p.date)h+='<time>'+String(p.date).replace(/[<>&"]/g,'')+'</time>';
        h+='<p></p>';
        if(p.url)h+='<p><a target="_blank" rel="noopener" href="'+encodeURI(p.url)+'">'+T('عرض على فيسبوك ←','View on Facebook →')+'</a></p>';
        h+='</div>';a.innerHTML=h;
        a.querySelector('p').textContent=(AR?p.text:(p.text_en||p.text))||'';
        box.appendChild(a);
      });
    }).catch(function(){});
  }

  // أرقام القسم الطبي
  var statEls=$$('[data-stat]');
  if(statEls.length&&window.fetch){
    var url=S.statsUrl||ROOT+'data/medical-stats.json';
    var parse=function(txt){
      try{return JSON.parse(txt)}catch(e){}
      var o={};txt.split(/\r?\n/).forEach(function(l){var m=l.split(',');if(m.length>=2)o[m[0].trim()]=m.slice(1).join(',').trim()});return o;
    };
    fetch(url,{cache:'no-cache'}).then(function(r){return r.ok?r.text():Promise.reject()}).then(function(txt){
      var d=parse(txt),n=function(k){return Number(d[k])};
      if(!(n('available')>=0)||!(n('unavailable')>=0))return;
      var total=n('available')+n('unavailable');
      d.percent=total?Math.round(n('available')/total*100):0;
      statEls.forEach(function(e){
        var k=e.getAttribute('data-stat'),v=d[k];
        if(v===undefined||v==='')return;
        e.textContent=(k==='updated')?v:Number(v).toLocaleString('en-US');
      });
      $$('[data-bar]').forEach(function(b){b.style.width=d.percent+'%'});
    }).catch(function(){});
  }

  // نموذج إرسال تفاصيل التبرع (لطلب وصل)
  var df=$('#donate-form');
  if(df){
    df.addEventListener('submit',function(e){
      e.preventDefault();
      var f=df.elements;
      var msg=T('السلام عليكم، قمت بالتبرع وأرغب بوصل.','Hello, I made a donation and would like a receipt.')+
        (f.amount.value?'\n'+T('المبلغ: ','Amount: ')+f.amount.value:'')+
        '\n'+T('النشاط: ','Activity: ')+f.program.value+
        (f.name.value?'\n'+T('الاسم: ','Name: ')+f.name.value:'')+
        (f.phone.value?'\n'+T('الهاتف: ','Phone: ')+f.phone.value:'');
      location.href=wa(msg);
    });
  }

  // نموذج التطوع
  var vf=$('#volunteer-form');
  if(vf){
    vf.addEventListener('submit',function(e){
      e.preventDefault();
      var f=vf.elements;
      var msg=T('طلب تطوع جديد','New volunteer request')+'\n'+T('الاسم: ','Name: ')+f.name.value+'\n'+T('العمر: ','Age: ')+f.age.value+
        '\n'+T('المحافظة: ','Governorate: ')+f.city.value+'\n'+T('الهاتف: ','Phone: ')+f.phone.value+
        '\n'+T('مجال التطوع: ','Area: ')+f.area.value+(f.note.value?'\n'+T('ملاحظات: ','Notes: ')+f.note.value:'');
      location.href=wa(msg);
    });
  }

  // نموذج التواصل
  var cf=$('#contact-form');
  if(cf){
    cf.addEventListener('submit',function(e){
      e.preventDefault();
      var f=cf.elements;
      location.href=wa(T('رسالة من الموقع','Message from the website')+'\n'+T('الاسم: ','Name: ')+f.name.value+'\n'+T('الموضوع: ','Subject: ')+f.subject.value+'\n'+f.message.value);
    });
  }
})();
