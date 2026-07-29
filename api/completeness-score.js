#!/usr/bin/env node
/**
 * completeness-score.js — 品类资产完整性评分脚本
 *
 * 规则（总分100）：
 *   基础字段 20分 — name / stage / market / competition
 *   模型    20分 — models（经营模式）
 *   风险    20分 — risks（风险字段）
 *   关联    30分 — 至少关联 case + framework + report
 *   版本    10分 — decisionLayer（决策层信息）
 *
 * 结果：≥70分 -> status: "recommended"
 *       <70分 -> status: "draft"（不推荐展示）
 *
 * 用法：
 *   node completeness-score.js                        – 读取本地 categories-schema.json
 *   node completeness-score.js <json-file-path>        – 指定文件
 *   node completeness-score.js --report                – 生成详细报告
 *   node completeness-score.js --markdown              – 输出 Markdown 表格
 */

const fs = require('fs');
const path = require('path');

// —————— 配置 ——————
const SCORE_WEIGHTS = {
  basicFields: 20,
  models: 20,
  risks: 20,
  relations: 30,
  decisionLayer: 10,
  TOTAL: 100,
};

// 关联类型权重
const RELATION_WEIGHTS = {
  cases: 12,
  frameworks: 9,
  reports: 9,
};

// 决策层子字段
const DECISION_FIELDS = [
  'entryBarrier',
  'suitableFor',
  'notSuitableFor',
  'typicalDailyRevenue',
  'paybackPeriod',
];

// —————— 评分函数 ——————

function scoreBasicFields(cat) {
  let score = 0;
  const fields = ['name', 'stage', 'market', 'competition'];
  const present = fields.filter(f => cat[f] != null && cat[f] !== '');
  score += (present.length / fields.length) * SCORE_WEIGHTS.basicFields;
  return { raw: Math.round(score), details: `${present.length}/${fields.length} 字段` };
}

function scoreModels(cat) {
  let score = 0;
  if (Array.isArray(cat.models) && cat.models.length > 0) {
    if (cat.models.length >= 3) score = SCORE_WEIGHTS.models;
    else if (cat.models.length >= 2) score = Math.round(SCORE_WEIGHTS.models * 0.7);
    else score = Math.round(SCORE_WEIGHTS.models * 0.4);
  }
  return { raw: score, details: `${cat.models?.length || 0} 种经营模式` };
}

function scoreRisks(cat) {
  let score = 0;
  if (Array.isArray(cat.risks) && cat.risks.length > 0) {
    if (cat.risks.length >= 3) score = SCORE_WEIGHTS.risks;
    else if (cat.risks.length >= 2) score = Math.round(SCORE_WEIGHTS.risks * 0.7);
    else score = Math.round(SCORE_WEIGHTS.risks * 0.4);
  }
  return { raw: score, details: `${cat.risks?.length || 0} 个风险点` };
}

function scoreRelations(cat) {
  let score = 0;
  const cases = Array.isArray(cat.relatedCaseIds) ? cat.relatedCaseIds : [];
  const frameworks = Array.isArray(cat.relatedFrameworkIds) ? cat.relatedFrameworkIds : [];
  const reports = Array.isArray(cat.relatedReportIds) ? cat.relatedReportIds : [];

  if (cases.length > 0) score += Math.min(RELATION_WEIGHTS.cases, cases.length * 4);
  if (frameworks.length > 0) score += Math.min(RELATION_WEIGHTS.frameworks, frameworks.length * 5);
  if (reports.length > 0) score += Math.min(RELATION_WEIGHTS.reports, reports.length * 3);

  score = Math.min(score, SCORE_WEIGHTS.relations);
  return {
    raw: Math.round(score),
    details: `案例${cases.length}/框架${frameworks.length}/报告${reports.length}`,
  };
}

function scoreDecisionLayer(cat) {
  let score = 0;
  const dl = cat.decisionLayer || {};
  const present = DECISION_FIELDS.filter(f => dl[f] != null && dl[f] !== '' && !(Array.isArray(dl[f]) && dl[f].length === 0));
  score += (present.length / DECISION_FIELDS.length) * SCORE_WEIGHTS.decisionLayer;
  return { raw: Math.round(score), details: `${present.length}/${DECISION_FIELDS.length} 决策字段` };
}

// —————— 主评分 ——————

function scoreOne(cat) {
  const basic = scoreBasicFields(cat);
  const models = scoreModels(cat);
  const risks = scoreRisks(cat);
  const relations = scoreRelations(cat);
  const decision = scoreDecisionLayer(cat);

  const total = basic.raw + models.raw + risks.raw + relations.raw + decision.raw;
  const status = total >= 70 ? 'recommended' : 'draft';

  return {
    id: cat.id,
    name: cat.name,
    score: total,
    status,
    breakdown: {
      basic: basic,
      models: models,
      risks: risks,
      relations: relations,
      decisionLayer: decision,
    },
  };
}

// —————— 批量评分 ——————

function scoreAll(categories) {
  return categories.map(scoreOne);
}

// —————— 报告输出 ——————

function printReport(results) {
  console.log('='.repeat(72));
  console.log('  品类资产完整性评分报告');
  console.log('='.repeat(72));
  console.log('');
  results.forEach(r => {
    const badge = r.status === 'recommended' ? '✅ 推荐' : '⚠️  草稿';
    console.log(`  ${r.id.padEnd(12)} ${r.name.padEnd(8)} ${String(r.score).padStart(3)}分  ${badge}`);
    console.log(`    基础:${String(r.breakdown.basic.raw).padStart(3)}分 (${r.breakdown.basic.details})  模型:${String(r.breakdown.models.raw).padStart(3)}分 (${r.breakdown.models.details})`);
    console.log(`    风险:${String(r.breakdown.risks.raw).padStart(3)}分 (${r.breakdown.risks.details})  关联:${String(r.breakdown.relations.raw).padStart(3)}分 (${r.breakdown.relations.details})`);
    console.log(`    决策:${String(r.breakdown.decisionLayer.raw).padStart(3)}分 (${r.breakdown.decisionLayer.details})`);
    console.log('');
  });
  const avg = results.reduce((s, r) => s + r.score, 0) / results.length;
  const recommended = results.filter(r => r.status === 'recommended').length;
  console.log(`  平均分: ${avg.toFixed(1)}  |  推荐 ${recommended}/${results.length}  |  阈值: 70分`);
  console.log('');
}

function printMarkdown(results) {
  console.log('| 品类 | 名称 | 总分 | 状态 | 基础 | 模型 | 风险 | 关联 | 决策层 |');
  console.log('|------|------|------|------|------|------|------|------|--------|');
  results.forEach(r => {
    const b = r.breakdown;
    console.log(`| ${r.id} | ${r.name} | ${r.score} | ${r.status} | ${b.basic.raw} | ${b.models.raw} | ${b.risks.raw} | ${b.relations.raw} | ${b.decisionLayer.raw} |`);
  });
}

// —————— CLI 入口 ——————

function main() {
  const args = process.argv.slice(2);
  const filePath = args[0] && !args[0].startsWith('--') ? args[0] : null;
  const doReport = args.includes('--report');
  const doMarkdown = args.includes('--markdown');

  const target = filePath || path.join(__dirname, 'categories-schema.json');

  if (!fs.existsSync(target)) {
    console.error(`❌ 文件不存在: ${target}`);
    process.exit(1);
  }

  let data;
  try {
    data = JSON.parse(fs.readFileSync(target, 'utf-8'));
  } catch (e) {
    console.error(`❌ 解析 JSON 失败: ${e.message}`);
    process.exit(1);
  }

  const categories = Array.isArray(data) ? data : [data];
  const results = scoreAll(categories);

  if (doMarkdown) {
    printMarkdown(results);
  } else if (doReport || args.length === 0) {
    printReport(results);
  } else {
    console.log(JSON.stringify(results, null, 2));
  }
}

if (require.main === module) {
  main();
}

module.exports = { scoreOne, scoreAll, scoreBasicFields, scoreModels, scoreRisks, scoreRelations, scoreDecisionLayer };
