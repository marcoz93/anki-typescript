#!/usr/bin/env node
// End-to-end check of Mathua's existing interface against the real pilot API.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { existsSync, mkdtempSync, openSync, closeSync, readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const { values } = parseArgs({ options: {
  mathua: { type: 'string' }, binary: { type: 'string', default: 'pilot-bin' },
  output: { type: 'string' }, 'chromium-module': { type: 'string' },
} });
assert(values.mathua, 'Use --mathua with the patched Mathua clone.');
const root = path.resolve(values.mathua);
const binary = path.resolve(root, values.binary);
assert(existsSync(binary), 'Build pilot-bin before this test.');
assert(existsSync(path.join(root, 'web/next-app/out/learn.html')), 'Build the frontend with NEXT_PUBLIC_SAME_ORIGIN_API=1 first.');
const { chromium } = await import(pathToFileURL(path.join(root, 'web/next-app/node_modules/playwright/index.mjs')));
const provider = values['chromium-module'] ? (await import(pathToFileURL(path.resolve(values['chromium-module'])))).default : null;
const work = mkdtempSync(path.join(tmpdir(), 'mathua-browser-'));
const logPath = path.join(work, 'server.log');
const fd = openSync(logPath, 'w');
const probe = createServer();
await new Promise(resolve => probe.listen(0, '127.0.0.1', resolve));
const port = probe.address().port;
await new Promise(resolve => probe.close(resolve));
const base = `http://127.0.0.1:${port}`;
const server = spawn(binary, ['-addr', `127.0.0.1:${port}`, '-db', path.join(work, 'pilot.db')], {
  cwd: root, stdio: ['ignore', fd, fd],
});
closeSync(fd);
const result = { passed: false, node: process.version, browser: '', checks: [], page_errors: [], api_errors: [] };
let browser;
let page;
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
const check = (name, observed) => result.checks.push({ name, passed: true, observed });

try {
  const deadline = Date.now() + 30000;
  while (true) {
    assert(server.exitCode === null, `Pilot exited: ${readFileSync(logPath, 'utf8')}`);
    try { if ((await fetch(base + '/api/health')).ok) break; } catch { /* Wait for the listener. */ }
    assert(Date.now() < deadline, 'Pilot startup timed out.');
    await pause(100);
  }
  browser = await chromium.launch(provider ? { executablePath: await provider.executablePath(), args: provider.args, headless: true } : { headless: true });
  result.browser = browser.version();
  page = await browser.newPage({ viewport: { width: 1280, height: 900 }, serviceWorkers: 'block' });
  page.setDefaultTimeout(15000);
  page.on('pageerror', error => result.page_errors.push(error.message));
  page.on('response', response => {
    const pathname = new URL(response.url()).pathname;
    if (pathname.startsWith('/api/lessons') && response.status() >= 400) result.api_errors.push({ path: pathname, status: response.status() });
  });
  const answerInput = page.getByRole('textbox', { name: 'Your answer', exact: true });

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
  async function answerCard() {
    for (let i = 0; i < 150; i++) {
      if (await answerInput.isVisible().catch(() => false)) return answerInput.locator('xpath=ancestor::form/..');
      const next = page.getByRole('button', { name: /^(Next →|Practice again(?: →)?)$/ }).first();
      if (await next.isVisible().catch(() => false)) await next.click();
      await pause(100);
    }
    throw new Error('No answer field: ' + (await page.locator('body').innerText()).slice(-2500));
  }
  async function submit(answer) {
    await answerInput.fill(answer);
    // The real API requires elapsed >= MinAnswerSeconds. Simulate a readable response time.
    await pause(400);
    const pending = page.waitForResponse(r => r.url() === base + '/api/study/answer' && r.request().method() === 'POST');
    await page.getByRole('button', { name: 'Check', exact: true }).click();
    const response = await pending;
    assert.equal(response.status(), 200);
    const body = await response.json();
    assert.notEqual(body.ungraded, true);
    // The normal response can omit ungraded. The existing interface accepts that contract.
    return { body, request: response.request().postDataJSON() };
  }
  async function authenticatedJSON(route) {
    return page.evaluate(async route => {
      const token = localStorage.getItem('mathua_token') || localStorage.getItem('mathua_guest_token');
      const response = await fetch(route, { headers: { Authorization: `Bearer ${token}` } });
      if (!response.ok) throw new Error(`HTTP ${response.status()}: ${route}`);
      return response.json();
    }, route);
  }

  const home = await page.goto(base, { waitUntil: 'domcontentloaded' });
  assert.equal(home.status(), 200);
  assert.equal(new URL(page.url()).searchParams.get('concept'), 'ts.value.numeric_literal');
  await page.locator('p:visible').filter({ hasText: 'Um literal numérico é uma expressão' }).first().waitFor();
  check('home_opens_existing_learn_page_with_lesson', { status: home.status(), concept: 'ts.value.numeric_literal' });

  await openConcept('ts.binding.const_number');
  await page.getByRole('note', { name: 'Prerequisites', exact: true }).waitFor();
  assert.equal(await answerInput.count(), 0);
  check('ui_blocks_unmet_prerequisites', { answer_fields: 0 });

  const amounts = ['mil', 'dois mil', 'três mil', 'quatro mil', 'cinco mil', 'seis mil', 'sete mil', 'oito mil', 'nove mil', 'dez mil', 'onze mil', 'doze mil', 'treze mil', 'catorze mil', 'quinze mil', 'dezesseis mil', 'dezessete mil', 'dezoito mil', 'dezenove mil', 'vinte mil'];
  await openConcept('ts.value.numeric_literal');
  for (const id of ['ts.value.numeric_literal', 'ts.type.number']) {
    let last;
    for (let attempt = 0; attempt < 6; attempt++) {
      const card = await answerCard();
      const question = await card.innerText();
      let answer = 'number';
      if (id === 'ts.value.numeric_literal') {
        const words = question.match(/O valor de um reembolso é ([^.]+)\./)?.[1];
        assert(amounts.includes(words), `Unknown amount: ${words}`);
        answer = String((amounts.indexOf(words) + 1) * 1000);
      }
      last = await submit(answer);
      assert.equal(last.body.correct, true);
      if (attempt === 0) assert.notEqual(last.body.new_status, 'MASTERED');
      await pause(450);
    }
    assert.equal(last.body.new_status, 'MASTERED');
    check('mastery_through_browser_' + id, { attempts: 6, new_status: last.body.new_status, normal_ungraded_present: Object.hasOwn(last.body, 'ungraded') });
    await followRecommendation(id === 'ts.value.numeric_literal' ? 'ts.type.number' : 'ts.binding.const_number');
  }

  const first = await (await answerCard()).innerText();
  const parseQuestion = text => {
    const match = text.match(/chamada ([A-Za-z]+), inicializada com o literal numérico ([0-9]+)/);
    assert(match, 'Constant prompt is missing name or value.');
    return { name: match[1], value: match[2] };
  };
  const before = parseQuestion(first);
  const wrong = await submit(`let ${before.name} = ${before.value};`);
  assert.equal(wrong.body.correct, false);
  await page.getByText('Not quite.', { exact: false }).waitFor();
  const next = await (await answerCard()).innerText();
  assert.notEqual(next, first);
  const after = parseQuestion(next);
  const code = `const ${after.name} = ${after.value};`;
  const correct = await submit(code);
  assert.equal(correct.body.correct, true);
  check('wrong_then_fresh_variant_then_correct', { wrong_question: wrong.request.question, wrong_answer: wrong.request.answer,
    next_question: correct.request.question, correct_answer: code, feedback: correct.body.feedback });

  await page.getByRole('button', { name: 'Report a problem', exact: true }).nth(1).click();
  const dialog = page.getByRole('dialog', { name: 'Report a problem', exact: true });
  await dialog.getByRole('combobox').selectOption('unclear');
  await dialog.getByRole('textbox').fill('Teste de feedback: confirmar que number é opcional neste exercício.');
  const reportResponse = page.waitForResponse(r => r.url() === base + '/api/reports' && r.request().method() === 'POST');
  await dialog.getByRole('button', { name: /Send|Submit/i }).click();
  const sent = await reportResponse;
  assert.equal(sent.status(), 200);
  const reportRequest = sent.request().postDataJSON();
  assert.equal(reportRequest.expected, correct.body.expected_answer);
  assert.equal(reportRequest.answer_given, code);
  assert.equal(reportRequest.question, correct.request.question);
  const mine = await authenticatedJSON('/api/reports/mine');
  assert.equal(mine.reports.length, 1);
  assert.equal(mine.reports[0].expected, correct.body.expected_answer);
  check('feedback_keeps_question_expected_and_given_answer', { report_id: mine.reports[0].id, status: mine.reports[0].status,
    expected: reportRequest.expected, answer_given: reportRequest.answer_given });

  await page.reload({ waitUntil: 'domcontentloaded' });
  await answerCard();
  const readiness = await authenticatedJSON('/api/lessons/ts.binding.const_number/readiness');
  assert.equal(readiness.eligible, true);
  assert(readiness.prerequisites.every(p => p.met));
  check('reload_preserves_identity_and_prerequisite_progress', { eligible: readiness.eligible });
  assert.deepEqual(result.page_errors, []);
  assert.deepEqual(result.api_errors, []);
  result.passed = true;
} catch (error) {
  result.error = error.stack || error.message;
  if (page) result.visible_page = await page.locator('body').innerText().catch(() => 'Page unavailable');
  process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
  await Promise.race([new Promise(resolve => server.once('exit', resolve)), pause(3000)]);
  if (server.exitCode === null) server.kill('SIGKILL');
  if (!result.passed) result.server_log = readFileSync(logPath, 'utf8').slice(-6000);
  rmSync(work, { recursive: true, force: true });
}

const output = JSON.stringify(result, null, 2) + '\n';
if (values.output) {
  mkdirSync(path.dirname(path.resolve(values.output)), { recursive: true });
  writeFileSync(values.output, output);
}
process.stdout.write(output);
