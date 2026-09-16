const records=[
 {id:"0001",title:"孫秋生二百人等造石像記",no:"2296",era:"001_太和",month:"無",year:"493",cave:"古陽洞",place:"南壁",text:"邑主中散大夫、滎陽太守孫道務。大伐太和七年，新城縣功曹孫秋生、新城縣功曹劉起祖二百人等敬造石像一區。願國祚永隆，三寶彌顯。現世眷屬，萬福雲歸；五道群生，咸同此願。"},
 {id:"0002",title:"長樂王丘穆陵亮夫人尉遲造彌勒像記",no:"1840",era:"001_太和",month:"11",year:"495",cave:"古陽洞",place:"北壁",text:"太和十九年十一月，使持節、司空公、長樂王丘穆陵亮夫人尉遲，爲亡息牛橛請工鏤石，造此彌勒像一區。願牛橛捨於分段之鄉，騰遊無礙之境。一切眾生，咸蒙斯福。"},
 {id:"0003",title:"一弗造像記",no:"1841",era:"001_太和",month:"無",year:"496",cave:"古陽洞",place:"北壁",text:"太和廿年，步輦郎張元祖不幸喪亡，妻一弗爲造像一區。願令亡夫直生佛國。"}
];
const highlight=t=>t.replace(/(彌勒|眾生)/g,"<mark>$1</mark>");
function recordHTML(r){return `<article class="record"><header><div><h3>${r.title}</h3><div class="meta">題記 ${r.no}／序號 ${r.id} · ${r.era.replace(/^\d+_/,"")} ${r.month}月 · 西曆 ${r.year} 年 · ${r.cave} ${r.place}</div></div></header><p>${highlight(r.text)}</p><button class="open-record" data-id="${r.id}">查看全部 28 個欄位</button></article>`}
document.querySelectorAll(".records").forEach(el=>el.innerHTML=records.map(recordHTML).join(""));
function showView(name){document.querySelectorAll(".view").forEach(v=>v.hidden=v.id!==`view-${name}`);document.querySelectorAll(".switch").forEach(b=>b.classList.toggle("active",b.dataset.view===name));location.hash=name;window.scrollTo(0,0)}
document.addEventListener("click",e=>{
 const viewButton=e.target.closest("[data-view]");if(viewButton){showView(viewButton.dataset.view);return}
 if(e.target.closest(".filter-toggle")||e.target.closest(".close-drawer")){document.querySelector(".facet-drawer").classList.toggle("closed");return}
 if(e.target.closest(".clear-input")){e.target.closest(".view").querySelector("textarea,input").value="";return}
 if(e.target.closest(".run-query")){const v=e.target.closest(".view");v.querySelectorAll(".result-count").forEach(x=>x.textContent="12 筆");return}
 if(e.target.closest(".apply-filter")){const v=e.target.closest(".view");v.querySelectorAll(".result-count").forEach(x=>x.textContent="24 筆");return}
 if(e.target.closest(".simulate-zero")){const v=e.target.closest(".view");v.querySelectorAll(".records,.guided-grid,.guided-results,.reading-layout,.reading-summary").forEach(x=>x.hidden=true);v.querySelector(".zero-state").hidden=false;return}
 if(e.target.closest(".reset-all")){const v=e.target.closest(".view");v.querySelectorAll(".zero-state").forEach(x=>x.hidden=true);v.querySelectorAll(".records,.reading-layout,.reading-summary,.guided-grid").forEach(x=>x.hidden=false);v.querySelectorAll(".result-count").forEach(x=>x.textContent="153 筆");return}
 if(e.target.closest(".next-step")){const v=e.target.closest(".view");v.querySelector(".guided-grid").hidden=true;v.querySelector(".guided-results").hidden=false;return}
 if(e.target.closest(".back-filter")){const v=e.target.closest(".view");v.querySelector(".zero-state").hidden=true;v.querySelector(".guided-results").hidden=true;v.querySelector(".guided-grid").hidden=false;return}
 const open=e.target.closest(".open-record");if(open){const r=records.find(x=>x.id===open.dataset.id);document.querySelector("#dialog-content").innerHTML=`<div class="dialog-inner"><small>完整資料／v0003</small><h2>${r.title}</h2><div class="detail-grid"><div><small>序號 (filename)</small>${r.id}</div><div><small>題記編號</small>${r.no}</div><div><small>年號</small>${r.era}</div><div><small>西曆年</small>${r.year}</div><div><small>窟龕名</small>${r.cave}</div><div><small>窟內位置</small>${r.place}</div></div><div class="fulltext"><small>題記錄文</small><p>${highlight(r.text)}</p></div><p><small>雛形以代表性欄位呈現；正式介面將列出全部 28 個原始欄位。</small></p></div>`;document.querySelector("#record-dialog").showModal()}
 if(e.target.closest(".dialog-close"))document.querySelector("#record-dialog").close();
});
if(location.hash&&location.hash!=="#a")history.replaceState(null,"",location.pathname+"#a");
