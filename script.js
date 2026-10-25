(()=>{
  const year=document.getElementById('current-year');if(year)year.textContent=new Date().getFullYear();
  const nav=document.getElementById('navigation'),toggle=document.getElementById('menu-toggle');
  const drop=document.querySelector('.nav-products');
  function closeMenu(){if(nav)nav.classList.remove('open');if(toggle){toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Open navigation')}if(drop)drop.open=false}
  if(nav&&toggle){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close navigation':'Open navigation')});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});document.addEventListener('click',e=>{if(!e.target.closest('.head-inner')&&nav.classList.contains('open'))closeMenu();if(drop?.open&&!e.target.closest('.nav-products'))drop.open=false});window.addEventListener('resize',()=>{if(window.innerWidth>780)closeMenu()})}
  const dialog=document.getElementById('lightbox');
  if(dialog){const photoButtons=[...document.querySelectorAll('[data-photo]')],pic=document.getElementById('lightbox-image'),cap=document.getElementById('lightbox-caption'),cnt=document.getElementById('lightbox-count');let active=0;
    function show(index){if(!photoButtons.length)return;active=(index+photoButtons.length)%photoButtons.length;const b=photoButtons[active];pic.src=b.dataset.photo;pic.alt=b.dataset.caption||'LED display photo';cap.textContent=b.dataset.caption||'';cnt.textContent=(active+1)+' / '+photoButtons.length}
    photoButtons.forEach((b,i)=>b.addEventListener('click',()=>{show(i);dialog.showModal()}));
    document.getElementById('lightbox-close')?.addEventListener('click',()=>dialog.close());
    document.getElementById('lightbox-prev')?.addEventListener('click',()=>show(active-1));
    document.getElementById('lightbox-next')?.addEventListener('click',()=>show(active+1));
    dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
    dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();show(active-1)}else if(e.key==='ArrowRight'){e.preventDefault();show(active+1)}})
  }
  const form=document.getElementById('quote-form');
  if(form){const product=document.getElementById('product');const qs=new URLSearchParams(location.search);if(qs.has('product')&&product){const chosen=qs.get('product');if([...product.options].some(o=>o.value===chosen))product.value=chosen}
    const status=document.getElementById('form-status');
    const labels={name:'Contact name',email:'Reply email',company:'Company',location:'Project location',product:'LED display category',width:'Width (metres)',height:'Height (metres)',environment:'Environment',stage:'Project stage',notes:'Further details'};
    function brief(){const data=new FormData(form);return ['CASTECHLED — LED DISPLAY EQUIPMENT INQUIRY','',...Object.entries(labels).map(([key,label])=>label+': '+(data.get(key)||'Not specified'))].join('\n')}
    form.addEventListener('submit',e=>{e.preventDefault();if(!form.reportValidity())return;const subject='CasTechLED — '+new FormData(form).get('product')+' equipment inquiry';status.textContent='Your email application should open. Please review and SEND the prepared email.';location.href='mailto:info@castechled.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(brief())});
    document.getElementById('copy-quote')?.addEventListener('click',async()=>{if(!form.reportValidity())return;const text=brief();try{await navigator.clipboard.writeText(text);status.textContent='Project brief copied. Paste it into an email to info@castechled.com.'}catch{const blob=new Blob([text],{type:'text/plain'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='castechled-project-inquiry.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1500);status.textContent='Project brief downloaded. Send it to info@castechled.com.'}})
  }
})();
