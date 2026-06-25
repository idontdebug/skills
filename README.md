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

## License

[MIT](./LICENSE)
