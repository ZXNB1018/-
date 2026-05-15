# 自动化股票交易系统 Agent 架构草案

本文给出一个面向实盘/仿真的自动化股票交易系统（Agent-Driven Trading System）的大体架构，目标是：
- 可扩展（支持多策略、多市场）
- 可观测（全链路日志、监控、审计）
- 可控风控（事前/事中/事后）
- 可迭代（研究→回测→仿真→小资金实盘）

---

## 1. 总体分层

建议采用“研究层 + 决策层 + 执行层 + 风控层 + 平台层”的五层结构：

1. **研究层（Research）**
   - 数据清洗、特征工程、因子挖掘
   - 策略原型开发与回测评估
   - 产出可部署的策略版本（模型参数 + 信号逻辑）

2. **决策层（Decision Agent）**
   - 汇总实时行情、账户状态、策略信号
   - 通过规则/模型生成交易意图（买/卖/调仓）
   - 输出标准化订单请求（含优先级、时效、风险标签）

3. **执行层（Execution）**
   - 订单切片与路由（券商 API）
   - 成交回报处理、重试与异常恢复
   - 提供成交质量分析（滑点、冲击成本）

4. **风控层（Risk Control）**
   - 事前：仓位、杠杆、行业集中度、黑名单
   - 事中：价格偏离、下单频率、单笔金额、熔断逻辑
   - 事后：VaR、最大回撤、归因分析、告警升级

5. **平台层（Platform / Infra）**
   - 任务编排、消息总线、缓存、数据库
   - 日志、监控、审计追踪、权限控制
   - CI/CD 与配置中心、密钥管理

---

## 2. Agent 视角的核心模块

可以将系统抽象为多个协作 Agent：

- **Market Agent（市场感知）**
  - 订阅行情、新闻、财报、宏观事件
  - 进行数据标准化并输出“市场状态快照”

- **Signal Agent（信号生成）**
  - 运行多策略（趋势、均值回复、事件驱动等）
  - 输出统一信号：`symbol, side, score, horizon, confidence`

- **Portfolio Agent（组合优化）**
  - 基于信号和风险预算做权重分配
  - 约束：行业暴露、单票上限、换手率、交易成本

- **Risk Agent（风险裁决）**
  - 对候选订单做准入审批
  - 可降级：缩量、延迟、拒单、强平

- **Execution Agent（执行代理）**
  - 将目标仓位转换为可执行订单
  - 支持 TWAP/VWAP/冰山等执行算法（后续扩展）

- **Ops Agent（运维守护）**
  - 健康检查、告警路由、自动恢复
  - 关键异常触发“人工接管模式”

---

## 3. 关键数据流（简化）

1. 数据源进入实时/离线管道（行情、基本面、替代数据）
2. Signal Agent 周期性或事件驱动生成候选信号
3. Portfolio Agent 生成目标持仓（Target Portfolio）
4. Risk Agent 审批并附加风控限制
5. Execution Agent 下单并接收成交回报
6. 回报写入账本与特征存储，反馈给研究层做持续学习

---

## 4. 存储与基础设施建议

- **时序数据**：行情、指标、PnL 曲线（如 Timescale/ClickHouse）
- **事务数据**：订单、成交、持仓、资金流水（PostgreSQL）
- **缓存层**：热点行情与风控阈值（Redis）
- **消息系统**：模块解耦（Kafka / NATS）
- **对象存储**：模型、回测报告、日志归档（S3 兼容）

---

## 5. 风控框架（最小可用集）

上线初期建议至少具备：

- 单票最大仓位限制（如 ≤ 总资产 10%）
- 组合最大回撤阈值（触发减仓/停机）
- 日内最大交易次数与最大成交额限制
- 异常波动暂停（价格跳变、流动性骤降）
- 券商连接异常时自动进入“只减仓不加仓”模式

---

## 6. 开发路线图（MVP → Production）

### 阶段 A：MVP（2~4 周）
- 单市场（例如美股）
- 单策略（例如均线趋势）
- 单券商仿真接口
- 基础回测 + 纸面交易 + 简单风控

### 阶段 B：增强版（4~8 周）
- 多策略组合与仓位优化
- 完整订单生命周期管理
- 监控看板与告警系统

### 阶段 C：生产化（持续迭代）
- 灰度实盘（小资金）
- 执行算法优化与交易成本建模
- 模型治理（版本、回滚、漂移监控）

---

## 7. 目录结构建议

```text
trading-agent/
  README.md
  configs/
    base.yaml
    prod.yaml
  data_pipeline/
    ingest/
    feature_store/
  research/
    factors/
    backtest/
  agents/
    market_agent/
    signal_agent/
    portfolio_agent/
    risk_agent/
    execution_agent/
  execution/
    broker_adapters/
    order_manager/
  risk/
    pre_trade/
    in_trade/
    post_trade/
  services/
    api/
    scheduler/
    monitoring/
  infra/
    docker/
    k8s/
  tests/
```

---

## 8. 技术选型（参考）

- **语言**：Python（研究与策略快迭代） + Go/Java（高性能执行模块可选）
- **回测**：vectorbt / backtrader / 自研撮合内核
- **编排**：Airflow / Prefect
- **服务框架**：FastAPI + gRPC
- **可观测性**：Prometheus + Grafana + OpenTelemetry

---

## 9. 合规与安全提示

- 严格隔离研发、仿真、实盘环境
- API Key 使用密钥管理系统，不明文落库
- 所有交易决策与参数变更必须审计留痕
- 实盘前进行压力测试、故障演练、回滚演练

> 免责声明：以上内容仅为系统设计与工程实践参考，不构成任何投资建议。
