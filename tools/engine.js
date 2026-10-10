var DecisionEngine = (() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // src/core/engine.ts
  var engine_exports = {};
  __export(engine_exports, {
    EXPLAINER_THRESHOLDS: () => EXPLAINER_THRESHOLDS,
    calculateBreakEven: () => calculateBreakEven,
    calculateCost: () => calculateCost,
    calculateDecision: () => calculateDecision,
    calculatePayback: () => calculatePayback,
    calculatePricing: () => calculatePricing,
    calculateQuote: () => calculateQuote,
    explainDecision: () => explainDecision,
    pct: () => pct,
    quoteCounterOffer: () => quoteCounterOffer,
    round2: () => round2,
    runCalculator: () => runCalculator
  });

  // src/core/types.ts
  var EXPLAINER_THRESHOLDS = {
    LOW_SAFETY_MARGIN: 0.1,
    // 安全余量低于 10% → 销量是关键变量
    LOW_CONTRIBUTION_RATE: 0.2,
    // 贡献率低于 20% → 成本是关键变量
    PRICE_DEVIATION_RATIO: 0.05,
    // 售价与目标价差距 < 5% → 售价是关键变量
    HIGH_FIXED_COST_RATIO: 0.15,
    // 固定成本占收入 > 15% → 固定成本是关键变量
    LOSS_MARGIN: 0
    // 利润率 = 0 时为亏损边界
  };

  // src/core/engine.ts
  function round2(n) {
    return Math.round(n * 100) / 100;
  }
  function pct(n) {
    return `${Math.round(n * 100)}%`;
  }
  function safeDiv(a, b) {
    if (!b || b === 0) return 0;
    return a / b;
  }
  function calculateCost(c) {
    const effectiveRate = 1 - (c.wasteRate || 0);
    const effectiveMaterialCost = safeDiv(c.materialCost, effectiveRate);
    const variableCostPerUnit = effectiveMaterialCost + (c.laborCost || 0) + (c.packagingCost || 0) + (c.shippingCost || 0) + (c.advertisingCost || 0);
    const platformAbsolute = 0;
    const fixedCostMonthly = c.fixedCost || 0;
    const costStructure = {
      material: round2(effectiveMaterialCost),
      labor: round2(c.laborCost || 0),
      packaging: round2(c.packagingCost || 0),
      shipping: round2(c.shippingCost || 0),
      platform: round2(platformAbsolute),
      payment: round2(c.paymentFee || 0),
      wasteAdjustment: round2(effectiveMaterialCost - (c.materialCost || 0)),
      fixed: round2(fixedCostMonthly)
    };
    const unitCost = variableCostPerUnit;
    const fullCost = variableCostPerUnit;
    return {
      unitCost: round2(unitCost),
      fullCost: round2(fullCost),
      variableCostPerUnit: round2(variableCostPerUnit),
      fixedCostMonthly: round2(fixedCostMonthly),
      costStructure,
      effectiveMaterialCost: round2(effectiveMaterialCost)
    };
  }
  function calculatePricing(cost, pv) {
    const costResult = calculateCost(cost);
    const variableCost = costResult.variableCostPerUnit;
    const feeRate = (cost.platformFee || 0) + (cost.paymentFee || 0);
    const refundAdj = cost.refundRate || 0;
    const mode = pv.mode ?? "A";
    switch (mode) {
      case "A": {
        const targetMargin = pv.targetMargin ?? 0.3;
        const suggestedPrice = safeDiv(
          variableCost,
          (1 - feeRate - refundAdj) * (1 - targetMargin)
        );
        return {
          mode,
          suggestedPrice: round2(suggestedPrice),
          grossMargin: round2(1 - safeDiv(variableCost, suggestedPrice)),
          netMargin: round2(1 - safeDiv(variableCost + suggestedPrice * feeRate, suggestedPrice))
        };
      }
      case "B": {
        const price = pv.sellingPrice;
        const feeAbsolute = price * feeRate;
        const netProfit = price - variableCost - feeAbsolute - price * refundAdj;
        return {
          mode,
          netProfit: round2(netProfit),
          grossMargin: round2(1 - safeDiv(variableCost, price)),
          netMargin: round2(safeDiv(netProfit, price))
        };
      }
      case "C": {
        const price = pv.sellingPrice;
        const targetMargin = pv.targetMargin ?? 0.2;
        const maxAcceptableCost = price * (1 - feeRate - refundAdj) * (1 - targetMargin);
        return {
          mode,
          maxAcceptableCost: round2(maxAcceptableCost),
          grossMargin: round2(1 - safeDiv(maxAcceptableCost, price)),
          netMargin: targetMargin
        };
      }
      case "D": {
        const base = pv.sellingPrice;
        const prices = [base * 0.7, base * 0.8, base * 0.9, base, base * 1.1, base * 1.2, base * 1.3];
        const sensitivityTable = prices.map((price) => {
          const feeAbsolute = price * feeRate;
          const netProfit = price - variableCost - feeAbsolute - price * refundAdj;
          return {
            price: round2(price),
            grossMargin: round2(1 - safeDiv(variableCost, price)),
            netMargin: round2(safeDiv(netProfit, price))
          };
        });
        const mid = sensitivityTable[3];
        return {
          mode,
          sensitivityTable,
          grossMargin: mid.grossMargin,
          netMargin: mid.netMargin
        };
      }
      default:
        return { mode: "A", grossMargin: 0, netMargin: 0 };
    }
  }
  function calculateBreakEven(cost, pv, targetMonthlyProfit) {
    const costResult = calculateCost(cost);
    const variableCost = costResult.variableCostPerUnit;
    const fixedMonthly = cost.fixedCost || 0;
    const price = pv.sellingPrice;
    const feeRate = (cost.platformFee || 0) + (cost.paymentFee || 0);
    const refundAdj = cost.refundRate || 0;
    const contributionPerUnit = price - variableCost - price * feeRate - price * refundAdj;
    const breakEvenMonthlyOrders = safeDiv(fixedMonthly, contributionPerUnit);
    const daysPerMonth = 30;
    const breakEvenOrdersPerDay = breakEvenMonthlyOrders / daysPerMonth;
    const breakEvenRevenuePerDay = breakEvenOrdersPerDay * price;
    const safeOrdersPerDay = breakEvenOrdersPerDay * 1.3;
    const safeRevenuePerDay = safeOrdersPerDay * price;
    const targetProfit = targetMonthlyProfit ?? 0;
    const targetOrdersMonthly = safeDiv(fixedMonthly + targetProfit, contributionPerUnit);
    const targetOrdersPerDay = targetOrdersMonthly / daysPerMonth;
    return {
      contributionPerUnit: round2(contributionPerUnit),
      breakEvenRevenue: round2(breakEvenRevenuePerDay),
      breakEvenOrders: Math.ceil(breakEvenOrdersPerDay),
      breakEvenUnitPrice: round2(price),
      safeRevenue: round2(safeRevenuePerDay),
      safeOrders: Math.ceil(safeOrdersPerDay),
      targetProfitOrders: Math.ceil(targetOrdersPerDay)
    };
  }
  function calculatePayback(iv) {
    const monthlyRevenue = iv.monthlyRevenue;
    const monthlyMargin = iv.monthlyGrossMargin ?? 0;
    const grossProfit = monthlyRevenue * monthlyMargin;
    const monthlyExpenses = (iv.monthlyRent || 0) + (iv.monthlyLabor || 0) + (iv.monthlyUtility || 0) + (iv.monthlyPlatform || 0) + (iv.monthlyMarketing || 0) + (iv.monthlyOther || 0);
    const monthlyCashFlow = grossProfit - monthlyExpenses;
    const investment = iv.initialInvestment;
    const paybackMonths = monthlyCashFlow > 0 ? Math.ceil(investment / monthlyCashFlow) : Infinity;
    const scenario = (revAdj) => {
      const rev = monthlyRevenue * (1 + revAdj);
      const profit = rev * monthlyMargin - monthlyExpenses;
      return {
        monthlyProfit: round2(profit),
        paybackMonths: profit > 0 ? Math.ceil(investment / profit) : Infinity
      };
    };
    return {
      monthlyCashFlow: round2(monthlyCashFlow),
      cumulativeCashFlow: round2(monthlyCashFlow * 12),
      paybackMonths,
      minimumCashReserve: round2(iv.minimumCashReserve ?? monthlyExpenses * 3),
      scenarios: {
        conservative: scenario(-0.2),
        baseline: scenario(0),
        optimistic: scenario(0.2)
      }
    };
  }
  function calculateQuote(qv) {
    const cost = qv.quoteCost;
    const base = cost;
    const costPrice = base;
    const floorPrice = base * 1.11;
    const suggestedPrice = base * 1.31;
    const targetPrice = base * 1.41;
    const creditDays = qv.creditPeriod || 0;
    const creditCost = base * creditDays * 0.05 / 365;
    return {
      costPrice: round2(costPrice),
      floorPrice: round2(floorPrice),
      suggestedPrice: round2(suggestedPrice),
      targetPrice: round2(targetPrice),
      marginAtSuggested: round2(1 - safeDiv(cost, suggestedPrice)),
      counterOffer: void 0
      // 议价响应由 UI 层触发（见 quoteCounterOffer）
    };
  }
  function quoteCounterOffer(quote, offerPrice, minQuantity) {
    const cost = quote.costPrice;
    const marginAfter = 1 - safeDiv(cost, offerPrice);
    return {
      offerPrice: round2(offerPrice),
      marginAfter: round2(marginAfter),
      minQuantityCondition: minQuantity
    };
  }
  function evaluateViability(contributionPerUnit, actualBreakEvenMonthly, monthlySalesVolume) {
    if (contributionPerUnit <= 0) {
      return {
        level: "unviable",
        title: "\u4E0D\u53EF\u7ECF\u8425",
        advice: "\u5F53\u524D\u552E\u4EF7\u65E0\u6CD5\u8986\u76D6\u5355\u4F4D\u53D8\u52A8\u6210\u672C\u53CA\u9500\u552E\u8D39\u7528\uFF0C\u4E0D\u5B58\u5728\u6709\u6548\u76C8\u4E8F\u5E73\u8861\u70B9\u3002",
        canOperate: false
      };
    }
    if (monthlySalesVolume >= actualBreakEvenMonthly) {
      return {
        level: "profitable",
        title: "\u53EF\u7ECF\u8425",
        advice: "\u5F53\u524D\u5047\u8BBE\u4E0B\u5177\u5907\u76C8\u5229\u80FD\u529B\u3002",
        canOperate: true
      };
    }
    return {
      level: "loss",
      title: "\u9884\u8BA1\u4E8F\u635F",
      advice: "\u5F53\u524D\u9500\u91CF\u4E0D\u8DB3\u4EE5\u8986\u76D6\u6708\u56FA\u5B9A\u6210\u672C\uFF0C\u9884\u8BA1\u4E8F\u635F\u3002",
      canOperate: false
    };
  }
  function calculateDecision(scenario) {
    const { cost, sellingPrice, monthlySalesVolume, targetMonthlyProfit } = scenario;
    const costResult = calculateCost(cost);
    const pvForPricing = {
      sellingPrice: 0,
      salesVolume: 0,
      mode: "A",
      targetMargin: 0.3
    };
    const pricingResult = calculatePricing(cost, pvForPricing);
    const theoreticalTargetPrice = pricingResult.suggestedPrice ?? sellingPrice;
    const pvForBE = {
      sellingPrice,
      salesVolume: monthlySalesVolume,
      mode: "A",
      targetMargin: 0.3
    };
    const breakEvenResult = calculateBreakEven(cost, pvForBE, targetMonthlyProfit);
    const variableCostPerUnit = costResult.variableCostPerUnit;
    const feeRate = (cost.platformFee || 0) + (cost.paymentFee || 0);
    const refundAdj = cost.refundRate || 0;
    const contributionPerUnitFull = sellingPrice - variableCostPerUnit - sellingPrice * feeRate - sellingPrice * refundAdj;
    const contributionPerUnit = round2(contributionPerUnitFull);
    const contributionRate = round2(contributionPerUnitFull / sellingPrice);
    const fixedCostMonthly = costResult.fixedCostMonthly;
    const daysPerMonth = 30;
    const theoreticalBreakEvenMonthly = safeDiv(fixedCostMonthly, contributionPerUnitFull);
    const theoreticalBreakEvenDaily = theoreticalBreakEvenMonthly / daysPerMonth;
    const minimumBreakEvenMonthly = Math.ceil(theoreticalBreakEvenMonthly);
    const actualBreakEvenDaily = breakEvenResult.breakEvenOrders;
    const executionTargetMonthly = actualBreakEvenDaily * daysPerMonth;
    const breakEvenRevenue = breakEvenResult.breakEvenRevenue;
    const projectedMonthlyRevenue = round2(sellingPrice * monthlySalesVolume);
    const projectedMonthlyProfit = round2(contributionPerUnitFull * monthlySalesVolume - fixedCostMonthly);
    const operatingMargin = round2(safeDiv(projectedMonthlyProfit, projectedMonthlyRevenue));
    let safetyMargin;
    if (monthlySalesVolume > 0) {
      safetyMargin = round2((monthlySalesVolume - executionTargetMonthly) / monthlySalesVolume);
    } else {
      safetyMargin = 0;
    }
    const metrics = {
      effectiveMaterialCost: costResult.effectiveMaterialCost,
      variableCostPerUnit,
      sellingPrice,
      theoreticalTargetPrice,
      contributionPerUnit,
      contributionRate,
      // 3. 盈亏平衡 — 三层
      theoreticalBreakEvenMonthly: round2(theoreticalBreakEvenMonthly),
      minimumBreakEvenMonthly,
      executionTargetMonthly,
      theoreticalBreakEvenDaily: round2(theoreticalBreakEvenDaily),
      actualBreakEvenDaily,
      // 收入
      theoreticalBreakEvenRevenueMonthly: round2(theoreticalBreakEvenMonthly * sellingPrice),
      minimumBreakEvenRevenueMonthly: round2(minimumBreakEvenMonthly * sellingPrice),
      executionTargetRevenueMonthly: round2(executionTargetMonthly * sellingPrice),
      breakEvenRevenue,
      fixedCostMonthly,
      // 4. 经营结果
      projectedMonthlyRevenue,
      projectedMonthlyProfit,
      operatingMargin,
      safetyMargin
    };
    const judgment = evaluateViability(
      contributionPerUnit,
      executionTargetMonthly,
      monthlySalesVolume
    );
    return {
      scenario,
      metrics,
      judgment,
      costResult,
      pricingResult,
      breakEvenResult
    };
  }
  function runCalculator(tool, input) {
    switch (tool) {
      case "cost":
        return calculateCost(input.cost);
      case "pricing":
        return calculatePricing(input.cost, input.priceVolume);
      case "breakeven":
        return calculateBreakEven(input.cost, input.priceVolume, input.targetMonthlyProfit);
      case "payback":
        return calculatePayback(input.investment);
      case "quote":
        return calculateQuote(input.quote);
      case "decision":
        return calculateDecision(input.scenario);
    }
  }
  function fmtMoney(n) {
    return "\xA5 " + round2(n).toFixed(2);
  }
  function fmtCount(n) {
    return round2(n).toFixed(0) + " \u5355";
  }
  function fmtCountFloat(n) {
    return round2(n).toFixed(2) + " \u5355";
  }
  function fmtPct(n) {
    return round2(n * 100).toFixed(2) + "%";
  }
  function rankKeyVariables(m, s) {
    const vars = [];
    if (m.safetyMargin < EXPLAINER_THRESHOLDS.LOW_SAFETY_MARGIN) {
      vars.push({
        field: "executionTargetMonthly",
        importance: "critical",
        reason: `\u5B89\u5168\u4F59\u91CF ${fmtPct(m.safetyMargin)} \u4F4E\u4E8E\u9608\u503C ${fmtPct(EXPLAINER_THRESHOLDS.LOW_SAFETY_MARGIN)}\uFF0C\u9500\u91CF\u76F4\u63A5\u5F71\u54CD\u76C8\u4E8F`,
        traceability: [
          { sourceType: "metric", sourceField: "safetyMargin", sourceValue: m.safetyMargin, ruleId: "KV01", explanation: "\u5B89\u5168\u4F59\u91CF < 10% \u2192 \u9500\u91CF\u662F\u5173\u952E\u53D8\u91CF" },
          { sourceType: "metric", sourceField: "executionTargetMonthly", sourceValue: m.executionTargetMonthly, ruleId: "KV01", explanation: "\u6267\u884C\u76EE\u6807\u9500\u91CF" }
        ]
      });
    }
    if (m.contributionRate < EXPLAINER_THRESHOLDS.LOW_CONTRIBUTION_RATE) {
      const importance = m.safetyMargin < EXPLAINER_THRESHOLDS.LOW_SAFETY_MARGIN ? "high" : "critical";
      vars.push({
        field: "contributionPerUnit",
        importance,
        reason: `\u8D21\u732E\u7387 ${fmtPct(m.contributionRate)} \u4F4E\u4E8E\u9608\u503C ${fmtPct(EXPLAINER_THRESHOLDS.LOW_CONTRIBUTION_RATE)}\uFF0C\u6BCF\u4E2A\u8BA2\u5355\u7684\u5229\u6DA6\u7A7A\u95F4\u6709\u9650`,
        traceability: [
          { sourceType: "metric", sourceField: "contributionRate", sourceValue: m.contributionRate, ruleId: "KV02", explanation: "\u8D21\u732E\u7387 < 20% \u2192 \u6210\u672C/\u8D21\u732E\u662F\u5173\u952E\u53D8\u91CF" },
          { sourceType: "metric", sourceField: "contributionPerUnit", sourceValue: m.contributionPerUnit, ruleId: "KV02", explanation: "\u5355\u4F4D\u8D21\u732E" }
        ]
      });
    }
    const priceDeviation = m.theoreticalTargetPrice > 0 ? Math.abs(m.sellingPrice - m.theoreticalTargetPrice) / m.theoreticalTargetPrice : Infinity;
    if (priceDeviation < EXPLAINER_THRESHOLDS.PRICE_DEVIATION_RATIO && m.sellingPrice > 0) {
      vars.push({
        field: "sellingPrice",
        importance: "high",
        reason: `\u5F53\u524D\u552E\u4EF7 ${fmtMoney(m.sellingPrice)} \u4E0E\u7406\u8BBA\u76EE\u6807\u4EF7 ${fmtMoney(m.theoreticalTargetPrice)} \u76F8\u5DEE ${fmtPct(priceDeviation)} < \u9608\u503C ${fmtPct(EXPLAINER_THRESHOLDS.PRICE_DEVIATION_RATIO)}\uFF0C\u552E\u4EF7\u4E0A\u5347\u7A7A\u95F4\u53D7\u9650`,
        traceability: [
          { sourceType: "metric", sourceField: "sellingPrice", sourceValue: m.sellingPrice, ruleId: "KV03", explanation: "\u5F53\u524D\u552E\u4EF7" },
          { sourceType: "metric", sourceField: "theoreticalTargetPrice", sourceValue: m.theoreticalTargetPrice, ruleId: "KV03", explanation: "\u7406\u8BBA\u76EE\u6807\u4EF7" },
          { sourceType: "rule", sourceField: "priceDeviation", sourceValue: priceDeviation, ruleId: "KV03", explanation: "\u4EF7\u5DEE\u6BD4\u7387 < 5% \u2192 \u552E\u4EF7\u5173\u952E" }
        ]
      });
    }
    const fixedCostRatio = safeDiv(m.fixedCostMonthly, m.projectedMonthlyRevenue);
    if (fixedCostRatio > EXPLAINER_THRESHOLDS.HIGH_FIXED_COST_RATIO && m.projectedMonthlyRevenue > 0) {
      vars.push({
        field: "fixedCostMonthly",
        importance: "high",
        reason: `\u56FA\u5B9A\u6210\u672C ${fmtMoney(m.fixedCostMonthly)} \u5360\u9884\u8BA1\u6536\u5165 ${fmtPct(fixedCostRatio)} \u8D85\u8FC7\u9608\u503C ${fmtPct(EXPLAINER_THRESHOLDS.HIGH_FIXED_COST_RATIO)}\uFF0C\u56FA\u5B9A\u6210\u672C\u538B\u529B\u5927`,
        traceability: [
          { sourceType: "metric", sourceField: "fixedCostMonthly", sourceValue: m.fixedCostMonthly, ruleId: "KV04", explanation: "\u6708\u56FA\u5B9A\u6210\u672C" },
          { sourceType: "metric", sourceField: "projectedMonthlyRevenue", sourceValue: m.projectedMonthlyRevenue, ruleId: "KV04", explanation: "\u9884\u8BA1\u6708\u6536\u5165" },
          { sourceType: "rule", sourceField: "fixedCostRatio", sourceValue: fixedCostRatio, ruleId: "KV04", explanation: "\u56FA\u5B9A\u6210\u672C\u6536\u5165\u6BD4 > 15% \u2192 \u56FA\u5B9A\u6210\u672C\u5173\u952E" }
        ]
      });
    }
    const importanceRank = { critical: 0, high: 1, medium: 2, low: 3 };
    return vars.sort((a, b) => importanceRank[a.importance] - importanceRank[b.importance] || b.field.localeCompare(a.field));
  }
  function explainDecision(analysis) {
    const { metrics: m, judgment: j, scenario: s } = analysis;
    const tr = [];
    let headline;
    if (j.level === "profitable") {
      headline = `\u5F53\u524D\u5047\u8BBE\u4E0B\u5177\u5907\u76C8\u5229\u80FD\u529B\uFF0C\u5B89\u5168\u4F59\u91CF ${fmtPct(m.safetyMargin)}\u3002`;
      tr.push({ sourceType: "metric", sourceField: "safetyMargin", sourceValue: m.safetyMargin, ruleId: "H01", explanation: "headline \u6765\u6E90\u4E8E safetyMargin" });
      tr.push({ sourceType: "judgment", sourceField: "level", sourceValue: j.level, ruleId: "H01", explanation: "\u5224\u65AD\u4E3A profitable" });
    } else if (j.level === "loss") {
      headline = `\u5F53\u524D\u9500\u91CF\u4E0D\u8DB3\u4EE5\u8986\u76D6\u6708\u56FA\u5B9A\u6210\u672C\uFF0C\u9884\u8BA1\u4E8F\u635F\u3002`;
      tr.push({ sourceType: "judgment", sourceField: "level", sourceValue: j.level, ruleId: "H02", explanation: "\u5224\u65AD\u4E3A loss" });
      tr.push({ sourceType: "metric", sourceField: "projectedMonthlyProfit", sourceValue: m.projectedMonthlyProfit, ruleId: "H02", explanation: "\u5229\u6DA6\u4E3A\u8D1F" });
    } else {
      headline = `\u5F53\u524D\u552E\u4EF7\u65E0\u6CD5\u8986\u76D6\u5355\u4F4D\u53D8\u52A8\u6210\u672C\u53CA\u9500\u552E\u8D39\u7528\uFF0C\u4E0D\u5B58\u5728\u6709\u6548\u76C8\u4E8F\u5E73\u8861\u70B9\u3002`;
      tr.push({ sourceType: "judgment", sourceField: "level", sourceValue: j.level, ruleId: "H03", explanation: "\u5224\u65AD\u4E3A unviable" });
      tr.push({ sourceType: "metric", sourceField: "contributionPerUnit", sourceValue: m.contributionPerUnit, ruleId: "H03", explanation: "\u5355\u4F4D\u8D21\u732E \u2264 0" });
    }
    const analysisPoints = [];
    analysisPoints.push({
      id: "AP01",
      title: "\u5355\u4F4D\u8D21\u732E",
      description: `\u8D21\u732E\u7387 ${fmtPct(m.contributionRate)} \u2014 \u6BCF\u5356\u51FA 1 \u5355\uFF0C\u4ECE\u53D8\u52A8\u6210\u672C\u4E2D\u8D21\u732E ${fmtMoney(m.contributionPerUnit)}\u3002`,
      priority: m.contributionRate < EXPLAINER_THRESHOLDS.LOW_CONTRIBUTION_RATE ? "high" : "medium",
      traceability: [
        { sourceType: "metric", sourceField: "contributionPerUnit", sourceValue: m.contributionPerUnit, ruleId: "AP01", explanation: "\u5355\u4F4D\u8D21\u732E\u76F4\u63A5\u6765\u81EA engine" },
        { sourceType: "metric", sourceField: "contributionRate", sourceValue: m.contributionRate, ruleId: "AP01", explanation: "\u8D21\u732E\u7387 = \u5355\u4F4D\u8D21\u732E \xF7 \u552E\u4EF7" }
      ]
    });
    analysisPoints.push({
      id: "AP02",
      title: "\u76C8\u4E8F\u5E73\u8861",
      description: `\u7406\u8BBA\u4FDD\u672C ${fmtCountFloat(m.theoreticalBreakEvenMonthly)} \u5355/\u6708\uFF0C\u6700\u5C0F\u4FDD\u672C ${fmtCount(m.minimumBreakEvenMonthly)} \u5355/\u6708\uFF0C\u6267\u884C\u76EE\u6807 ${fmtCount(m.executionTargetMonthly)} \u5355/\u6708\u3002`,
      priority: "high",
      traceability: [
        { sourceType: "metric", sourceField: "theoreticalBreakEvenMonthly", sourceValue: m.theoreticalBreakEvenMonthly, ruleId: "AP02", explanation: "\u7406\u8BBA\u4FDD\u672C (float)" },
        { sourceType: "metric", sourceField: "minimumBreakEvenMonthly", sourceValue: m.minimumBreakEvenMonthly, ruleId: "AP02", explanation: "\u6700\u5C0F\u4FDD\u672C (ceil)" },
        { sourceType: "metric", sourceField: "executionTargetMonthly", sourceValue: m.executionTargetMonthly, ruleId: "AP02", explanation: "\u6267\u884C\u76EE\u6807" }
      ]
    });
    const safetyStatus = m.safetyMargin > 0.3 ? "\u5145\u8DB3" : m.safetyMargin > 0 ? "\u504F\u7D27" : "\u4E0D\u8DB3";
    const beGap = m.executionTargetMonthly - s.monthlySalesVolume;
    const gapText = beGap > 0 ? `\u8DDD\u6267\u884C\u76EE\u6807\u8FD8\u5DEE ${fmtCount(beGap)}` : `\u5DF2\u8D85\u51FA\u6267\u884C\u76EE\u6807 ${fmtCount(-beGap)}`;
    analysisPoints.push({
      id: "AP03",
      title: "\u5B89\u5168\u4F59\u91CF",
      description: `\u5B89\u5168\u4F59\u91CF ${fmtPct(m.safetyMargin)} \u2014 ${safetyStatus}\u3002${gapText}\u3002`,
      priority: m.safetyMargin < EXPLAINER_THRESHOLDS.LOW_SAFETY_MARGIN ? "high" : "medium",
      traceability: [
        { sourceType: "metric", sourceField: "safetyMargin", sourceValue: m.safetyMargin, ruleId: "AP03", explanation: "\u5B89\u5168\u4F59\u91CF" },
        { sourceType: "metric", sourceField: "executionTargetMonthly", sourceValue: m.executionTargetMonthly, ruleId: "AP03", explanation: "\u6267\u884C\u76EE\u6807" },
        { sourceType: "scenario", sourceField: "monthlySalesVolume", sourceValue: s.monthlySalesVolume, ruleId: "AP03", explanation: "\u9884\u8BA1\u9500\u91CF" }
      ]
    });
    analysisPoints.push({
      id: "AP04",
      title: "\u7ECF\u8425\u5229\u6DA6",
      description: `\u9884\u8BA1\u6708\u7ECF\u8425\u5229\u6DA6 ${fmtMoney(m.projectedMonthlyProfit)}\uFF0C\u5229\u6DA6\u7387 ${fmtPct(m.operatingMargin)}\uFF0C\u6536\u5165 ${fmtMoney(m.projectedMonthlyRevenue)}\u3002`,
      priority: m.operatingMargin < EXPLAINER_THRESHOLDS.LOSS_MARGIN ? "high" : "medium",
      traceability: [
        { sourceType: "metric", sourceField: "projectedMonthlyProfit", sourceValue: m.projectedMonthlyProfit, ruleId: "AP04", explanation: "\u5229\u6DA6" },
        { sourceType: "metric", sourceField: "operatingMargin", sourceValue: m.operatingMargin, ruleId: "AP04", explanation: "\u5229\u6DA6\u7387" }
      ]
    });
    const riskFactors = [];
    if (j.level === "unviable") {
      riskFactors.push({
        id: "RF01",
        level: "BLOCK",
        title: "\u65E0\u6CD5\u76C8\u5229",
        description: `\u5355\u4F4D\u8D21\u732E ${fmtMoney(m.contributionPerUnit)} \u2264 0\uFF0C\u65E0\u6CD5\u627E\u5230\u6709\u6548\u76C8\u4E8F\u5E73\u8861\u70B9\u3002`,
        priority: "high",
        traceability: [
          { sourceType: "metric", sourceField: "contributionPerUnit", sourceValue: m.contributionPerUnit, ruleId: "RF01", explanation: "\u5355\u4F4D\u8D21\u732E \u2264 0 \u2192 \u4E0D\u53EF\u7ECF\u8425" }
        ]
      });
    } else if (j.level === "loss") {
      riskFactors.push({
        id: "RF02",
        level: "HIGH",
        title: "\u9500\u91CF\u4E0D\u8DB3",
        description: `\u9884\u8BA1\u9500\u91CF ${fmtCount(s.monthlySalesVolume)} \u4F4E\u4E8E\u6267\u884C\u76EE\u6807 ${fmtCount(m.executionTargetMonthly)}\u3002`,
        priority: "high",
        traceability: [
          { sourceType: "metric", sourceField: "executionTargetMonthly", sourceValue: m.executionTargetMonthly, ruleId: "RF02", explanation: "\u6267\u884C\u76EE\u6807" },
          { sourceType: "scenario", sourceField: "monthlySalesVolume", sourceValue: s.monthlySalesVolume, ruleId: "RF02", explanation: "\u9884\u8BA1\u9500\u91CF" }
        ]
      });
    } else {
      if (m.safetyMargin < EXPLAINER_THRESHOLDS.LOW_SAFETY_MARGIN) {
        riskFactors.push({
          id: "RF03",
          level: "WARNING",
          title: "\u5B89\u5168\u4F59\u91CF\u4E0D\u8DB3",
          description: `\u5B89\u5168\u4F59\u91CF\u4EC5 ${fmtPct(m.safetyMargin)}\uFF0C\u4F4E\u4E8E ${fmtPct(EXPLAINER_THRESHOLDS.LOW_SAFETY_MARGIN)} \u9608\u503C\u3002`,
          priority: "high",
          traceability: [
            { sourceType: "metric", sourceField: "safetyMargin", sourceValue: m.safetyMargin, ruleId: "RF03", explanation: "\u5B89\u5168\u4F59\u91CF < 10%" }
          ]
        });
      }
      if (m.contributionRate < EXPLAINER_THRESHOLDS.LOW_CONTRIBUTION_RATE) {
        riskFactors.push({
          id: "RF04",
          level: "WARNING",
          title: "\u8D21\u732E\u7387\u8F83\u4F4E",
          description: `\u8D21\u732E\u7387 ${fmtPct(m.contributionRate)} \u4F4E\u4E8E ${fmtPct(EXPLAINER_THRESHOLDS.LOW_CONTRIBUTION_RATE)}\uFF0C\u76C8\u5229\u7A7A\u95F4\u6709\u9650\u3002`,
          priority: "medium",
          traceability: [
            { sourceType: "metric", sourceField: "contributionRate", sourceValue: m.contributionRate, ruleId: "RF04", explanation: "\u8D21\u732E\u7387 < 20%" }
          ]
        });
      }
      const fixedCostRatioRF = safeDiv(m.fixedCostMonthly, m.projectedMonthlyRevenue);
      if (fixedCostRatioRF > EXPLAINER_THRESHOLDS.HIGH_FIXED_COST_RATIO && m.projectedMonthlyRevenue > 0) {
        riskFactors.push({
          id: "RF05",
          level: "HIGH",
          title: "\u56FA\u5B9A\u6210\u672C\u538B\u529B\u8F83\u9AD8",
          description: `\u56FA\u5B9A\u6210\u672C ${fmtMoney(m.fixedCostMonthly)} \u5360\u9884\u8BA1\u6708\u6536\u5165\u7EA6 ${fmtPct(fixedCostRatioRF)}\uFF0C\u8D85\u8FC7 ${fmtPct(EXPLAINER_THRESHOLDS.HIGH_FIXED_COST_RATIO)} \u98CE\u9669\u9608\u503C\u3002`,
          priority: "high",
          traceability: [
            { sourceType: "metric", sourceField: "fixedCostMonthly", sourceValue: m.fixedCostMonthly, ruleId: "RF05", explanation: "\u6708\u56FA\u5B9A\u6210\u672C" },
            { sourceType: "metric", sourceField: "projectedMonthlyRevenue", sourceValue: m.projectedMonthlyRevenue, ruleId: "RF05", explanation: "\u9884\u8BA1\u6708\u6536\u5165" },
            { sourceType: "rule", sourceField: "fixedCostRatio", sourceValue: fixedCostRatioRF, ruleId: "RF05", explanation: "\u56FA\u5B9A\u6210\u672C\u6536\u5165\u6BD4 > 15% \u2192 \u56FA\u5B9A\u6210\u672C\u98CE\u9669 HIGH" }
          ]
        });
      }
    }
    const keyVariables = rankKeyVariables(m, s);
    const suggestedActions = [];
    if (j.level === "unviable") {
      suggestedActions.push({
        id: "SA01",
        priority: "high",
        title: "\u8C03\u6574\u552E\u4EF7\u6216\u964D\u4F4E\u6210\u672C",
        description: "\u5F53\u524D\u5355\u4F4D\u8D21\u732E \u2264 0\uFF0C\u5FC5\u987B\u63D0\u9AD8\u552E\u4EF7\u6216\u964D\u4F4E\u53D8\u52A8\u6210\u672C\u540E\u518D\u8BC4\u4F30\u3002",
        metricFields: ["contributionPerUnit", "sellingPrice", "variableCostPerUnit"],
        traceability: [
          { sourceType: "metric", sourceField: "contributionPerUnit", sourceValue: m.contributionPerUnit, ruleId: "SA01", explanation: "\u8D21\u732E \u2264 0 \u2192 \u5FC5\u987B\u8C03\u6574" }
        ]
      });
    } else if (j.level === "loss") {
      suggestedActions.push({
        id: "SA02",
        priority: "high",
        title: "\u63D0\u5347\u9500\u91CF",
        description: `\u5F53\u524D\u9884\u8BA1\u9500\u91CF ${fmtCount(s.monthlySalesVolume)} \u4F4E\u4E8E\u6267\u884C\u76EE\u6807 ${fmtCount(m.executionTargetMonthly)}\uFF0C\u9700\u8981\u589E\u52A0 ${m.executionTargetMonthly - s.monthlySalesVolume} \u5355\u3002`,
        metricFields: ["monthlySalesVolume", "executionTargetMonthly", "safetyMargin"],
        traceability: [
          { sourceType: "scenario", sourceField: "monthlySalesVolume", sourceValue: s.monthlySalesVolume, ruleId: "SA02", explanation: "\u9884\u8BA1\u9500\u91CF" },
          { sourceType: "metric", sourceField: "executionTargetMonthly", sourceValue: m.executionTargetMonthly, ruleId: "SA02", explanation: "\u6267\u884C\u76EE\u6807" }
        ]
      });
    } else {
      if (m.safetyMargin < EXPLAINER_THRESHOLDS.LOW_SAFETY_MARGIN) {
        suggestedActions.push({
          id: "SA03",
          priority: "high",
          title: "\u5148\u786E\u8BA4\u9500\u91CF",
          description: "\u5B89\u5168\u4F59\u91CF\u4E0D\u8DB3\uFF0C\u5E94\u4F18\u5148\u9A8C\u8BC1\u771F\u5B9E\u6708\u9500\u91CF\u662F\u5426\u7A33\u5B9A\u8FBE\u5230\u6267\u884C\u76EE\u6807\u3002",
          metricFields: ["safetyMargin", "monthlySalesVolume", "executionTargetMonthly"],
          traceability: [
            { sourceType: "metric", sourceField: "safetyMargin", sourceValue: m.safetyMargin, ruleId: "SA03", explanation: "\u5B89\u5168\u4F59\u91CF < 10% \u2192 \u9500\u91CF\u4F18\u5148" }
          ]
        });
      } else {
        const fixedCostRatioSA = safeDiv(m.fixedCostMonthly, m.projectedMonthlyRevenue);
        const fixedCostNote = fixedCostRatioSA > EXPLAINER_THRESHOLDS.HIGH_FIXED_COST_RATIO && m.projectedMonthlyRevenue > 0 ? `\uFF0C\u540C\u65F6\u56FA\u5B9A\u6210\u672C\u5360\u9884\u8BA1\u6708\u6536\u5165\u7EA6 ${fmtPct(fixedCostRatioSA)}\uFF08\u8D85\u8FC7 ${fmtPct(EXPLAINER_THRESHOLDS.HIGH_FIXED_COST_RATIO)} \u9608\u503C\uFF09\uFF0C\u5EFA\u8BAE\u5BA1\u89C6\u56FA\u5B9A\u6210\u672C\u7ED3\u6784` : "";
        suggestedActions.push({
          id: "SA04",
          priority: "high",
          title: "\u7A33\u5B9A\u6267\u884C\u89C4\u6A21",
          description: `\u5F53\u524D\u5904\u4E8E\u76C8\u5229\u533A\u95F4\uFF0C\u5B89\u5168\u4F59\u91CF ${fmtPct(m.safetyMargin)}\uFF0C\u53EF\u4E13\u6CE8\u63D0\u5347\u5355\u4F4D\u8D21\u732E\u7387\u6216\u6269\u5C55\u9500\u91CF${fixedCostNote}\u3002`,
          metricFields: ["safetyMargin", "contributionRate", "projectedMonthlyProfit", "fixedCostMonthly"],
          traceability: [
            { sourceType: "metric", sourceField: "safetyMargin", sourceValue: m.safetyMargin, ruleId: "SA04", explanation: "\u5B89\u5168\u4F59\u91CF \u2265 10% \u2192 \u7A33\u5B9A\u6267\u884C\u89C4\u6A21" }
          ]
        });
      }
      if (m.contributionRate < EXPLAINER_THRESHOLDS.LOW_CONTRIBUTION_RATE) {
        suggestedActions.push({
          id: "SA05",
          priority: "medium",
          title: "\u4F18\u5316\u5355\u4F4D\u6210\u672C",
          description: `\u8D21\u732E\u7387 ${fmtPct(m.contributionRate)} \u8F83\u4F4E\uFF0C\u964D\u4F4E\u53D8\u52A8\u6210\u672C\u53EF\u76F4\u63A5\u63D0\u5347\u5355\u4F4D\u8D21\u732E\u3002`,
          metricFields: ["contributionRate", "contributionPerUnit", "variableCostPerUnit"],
          traceability: [
            { sourceType: "metric", sourceField: "contributionRate", sourceValue: m.contributionRate, ruleId: "SA05", explanation: "\u8D21\u732E\u7387 < 20% \u2192 \u4F18\u5316\u6210\u672C" }
          ]
        });
      }
    }
    const allTrace = [
      ...tr,
      ...analysisPoints.flatMap((a) => a.traceability),
      ...riskFactors.flatMap((r) => r.traceability),
      ...keyVariables.flatMap((k) => k.traceability),
      ...suggestedActions.flatMap((a) => a.traceability)
    ];
    return {
      judgment: j,
      headline,
      analysisPoints,
      riskFactors,
      keyVariables,
      suggestedActions,
      traceability: allTrace
    };
  }
  return __toCommonJS(engine_exports);
})();
