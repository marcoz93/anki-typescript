#!/usr/bin/env node
// End-to-end check of Mathua's existing interface against the real pilot API.
// The interface must be built with NEXT_PUBLIC_TS_PILOT=1 and NEXT_PUBLIC_SAME_ORIGIN_API=1.
// Answers come from the editorial package in conteudo/typescript-v1, found by the visible question.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { existsSync, mkdtempSync, openSync, closeSync, readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const { values } = parseArgs({ options: {
  mathua: { type: 'string' }, binary: { type: 'string', default: 'pilot-bin' },
  output: { type: 'string' }, 'chromium-module': { type: 'string' },
  // Optional directory for PNG captures of the study path.
  screenshots: { type: 'string' },
  // Editorial package; default is conteudo/typescript-v1 of the repository holding this script.
  content: { type: 'string' },
} });
assert(values.mathua, 'Use --mathua with the patched Mathua clone.');
const root = path.resolve(values.mathua);
const binary = path.resolve(root, values.binary);
assert(existsSync(binary), 'Build pilot-bin before this test.');
assert(existsSync(path.join(root, 'web/next-app/out/learn.html')), 'Build the frontend with NEXT_PUBLIC_TS_PILOT=1 NEXT_PUBLIC_SAME_ORIGIN_API=1 first.');
const contentDir = path.resolve(values.content ?? path.join(path.dirname(fileURLToPath(import.meta.url)), '../../../conteudo/typescript-v1'));
const families = JSON.parse(readFileSync(path.join(contentDir, 'exercicios.json'), 'utf8')).families;
const { chromium } = await import(pathToFileURL(path.join(root, 'web/next-app/node_modules/playwright/index.mjs')));
const provider = values['chromium-module'] ? (await import(pathToFileURL(path.resolve(values['chromium-module'])))).default : null;
const work = mkdtempSync(path.join(tmpdir(), 'mathua-browser-'));
const logPath = path.join(work, 'server.log');
const probe = createServer();
await new Promise(resolve => probe.listen(0, '127.0.0.1', resolve));
const port = probe.address().port;
await new Promise(resolve => probe.close(resolve));
const base = `http://127.0.0.1:${port}`;
const shots = values.screenshots ? path.resolve(values.screenshots) : null;
if (shots) mkdirSync(shots, { recursive: true });
const result = { passed: false, platform: `${process.platform} ${process.arch}`, node: process.version, browser: '', checks: [], screenshots: [], practice_fetches: [], page_errors: [], api_errors: [] };
let browser;
let page;
let server;
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
const check = (name, observed) => result.checks.push({ name, passed: true, observed });

// The same database is reused across starts, so a restart keeps the learner's progress.
async function startServer() {
  const fd = openSync(logPath, 'a');
  server = spawn(binary, ['-addr', `127.0.0.1:${port}`, '-db', path.join(work, 'pilot.db'), '-content', contentDir], { cwd: root, stdio: ['ignore', fd, fd] });
  closeSync(fd);
  const deadline = Date.now() + 60000;
  while (true) {
    assert(server.exitCode === null, `Pilot exited: ${readFileSync(logPath, 'utf8')}`);
    try { if ((await fetch(base + '/api/health')).ok) break; } catch { /* Wait for the listener. */ }
    assert(Date.now() < deadline, 'Pilot startup timed out.');
    await pause(100);
  }
}
async function stopServer() {
  if (server.exitCode !== null || server.signalCode !== null) return;
  server.kill('SIGTERM');
  await Promise.race([new Promise(resolve => server.once('exit', resolve)), pause(3000)]);
  if (server.exitCode === null && server.signalCode === null) server.kill('SIGKILL');
}

// English source text of the study path. None of it may remain visible in the pilot build.
const ENGLISH = ['Your answer', 'Check', 'Not quite', 'you answered', 'Answer:', 'Next →', 'Practice again', 'Complete,',
  'Prerequisites', 'Required prerequisite', 'Not started', 'Study →', 'Choose another topic', 'Back to Profile',
  'Report a problem', "What's wrong?", 'Send report', 'Cancel', 'Thanks, reported', 'Task XP summary', 'Reference, the full lesson'];
// Destinations that show the bundled mathematics catalog or Mathua's own documentation.
const HIDDEN = ['/graph', '/glossary', '/docs', '/docs/contributing', '/how-it-works', '/note', '/announcements'];
// Destinations the learner needs: study, choose a topic, progress and own reports.
const REQUIRED = ['/learn', '/domains', '/history', '/reports', '/my-reports'];
// Whole-phrase match, so "Cancel" does not match "Cancelar".
const englishIn = text => ENGLISH.filter(s => new RegExp('(^|[^\\p{L}])' + s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '($|[^\\p{L}])', 'iu').test(text));

// The page renders `code` without the backticks and collapses whitespace.
const flat = text => text.replace(/`/g, '').replace(/\s+/g, ' ').trim();
// Finds the family and case shown in a question card of a concept. Prompt and context code together
// identify one case inside a concept; the longest context wins when one prompt is a prefix of another.
function caseOnCard(conceptId, cardText) {
  const shown = flat(cardText);
  let best = null;
  for (const family of families.filter(f => f.concept_id === conceptId)) {
    for (const item of family.cases) {
      const context = item.context_code.split('\n').map(flat).filter(Boolean);
      if (!shown.includes(flat(item.prompt)) || !context.every(line => shown.includes(line))) continue;
      const weight = flat(item.prompt).length + context.join(' ').length;
      if (!best || weight > best.weight) best = { family, item, weight };
    }
  }
  assert(best, `No case of ${conceptId} matches the card: ${shown.slice(0, 300)}`);
  return best;
}

try {
  await startServer();
  browser = await chromium.launch(provider ? { executablePath: await provider.executablePath(), args: provider.args, headless: true } : { headless: true });
  result.browser = browser.version();
  page = await browser.newPage({ viewport: { width: 1280, height: 900 }, serviceWorkers: 'block' });
  page.setDefaultTimeout(15000);
  page.on('pageerror', error => result.page_errors.push(error.message));
  page.on('response', async response => {
    const url = new URL(response.url());
    const pathname = url.pathname;
    if (pathname.startsWith('/api/lessons') && response.status() >= 400) result.api_errors.push({ path: pathname, status: response.status() });
    // Every practice fetch: what the page asked to exclude and which cases the server served.
    const practice = /^\/api\/lessons\/([^/]+)\/practice$/.exec(pathname);
    if (practice && response.status() === 200) {
      const body = await response.json().catch(() => null);
      const id = decodeURIComponent(practice[1]);
      result.practice_fetches.push({ concept: id, section: Number(url.searchParams.get('kp_ordinal') || 0), excluded: url.searchParams.getAll('exclude').length,
        served: (body?.questions ?? []).map(q => caseOnCard(id, q.question).item.id) });
    }
  });
  const answerInput = page.getByRole('textbox', { name: 'Sua resposta', exact: true });
  const mainText = async () => (await page.locator('main').innerText());
  const shot = async name => {
    if (!shots) return;
    await page.screenshot({ path: path.join(shots, name + '.png') });
    result.screenshots.push(name + '.png');
  };
  // Visible text only: an English word inside a served question or lesson would be content, and none is.
  const assertPortuguese = async where => {
    const found = englishIn(await mainText());
    assert.deepEqual(found, [], `English study text at ${where}: ${found.join(', ')}`);
  };
  const concept = () => new URL(page.url()).searchParams.get('concept');

  async function openConcept(id) {
    await page.goto(`${base}/learn?concept=${id}`, { waitUntil: 'domcontentloaded' });
  }
  async function followRecommendation(id) {
    const link = page.locator(`a:visible[href^="/learn?concept=${id}"]`).first();
    await link.waitFor();
    const label = await link.innerText();
    await link.click();
    await page.waitForURL(url => url.searchParams.get('concept') === id);
    check('navigation_to_' + id, { label, concept: id });
  }
  // The open question card: the one whose answer field is still editable.
  async function answerCard() {
    for (let i = 0; i < 150; i++) {
      if (await answerInput.isVisible().catch(() => false)) return answerInput.locator('xpath=ancestor::form/..');
      const next = page.getByRole('button', { name: /^(Próximo →|Praticar novamente(?: →)?)$/ }).first();
      if (await next.isVisible().catch(() => false)) await next.click();
      await pause(100);
    }
    throw new Error('No answer field: ' + (await page.locator('body').innerText()).slice(-2500));
  }
  async function currentCase() {
    const card = await answerCard();
    return { card, ...caseOnCard(concept(), await card.innerText()) };
  }
  // how: 'fill' sets the field, 'type' presses each key, 'tap' clicks the button of an alternative.
  async function submit(card, answer, how = 'fill') {
    if (how === 'tap') {
      await card.getByRole('button', { name: new RegExp('^' + answer + '\\b') }).click();
      assert.equal(await answerInput.inputValue(), answer);
    } else if (how === 'type') {
      await answerInput.click();
      await answerInput.pressSequentially(answer, { delay: 5 });
      assert.equal(await answerInput.inputValue(), answer);
    } else {
      await answerInput.fill(answer);
    }
    // The real API requires elapsed >= MinAnswerSeconds. Simulate a readable response time.
    await pause(400);
    const pending = page.waitForResponse(r => r.url() === base + '/api/study/answer' && r.request().method() === 'POST');
    await page.getByRole('button', { name: 'Verificar', exact: true }).click();
    const response = await pending;
    assert.equal(response.status(), 200);
    const body = await response.json();
    // The normal response can omit ungraded. Only true means the grader failed.
    assert.notEqual(body.ungraded, true);
    await pause(450);
    return { body, request: response.request().postDataJSON() };
  }
  // Answers the concept correctly until the engine reports MASTERED. Returns what was served.
  // fresh: the concept was not practised before in this run, so the rotation starts clean.
  async function master(id, how, variant = answer => answer, fresh = true) {
    const served = [];
    for (let attempt = 0; attempt < 14; attempt++) {
      const { card, family, item } = await currentCase();
      const answer = variant(item.answer);
      const done = await submit(card, answer, how);
      assert.equal(done.body.correct, true, `${item.id}: ${answer} rejected: ${done.body.feedback}`);
      served.push({ family: family.id, case: item.id, answer });
      if (served.length === 1) assert.notEqual(done.body.new_status, 'MASTERED');
      if (done.body.new_status === 'MASTERED') {
        const distinct = new Set(served.map(s => s.case)).size;
        // The bank of a section is finite. No case may come back before the others were shown.
        if (fresh) assert.equal(distinct, Math.min(served.length, family.cases.length), `${id} repeated a case early: ${served.map(s => s.case).join(' ')}`);
        check('mastery_through_browser_' + id, { answers: served.length, new_status: 'MASTERED', distinct_cases: distinct, cases: served.map(s => s.case), sample_answer: answer });
        return served;
      }
    }
    throw new Error(`${id} not mastered after 14 correct answers`);
  }
  async function authenticatedJSON(route) {
    return page.evaluate(async route => {
      const token = localStorage.getItem('mathua_token') || localStorage.getItem('mathua_guest_token');
      const response = await fetch(route, { headers: { Authorization: `Bearer ${token}` } });
      if (!response.ok) throw new Error(`HTTP ${response.status}: ${route}`);
      return response.json();
    }, route);
  }

  // 1. The address opens the first concept of the ladder with its lesson.
  const home = await page.goto(base, { waitUntil: 'domcontentloaded' });
  assert.equal(home.status(), 200);
  assert.equal(concept(), 'ts.value.literal_notation');
  await page.locator('p:visible').filter({ hasText: 'Um valor é aquilo com que o programa opera.' }).first().waitFor();
  await page.getByRole('button', { name: 'Próximo →', exact: true }).first().waitFor();
  await assertPortuguese('lesson');
  await shot('01-aula');
  check('home_opens_first_concept_with_its_lesson', { status: home.status(), concept: concept() });

  // Navigation fit for the pilot: nothing leads to the mathematics catalog, the study functions stay.
  const hrefs = await page.evaluate(() => [...new Set([...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')))]);
  assert.deepEqual(HIDDEN.filter(h => hrefs.includes(h)), [], 'Navigation still links to the mathematics catalog.');
  assert.deepEqual(REQUIRED.filter(h => !hrefs.includes(h)), [], 'Navigation lost a destination the learner needs.');
  const sidebarLabels = await page.locator('[data-sidebar="menu-button"]:visible').allInnerTexts();
  for (const label of ['Estudar', 'Histórico', 'Relatório de progresso', 'Meus relatos e avisos']) {
    assert(sidebarLabels.some(text => text.trim() === label), `Sidebar entry missing: ${label}`);
  }
  check('navigation_fits_the_pilot', { hidden_absent: HIDDEN, required_present: REQUIRED, sidebar: sidebarLabels.map(t => t.replace(/\s+/g, ' ').trim()).filter(Boolean) });

  // 2. A concept with unmet prerequisites shows them and offers no answer field.
  await openConcept('ts.binding.const_number');
  const locked = page.getByRole('note', { name: 'Pré-requisitos', exact: true });
  await locked.waitFor();
  assert.equal(await answerInput.count(), 0);
  assert.match(await locked.innerText(), /Você ainda não pode praticar este tópico/);
  await assertPortuguese('locked concept');
  await shot('02-pre-requisitos');
  check('ui_blocks_unmet_prerequisites', { concept: 'ts.binding.const_number', answer_fields: 0 });

  // 3. A new concept answered by tapping alternatives: a miss, a variant of the same family, mastery.
  await openConcept('ts.value.literal_notation');
  let shown = await currentCase();
  assert.equal(await page.locator('button[aria-label^="Insert "]').count(), 0, 'The mathematical symbol palette is still rendered.');
  assert.equal(await shown.card.getByRole('button', { name: /^[A-D]\b/ }).count(), 4);
  await assertPortuguese('choice question');
  await shot('03-pergunta-de-alternativas');
  const wrongLetter = ['A', 'B', 'C', 'D'].find(letter => letter !== shown.item.answer);
  const missed = await submit(shown.card, wrongLetter, 'tap');
  assert.equal(missed.body.correct, false);
  await page.getByText('✗ Ainda não.', { exact: false }).waitFor();
  await page.getByText(shown.item.explanation, { exact: false }).first().waitFor();
  await shot('04-correcao-de-alternativa');
  const after = await currentCase();
  assert.equal(after.family.id, shown.family.id);
  assert.notEqual(after.item.id, shown.item.id);
  check('choice_miss_shows_instance_explanation_and_same_family_variant', { family: shown.family.id, missed_case: shown.item.id, tapped: wrongLetter,
    reference_shown: missed.body.expected_answer, explanation_shown: shown.item.explanation, variant_case: after.item.id });
  await master('ts.value.literal_notation', 'tap', answer => answer, false);
  const unlocked = await authenticatedJSON('/api/lessons/ts.value.string_literal/readiness');
  assert.equal(unlocked.eligible, true);
  check('new_concept_mastery_unlocks_its_dependent', { mastered: 'ts.value.literal_notation', eligible: 'ts.value.string_literal' });

  // 4. The three original concepts keep their IDs. A numeric separator is a valid answer that
  //    differs from the model answer.
  await openConcept('ts.value.numeric_literal');
  await master('ts.value.numeric_literal', 'type', answer => answer.replace(/(\d)(\d{3})$/, '$1_$2'));
  await openConcept('ts.type.number');
  await master('ts.type.number', 'fill');
  await followRecommendation('ts.binding.const_number');

  // 5. Code answer: a miss shows what is wrong with it, then a variant accepts an inferred type.
  shown = await currentCase();
  const letAnswer = shown.item.answer.replace('const ', 'let ');
  const wrong = await submit(shown.card, letAnswer, 'type');
  assert.equal(wrong.body.correct, false);
  await page.getByText('✗ Ainda não.', { exact: false }).waitFor();
  await page.getByText('A tarefa pede const', { exact: false }).waitFor();
  await page.getByText('Resposta:', { exact: false }).first().waitFor();
  await assertPortuguese('wrong answer');
  await shot('05-correcao-de-codigo');
  const variant = await currentCase();
  assert.equal(variant.family.id, 'F010');
  assert.notEqual(variant.item.id, shown.item.id);
  const inferred = variant.item.answer.replace(': number', '').replace(/;$/, '');
  assert.notEqual(inferred, variant.item.answer);
  const correct = await submit(variant.card, inferred, 'type');
  assert.equal(correct.body.correct, true);
  await page.getByText(`você respondeu “${inferred}”`, { exact: false }).waitFor();
  check('code_miss_names_the_cause_then_variant_accepts_valid_alternative', { missed_case: shown.item.id, wrong_answer: letAnswer,
    cause_shown: wrong.body.feedback, variant_case: variant.item.id, model_answer: variant.item.answer, accepted_answer: inferred });
  check('study_path_text_is_portuguese', { english_source_strings_checked: ENGLISH.length,
    screens: ['lesson', 'locked concept', 'choice question', 'wrong answer', 'report dialog'] });

  // 6. Reporting a question keeps the question, the reference answer and the given answer.
  await page.getByRole('button', { name: 'Relatar um problema', exact: true }).nth(1).click();
  const dialog = page.getByRole('dialog', { name: 'Relatar um problema', exact: true });
  await dialog.getByRole('combobox').selectOption('unclear');
  await dialog.getByRole('textbox').fill('Teste de feedback: confirmar que a anotação é opcional neste exercício.');
  assert.deepEqual(englishIn(await dialog.innerText()), []);
  await shot('06-relato');
  const reportResponse = page.waitForResponse(r => r.url() === base + '/api/reports' && r.request().method() === 'POST');
  await dialog.getByRole('button', { name: 'Enviar relato', exact: true }).click();
  const sent = await reportResponse;
  assert.equal(sent.status(), 200);
  const reportRequest = sent.request().postDataJSON();
  assert.equal(reportRequest.expected, correct.body.expected_answer);
  assert.equal(reportRequest.answer_given, inferred);
  assert.equal(reportRequest.question, correct.request.question);
  await page.getByText('Obrigado, relato enviado', { exact: false }).waitFor();
  const mine = await authenticatedJSON('/api/reports/mine');
  assert.equal(mine.reports.length, 1);
  // The stored concept and question identify the family and the case under review.
  const reported = caseOnCard(mine.reports[0].concept_id, mine.reports[0].question);
  assert.equal(reported.item.id, variant.item.id);
  check('report_keeps_question_reference_and_given_answer', { report_id: mine.reports[0].id, status: mine.reports[0].status,
    concept: mine.reports[0].concept_id, family: reported.family.id, case: reported.item.id, expected: reportRequest.expected, answer_given: reportRequest.answer_given });
  await page.goto(`${base}/my-reports`, { waitUntil: 'domcontentloaded' });
  await page.getByText('Teste de feedback: confirmar que a anotação é opcional neste exercício.', { exact: false }).waitFor();
  await shot('07-meus-relatos');
  check('learner_reads_own_report_on_my_reports_page', { reports_listed: 1, report_id: mine.reports[0].id });

  // 7. A concept with two families: each section serves one family, also after a miss.
  await openConcept('ts.binding.const_semantics');
  const sections = [];
  for (const familyId of ['F009', 'F013']) {
    shown = await currentCase();
    assert.equal(shown.family.id, familyId);
    const letter = ['A', 'B', 'C', 'D'].find(l => l !== shown.item.answer);
    assert.equal((await submit(shown.card, letter, 'tap')).body.correct, false);
    const cases = [shown.item.id];
    // Two correct answers in a row close a section of the existing stepper.
    for (let i = 0; i < 2; i++) {
      const next = await currentCase();
      assert.equal(next.family.id, familyId, `section of ${familyId} served ${next.item.id}`);
      assert(!cases.includes(next.item.id), `${next.item.id} repeated inside the section`);
      cases.push(next.item.id);
      assert.equal((await submit(next.card, next.item.answer, 'tap')).body.correct, true);
    }
    if (familyId === 'F013') await shot('08-secao-com-codigo-de-contexto');
    sections.push({ family: familyId, cases });
  }
  check('each_section_keeps_its_family_after_a_miss', { concept: 'ts.binding.const_semantics', sections });

  // 8. Progress survives a reload and a real restart on the same database.
  await openConcept('ts.binding.const_number');
  await answerCard();
  let readiness = await authenticatedJSON('/api/lessons/ts.binding.const_number/readiness');
  assert.equal(readiness.eligible, true);
  assert(readiness.prerequisites.every(p => p.met));
  await page.reload({ waitUntil: 'domcontentloaded' });
  await answerCard();
  check('reload_preserves_identity_and_prerequisite_progress', { eligible: readiness.eligible });
  await stopServer();
  await startServer();
  await page.reload({ waitUntil: 'domcontentloaded' });
  await answerCard();
  readiness = await authenticatedJSON('/api/lessons/ts.binding.const_number/readiness');
  assert.equal(readiness.eligible, true);
  assert(readiness.prerequisites.every(p => p.met));
  const afterRestart = await authenticatedJSON('/api/reports/mine');
  assert.equal(afterRestart.reports.length, 1);
  check('server_restart_preserves_progress_and_reports', { processes_started: 2, eligible: readiness.eligible, reports: afterRestart.reports.length });

  assert.deepEqual(result.page_errors, []);
  assert.deepEqual(result.api_errors, []);
  result.passed = true;
} catch (error) {
  result.error = error.stack || error.message;
  if (page) result.visible_page = await page.locator('body').innerText().catch(() => 'Page unavailable');
  process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  if (server) await stopServer();
  if (!result.passed) result.server_log = readFileSync(logPath, 'utf8').slice(-6000);
  rmSync(work, { recursive: true, force: true });
}

const output = JSON.stringify(result, null, 2) + '\n';
if (values.output) {
  mkdirSync(path.dirname(path.resolve(values.output)), { recursive: true });
  writeFileSync(values.output, output);
}
process.stdout.write(output);
