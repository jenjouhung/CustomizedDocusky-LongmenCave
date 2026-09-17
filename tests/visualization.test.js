import test from 'node:test';
import assert from 'node:assert/strict';
import {prepareItems,zoomRowHeight,zoomLabelSize,VisualizationState} from '../web/core/visualization.js';

const items=[{value:'"太妃"',count:7},{value:'"法僧"',count:3},{value:'"惠感"',count:4},{value:'"ABC"',count:2}];
test('視覺化搜尋保留全部項目並標記符合者',()=>{const result=prepareItems(items,'法','count-desc');assert.equal(result.length,4);assert.deepEqual(result.filter(x=>x.matched).map(x=>x.label),['法僧'])});
test('視覺化搜尋拉丁字母不分大小寫',()=>{assert.equal(prepareItems(items,'abc').filter(x=>x.matched).length,1);assert.equal(prepareItems(items,'ABC').filter(x=>x.matched).length,1)});
test('視覺化排序穩定',()=>{assert.deepEqual(prepareItems(items,'','count-desc').map(x=>x.label),['太妃','惠感','法僧','ABC']);assert.deepEqual(prepareItems(items,'','title-asc').map(x=>x.label),['太妃','法僧','惠感','ABC'])});
test('縮放高度限制於10至200百分比且新100等同舊140',()=>{assert.equal(zoomRowHeight(0),zoomRowHeight(100));assert.equal(zoomRowHeight(10),12);assert.equal(zoomRowHeight(100),48);assert.equal(zoomRowHeight(200),88);assert.equal(zoomRowHeight(500),88)});
test('縮放接受百分之一的連續值',()=>{assert.notEqual(zoomRowHeight(101),zoomRowHeight(110));assert.ok(zoomRowHeight(101)>=zoomRowHeight(100))});
test('標籤字級隨新縮放基準連續調整',()=>{assert.equal(zoomLabelSize(10),12);assert.equal(zoomLabelSize(100),19.2);assert.equal(zoomLabelSize(200),27.2);assert.ok(zoomLabelSize(101)>zoomLabelSize(100))});
test('標示與圖形縮放狀態獨立保存',()=>{const state=new VisualizationState();state.setSource('v1:field');state.toggle('"太妃"');state.zoom.bar=170;state.search='太';state.palette='moss';assert.ok(state.selected.has('"太妃"'));assert.equal(state.zoom.bar,170);state.setSource('v1:field');assert.equal(state.search,'太');state.setSource('v1:other');assert.equal(state.search,'');assert.equal(state.selected.size,0);assert.equal(state.palette,'moss')});
