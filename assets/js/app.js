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
  function bindCopy(scope){
    $$('[data-copy]',scope).forEach(function(b){
      if(b._bound)return;b._bound=true;
      var label=b.textContent;
      b.addEventListener('click',function(){
        var v=b.getAttribute('data-copy');
        var done=function(){b.textContent=b.getAttribute('data-done')||'OK';setTimeout(function(){b.textContent=label},1800)};
        if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(v).then(done,function(){sel(b,v);done()})}
        else{sel(b,v);done()}
      });
    });
  }
  function sel(b,v){
    var n=b.previousElementSibling&&b.previousElementSibling.querySelector('.num');
    if(n&&window.getSelection){var r=document.createRange();r.selectNodeContents(n);var s=window.getSelection();s.removeAllRanges();s.addRange(r)}
  }
  bindCopy(document);

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

  // ===== المحتوى من لوحة ووردبريس (أخبار، أنشطة، معلومات التبرع) =====
  var CMS=(S.cmsUrl||'').replace(/\/+$/,'');
  if(CMS&&window.fetch){
    var LNG=AR?'ar':'en',OTH=AR?'en':'ar';
    var pick=function(o){return o?(o[LNG]||o[OTH]||''):''};
    var api=function(p){return fetch(CMS+p,{headers:{Accept:'application/json'}}).then(function(r){if(!r.ok)throw new Error(r.status);return r.json()})};
    var mk=function(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e};
    var okUrl=function(u){return /^https?:\/\//i.test(u||'')?u:''};
    var fmtDate=function(d){try{return new Date(d).toLocaleDateString(AR?'ar-IQ':'en-GB',{year:'numeric',month:'long',day:'numeric'})}catch(e){return ''}};
    var LOCAL={renovation:'hero-team.webp',food:'food.webp',education:'school-bags.webp',appliances:'appliances.webp'};
    var PATHS={cross:'M9 3h6v6h6v6h-6v6H9v-6H3V9h6z',shirt:'M8 3l-5 3 2 4 3-1v12h8V9l3 1 2-4-5-3a4 4 0 0 1-8 0z',tools:'M14.7 6.3a4 4 0 0 0-5 5L3 18l3 3 6.7-6.7a4 4 0 0 0 5-5l-2.5 2.5-2.2-.5-.5-2.2z',moon:'M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z',heart:'M12 21s-8-5.3-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.7-8 11-8 11z',gift:'M3 9h18v4H3zM5 13h14v8H5zM11 9h2v12h-2z'};
    var svgIcon=function(name){
      var ns='http://www.w3.org/2000/svg',sv=document.createElementNS(ns,'svg');
      sv.setAttribute('viewBox','0 0 24 24');sv.setAttribute('fill','currentColor');sv.setAttribute('aria-hidden','true');
      var pa=document.createElementNS(ns,'path');pa.setAttribute('d',PATHS[name]||PATHS.heart);sv.appendChild(pa);return sv;
    };
    var excerpt=function(t,n){t=(t||'').replace(/\s+/g,' ').trim();return t.length>n?t.slice(0,n).replace(/\s+\S*$/,'')+'…':t};
    var imgEl=function(src,alt){var i=document.createElement('img');i.loading='lazy';i.alt=alt||'';i.src=src;return i};
    var btnStyle='align-self:flex-start;min-height:40px;padding:4px 16px;font-size:15px';

    var newsCard=function(it){
      var a=mk('article','card'),title=pick(it.title);
      var u=it.image&&okUrl(it.image.url);
      if(u){var im=mk('div','im');im.appendChild(imgEl(u,(it.image&&it.image.alt)||title));a.appendChild(im)}
      var tx=mk('div','tx');
      tx.appendChild(mk('time','meta',fmtDate(it.date)));
      tx.appendChild(mk('h3','',title));
      var ex=excerpt(pick(it.text),150);if(ex)tx.appendChild(mk('p','',ex));
      var more=mk('a','btn btn-line-d',T('اقرأ المزيد','Read more'));
      more.href='news-item.html?id='+encodeURIComponent(it.id);more.style.cssText=btnStyle;
      tx.appendChild(more);a.appendChild(tx);return a;
    };
    var actCard=function(it,idx,link){
      var a=mk('article','card'),title=pick(it.title);if(it.slug&&!link)a.id=it.slug;
      var src=(it.image&&okUrl(it.image.url))||(LOCAL[it.slug]?ROOT+'assets/img/'+LOCAL[it.slug]:'');
      if(src){var im=mk('div','im');im.appendChild(imgEl(src,(it.image&&it.image.alt)||title));a.appendChild(im)}
      else{var ic=mk('div','ico'+(idx%3===1?' tint2':idx%3===2?' tint3':''));ic.appendChild(svgIcon(it.icon));a.appendChild(ic)}
      var tx=mk('div','tx');tx.appendChild(mk('h3','',title));
      var tt=pick(it.text);if(tt)tx.appendChild(mk('p','',excerpt(tt,220)));
      var b=mk('a','btn btn-line-d',link?T('التفاصيل','Details'):T('ادعم هذا النشاط','Support this activity'));
      b.href=link?'activities.html#'+encodeURIComponent(it.slug):'donate.html';b.style.cssText=btnStyle;
      tx.appendChild(b);a.appendChild(tx);return a;
    };

    // الرئيسية: آخر الأخبار
    var hn=$('#cms-news-home');
    if(hn)api('/news?per_page=3').then(function(d){
      if(!d.items||!d.items.length)return;
      d.items.forEach(function(it){hn.appendChild(newsCard(it))});
      $('#home-news-sec').hidden=false;
    }).catch(function(){});

    // صفحة الأخبار
    var nl=$('#cms-news');
    if(nl){
      var page=1,loadNews=function(){
        api('/news?per_page=9&page='+page).then(function(d){
          if(!d.items||!d.items.length)return;
          d.items.forEach(function(it){nl.appendChild(newsCard(it))});
          $('#cms-news-sec').hidden=false;
          var old=$('#news-more');if(old)old.parentNode.removeChild(old);
          if(page<d.pages){
            var btn=mk('button','btn btn-line-d',T('عرض المزيد','Load more'));btn.id='news-more';btn.type='button';btn.style.marginTop='24px';
            btn.addEventListener('click',function(){page++;loadNews()});
            nl.parentNode.appendChild(btn);
          }
        }).catch(function(){});
      };
      loadNews();
    }

    // صفحة خبر واحد
    var ni=$('#news-item');
    if(ni){
      var id=new URLSearchParams(location.search).get('id');
      var fail=function(){ni.textContent='';ni.appendChild(mk('p','',T('تعذّر تحميل الخبر.','Could not load this news item.')))};
      if(!/^\d+$/.test(id||''))fail();
      else api('/news/'+id).then(function(it){
        var title=pick(it.title);ni.textContent='';
        ni.appendChild(mk('h1','',title));
        ni.appendChild(mk('time','meta',fmtDate(it.date)));
        var u=it.image&&okUrl(it.image.url);
        if(u){var f=mk('div','band');f.appendChild(imgEl(u,(it.image&&it.image.alt)||title));ni.appendChild(f)}
        (pick(it.text)||'').split(/\n\s*\n/).forEach(function(par){if(par.trim()){var p=mk('p','',par.trim());p.style.whiteSpace='pre-line';ni.appendChild(p)}});
        var lk=okUrl(it.link);
        if(lk){var l=mk('a','btn btn-green',T('عرض المنشور الأصلي','View original post'));l.href=lk;l.target='_blank';l.rel='noopener';l.style.marginTop='18px';ni.appendChild(l)}
        var back=mk('p');back.style.marginTop='24px';var bl=mk('a','',(ni.getAttribute('data-back')||'')+' '+T('←','→'));bl.href='news.html';back.appendChild(bl);ni.appendChild(back);
        document.title=title+' | '+T('منظمة بناة العراق','Iraq Builders');
      }).catch(fail);
    }

    // الأنشطة
    var al=$('#cms-activities');
    if(al)api('/activities').then(function(d){
      if(!d.items||!d.items.length)return;
      d.items.forEach(function(it,i){al.appendChild(actCard(it,i,false))});
      $('#cms-activities-sec').hidden=false;
      $$('[data-fallback]').forEach(function(e){e.parentNode.removeChild(e)});
      if(location.hash){var t=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(t)t.scrollIntoView()}
    }).catch(function(){});
    var ha=$('#home-activities');
    if(ha)api('/activities').then(function(d){
      var list=(d.items||[]).filter(function(x){return x.featured});
      if(!list.length)list=(d.items||[]).slice(0,4);
      list=list.slice(0,4);if(!list.length)return;
      ha.textContent='';list.forEach(function(it,i){ha.appendChild(actCard(it,i,true))});
    }).catch(function(){});

    // معلومات التبرع
    var pm=$('#pay-methods');
    if(pm)api('/donation').then(function(d){
      if(!d.methods||!d.methods.length)return;
      pm.textContent='';
      d.methods.forEach(function(m){
        var row=mk('div','payrow'),box=mk('div');
        box.appendChild(mk('b','',pick(m.label)));
        var n=mk('span','num',m.number);n.setAttribute('dir','ltr');box.appendChild(n);
        var cb=mk('button','btn btn-line-d copy',T('نسخ','Copy'));cb.type='button';cb.setAttribute('data-copy',m.number);cb.setAttribute('data-done',T('تم النسخ','Copied'));
        row.appendChild(box);row.appendChild(cb);pm.appendChild(row);
      });
      bindCopy(pm);
      var note=$('#pay-note .paynote');var nt=d.note&&pick(d.note);if(note&&nt)note.textContent=nt;
    }).catch(function(){});
  }
})();
