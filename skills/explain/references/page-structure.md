# 解释页结构与组件（写入 `__CONTENT__`）

页面骨架（顶部导航栏 #1、深色切换、导出 PDF、Mermaid 缩放/重置、表格搜索筛选、打印优化）都在 `assets/template.html` 里，且 Tailwind 与 Mermaid 已内联。你只需把**第 2–8 个区块**的 HTML 写进 `content.html`（即模板的 `__CONTENT__`）。导航栏(#1) 由模板用 `--title` / `--path` 填充。

样式用模板预定义的 Tailwind 组件类（`@apply` 定义），直接写短类名即可；需要时也可叠加任意 Tailwind 工具类。**严格按下面 1→8 的顺序**。

## JS 钩子约定（必须遵守，否则交互失效）
- **可缩放图**：`<div class="diagram"><pre class="mermaid">…</pre></div>`。脚本会渲染 Mermaid 并自动加缩放/重置工具条。手写 SVG 同样放进 `<div class="diagram">`。
- **规则矩阵搜索/筛选**：外层 `<div data-rules>`，内含 `<input data-rules-search>`、`<select data-rules-filter>`（option 的 value 用 `all/high/med/low`），表格 `<tbody>` 每行 `<tr data-risk="high|med|low|none">`。脚本按文本 + 风险等级过滤。
- **手风琴**：原生 `<details class="acc"><summary>…</summary><div class="acc-body">…</div></details>`，打印时自动展开。
- **导航**：每个 `<section id="...">` 带 `<h2 class="h-sec">`，顶部导航会自动收录（Hero 用 `<h1>`，不进导航）。

## 区块模板（按顺序）

### 2. Hero + 关键指标卡片
```html
<section id="hero" class="section">
  <div class="rounded-2xl border border-slate-200 dark:border-slate-700 bg-gradient-to-br from-brand-50 to-white dark:from-slate-800 dark:to-slate-900 p-7">
    <span class="chip mb-3"><b>业务逻辑讲解</b></span>
    <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">XxxService.method —— 一句话定位</h1>
    <p class="lead mt-2 max-w-3xl">为谁、解决什么问题。</p>
  </div>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
    <div class="metric"><div class="kpi-num">5</div><div class="kpi-label">处理分支</div></div>
    <div class="metric"><div class="kpi-num">3</div><div class="kpi-label">订单状态</div></div>
    <div class="metric"><div class="kpi-num">4</div><div class="kpi-label">返回码</div></div>
    <div class="metric"><div class="kpi-num">3</div><div class="kpi-label">已知风险</div></div>
  </div>
</section>
```

### 3. 执行摘要（业务高层概述）
```html
<section id="summary" class="section">
  <h2 class="h-sec"><span class="idx">01</span>执行摘要</h2>
  <div class="callout callout-note"><p class="lead">面向非作者读者的 3–5 句高层概述：这段代码在业务上做什么、关键分流维度、最该注意的一点。</p></div>
</section>
```

### 4. 核心业务流程（大图 + 控制按钮 + 步骤列表）
缩放/重置按钮由脚本自动加，无需手写。
```html
<section id="flow" class="section">
  <h2 class="h-sec"><span class="idx">02</span>核心业务流程</h2>
  <div class="diagram">
    <pre class="mermaid">
flowchart TD
  S["入口"] --> Q1{"orderType == 充值?"}
  Q1 -- 是 --> R1["改资金账<br/>return 0001"]
  Q1 -- 否 --> C["通用计费"]
    </pre>
    <div class="cap">命中即 return；颜色与下方步骤/卡片对应</div>
  </div>
  <ol class="steps mt-4">
    <li><b>第一步</b>：……</li>
    <li><b>第二步</b>：……</li>
  </ol>
</section>
```

### 5. 详细逻辑拆解（手风琴：每步含业务含义 + 技术说明）
```html
<section id="detail" class="section">
  <h2 class="h-sec"><span class="idx">03</span>详细逻辑拆解</h2>
  <details class="acc" open>
    <summary>① 充值分支 <span class="badge badge-info ml-1">return 0001</span></summary>
    <div class="acc-body">
      <p><b>业务含义：</b>充值不是停车订单，只改"钱"的账，不碰 order 表。</p>
      <p class="mt-2"><b>技术说明：</b>命中 <code>orderType=="充值"</code> 时，改 <code>SettlementDetails</code> / <code>TradeRelationship</code> 渠道为 <code>balance-recharge</code>，调 <code>notifyForReCharge</code>。</p>
    </div>
  </details>
  <details class="acc">
    <summary>② 长租分支 <span class="badge badge-info ml-1">return 0002</span></summary>
    <div class="acc-body">…</div>
  </details>
</section>
```

### 6. 业务规则矩阵（可搜索 + 风险筛选；风险用彩色徽章）
```html
<section id="rules" class="section">
  <h2 class="h-sec"><span class="idx">04</span>业务规则矩阵</h2>
  <div data-rules class="card !p-0 overflow-hidden">
    <div class="flex flex-wrap gap-2 p-3 border-b border-slate-200 dark:border-slate-700">
      <input data-rules-search type="search" placeholder="搜索规则 / 条件…" class="flex-1 min-w-[160px] rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 px-3 py-1.5 text-sm">
      <select data-rules-filter class="rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 px-3 py-1.5 text-sm">
        <option value="all">全部风险</option><option value="high">高</option><option value="med">中</option><option value="low">低</option>
      </select>
    </div>
    <div class="overflow-x-auto">
      <table class="tbl">
        <thead><tr><th>规则</th><th>条件</th><th>结果</th><th>风险</th></tr></thead>
        <tbody>
          <tr data-risk="high"><td>SOLID 不落库</td><td><code>parkingType ∉ {road,seal}</code></td><td>声称成功但不 update</td><td><span class="badge badge-high">高</span></td></tr>
          <tr data-risk="low"><td>长租全额</td><td><code>orderType=="长租"</code></td><td>PAID，实收=计费</td><td><span class="badge badge-low">低</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
```

### 7. 风险与改进建议（卡片网格，按严重程度分类）
```html
<section id="risks" class="section">
  <h2 class="h-sec"><span class="idx">05</span>风险与改进建议</h2>
  <div class="grid md:grid-cols-2 gap-3">
    <div class="riskcard riskcard-high">
      <div class="flex items-center gap-2 mb-1.5"><span class="badge badge-high">高</span><span class="card-t">SOLID 类型静默不落库</span></div>
      <p class="text-sm text-slate-600 dark:text-slate-300">末尾只有 ROAD/SEAL 两个 if、无 else，其它类型改了内存却不 update。</p>
      <p class="text-sm mt-2"><b>建议：</b>补 else 分支或断言，至少记录告警日志。</p>
    </div>
    <div class="riskcard riskcard-med">
      <div class="flex items-center gap-2 mb-1.5"><span class="badge badge-med">中</span><span class="card-t">充值分支不判空</span></div>
      <p class="text-sm text-slate-600 dark:text-slate-300">…</p>
    </div>
  </div>
</section>
```

### 8. 附录（元数据）
```html
<section id="appendix" class="section">
  <h2 class="h-sec"><span class="idx">06</span>附录</h2>
  <div class="grid sm:grid-cols-3 gap-3 text-sm">
    <div class="card"><div class="card-t">分析对象</div><code>src/.../OrderService.java#updateOrderWhenPaySuccess</code></div>
    <div class="card"><div class="card-t">相关文件</div><ul class="mt-1 space-y-1"><li><code>OrderService.java:1085</code></li><li><code>OrderStatusEnum.java</code></li></ul></div>
    <div class="card"><div class="card-t">生成时间</div>2026-06-25 · explain skill</div>
  </div>
</section>
```

## 组件速查
- 提示框：`callout callout-note`（蓝）/ `callout callout-warn`（橙）/ `callout callout-ok`（绿）；内用 `<span class="ctag">标签</span>` 起头。
- 徽章：`badge badge-high|badge-med|badge-low|badge-info`。
- 卡片：`card` + `card-t`（标题）；指标卡 `metric` + `kpi-num` + `kpi-label`；风险卡 `riskcard riskcard-high|med|low`。
- 步骤条：`<ol class="steps">`，数值高亮 `<span class="val">6.00</span>`。
- 图说明：`<div class="cap">`。并排：`grid md:grid-cols-2 gap-3`。

## 图的画法
- 标准图用 `<pre class="mermaid">`（`flowchart` / `sequenceDiagram` / `stateDiagram-v2` / `gantt`）。中文标签**务必加引号**：`A["订单=已支付"]`，否则 `()=+:` 会让解析失败。
- 定制图（如收费/免费时间段涂色的时间轴）直接在 `<div class="diagram">` 里手写内联 `<svg>`——零依赖、离线稳、贴合内容。
- 每张图都进 `<div class="diagram">` 才能获得缩放/重置工具条。
