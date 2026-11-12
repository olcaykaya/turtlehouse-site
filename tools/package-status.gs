/**
 * Turtle House — automatic "Package status" sheet in every client month folder.
 *
 * Folder layout it expects (same as today):
 *   ROOT (your clients folder)
 *     └ AnyDay                      ← client folder
 *         └ Anyday-October-2026     ← month folder (one per month)
 *             ├ Videos   ├ Photos   └ Horizontal
 *
 * 1. Fill the "Packages" sheet that the script creates (one row per client: how many of each are included per month).
 * 2. The script counts the files in Videos / Photos / Horizontal of every month folder and writes
 *    "📦 Package status" (a Google Sheet) into that month folder. Clients with folder access can see it.
 * 3. Runs every hour automatically after you run setup() once.
 */

const ROOT_FOLDER_ID = '1QdrZ0D-EXrpl8fonoZvKVAto81bOwobf';   // the folder that contains AnyDay, Chefa, ... (from its URL)
const CATEGORIES = ['Videos', 'Photos', 'Horizontal'];  // sub-folder names = rows in the client table
const LABELS = { Videos: 'Reels / vertical videos', Photos: 'Photos', Horizontal: 'Horizontal videos' };
const STATUS_NAME = '📦 Package status';
const CONTACT = 'hi@turtlehouseproductions.com · 407 470 9303';

/** Run once: creates the Packages sheet (if needed), runs the update, installs the hourly trigger. */
function setup() {
  packagesSheet_();
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('updateAll').timeBased().everyHours(1).create();
  updateAll();
}

/** Master list you edit: Client folder name | Videos | Photos | Horizontal | Note */
function packagesSheet_() {
  const props = PropertiesService.getScriptProperties();
  let id = props.getProperty('PACKAGES_ID'), ss;
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; } }
  if (!ss) {
    ss = SpreadsheetApp.create('Turtle House — Client packages (private)');
    const sh = ss.getSheets()[0];
    sh.setName('Packages');
    sh.getRange(1, 1, 1, 5).setValues([['Client folder name', 'Videos', 'Photos', 'Horizontal', 'Note shown to client (optional)']]).setFontWeight('bold');
    const root = DriveApp.getFolderById(ROOT_FOLDER_ID);
    const rows = [], it = root.getFolders();
    while (it.hasNext()) rows.push([it.next().getName(), 0, 0, 0, '']);
    if (rows.length) sh.getRange(2, 1, rows.length, 5).setValues(rows);
    sh.setFrozenRows(1); sh.autoResizeColumns(1, 5);
    props.setProperty('PACKAGES_ID', ss.getId());
    Logger.log('Packages sheet created: ' + ss.getUrl() + '  ← fill in the numbers');
  }
  return ss.getSheetByName('Packages');
}

function readPackages_() {
  const v = packagesSheet_().getDataRange().getValues(), out = {};
  v.slice(1).forEach(r => { if (r[0]) out[String(r[0]).trim().toLowerCase()] = { Videos: +r[1] || 0, Photos: +r[2] || 0, Horizontal: +r[3] || 0, note: r[4] || '' }; });
  return out;
}

function countFiles_(folder) {
  let n = 0;
  const f = folder.getFiles();
  while (f.hasNext()) { const file = f.next(); if (!file.getName().startsWith('.') && file.getName() !== STATUS_NAME) n++; }
  const sub = folder.getFolders();
  while (sub.hasNext()) n += countFiles_(sub.next());
  return n;
}

function updateAll() {
  const pk = readPackages_();
  const clients = DriveApp.getFolderById(ROOT_FOLDER_ID).getFolders();
  while (clients.hasNext()) {
    const client = clients.next(), p = pk[client.getName().trim().toLowerCase()];
    if (!p) continue;                                   // client not in Packages sheet → skip
    // only the newest month folder (the one that has Videos / Photos / Horizontal) gets a status sheet
    const months = client.getFolders();
    let latest = null;
    while (months.hasNext()) {
      const m = months.next();
      if (!CATEGORIES.some(c => m.getFoldersByName(c).hasNext())) continue;
      if (!latest || m.getDateCreated() > latest.getDateCreated()) latest = m;
    }
    if (!latest) continue;
    const counts = {};
    CATEGORIES.forEach(c => { const it = latest.getFoldersByName(c); counts[c] = it.hasNext() ? countFiles_(it.next()) : 0; });
    writeStatus_(client.getName(), latest, p, counts);
  }
}

const SHORT = { Videos: ['Reel', 'Reels'], Photos: ['Photo', 'Photos'], Horizontal: ['Horizontal', 'Horizontal'] };

/** The status lives in a FOLDER NAME so clients see it without clicking: "📦 Remaining: 1 Reel · 0 Photos" */
function statusFolder_(month, title) {
  const props = PropertiesService.getScriptProperties(), key = 'SF_' + month.getId();
  let f = null, id = props.getProperty(key);
  if (id) { try { f = DriveApp.getFolderById(id); if (f.isTrashed()) f = null; } catch (e) { f = null; } }
  if (!f) { f = month.createFolder(title); props.setProperty(key, f.getId()); }
  if (f.getName() !== title) f.setName(title);
  return f;
}

function writeStatus_(clientName, month, p, counts) {
  const parts = [];
  let left = 0;
  CATEGORIES.forEach(c => {
    if (p[c] > 0) { const r = Math.max(0, p[c] - counts[c]); left += r; parts.push(r + ' ' + SHORT[c][r === 1 ? 0 : 1]); }
  });
  const title = left === 0 ? '✅ Package complete — all delivered' : '📦 Remaining: ' + parts.join(' · ');
  const folder = statusFolder_(month, title);
  const it = folder.getFilesByName(STATUS_NAME);
  let ss;
  if (it.hasNext()) ss = SpreadsheetApp.openById(it.next().getId());
  else {
    ss = SpreadsheetApp.create(STATUS_NAME);
    DriveApp.getFileById(ss.getId()).moveTo(folder);
  }
  const sh = ss.getSheets()[0];
  sh.clear(); sh.setName('Status');
  const rows = [[clientName + ' — ' + month.getName(), '', '', ''], ['', '', '', ''], ['', 'Included', 'Delivered', 'Remaining']];
  CATEGORIES.forEach(c => { if (p[c] > 0 || counts[c] > 0) rows.push([LABELS[c], p[c], counts[c], Math.max(0, p[c] - counts[c])]); });
  rows.push(['', '', '', '']);
  rows.push(['Last updated: ' + Utilities.formatDate(new Date(), 'America/New_York', 'MMM d, yyyy h:mm a') + ' (ET)', '', '', '']);
  if (p.note) rows.push([p.note, '', '', '']);
  rows.push(['Questions? ' + CONTACT, '', '', '']);
  sh.getRange(1, 1, rows.length, 4).setValues(rows);
  sh.getRange(1, 1).setFontSize(16).setFontWeight('bold');
  sh.getRange(3, 1, 1, 4).setFontWeight('bold').setBackground('#121212').setFontColor('#ffffff');
  const n = rows.length - 3 - (p.note ? 4 : 3);
  if (n > 0) {
    sh.getRange(4, 4, n, 1).setFontWeight('bold').setFontColor('#ff4a1c');
    sh.getRange(4, 1, n, 4).setFontSize(13);
  }
  sh.setColumnWidth(1, 260); [2, 3, 4].forEach(c => sh.setColumnWidth(c, 110));
  sh.getRange(3, 2, n + 1, 3).setHorizontalAlignment('center');
  sh.setHiddenGridlines(true);
}
