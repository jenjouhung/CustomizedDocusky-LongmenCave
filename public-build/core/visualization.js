import {label,sortFacets} from './facets.js';

export function normalizeSearch(value){return String(value??'').toLocaleLowerCase()}
export function prepareItems(items,query='',sort='count-desc'){
 const term=normalizeSearch(query);
 return sortFacets(items,sort).map(item=>({...item,label:label(item.value),matched:!term||normalizeSearch(label(item.value)).includes(term)}));
}
export function zoomRowHeight(zoom){const n=Math.max(10,Math.min(200,Number(zoom)||100));return 12+(n-10)*.4}
export function zoomLabelSize(zoom){const n=Math.max(10,Math.min(200,Number(zoom)||100));return Math.round((12+(n-10)*.08)*100)/100}
export class VisualizationState{
 constructor(){this.source=null;this.search='';this.sort='count-desc';this.palette='pine';this.selected=new Set();this.zoom={bar:100}}
 setSource(source,preferredSort='count-desc'){if(this.source===source)return;this.source=source;this.search='';this.sort=['count-desc','title-asc'].includes(preferredSort)?preferredSort:'count-desc';this.selected.clear();this.zoom.bar=100}
 toggle(value){this.selected.has(value)?this.selected.delete(value):this.selected.add(value)}
 clearSelection(){this.selected.clear()}
}
