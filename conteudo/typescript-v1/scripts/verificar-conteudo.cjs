#!/usr/bin/env node
// Verifica apenas o conteúdo confiável deste repositório. Não é corretor de respostas de alunos.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const os = require('node:os');

const root = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
function option(name, fallback) {
  const at = args.indexOf(name);
  return at < 0 ? fallback : args[at + 1];
}
const tsPath = option('--typescript', path.resolve(root, '../../pilotos/mathua/mathua/cmd/typescript-pilot/node_modules/typescript'));
const ts = require(path.resolve(tsPath));
const output = path.resolve(option('--output', path.join(root, 'evidencias/validacao.json')));
const curriculum = JSON.parse(fs.readFileSync(path.join(root, 'curriculo.json'), 'utf8'));
const exercises = JSON.parse(fs.readFileSync(path.join(root, 'exercicios.json'), 'utf8'));
const errors = [];
const counts = {stages: 0, concepts: 0, families: 0, cases: 0, distinct_questions: 0,
  compiled_files: 0, code_answers: 0, diagnostic_cases: 0, choice_cases: 0,
  interpreted_answers: 0, type_queries: 0, function_boundary_assertions: 0, integrated_assertions: 0};
function check(label, work) {
  try { work(); } catch (e) { errors.push({check: label, message: e.message}); }
}
function hash(file) { return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'); }
function same(actual, expected, label) { assert.deepStrictEqual(actual, expected, label); }
function normalize(value) {
  if (value === undefined) return {$undefined: true};
  if (Array.isArray(value)) return Array.from(value, normalize);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, normalize(v)]));
  return value;
}
function run(source) {
  const logs = [];
  const context = {console: {log: (...values) => logs.push(normalize(values))}};
  const result = ts.transpileModule(source, {compilerOptions: {target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS}});
  vm.runInNewContext(result.outputText, context, {timeout: 1000});
  return {value: normalize(context.__observed), logs};
}
function sourceFile(source) { return ts.createSourceFile('case.ts', source, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS); }
function observeLast(source) {
  const file = sourceFile(source);
  const last = file.statements[file.statements.length - 1];
  assert(ts.isExpressionStatement(last), 'A última instrução precisa ser a expressão consultada.');
  return run(source.slice(0, last.pos) + '\nglobalThis.__observed = (' + last.expression.getText(file) + ');').value;
}
function expectedValue(answer) {
  if (answer === 'undefined') return {$undefined: true};
  if (['required', 'not_required'].includes(answer)) return answer;
  return JSON.parse(answer);
}
function acyclic(items, id, dependencies) {
  const byId = new Map(items.map(x => [id(x), x]));
  const done = new Set();
  const active = new Set();
  function visit(key) {
    assert(byId.has(key), `Dependência desconhecida: ${key}`);
    if (done.has(key)) return;
    assert(!active.has(key), `Ciclo de dependências em ${key}`);
    active.add(key);
    for (const dep of dependencies(byId.get(key))) visit(dep);
    active.delete(key); done.add(key);
  }
  for (const key of byId.keys()) visit(key);
}

check('estrutura, cobertura e dependências', () => {
  counts.stages = curriculum.stages.length;
  counts.concepts = curriculum.concepts.length;
  counts.families = exercises.families.length;
  counts.cases = exercises.families.reduce((n, f) => n + f.cases.length, 0);
  same([counts.stages, counts.concepts, counts.families, counts.cases], [15, 46, 74, 444]);
  const familyIds = exercises.families.map(f => f.id);
  same(new Set(familyIds).size, 74);
  same(new Set(exercises.families.flatMap(f => f.cases.map(c => c.id))).size, 444);
  same(new Set(curriculum.concepts.map(c => c.id)).size, 46);
  same([...curriculum.concepts.flatMap(c => c.family_ids)].sort(), [...familyIds].sort());
  same(exercises.families.map(f => f.source_card_id), Array.from({length: 74}, (_, i) => `C${String(i + 1).padStart(3, '0')}`));
  acyclic(curriculum.stages, x => x.id, x => x.teaching_prerequisites);
  acyclic(curriculum.concepts, x => x.id, x => x.prerequisites);
  const byConcept = new Map(curriculum.concepts.map(c => [c.id, c]));
  for (const concept of curriculum.concepts) {
    assert(concept.family_ids.length > 0);
    for (const dep of concept.prerequisites) assert(byConcept.get(dep).stage <= concept.stage, `${concept.id} exige um degrau posterior.`);
  }
  for (const stage of curriculum.stages) assert(stage.lesson_markdown.length > 500, `Aula ausente: ${stage.id}`);
  for (const [id, dependencies] of [
    ['ts.value.numeric_literal', []], ['ts.type.number', []],
    ['ts.binding.const_number', ['ts.value.numeric_literal', 'ts.type.number']]
  ]) same(byConcept.get(id).prerequisites, dependencies, `Contrato existente: ${id}`);
  for (const family of exercises.families) {
    same(family.cases.length, 6, family.id);
    const concept = byConcept.get(family.concept_id);
    same(family.stage, `D${String(concept.stage).padStart(2, '0')}`);
    const distinct = new Set(family.cases.map(c => JSON.stringify([c.prompt, c.context_code]))).size;
    same(distinct, 6, `Só mudar a alternativa ou o ID não cria uma pergunta diferente: ${family.id}`);
    counts.distinct_questions += distinct;
    for (const c of family.cases) {
      assert(c.prompt && c.answer && c.explanation && c.criterion, c.id);
      if (family.mode === 'choice') {
        same(c.choices.length, 4, c.id);
        same(new Set(c.choices.map(x => x.text)).size, 4, c.id);
        same(c.choices.filter(x => x.id === c.answer).length, 1, c.id);
        same(c.choices.find(x => x.id === c.answer).text, c.answer_explanation, c.id);
        counts.choice_cases++;
      }
    }
  }
});
check('fontes preservadas', () => {
  for (const [name, expected] of Object.entries(curriculum.source_sha256)) same(hash(path.join(root, 'fontes', name)), expected, name);
  same(curriculum.source_sha256['anki_typescript_v1.tsv'], '4288391e8f6a49266a82b75d0615dc61be8baa42f513128fed1feae2893f3ac7');
});

const files = new Map();
const cases = new Map();
for (const family of exercises.families) {
  for (const c of family.cases) {
    let source = c.context_code;
    if (family.mode === 'code') {
      source += '\n' + (c.code_form === 'expression' ? `const __answer = (${c.answer});` : c.answer);
      counts.code_answers++;
    }
    if (!source.trim()) continue;
    const file = path.join(root, '__virtual__', c.id + '.ts');
    files.set(file, source + '\nexport {};\n');
    cases.set(file, {family, c});
  }
}
const integratedFile = path.join(root, 'fontes/reembolsos.ts');
files.set(integratedFile, fs.readFileSync(integratedFile, 'utf8') + '\nexport {};\n');
const compilerOptions = {strict: true, noEmit: true, target: ts.ScriptTarget.ES2022,
  module: ts.ModuleKind.CommonJS, types: [], skipLibCheck: true};
const host = ts.createCompilerHost(compilerOptions);
const originalGet = host.getSourceFile.bind(host);
host.getSourceFile = (file, languageVersion, onError, shouldCreate) => files.has(file)
  ? ts.createSourceFile(file, files.get(file), languageVersion, true)
  : originalGet(file, languageVersion, onError, shouldCreate);
const program = ts.createProgram([...files.keys()], compilerOptions, host);
const diagnostics = ts.getPreEmitDiagnostics(program);
const checker = program.getTypeChecker();
counts.compiled_files = files.size;
const byFile = new Map();
for (const diagnostic of diagnostics) {
  const file = diagnostic.file?.fileName || '<global>';
  if (!byFile.has(file)) byFile.set(file, []);
  byFile.get(file).push(diagnostic);
}
for (const [file, data] of cases) {
  check(`TypeScript ${data.c.id}`, () => {
    const received = byFile.get(file) || [];
    if (data.c.context_expected_diagnostic) {
      same(received.map(d => d.code), [data.c.context_expected_diagnostic], data.c.id);
      counts.diagnostic_cases++;
    } else {
      same(received.map(d => ts.flattenDiagnosticMessageText(d.messageText, '\n')), [], data.c.id);
    }
  });
}
for (const [file, received] of byFile) {
  if (!cases.has(file)) check(`TypeScript ${path.basename(file)}`, () => same(received.map(d => d.code), []));
}

for (const family of exercises.families) {
  const number = Number(family.id.slice(1));
  for (const c of family.cases) {
    if (family.mode === 'value') check(`interpretação ${c.id}`, () => {
      let actual;
      if ([73, 74].includes(number)) actual = run(c.context_code).logs.length;
      else if (number === 37) {
        const file = sourceFile(c.context_code);
        const last = file.statements[file.statements.length - 1];
        assert(ts.isExpressionStatement(last) && ts.isCallExpression(last.expression));
        actual = Number(last.expression.arguments[0].getText(file));
      } else actual = observeLast(c.context_code);
      same(actual, expectedValue(c.answer), c.id);
      counts.interpreted_answers++;
    });
    if (number === 53) check(`ramo ${c.id}`, () => {
      const expected = c.answer_explanation.includes('ramo if') ? 'A' : 'B';
      same(run(c.context_code).logs, [[expected]], c.id);
      counts.interpreted_answers++;
    });
    if (number === 70) check(`tipo de find ${c.id}`, () => {
      const file = program.getSourceFile(path.join(root, '__virtual__', c.id + '.ts'));
      let found;
      for (const statement of file.statements) if (ts.isVariableStatement(statement)) {
        for (const declaration of statement.declarationList.declarations) if (declaration.name.getText(file) === 'found') found = declaration;
      }
      assert(found);
      const type = checker.typeToString(checker.getTypeAtLocation(found.name));
      const parts = value => value.split('|').map(x => x.trim()).sort();
      same(parts(type), parts(c.answer), c.id);
      counts.type_queries++;
    });
    if ([30, 45, 52, 58].includes(number)) check(`fronteiras da função ${c.id}`, () => {
      const file = sourceFile(c.answer);
      const first = file.statements[0];
      const declared = ts.isFunctionDeclaration(first) ? first : first.declarationList.declarations[0];
      const name = declared.name.getText(file);
      const prefix = c.context_code + '\n' + c.answer;
      if (number === 45) {
        for (const value of [-1, 0, 1]) {
          same(run(prefix + `\nglobalThis.__observed = ${name}(${value});`).value, value > 0, c.id);
          counts.function_boundary_assertions++;
        }
      } else if (number === 52) {
        const limit = Number(c.answer.match(/>\s*(\d+)/)[1]);
        for (const value of [limit - 1, limit, limit + 1]) {
          same(run(prefix + `\nglobalThis.__observed = ${name}(${value});`).value, value > limit ? 'required' : 'not_required', c.id);
          counts.function_boundary_assertions++;
        }
      } else {
        const property = c.answer.match(/return\s+\w+\.(\w+)/)[1];
        for (const value of [0, 5000, 15000]) {
          same(run(prefix + `\nglobalThis.__observed = ${name}({id: "caso", ${property}: ${value}});`).value, value, c.id);
          counts.function_boundary_assertions++;
        }
        if (number === 58) {
          same(run(prefix + `\nglobalThis.__observed = ${name}(undefined);`).value, {$undefined: true}, c.id);
          counts.function_boundary_assertions++;
        }
      }
    });
  }
}

let integratedObserved;
check('programa integrado original', () => {
  const original = fs.readFileSync(integratedFile, 'utf8');
  integratedObserved = run(original).logs;
  const expected = [
    [['required', 'not_required', 'not_required']],
    [[{id: 'reembolso-01', amount: 15000}]],
    ['not_required'], [{$undefined: true}], ['reembolso-01']
  ];
  same(integratedObserved, expected);
  counts.integrated_assertions += 5;
  for (const [amount, expectedStatus] of [[9999, 'not_required'], [10000, 'not_required'], [10001, 'required']]) {
    same(run(original + `\nglobalThis.__observed = classifyRefund({id: "fronteira", amount: ${amount}}, 10000);`).value, expectedStatus);
    counts.integrated_assertions++;
  }
  same(run(original + '\nglobalThis.__observed = getReviewStatus(undefined, 10000);').value, {$undefined: true});
  counts.integrated_assertions++;
});

const report = {
  passed: errors.length === 0,
  environment: {platform: os.platform(), arch: os.arch(), node: process.version, typescript: ts.version},
  compiler_options: {strict: true, target: 'ES2022', module: 'CommonJS'},
  counts, source_sha256: curriculum.source_sha256, integrated_observed: integratedObserved, errors,
  limits: [
    'Verificação de conteúdo editorial; não executa nem altera o aplicativo Mathua.',
    'As questões de significado e seus distratores exigem revisão editorial; consistência estrutural não prova qualidade pedagógica.',
    'Aceitar todas as soluções corretas e rejeitar todas as incorretas depende da implementação futura dos corretores.',
    'O uso de vm serve apenas para executar gabaritos confiáveis deste repositório; não constitui isolamento para código enviado por alunos.',
    'Não mede domínio, retenção, dificuldade nem calibração com alunos reais.'
  ]
};
fs.mkdirSync(path.dirname(output), {recursive: true});
fs.writeFileSync(output, JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({passed: report.passed, environment: report.environment, counts, errors}, null, 2));
if (!report.passed) process.exitCode = 1;
