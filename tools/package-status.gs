/**
 * Turtle House — delivery counter in folder names (clients see it without clicking).
 *
 * HOW TO USE (inside any client month folder, e.g. AnyDay / Anyday-October-2026):
 *   Create:   "Photos 10"   "Videos 5"            → package size = the number at the end
 *   Script renames every 5 min:  "Photos · 7 of 10 delivered · 3 left"   →   "Photos · 10 of 10 delivered ✓"
 *   Change package:   rename to "Photos 12"
 *   Fix a wrong count: rename to "Photos 10 =8"   (= delivered so far; later uploads keep counting on top)
 *
 * Counts every file inside the folder (sub-folders included). Run setup() once.
 */

const ROOT_FOLDER_ID = '1QdrZ0D-EXrpl8fonoZvKVAto81bOwobf';  // folder that contains AnyDay, Chefa, ...
const MAX_DEPTH = 4;                                          // root → client → month → Photos

function setup() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('updateAll').timeBased().everyMinutes(5).create();
  updateAll();
}

function updateAll() {
  const props = PropertiesService.getScriptProperties();
  walk_(DriveApp.getFolderById(ROOT_FOLDER_ID), 0, props);
}

function walk_(folder, depth, props) {
  if (depth > MAX_DEPTH) return;
  const it = folder.getFolders();
  while (it.hasNext()) {
    const f = it.next();
    if (!handle_(f, props)) walk_(f, depth + 1, props);   // tracked folders are leaves; don't descend
  }
}

/** returns true if this folder is a tracked deliverable folder */
function handle_(f, props) {
  const key = 'T_' + f.getId(), name = f.getName().trim();
  let st = JSON.parse(props.getProperty(key) || 'null');

  // 1) user typed "Name 10" or "Name 10 =8" (new folder, or edited an existing one)
  const m = name.match(/^(.*?\S)\s+(\d{1,4})(?:\s*=\s*(\d{1,4}))?$/);
  if (m && name.indexOf(' · ') < 0) {
    const actual = count_(f);
    st = { base: m[1], target: +m[2], offset: st ? st.offset : 0 };
    if (m[3] !== undefined) st.offset = +m[3] - actual;   // manual correction
    props.setProperty(key, JSON.stringify(st));
  }
  if (!st) return false;

  // 2) refresh the label
  const done = Math.max(0, count_(f) + (st.offset || 0));
  const left = Math.max(0, st.target - done);
  const label = left === 0
    ? `${st.base} · ${done} of ${st.target} delivered ✓`
    : `${st.base} · ${done} of ${st.target} delivered · ${left} left`;
  if (name !== label) f.setName(label);
  return true;
}

function count_(folder) {
  let n = 0;
  const files = folder.getFiles();
  while (files.hasNext()) { if (!files.next().getName().startsWith('.')) n++; }
  const subs = folder.getFolders();
  while (subs.hasNext()) n += count_(subs.next());
  return n;
}
