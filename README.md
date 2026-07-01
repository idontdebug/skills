# skills

我日常使用的 agent skills,可在任意支持的 coding agent 中一键安装。

## 安装

通过 [`npx skills`](https://github.com/vercel-labs/skills) 安装:

```bash
# 安装本仓库全部 skill
npx skills add idontdebug/skills

# 只安装某个 skill
npx skills add idontdebug/skills --skill explain-code

# 查看可用的 skill
npx skills add idontdebug/skills --list
```

支持 Claude Code、Codex、Cursor、Droid 等 70+ agent,会自动检测已安装的 agent 并写入对应的 `skills/` 目录。

## Skills

### explain-code

按需调用的代码业务逻辑讲解器。指给它一段代码,它不会逐行复述语法,而是讲清楚这段代码在**业务上**做了什么、为什么这么做,并产出一个**自包含的 HTML 解释页**(Tailwind 样式、浅/深色、离线单文件),用具体走查例子 + 可视化图表(流程图、时序图、状态图、时间轴、决策表)来帮你建立心智模型。

仅在显式调用时运行(`/explain-code` 或明确要求用该 skill),不会自动触发。

### story-test

为 Vue 3 + Vite 项目配置 Storybook + Vitest addon,并为组件编写带 `play` 断言的 **stories**,在真实浏览器里逐个状态地验证 UI 行为(每个状态在侧边栏直接显示通过/失败)。适用于:测试 Vue 组件、验证输入框/按钮/表单是否正常、覆盖边界情况(空值、超长文本、纯空白、特殊字符、禁用态)、接入 Storybook、编写 stories、搭建组件/交互测试——即使你没提到 "Storybook" 也会触发。

### adversarial-review

用对抗性思维审查规格类文档(OpenSpec change proposal、设计文档、PRD、RFC)。读完文档后列出关键决策/假设/现状声称的清单,逐条用**假设挖掘、失败场景构造、反方案/魔鬼代言人、歧义遗漏检测**四种手法找茬,有代码库时会用 Grep/Read 交叉核实文档里关于"现状"的声称,再回头自我验证过滤掉纯粹为挑刺而挑刺的伪问题,最后把站得住脚的发现按严重度排序输出。只读,不会帮你改文档。

仅在显式调用时运行(明确要求做对抗性/红队审查),不会在你写文档时自动触发。

## License

[MIT](./LICENSE)
