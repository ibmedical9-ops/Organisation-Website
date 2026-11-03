(function(){
  var S=window.SITE||{};
  var $=function(s,r){return (r||document).querySelector(s)};
  var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};

  // قائمة الجوال
  var btn=$('.menu-btn'),nav=$('.nav');
  if(btn&&nav){btn.addEventListener('click',function(){
    var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o);btn.textContent=o?'✕':'☰';
  });}

  // السنة
  $$('[data-year]').forEach(function(e){e.textContent=new Date().getFullYear()});

  // رابط واتساب عام
  function wa(text){return 'https://wa.me/'+S.whatsapp+'?text='+encodeURIComponent(text)}
  $$('[data-wa]').forEach(function(a){a.href=wa(a.getAttribute('data-wa')||'السلام عليكم، أود الاستفسار')});

  // صفحة فيسبوك: تحميل متأخر
  var fb=$('#fb-frame');
  if(fb){
    var load=function(){
      var w=Math.min(500,fb.parentNode.clientWidth-24)||340;
      fb.src='https://www.facebook.com/plugins/page.php?href='+encodeURIComponent(S.facebook)+
        '&tabs=timeline&width='+w+'&height=640&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false&locale=ar_AR';
    };
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){load();io.disconnect()}},{rootMargin:'300px'});io.observe(fb);
    }else load();
  }

  // منشورات من ملف data/posts.json (اختياري)
  var box=$('#posts');
  if(box&&window.fetch){
    fetch('data/posts.json',{cache:'no-cache'}).then(function(r){return r.ok?r.json():[]}).then(function(list){
      list.slice(0,6).forEach(function(p){
        var a=document.createElement('article');a.className='post';
        var h='';
        if(p.image)h+='<img loading="lazy" alt="" src="'+encodeURI(p.image)+'">';
        h+='<div>';
        if(p.date)h+='<time>'+String(p.date).replace(/[<>&"]/g,'')+'</time>';
        h+='<p></p>';
        if(p.url)h+='<p><a target="_blank" rel="noopener" href="'+encodeURI(p.url)+'">عرض على فيسبوك ←</a></p>';
        h+='</div>';a.innerHTML=h;
        a.querySelector('p').textContent=p.text||'';
        box.appendChild(a);
      });
    }).catch(function(){});
  }


  // أرقام القسم الطبي (تحديث مباشر من ملف JSON أو CSV)
  var statEls=$$('[data-stat]');
  if(statEls.length&&window.fetch){
    var url=S.statsUrl||'data/medical-stats.json';
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

  // نموذج التبرع
  var df=$('#donate-form');
  if(df){
    var q=new URLSearchParams(location.search);
    if(q.get('program')&&df.program){df.program.value=q.get('program')}
    var custom=$('#amount-custom');
    $$('input[name=amount]',df).forEach(function(r){r.addEventListener('change',function(){custom.value=''})});
    custom&&custom.addEventListener('input',function(){$$('input[name=amount]',df).forEach(function(r){r.checked=false})});
    df.addEventListener('submit',function(e){
      e.preventDefault();
      var chosen=$('input[name=amount]:checked',df);
      var amount=custom.value?custom.value+' دينار عراقي':(chosen?chosen.value+' دينار عراقي':'');
      var msg='السلام عليكم، أرغب بالتبرع'+(amount?' بمبلغ '+amount:'')+' لبرنامج: '+df.program.value+
        (df.name.value?'\nالاسم: '+df.name.value:'')+'\nأرجو إرسال تفاصيل التحويل الرسمية.';
      location.href=wa(msg);
    });
  }

  // نموذج التطوع
  var vf=$('#volunteer-form');
  if(vf){
    vf.addEventListener('submit',function(e){
      e.preventDefault();
      var f=vf.elements;
      var msg='طلب تطوع جديد\nالاسم: '+f.name.value+'\nالعمر: '+f.age.value+'\nالمحافظة: '+f.city.value+
        '\nالهاتف: '+f.phone.value+'\nمجال التطوع: '+f.area.value+(f.note.value?'\nملاحظات: '+f.note.value:'');
      location.href=wa(msg);
    });
  }

  // نموذج التواصل
  var cf=$('#contact-form');
  if(cf){
    cf.addEventListener('submit',function(e){
      e.preventDefault();
      var f=cf.elements;
      location.href=wa('رسالة من الموقع\nالاسم: '+f.name.value+'\nالموضوع: '+f.subject.value+'\n'+f.message.value);
    });
  }
})();
