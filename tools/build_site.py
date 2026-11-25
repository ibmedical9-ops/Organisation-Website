import os
# يولّد صفحات الموقع (عربي + إنجليزي) في جذر المستودع: python3 tools/build_site.py
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
BASE='https://iraqbuilders.org/'
WA='9647730557766'
LG='ar'
P=''
def t(ar,en): return ar if LG=='ar' else en

PAGES=['index','about','activities','news','volunteer','contact']
def NAV():
    return [('index.html',t('الرئيسية','Home')),('about.html',t('من نحن','About')),('activities.html',t('أنشطتنا','Activities')),('news.html',t('الأخبار','News')),('volunteer.html',t('تطوع معنا','Volunteer')),('contact.html',t('تواصل','Contact'))]

def icon(name):
    p={
    'cross':'M9 3h6v6h6v6h-6v6H9v-6H3V9h6z',
    'shirt':'M8 3l-5 3 2 4 3-1v12h8V9l3 1 2-4-5-3a4 4 0 0 1-8 0z',
    'tools':'M14.7 6.3a4 4 0 0 0-5 5L3 18l3 3 6.7-6.7a4 4 0 0 0 5-5l-2.5 2.5-2.2-.5-.5-2.2z',
    'moon':'M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z',
    'heart':'M12 21s-8-5.3-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.7-8 11-8 11z',
    'gift':'M3 9h18v4H3zM5 13h14v8H5zM11 9h2v12h-2z',
    'wa':'M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5 14c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .2-3.2-.7-2.700-1.100-4.400-3.800-4.600-4-.1-.2-1.100-1.500-1.100-2.800s.7-2 1-2.300c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.2-.3.4-.1.7.2.3.8 1.300 1.700 2 1.100 1 2 1.300 2.300 1.400.3.1.5.1.6-.1l.9-1c.2-.2.4-.2.6-.1l1.900.9c.3.1.5.2.5.3.1.2.1.8-.1 1.300z'}[name]
    return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{p}"/></svg>'
def wa_path(): return icon('wa').split('d="')[1].split('"')[0]

def alt_url(page):
    # رابط النسخة الأخرى من نفس الصفحة
    return ('en/'+page) if LG=='ar' else ('../'+page)

def head(title,desc,page):
    nv=''.join(f'<a href="{h}"{" aria-current=page" if h==page else ""}>{n}</a>' for h,n in NAV())
    ld='{"@context":"https://schema.org","@type":"NGO","name":"منظمة بناة العراق الخيرية","alternateName":"Iraq Builders","url":"%s","logo":"%sassets/img/logo.png","foundingDate":"2013","telephone":"+9647730557766","sameAs":["https://www.facebook.com/iraqbuildersteam/","https://www.instagram.com/iraqbuilders","https://www.youtube.com/@IraqBuilders"],"areaServed":"IQ"}'%(BASE,BASE)
    ar_url=BASE+('' if page=='index.html' else page); en_url=BASE+'en/'+('' if page=='index.html' else page)
    me=ar_url if LG=='ar' else en_url
    sw=t('English','عربي')
    return f'''<!doctype html>
<html lang="{LG}" dir="{t('rtl','ltr')}" data-root="{P}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0f3d22">
<link rel="canonical" href="{me}">
<link rel="alternate" hreflang="ar" href="{ar_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="icon" href="{P}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{P}assets/img/logo-192.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="{t('ar_IQ','en_US')}">
<meta property="og:site_name" content="{t('منظمة بناة العراق الخيرية','Iraq Builders Organization')}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@600;800&display=swap">
<link rel="stylesheet" href="{P}assets/css/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">{t('تخطَّ إلى المحتوى','Skip to content')}</a>
<header class="top"><div class="container">
<a class="brand" href="index.html"><img src="{P}assets/img/logo-192.png" width="48" height="48" alt="{t('شعار منظمة بناة العراق','Iraq Builders logo')}"><span>{t('منظمة بناة العراق','Iraq Builders')}<small>{t('IRAQ BUILDERS','ORGANIZATION')}</small></span></a>
<button class="menu-btn" aria-label="{t('القائمة','Menu')}" aria-expanded="false">☰</button>
<nav class="nav" aria-label="{t('القائمة الرئيسية','Main menu')}">{nv}<a class="lang" href="{alt_url(page)}" hreflang="{t('en','ar')}" lang="{t('en','ar')}">{sw}</a><a class="btn btn-sun" href="donate.html">{t('تبرع الآن','Donate now')}</a></nav>
</div></header>
<main id="main">
'''

def foot():
    nv=''.join(f'<li><a href="{h}">{n}</a></li>' for h,n in NAV())
    return f'''</main>
<footer><div class="container">
<div class="fgrid">
<div><h3>{t('منظمة بناة العراق الخيرية','Iraq Builders Organization')}</h3><p>{t('منظمة تطوعية غير حكومية، مستقلة ولا تنتمي إلى أي جهة سياسية أو دينية. تأسست عام 2013 كمبادرة شبابية، ثم سُجّلت رسميًا كمنظمة مجتمع مدني.','A non-governmental volunteer organization, independent of any political or religious body. Founded in 2013 as a youth initiative and later officially registered as a civil society organization.')}</p></div>
<div><h3>{t('الموقع','Site')}</h3><ul>{nv}<li><a href="donate.html">{t('تبرع الآن','Donate now')}</a></li></ul></div>
<div><h3>{t('أنشطتنا','Activities')}</h3><ul><li><a href="activities.html#renovation">{t('ترميم المنازل','Home renovation')}</a></li><li><a href="activities.html#food">{t('المساعدات الغذائية','Food aid')}</a></li><li><a href="activities.html#education">{t('التعليم','Education')}</a></li><li><a href="activities.html#medical">{t('القسم الطبي','Medical department')}</a></li><li><a href="activities.html#khatwa">{t('مشروع خطوة','Khatwa project')}</a></li><li><a href="activities.html#ramadan">{t('أنشطة رمضان','Ramadan activities')}</a></li></ul></div>
<div><h3>{t('تواصل معنا','Contact us')}</h3><ul>
<li><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{t('واتساب','WhatsApp')}: <span dir="ltr">+964 773 055 7766</span></a></li>
<li><a href="https://www.facebook.com/iraqbuildersteam/" target="_blank" rel="noopener">{t('فيسبوك','Facebook')}</a></li>
<li><a href="https://www.instagram.com/iraqbuilders" target="_blank" rel="noopener">{t('إنستغرام','Instagram')}</a></li>
<li><a href="https://www.youtube.com/@IraqBuilders" target="_blank" rel="noopener">{t('يوتيوب','YouTube')}</a></li></ul></div>
</div>
<div class="copy"><span>© <span data-year>2026</span> {t('منظمة بناة العراق. جميع الحقوق محفوظة.','Iraq Builders Organization. All rights reserved.')}</span><span>iraqbuilders.org</span></div>
</div></footer>
<a class="wa-float" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="{t('تواصل عبر واتساب','Chat on WhatsApp')}"><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{wa_path()}"/></svg><span>{t('واتساب','WhatsApp')}</span></a>
<script src="{P}assets/js/config.js"></script>
<script src="{P}assets/js/app.js"></script>
</body></html>'''

def write(name,title,desc,body):
    d=OUT if LG=='ar' else OUT+'en/'
    os.makedirs(d,exist_ok=True)
    open(d+name,'w',encoding='utf8').write(head(title,desc,name)+body+foot())

def hero_page(h1,p): return f'<div class="page-hero"><div class="container"><h1>{h1}</h1><p>{p}</p></div></div>'
def more(): return t('التفاصيل','Details')
def arrow(): return t('←','→')
def card_img(img,alt,h,p,link=None,pos='center'):
    a=f'<a href="{link}" class="btn btn-line-d" style="align-self:flex-start;min-height:40px;padding:4px 16px;font-size:15px">{more()}</a>' if link else ''
    return f'<article class="card"><div class="im"><img src="{P}assets/img/{img}" alt="{alt}" loading="lazy" style="object-position:{pos}"></div><div class="tx"><h3>{h}</h3><p>{p}</p>{a}</div></article>'
def card_ico(ic,tint,h,p):
    return f'<article class="card"><div class="ico {tint}">{icon(ic)}</div><div class="tx"><h3>{h}</h3><p>{p}</p></div></article>'

def FBBOX():
    return f'<div class="fbwrap"><p class="fb-note">{t("للمزيد من المنشورات","For more posts")} <a href="https://www.facebook.com/iraqbuildersteam/" target="_blank" rel="noopener">{t("افتح صفحتنا على فيسبوك","open our Facebook page")}</a></p><iframe id="fb-frame" title="{t("آخر منشورات صفحة منظمة بناة العراق على فيسبوك","Latest posts from the Iraq Builders Facebook page")}" loading="lazy" allow="encrypted-media"></iframe></div>'
def SOCIAL():
    return f'<ul class="links"><li><a class="btn btn-green" href="https://www.facebook.com/iraqbuildersteam/" target="_blank" rel="noopener">{t("صفحتنا على فيسبوك","Our Facebook page")}</a></li><li><a class="btn btn-line-d" href="https://www.instagram.com/iraqbuilders" target="_blank" rel="noopener">{t("إنستغرام","Instagram")}</a></li><li><a class="btn btn-line-d" href="https://www.youtube.com/@IraqBuilders" target="_blank" rel="noopener">{t("يوتيوب","YouTube")}</a></li></ul>'
def PARTNERS():
    return f'<div class="partners"><img src="{P}assets/img/partner-fresh.webp" alt="Fresh" loading="lazy" width="150" height="41"><img src="{P}assets/img/partner-kareem.webp" alt="كريم / Careem" loading="lazy" width="150" height="41"><img src="{P}assets/img/partner-earthlink.webp" alt="Earthlink" loading="lazy" width="150" height="41"><img src="{P}assets/img/partner-atlas.webp" alt="Atlas Plast" loading="lazy" width="150" height="41"></div>'

def MED():
    return f'''<section class="sand" id="medical" style="scroll-margin-top:90px"><div class="container">
<div class="head"><span class="kicker">{t('القسم الطبي','Medical department')}</span><h2>{t('الدعم الدوائي بالأرقام','Medicine support in numbers')}</h2><p>{t('أرقام محدّثة من نظام الصرف في القسم الطبي. تعرض إحصاءات مجمّعة فقط، دون أي بيانات شخصية للمستفيدين.','Figures updated from the medical department dispensing system. Aggregated statistics only, with no personal data about beneficiaries.')}</p></div>
<div class="stats" aria-live="polite">
<div class="stat"><b data-stat="families">91</b><span>{t('عائلة مشمولة بالصرف','Families covered by dispensing')}</span></div>
<div class="stat"><b data-stat="dispensed">439</b><span>{t('دواء مشمول بالصرف','Medicines covered by dispensing')}</span></div>
<div class="stat ok"><b data-stat="available">386</b><span>{t('دواء متوفر','Medicines available')}</span></div>
<div class="stat no"><b data-stat="unavailable">53</b><span>{t('دواء غير متوفر حاليًا','Medicines currently unavailable')}</span></div>
</div>
<div class="meter" role="img" aria-label="{t('نسبة توفر الأدوية','Medicine availability rate')}"><div class="meter-top"><span>{t('نسبة توفر الأدوية','Medicine availability rate')}</span><b><span data-stat="percent">88</span>%</b></div><div class="meter-bar"><i data-bar style="width:88%"></i></div></div>
<p class="hint" style="margin-top:12px">{t('آخر تحديث','Last updated')}: <time data-stat="updated" dir="ltr">2026-11-03</time></p>
<div class="row" style="margin-top:20px"><a class="btn btn-sun" href="donate.html">{t('ساهم بتوفير الأدوية الناقصة','Help supply the missing medicines')}</a></div>
</div></section>'''

def home():
    return f'''
<section class="hero" style="padding:0"><div class="container">
<span class="eyebrow">{t('منظمة تطوعية مستقلة منذ 2013','Independent volunteer organization since 2013')}</span>
<h1>{t('نبني بيوتًا، ونعيد الأمل لعائلات العراق','We build homes and restore hope for families across Iraq')}</h1>
<p class="lead">{t('نرمم المنازل المتضررة، ونوزع المساعدات الغذائية، ونرعى الأيتام، ونمكّن الشباب، في مختلف المحافظات العراقية.','We renovate damaged homes, distribute food aid, care for orphans and empower young people in governorates across Iraq.')}</p>
<div class="row"><a class="btn btn-sun" href="donate.html">{t('تبرع الآن','Donate now')}</a><a class="btn btn-line" href="volunteer.html">{t('تطوع معنا','Volunteer with us')}</a></div>
</div></section>
<div class="facts"><div class="container"><ul>
<li><b>2013</b>{t('بداية المبادرة الشبابية','Youth initiative begins')}</li>
<li><b>{t('مسجلة رسميًا','Registered')}</b>{t('منظمة مجتمع مدني','Civil society organization')}</li>
<li><b>{t('مستقلة','Independent')}</b>{t('بلا انتماء سياسي أو ديني','No political or religious affiliation')}</li>
<li><b>{t('كل المحافظات','All governorates')}</b>{t('عمل ميداني بجهود المتطوعين','Field work by volunteers')}</li></ul></div></div>

<section><div class="container split">
<div><span class="kicker">{t('من نحن','About us')}</span><h2 style="font-size:clamp(26px,3.4vw,36px)">{t('شباب تطوعوا ليبنوا مجتمعًا أكثر تماسكًا وعدالة','Young people who volunteered to build a more cohesive and fairer society')}</h2>
<p style="margin-top:14px">{t('انطلقت المنظمة عام 2013 مبادرة شبابية تطوعية، إيمانًا بدور العمل الإنساني والتنموي في بناء المجتمع، ثم جرى تسجيلها رسميًا كمنظمة مجتمع مدني.','The organization began in 2013 as a volunteer youth initiative, driven by a belief in the role of humanitarian and development work in building society, and was later officially registered as a civil society organization.')}</p>
<p>{t('نعمل على دعم الأسر المحتاجة بمشاريع إنسانية وتنموية متنوعة، ونعزز ثقافة التطوع وروح التعاون بين الشباب العراقي.','We support families in need through diverse humanitarian and development projects, and promote a culture of volunteering and cooperation among Iraqi youth.')}</p>
<a class="btn btn-green" href="about.html">{t('اعرف المزيد عنا','Learn more about us')}</a></div>
<div class="ph"><img src="{P}assets/img/team-steps.webp" alt="{t('فريق متطوعي بناة العراق مجتمعين بستراتهم','Iraq Builders volunteers gathered in their vests')}" loading="lazy"></div>
</div></section>

<section class="sand"><div class="container">
<div class="head"><span class="kicker">{t('أنشطتنا','Our activities')}</span><h2>{t('أين يذهب دعمك','Where your support goes')}</h2><p>{t('كل نشاط يخدم حاجة محددة لدى العائلات. اختر ما يقترب من قلبك.','Every activity meets a specific need of families. Choose the one closest to your heart.')}</p></div>
<div class="grid" id="home-activities">
{card_img('hero-team.webp',t('متطوعون بالخوذ والستر في موقع ترميم','Volunteers in helmets and vests at a renovation site'),t('مهمة بناء','Building Mission'),t('ترميم المنازل المتضررة لتوفير سقف آمن للعائلات المتعففة.','Renovating damaged homes to give families in need a safe roof.'),'activities.html#renovation','40% 30%')}
{card_img('food.webp',t('متطوع يحمل كيس مواد غذائية','A volunteer carrying a sack of food'),t('سلال غذائية','Food baskets'),t('توزيع سلال غذائية على الأسر المحتاجة.','Distributing food baskets to families in need.'),'activities.html#food')}
{card_img('school-bags.webp',t('توزيع حقائب مدرسية على الأطفال','Handing out school bags to children'),t('حقيبة مدرسية','School bags'),t('حقائب مجهزة بالكامل للطلاب المحتاجين.','Fully equipped school bags for students in need.'),'activities.html#education','60% 40%')}
{card_img('appliances.webp',t('متطوعان يحملان جهازًا منزليًا','Two volunteers carrying a home appliance'),t('أجهزة منزلية','Home appliances'),t('توزيع أجهزة كهربائية ومنزلية للأسر ذات الدخل المحدود.','Distributing essential electrical and household appliances to low-income families.'),'activities.html#appliances')}
</div>
<p style="margin-top:26px"><a class="btn btn-line-d" href="activities.html">{t('كل الأنشطة','All activities')}</a></p>
</div></section>

<section id="home-news-sec" hidden><div class="container">
<div class="head"><span class="kicker">{t('الأخبار','News')}</span><h2>{t('آخر الأخبار','Latest news')}</h2></div>
<div id="cms-news-home" class="grid g3"></div>
<p style="margin-top:26px"><a class="btn btn-line-d" href="news.html">{t('كل الأخبار','All news')}</a></p>
</div></section>

{MED()}

<section><div class="container">
<div class="head"><span class="kicker">{t('شارك معنا','Get involved')}</span><h2>{t('أربع طرق لتكون جزءًا من التغيير','Four ways to be part of the change')}</h2></div>
<div class="ways">
<div class="way hot"><h3>{t('تبرع','Donate')}</h3><p>{t('اطّلع على معلومات التبرع وساهم عبر ماستر كارد أو زين كاش.','See our donation details and give by Mastercard or Zain Cash.')}</p><a class="btn btn-sun" href="donate.html">{t('تبرع الآن','Donate now')}</a></div>
<div class="way"><h3>{t('تطوع','Volunteer')}</h3><p>{t('انضم إلى فريق ميداني يرمم ويوزع ويرعى. نرحب بكل الأعمار والتخصصات.','Join a field team that renovates, distributes and cares. All ages and skills are welcome.')}</p><a class="btn btn-green" href="volunteer.html">{t('سجّل كمتطوع','Register as a volunteer')}</a></div>
<div class="way"><h3>{t('ساهم عينيًا','Give in kind')}</h3><p>{t('مواد غذائية أو أجهزة أو ملابس أو مستلزمات مدرسية للأسر المحتاجة.','Food, appliances, clothing or school supplies for families in need.')}</p><a class="btn btn-green" data-wa="{t('السلام عليكم، أرغب بالمساهمة بتبرع عيني.','Hello, I would like to make an in-kind donation.')}" href="#">{t('تواصل معنا','Contact us')}</a></div>
<div class="way"><h3>{t('انشر وتابع','Follow and share')}</h3><p>{t('تابعنا على فيسبوك وإنستغرام وانشر أخبارنا بين أصدقائك.','Follow us on Facebook and Instagram and share our news with friends.')}</p><a class="btn btn-green" href="news.html">{t('آخر الأخبار','Latest news')}</a></div>
</div></div></section>

<section class="sand"><div class="container social-box">
<div><span class="kicker">{t('من فيسبوك','From Facebook')}</span><h2 style="font-size:clamp(26px,3.4vw,36px)">{t('آخر ما ننشره من الميدان','Latest from the field')}</h2>
<p style="margin-top:12px;color:var(--muted)">{t('منشورات من صفحتنا على فيسبوك، لتتابع أعمال الفريق أولًا بأول دون مغادرة الموقع.','Posts from our Facebook page, so you can follow the team\'s work as it happens without leaving the site.')}</p>
<div id="posts" class="posts" style="margin-top:20px"></div>{SOCIAL()}</div>
{FBBOX()}
</div></section>

<section><div class="container"><div class="head" style="text-align:center;margin-inline:auto"><span class="kicker">{t('شركاء العمل الإنساني','Humanitarian partners')}</span><h2>{t('جهات تدعم رسالتنا','Organizations supporting our mission')}</h2></div>{PARTNERS()}</div></section>

<div class="cta"><div class="container"><h2>{t('كن جزءًا من التغيير','Be part of the change')}</h2><p>{t('ساهم معنا في إحداث تغيير حقيقي في حياة الأسر المحتاجة، وكن جزءًا من مستقبل أفضل لبلدنا.','Help make a real difference in the lives of families in need and be part of a better future for our country.')}</p>
<div class="row"><a class="btn btn-sun" href="donate.html">{t('تبرع الآن','Donate now')}</a><a class="btn btn-line" href="volunteer.html">{t('استمارة التطوع','Volunteer form')}</a></div></div></div>
'''

def about():
    return hero_page(t('من نحن','About us'),t('منظمة تطوعية مستقلة تعمل لبناء مجتمع أكثر تماسكًا وعدالة.','An independent volunteer organization working to build a more cohesive and fairer society.'))+f'''
<section><div class="container"><div class="prose">
<h2 style="margin-top:0">{t('قصتنا','Our story')}</h2>
<p>{t('منظمة بناة العراق منظمة تطوعية غير حكومية، مستقلة ولا تنتمي إلى أي جهة سياسية أو دينية. تأسست عام 2013 كمبادرة شبابية تطوعية، ثم جرى تسجيلها رسميًا كمنظمة مجتمع مدني، انطلاقًا من إيمانها بدور العمل الإنساني والتنموي في بناء مجتمع أكثر تماسكًا وعدالة.','Iraq Builders is a non-governmental volunteer organization, independent of any political or religious body. It was founded in 2013 as a volunteer youth initiative and later officially registered as a civil society organization, out of a belief in the role of humanitarian and development work in building a more cohesive and fairer society.')}</p>
<div class="band"><img src="{P}assets/img/team-steps.webp" alt="{t('متطوعو منظمة بناة العراق','Iraq Builders volunteers')}" loading="lazy"></div>
<h2>{t('ماذا نفعل','What we do')}</h2>
<p>{t('تهدف المنظمة إلى دعم الأسر المحتاجة في العراق من خلال مشاريع إنسانية وتنموية متنوعة، تشمل ترميم المنازل المتضررة، وتوزيع المساعدات الغذائية، ورعاية الأيتام، بما يسهم في تحسين الظروف المعيشية للعائلات المتعففة في مختلف المحافظات العراقية.','The organization aims to support families in need in Iraq through diverse humanitarian and development projects, including renovating damaged homes, distributing food aid and caring for orphans, helping improve living conditions for families across Iraqi governorates.')}</p>
<p>{t('كما تعمل على تعزيز ثقافة التطوع وروح التعاون بين الشباب العراقي، وتمكينهم من أداء دور فاعل في خدمة مجتمعهم.','It also works to promote a culture of volunteering and cooperation among Iraqi youth, enabling them to play an active role in serving their community.')}</p>
<h2>{t('نحو التنمية المستدامة','Toward sustainable development')}</h2>
<p>{t('أطلقت المنظمة مشروع «خطوة»، وهو مشروع يركز على تمكين الشباب والباحثين عن العمل عبر تطوير مهاراتهم المهنية ودمجهم في سوق العمل.','The organization launched the Khatwa project, a project focused on empowering young people and job seekers by developing their professional skills and integrating them into the labor market.')}</p>
<ul class="tl">
<li><b>2013</b><br>{t('انطلاق المبادرة كفريق شبابي تطوعي.','The initiative begins as a volunteer youth team.')}</li>
<li><b>{t('التسجيل الرسمي','Official registration')}</b><br>{t('تسجيل المنظمة كمنظمة مجتمع مدني.','Registered as a civil society organization.')}</li>
<li><b>{t('اليوم','Today')}</b><br>{t('أنشطة متعددة تصل إلى عائلات في مختلف المحافظات، ومشروع «خطوة» لتمكين الشباب.','Multiple activities reaching families across governorates, and the Khatwa project empowering young people.')}</li></ul>
</div></div></section>

<section class="sand" id="transparency"><div class="container">
<div class="head"><span class="kicker">{t('الشفافية والمساءلة','Transparency and accountability')}</span><h2>{t('نؤمن أن الثقة تُبنى بالوضوح','We believe trust is built on clarity')}</h2><p>{t('نخصص هذا القسم لنشر وثائق المنظمة وتقاريرها ليطّلع عليها الداعمون والشركاء.','This section publishes the organization\'s documents and reports for supporters and partners.')}</p></div>
<div class="docs">
<div class="doc">{t('شهادة تسجيل المنظمة','Organization registration certificate')}<span>{t('تُضاف قريبًا','Coming soon')}</span></div>
<div class="doc">{t('التقرير السنوي','Annual report')}<span>{t('تُضاف قريبًا','Coming soon')}</span></div>
<div class="doc">{t('أسماء الهيئة الإدارية','Board members')}<span>{t('تُضاف قريبًا','Coming soon')}</span></div>
<div class="doc">{t('التقارير المالية','Financial reports')}<span>{t('تُضاف قريبًا','Coming soon')}</span></div>
</div></div></section>

<div class="cta"><div class="container"><h2>{t('انضم إلى رحلتنا','Join our journey')}</h2><p>{t('سواء بوقتك أو بمالك أو بنشر رسالتنا، لك مكان بيننا.','Whether with your time, your money or by spreading our message, there is a place for you with us.')}</p><div class="row"><a class="btn btn-sun" href="donate.html">{t('تبرع الآن','Donate now')}</a><a class="btn btn-line" href="volunteer.html">{t('تطوع معنا','Volunteer with us')}</a></div></div></div>'''

def activities():
    def prog(id_,img,alt,h,p):
        return f'''<article class="split" id="{id_}" style="padding-block:34px;scroll-margin-top:90px"><div class="ph"><img src="{P}assets/img/{img}" alt="{alt}" loading="lazy"></div><div><h2 style="font-size:28px">{h}</h2><p style="margin-top:12px">{p}</p><a class="btn btn-green" href="donate.html">{t('ادعم هذا النشاط','Support this activity')}</a></div></article>'''
    return hero_page(t('أنشطتنا','Our activities'),t('مشاريع إنسانية وتنموية تصل إلى العائلات المحتاجة في مختلف المحافظات.','Humanitarian and development projects reaching families in need across governorates.'))+f'''
<section id="cms-activities-sec" hidden><div class="container">
<div id="cms-activities" class="grid g3"></div>
</div></section>

<section data-fallback><div class="container">
{prog('renovation','hero-team.webp',t('متطوعون بالخوذ والستر في موقع ترميم','Volunteers in helmets and vests at a renovation site'),t('مهمة بناء (ترميم المنازل)','Building Mission (home renovation)'),t('بفضل جهود المتطوعين وتكاتف الأيادي الخيرة، نرمم المنازل المتضررة ونوفر سقفًا آمنًا وبيئة مناسبة للعائلات المتعففة.','Thanks to the efforts of volunteers and generous hands, we renovate damaged homes and provide a safe roof and a suitable environment for families in need.'))}
{prog('food','food.webp',t('متطوع يحمل مواد غذائية','A volunteer carrying food supplies'),t('سلال غذائية','Food baskets'),t('بدعم من فريق بناة العراق التطوعي نوزع سلالًا غذائية على الأسر المحتاجة.','With the support of the Iraq Builders volunteer team, we distribute food baskets to families in need.'))}
{prog('education','school-bags.webp',t('توزيع حقائب مدرسية على الأطفال','Handing out school bags to children'),t('حقيبة مدرسية','School bags'),t('حقائب مدرسية مجهزة بالكامل للطلاب المحتاجين، ضمن مبادرة الفريق لدعم التعليم.','Fully equipped school bags for students in need, as part of the team\'s initiative to support education.'))}
{prog('appliances','appliances.webp',t('متطوعان يحملان جهازًا منزليًا','Two volunteers carrying a home appliance'),t('أجهزة كهربائية ومنزلية','Electrical and home appliances'),t('نوزع الأجهزة الكهربائية والمنزلية الضرورية للأسر ذات الدخل المحدود، لتحسين جودة الحياة اليومية وتخفيف الأعباء المالية.','We distribute essential electrical and household appliances to low-income families, improving daily life and easing financial burdens.'))}
</div></section>

<section class="sand" data-fallback><div class="container">
<div class="head"><span class="kicker">{t('أنشطة أخرى','More activities')}</span><h2>{t('دعم يلمس تفاصيل الحياة','Support that touches everyday life')}</h2></div>
<div class="grid">
{card_ico('cross','',t('رعاية طبية','Medical care'),t('عمليات وأدوية: تغطية تكاليف العمليات الجراحية والدواء للمحتاجين.','Surgeries and medicines: covering the cost of surgical operations and medicine for those in need.'))}
{card_ico('shirt','tint2',t('كسوة العيد','Eid clothing'),t('ملابس جديدة للأطفال والعائلات في أعياد الفطر والأضحى.','New clothes for children and families at Eid al-Fitr and Eid al-Adha.'))}
{card_ico('tools','tint3',t('مشاريع تشغيلية','Livelihood projects'),t('تعزيز الاستقلالية الاقتصادية للأفراد بتوفير فرص عمل ومشاريع صغيرة.','Strengthening individuals\' economic independence through jobs and small projects.'))}
{card_ico('heart','',t('كفالات','Sponsorships'),t('أنشطة كفالة طبية ودراسية ومعيشية للأسر والأفراد المحتاجين.','Medical, educational and living sponsorship programs for families and individuals in need.'))}
{card_ico('gift','tint2',t('مساعدات مالية','Financial aid'),t('مساعدات مالية للأسر والأفراد الذين يواجهون صعوبات اقتصادية.','Financial assistance for families and individuals facing economic hardship.'))}
</div></div></section>

{MED()}

<section id="khatwa" style="scroll-margin-top:90px"><div class="container split">
<div><span class="kicker">{t('التنمية المستدامة','Sustainable development')}</span><h2 id="khatwa-title" style="font-size:30px">{t('مشروع خطوة','Khatwa project')}</h2>
<p id="khatwa-text" style="margin-top:12px">{t('مشروع يمكّن الشباب والباحثين عن العمل عبر تطوير مهاراتهم المهنية ودمجهم في سوق العمل. يسعى المشروع إلى سد الفجوة بين المهارات التي يمتلكها الباحثون عن العمل واحتياجات السوق، وتدريب الأفراد على مهارات مهنية متخصصة.','A project that empowers young people and job seekers by developing their professional skills and integrating them into the labor market. It aims to bridge the gap between job seekers\' skills and market needs, and to train individuals in specialized professional skills.')}</p>
<a class="btn btn-green" data-wa="{t('السلام عليكم، أرغب بالاستفسار عن مشروع خطوة.','Hello, I would like to ask about the Khatwa project.')}" href="#">{t('استفسر عن مشروع خطوة','Ask about Khatwa')}</a></div>
<div class="ph"><img id="khatwa-img" src="{P}assets/img/volunteers-boxes.webp" alt="{t('متطوعون وشباب من فريق المنظمة','Volunteers and young people from the team')}" loading="lazy"></div>
</div></section>

<section class="sand" id="ramadan" style="scroll-margin-top:90px"><div class="container">
<div class="head"><span class="kicker">{t('موسمي','Seasonal')}</span><h2>{t('أنشطة رمضان','Ramadan activities')}</h2><p>{t('في رمضان نضاعف عملنا لنصل إلى أكبر عدد من العائلات.','In Ramadan we double our work to reach as many families as possible.')}</p></div>
<div class="grid" id="ramadan-grid">
{card_ico('moon','',t('إفطار العوائل','Family iftars'),t('موائد إفطار للعائلات المحتاجة.','Iftar tables for families in need.'))}
{card_ico('heart','tint2',t('زكاة الفطرة','Zakat al-Fitr'),t('نوصل زكاة الفطرة لمستحقيها.','Delivering Zakat al-Fitr to those who deserve it.'))}
{card_ico('gift','',t('سلات رمضانية','Ramadan baskets'),t('سلات غذائية خاصة بالشهر الفضيل.','Food baskets for the holy month.'))}
{card_ico('shirt','tint3',t('كسوة العيد','Eid clothing'),t('فرحة العيد بملابس جديدة للأطفال.','The joy of Eid with new clothes for children.'))}
</div></div></section>
<div class="cta"><div class="container"><h2>{t('اختر نشاطًا وساهم اليوم','Choose an activity and give today')}</h2><p>{t('كل مساهمة تتحول إلى عمل على الأرض.','Every contribution becomes work on the ground.')}</p><div class="row"><a class="btn btn-sun" href="donate.html">{t('تبرع الآن','Donate now')}</a></div></div></div>'''

def news():
    return hero_page(t('الأخبار','News'),t('آخر أنشطة الفريق من صفحتنا الرسمية على فيسبوك.','Latest team activities from our official Facebook page.'))+f'''
<section id="cms-news-sec" hidden><div class="container">
<div id="cms-news" class="grid g3"></div>
</div></section>

<section><div class="container social-box">
<div><div id="posts" class="posts"></div>
<h2 style="font-size:28px">{t('تابع أعمالنا أولًا بأول','Follow our work as it happens')}</h2>
<p style="margin-top:12px;color:var(--muted)">{t('المنشورات التي نضيفها تظهر هنا. للمشاهدة الكاملة وللتفاعل مع المنشورات، زر صفحتنا الرسمية.','Posts we add appear here. For the full feed and to interact with posts, visit our official page.')}</p>
{SOCIAL()}</div>
{FBBOX()}
</div></section>'''


def news_item():
    return f'''<section><div class="container"><article class="article" id="news-item" data-back="{t('كل الأخبار','All news')}">
<p class="hint" id="news-loading">{t('جارٍ التحميل…','Loading…')}</p>
<noscript><p>{t('فعّل جافاسكربت لعرض الخبر.','Please enable JavaScript to view this news item.')}</p></noscript>
</article></div></section>'''

def volunteer():
    ta='dir="ltr" style="text-align:right"' if LG=='ar' else 'dir="ltr"'
    opts=[('العمل الميداني (ترميم وتوزيع)','Field work (renovation and distribution)'),('التنظيم والإدارة','Organization and administration'),('التصوير والإعلام','Photography and media'),('التدريب (مشروع خطوة)','Training (Khatwa project)'),('الدعم الطبي','Medical support'),('أخرى','Other')]
    o=''.join(f'<option>{t(a,b)}</option>' for a,b in opts)
    return hero_page(t('تطوع معنا','Volunteer with us'),t('ساهم بوقتك ومهاراتك في إحداث تغيير حقيقي في حياة الأسر المحتاجة.','Give your time and skills to make a real difference in the lives of families in need.'))+f'''
<section><div class="container layout">
<div><h2 style="font-size:28px;margin-bottom:18px">{t('استمارة التطوع','Volunteer form')}</h2>
<form class="form" id="volunteer-form">
<label>{t('الاسم الكامل','Full name')}<input name="name" required autocomplete="name"></label>
<div class="two"><label>{t('العمر','Age')}<input name="age" type="number" min="15" max="80" required inputmode="numeric"></label>
<label>{t('المحافظة','Governorate')}<input name="city" required></label></div>
<label>{t('رقم الهاتف','Phone number')}<input name="phone" type="tel" required inputmode="tel" autocomplete="tel" {ta}></label>
<label>{t('مجال التطوع','Volunteer area')}<select name="area">{o}</select></label>
<label>{t('ملاحظات (اختياري)','Notes (optional)')}<textarea name="note"></textarea></label>
<button class="btn btn-wa" type="submit">{t('إرسال الطلب عبر واتساب','Send request via WhatsApp')}</button>
<p class="hint">{t('عند الضغط يُفتح واتساب برسالة جاهزة تحمل بياناتك، وتُرسل إلى فريق التطوع.','WhatsApp opens with a ready message containing your details, to be sent to the volunteer team.')}</p>
</form></div>
<aside class="side"><h3>{t('لماذا تتطوع معنا؟','Why volunteer with us?')}</h3>
<p>{t('نعمل بروح الفريق، ونمنح المتطوعين فرصة لخدمة مجتمعهم وتطوير مهاراتهم.','We work as a team and give volunteers a chance to serve their community and develop their skills.')}</p>
<ul class="contact-list"><li><b>{t('أسئلة سريعة؟','Quick questions?')}</b><a href="#" data-wa="{t('السلام عليكم، لدي استفسار عن التطوع.','Hello, I have a question about volunteering.')}">{t('راسلنا على واتساب','Message us on WhatsApp')}</a></li></ul></aside>
</div></section>'''

def donate():
    ta='dir="ltr" style="text-align:right"' if LG=='ar' else 'dir="ltr"'
    opts=[('أي نشاط بحسب الحاجة','Wherever needed most'),('مهمة بناء (ترميم المنازل)','Building Mission (home renovation)'),('سلال غذائية','Food baskets'),('حقيبة مدرسية','School bags'),('أجهزة كهربائية ومنزلية','Electrical and home appliances'),('رعاية طبية وأدوية','Medical care and medicines'),('كسوة العيد','Eid clothing'),('مشروع خطوة','Khatwa project'),('أنشطة رمضان','Ramadan activities')]
    o=''.join(f'<option>{t(a,b)}</option>' for a,b in opts)
    copy=t('نسخ','Copy')
    return hero_page(t('تبرع الآن','Donate now'),t('كل مساهمة تتحول إلى عمل حقيقي على الأرض.','Every contribution becomes real work on the ground.'))+f'''
<section><div class="container layout">
<div>
<div class="paybox" id="donation-info">
<h2>{t('معلومات التبرع','Donation information')}</h2>
<div id="pay-methods" class="pay-methods">
<div class="payrow"><div><b>{t('ماستر كارد (الرافدين)','Mastercard (Al-Rafidain)')}</b><span class="num" dir="ltr">6173766863</span></div><button type="button" class="btn btn-line-d copy" data-copy="6173766863" data-done="{t('تم النسخ','Copied')}">{copy}</button></div>
<div class="payrow"><div><b>{t('زين كاش','Zain Cash')}</b><span class="num" dir="ltr">07815109866</span></div><button type="button" class="btn btn-line-d copy" data-copy="07815109866" data-done="{t('تم النسخ','Copied')}">{copy}</button></div>
</div>
<div id="pay-note">
<p class="paynote">{t('يرجى ذكر اسمكم ورقم هاتفكم في ملاحظات التحويل في حال رغبتكم بالحصول على وصل لتبرعكم الكريم.','Please mention your name and phone number in the transfer notes if you would like a receipt for your generous donation.')}</p>
</div>
<p class="paynote">{t('أو التواصل مع واتساب المنظمة:','Or contact the organization on WhatsApp:')} <a href="#" data-wa="{t('السلام عليكم، أرغب بالتبرع وبالحصول على وصل.','Hello, I would like to donate and receive a receipt.')}">{t('راسلنا على واتساب','Message us on WhatsApp')}</a></p>
</div>
<h2 style="font-size:24px;margin:34px 0 14px">{t('أرسل لنا تفاصيل تبرعك','Send us your donation details')}</h2>
<form class="form" id="donate-form">
<div class="two"><label>{t('المبلغ','Amount')}<input name="amount" inputmode="numeric" placeholder="{t('مثال: 25,000 دينار','e.g. 25,000 IQD')}"></label>
<label>{t('النشاط','Activity')}<select name="program">{o}</select></label></div>
<div class="two"><label>{t('الاسم','Name')}<input name="name" autocomplete="name"></label>
<label>{t('رقم الهاتف','Phone number')}<input name="phone" type="tel" inputmode="tel" autocomplete="tel" {ta}></label></div>
<button class="btn btn-sun" type="submit">{t('إرسال التفاصيل عبر واتساب','Send details via WhatsApp')}</button>
<p class="hint">{t('هذا الإرسال اختياري، ويساعدنا على إصدار وصل لتبرعك. لا نطلب أي بيانات بطاقة في هذا الموقع.','This step is optional and helps us issue a receipt for your donation. We never ask for card details on this site.')}</p>
</form></div>
<aside class="side"><h3>{t('ثقة وشفافية','Trust and transparency')}</h3>
<p>{t('منظمة مسجلة رسميًا كمنظمة مجتمع مدني، ومستقلة عن أي جهة سياسية أو دينية.','Officially registered as a civil society organization, independent of any political or religious body.')}</p>
<p><a href="about.html#transparency">{t('اطّلع على وثائق الشفافية','View our transparency documents')}</a></p>
<h3 style="margin-top:8px">{t('تفضّل المساهمة العينية؟','Prefer to give in kind?')}</h3>
<p>{t('مواد غذائية، أجهزة، ملابس، أو مستلزمات مدرسية.','Food, appliances, clothing or school supplies.')}</p>
<a class="btn btn-green" href="#" data-wa="{t('السلام عليكم، أرغب بالمساهمة بتبرع عيني.','Hello, I would like to make an in-kind donation.')}">{t('تواصل معنا','Contact us')}</a></aside>
</div></section>'''

def contact():
    subs=[('استفسار عام','General inquiry'),('شراكة أو دعم مؤسسي','Partnership or institutional support'),('تبرع','Donation'),('تطوع','Volunteering'),('إعلام','Media')]
    o=''.join(f'<option>{t(a,b)}</option>' for a,b in subs)
    return hero_page(t('تواصل معنا','Contact us'),t('يسعدنا سماعك: استفسار، اقتراح، أو شراكة.','We would love to hear from you: a question, suggestion or partnership.'))+f'''
<section><div class="container layout">
<div><h2 style="font-size:28px;margin-bottom:18px">{t('أرسل لنا رسالة','Send us a message')}</h2>
<form class="form" id="contact-form">
<label>{t('الاسم','Name')}<input name="name" required autocomplete="name"></label>
<label>{t('الموضوع','Subject')}<select name="subject">{o}</select></label>
<label>{t('رسالتك','Your message')}<textarea name="message" required></textarea></label>
<button class="btn btn-wa" type="submit">{t('إرسال عبر واتساب','Send via WhatsApp')}</button></form></div>
<aside class="side"><h3>{t('معلومات التواصل','Contact information')}</h3>
<ul class="contact-list">
<li><b>{t('واتساب','WhatsApp')}</b><a href="https://wa.me/{WA}" target="_blank" rel="noopener" dir="ltr">+964 773 055 7766</a></li>
<li><b>{t('فيسبوك','Facebook')}</b><a href="https://www.facebook.com/iraqbuildersteam/" target="_blank" rel="noopener" dir="ltr">iraqbuildersteam</a></li>
<li><b>{t('إنستغرام','Instagram')}</b><a href="https://www.instagram.com/iraqbuilders" target="_blank" rel="noopener" dir="ltr">@iraqbuilders</a></li>
<li><b>{t('يوتيوب','YouTube')}</b><a href="https://www.youtube.com/@IraqBuilders" target="_blank" rel="noopener" dir="ltr">@IraqBuilders</a></li></ul></aside>
</div></section>'''

META={
 'index':(('منظمة بناة العراق الخيرية | Iraq Builders','منظمة تطوعية غير حكومية منذ 2013: ترميم المنازل، المساعدات الغذائية، رعاية الأيتام، ومشروع خطوة لتمكين الشباب في العراق.'),
          ('Iraq Builders Organization | منظمة بناة العراق','Independent volunteer organization since 2013: home renovation, food aid, orphan care and the Khatwa project empowering young people in Iraq.'),home),
 'about':(('من نحن | منظمة بناة العراق الخيرية','تعرّف على منظمة بناة العراق: منظمة تطوعية مستقلة تأسست عام 2013 ومسجلة رسميًا، تدعم الأسر المحتاجة وتمكّن الشباب.'),
          ('About us | Iraq Builders Organization','Learn about Iraq Builders: an independent volunteer organization founded in 2013 and officially registered, supporting families in need and empowering youth.'),about),
 'activities':(('أنشطتنا | منظمة بناة العراق الخيرية','ترميم المنازل، سلال غذائية، حقائب مدرسية، رعاية طبية، كسوة العيد، ومشروع خطوة: أنشطة منظمة بناة العراق.'),
          ('Our activities | Iraq Builders Organization','Home renovation, food baskets, school bags, medical care, Eid clothing and the Khatwa project: the activities of Iraq Builders.'),activities),
 'news':(('الأخبار | منظمة بناة العراق الخيرية','آخر أخبار وأنشطة منظمة بناة العراق من صفحتها الرسمية على فيسبوك.'),
          ('News | Iraq Builders Organization','Latest news and activities of Iraq Builders from its official Facebook page.'),news),
 'news-item':(('خبر | منظمة بناة العراق الخيرية','تفاصيل خبر من منظمة بناة العراق.'),
          ('News | Iraq Builders Organization','News from Iraq Builders.'),news_item),
 'volunteer':(('تطوع معنا | منظمة بناة العراق الخيرية','سجّل كمتطوع في منظمة بناة العراق وساهم في ترميم المنازل وتوزيع المساعدات ودعم الشباب.'),
          ('Volunteer with us | Iraq Builders Organization','Register as a volunteer with Iraq Builders and help renovate homes, distribute aid and support young people.'),volunteer),
 'donate':(('تبرع الآن | منظمة بناة العراق الخيرية','تبرع لمنظمة بناة العراق عبر ماستر كارد (الرافدين) أو زين كاش لدعم ترميم المنازل والمساعدات الغذائية والدعم الطبي وتمكين الشباب.'),
          ('Donate now | Iraq Builders Organization','Donate to Iraq Builders by Mastercard (Al-Rafidain) or Zain Cash to support home renovation, food aid, medical support and youth empowerment.'),donate),
 'contact':(('تواصل معنا | منظمة بناة العراق الخيرية','تواصل مع منظمة بناة العراق عبر واتساب أو فيسبوك أو إنستغرام أو يوتيوب.'),
          ('Contact us | Iraq Builders Organization','Contact Iraq Builders on WhatsApp, Facebook, Instagram or YouTube.'),contact),
}

for lang in ('ar','en'):
    LG=lang; P='' if lang=='ar' else '../'
    for pg,(ar,en,fn) in META.items():
        title,desc=ar if lang=='ar' else en
        write(pg+'.html',title,desc,fn())

LG='ar';P=''
write('404.html','الصفحة غير موجودة | منظمة بناة العراق','الصفحة التي تبحث عنها غير موجودة.',
 hero_page('الصفحة غير موجودة','ربما نُقلت الصفحة أو تغيّر رابطها.')+'<section><div class="container"><p><a class="btn btn-green" href="/index.html">العودة إلى الصفحة الرئيسية</a></p></div></section>')
urls=[]
for pg in ['index']+[p for p in META if p not in ('index','news-item')]:
    f='' if pg=='index' else pg+'.html'
    urls+= [BASE+f, BASE+'en/'+f]
open(OUT+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc></url>\n' for u in urls)+'</urlset>\n')
open(OUT+'robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /cms/\nDisallow: /new/\nSitemap: {BASE}sitemap.xml\n')
print('built')
# صفحة 404: روابط مطلقة من الجذر
_p=OUT+'404.html';_h=open(_p,encoding='utf8').read().replace('<head>','<head>\n<base href="/">',1);open(_p,'w',encoding='utf8').write(_h)
