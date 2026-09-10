// V11177 · T1.6 — DOM/JS-LEVEL ASSERTION tren DUNG BYTES ma /du-doan dang phuc vu.
// Khong tai dung logic bang Python; TRICH NGUYEN VAN ham JS tu trang da phuc vu
// roi thuc thi chung trong runtime JS that.
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync(__dirname + '/served.html', 'utf8');

function trichHam(ten) {
  const i = html.indexOf('function ' + ten + '(');
  if (i < 0) throw new Error('khong tim thay ham ' + ten);
  let d = 0, j = html.indexOf('{', i), k = j;
  for (; k < html.length; k++) {
    if (html[k] === '{') d++;
    else if (html[k] === '}') { d--; if (d === 0) break; }
  }
  return html.slice(i, k + 1);
}

const src = trichHam('_v11177_canon');
const ctx = { Object: Object, console: console };
vm.createContext(ctx);
vm.runInContext(src, ctx);
vm.runInContext(`
  function chon(response, bundle, sourcePreds) {
    var c = _v11177_canon(response, bundle, 'quality_filtered_models');
    var ds = c.canonical ? c.list : [];
    if (!c.canonical && sourcePreds && sourcePreds.wr_gate_filtered) ds = sourcePreds.wr_gate_filtered;
    return { ds: ds, canonical: c.canonical, dem: c.canonical ? ds.length : null };
  }
`, ctx);

let dat = 0, hong = 0;
function ok(t, c, g) {
  if (c) { dat++; console.log('  DAT  ' + t + (g ? '   ' + g : '')); }
  else { hong++; console.log('  HONG ' + t + (g ? '   ' + g : '')); }
}
const CAP = ['claude-opus-4-6', 'claude-sonnet-4-6'];
const XAU = ['gpt-5-mini'];
const chon = ctx.chon;

console.log('='.repeat(86));
console.log('  V11177 · DOM/JS-LEVEL — chay ham JS THAT trich tu trang /du-doan dang phuc vu');
console.log('='.repeat(86));

ok('J0 ham _v11177_canon CO trong bytes dang phuc vu', src.indexOf('_v11177_canon') >= 0);

let r = chon({}, {}, { wr_gate_filtered: CAP.concat(XAU) });
ok('J1 FIELD_ABSENT => fallback legacy', r.canonical === false && r.ds.length === 3, JSON.stringify(r.ds));

r = chon({ quality_filtered_models: [] }, {}, { wr_gate_filtered: CAP });
ok('J2 FIELD_PRESENT_EMPTY => giu [], KHONG fallback', r.canonical === true && r.ds.length === 0, JSON.stringify(r.ds));

r = chon({ quality_filtered_models: XAU }, {}, { wr_gate_filtered: CAP.concat(XAU) });
ok('J3 FIELD_PRESENT_NON_EMPTY => dung canonical', r.ds.length === 1 && r.ds[0] === 'gpt-5-mini', JSON.stringify(r.ds));

// FIXTURE THAT: MT 2026-09-10 — DB tho co 2 model bi TRAN, API tra []
r = chon({ quality_filtered_models: [], quality_filtered_model_count: 2 }, {},
         { wr_gate_filtered: ['claude-opus-4-6', 'claude-sonnet-4-6'] });
ok('J4 FIXTURE MT 10/09: UI KHONG hien 2 model bi TRAN',
   r.ds.length === 0 && CAP.every(m => r.ds.indexOf(m) < 0), 'hien=' + JSON.stringify(r.ds));
ok('J5 FIXTURE MT 10/09: dem = 0, dong nhat voi danh sach', r.dem === 0, 'dem=' + r.dem);

r = chon({ quality_filtered_models: XAU }, {}, { wr_gate_filtered: CAP.concat(XAU) });
ok('J6 loi chat luong THAT van hien (khong tay trang)', r.ds.indexOf('gpt-5-mini') >= 0, JSON.stringify(r.ds));

r = chon({ quality_filtered_models: null }, { quality_filtered_models: [] }, { wr_gate_filtered: CAP });
ok('J7 response null nhung bundle CO [] => dung bundle, KHONG fallback', r.canonical === true && r.ds.length === 0, JSON.stringify(r.ds));

// bat bien: khong con duong fallback cu
ok('J8 KHONG con `!filteredModels.length &&` cu trong bytes phuc vu',
   html.indexOf('if (!filteredModels.length && sourcePreds') < 0);
ok('J9 KHONG con `!qualityFilteredModels.length &&` cu',
   html.indexOf('if (!qualityFilteredModels.length && sourcePreds') < 0);

console.log('='.repeat(86));
console.log('  TONG: ' + dat + '/' + (dat + hong) + ' DAT');
console.log('='.repeat(86));
process.exit(hong ? 1 : 0);
