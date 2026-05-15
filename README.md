# 自动化股票交易系统 Agent 架构与开发启动

本文先给出总体架构，并已按路线图启动 **阶段 A（MVP）** 的最小代码骨架。

## 当前进度（2026-05-15）

- ✅ 完成高层架构文档
- ✅ 初始化项目目录结构（agents / risk / execution / services / tests）
- ✅ 落地首个示例策略：SMA Cross Signal Agent
- ✅ 落地最小事前风控检查（最大仓位）
- ✅ 落地统一订单请求模型
- ✅ 落地单周期调度入口（paper loop）
- ✅ 添加策略单元测试样例

---

## 1. 总体分层

建议采用“研究层 + 决策层 + 执行层 + 风控层 + 平台层”的五层结构：

1. **研究层（Research）**：因子、特征、回测与评估
2. **决策层（Decision Agent）**：行情/账户/策略信号融合决策
3. **执行层（Execution）**：订单路由、成交回报、执行质量
4. **风控层（Risk Control）**：事前/事中/事后风险约束
5. **平台层（Platform）**：编排、存储、监控、审计、权限

---

## 2. Agent 协作模块

- **Market Agent**：市场数据摄取与标准化
- **Signal Agent**：策略信号生成
- **Portfolio Agent**：目标仓位优化
- **Risk Agent**：风险审批与降级
- **Execution Agent**：订单执行与回报
- **Ops Agent**：监控告警与自动恢复

---

## 3. 已启动的 MVP 代码骨架

```text
trading_agent/
  __init__.py
  configs/
    base.yaml
  agents/
    signal_agent/
      strategy.py
  risk/
    pre_trade/
      checks.py
  execution/
    order_manager/
      orders.py
  services/
    scheduler/
      run_cycle.py
  tests/
    test_strategy.py
```

---

## 4. MVP 首个实现说明

### 4.1 Signal Agent（SMA Cross）
- 输入：`symbol + close prices`
- 逻辑：快均线高于慢均线 => `BUY`；否则 `HOLD`
- 输出：标准信号对象 `Signal(symbol, side, confidence)`

### 4.2 Risk Agent（Pre-trade）
- 规则：单票目标仓位不得超过净值比例上限
- 返回：`RiskDecision(approved, reason)`

### 4.3 Execution Domain Model
- 统一订单请求：`OrderRequest(symbol, side, quantity, order_type)`

### 4.4 Scheduler
- 提供 `run_cycle(...)` 作为单轮调度入口，便于后续接入实时数据与券商适配器

---

## 5. 下一步（按路线图继续）

1. 接入 Paper Broker Adapter（模拟下单/成交）
2. 串联完整链路：Signal -> Risk -> Order -> Fill
3. 增加持仓与资金账本
4. 增加日内风控（交易次数、最大成交额、熔断）
5. 增加基础监控指标（信号数、拒单数、成交率、PnL）

---

## 6. 运行与测试（本地）

```bash
python -m pytest trading_agent/tests -q
```

> 免责声明：以上内容仅为系统设计与工程实践参考，不构成任何投资建议。
