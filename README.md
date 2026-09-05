# AI Revenue Recovery Controller — Master Planning Document

Status: **Implementation Complete. Backend and Frontend fully functional.**

### Implementation Status
- **Razorpay SDK Integration**: Fully implemented. The AI safely orchestrates real payment captures and link generation via the sandbox API, backed by Tenacity auto-retries.
- **Saga State Machine**: Fully implemented. Replaced sequential stubs with an async, event-driven Pub/Sub saga for resilient case handling and LLM execution.
- **Escalations & Guardrails**: Fully implemented. Cases safely stall into the Human Review Queue when blocked by policies or when the AI falls back gracefully.
- **Real-time Recovery Analytics**: Fully implemented. Real live financial dashboards aggregating live amounts from successfully recovered cases.
- **Database Engine Portability**: The codebase utilizes an abstraction layer through `AbstractRepository` enabling engine-agnostic logic, currently utilizing SQLite via aiosqlite for simplicity of MVP setup.

## Table of Contents

**PART A — Problem, Solution & Product Definition**
1. The Problem
2. Our Solution
3. Tech Stack
4. Initial Scope (MVP)
5. Core Product Metric
6. Safety Principle
7. Scenario Detail (A–H)
8. Illustrative Industry Applications
9. Razorpay API Analysis (A, B, C)

**PART B — Backend Planning**
1. Backend Responsibilities
2. Core Backend Modules
3. Database Planning
4. Common Tool Layer
5. Agent Architecture
6. Event System
7. Recovery Case Lifecycle
8. Policy / Guardrail Planning
9. Analytics / Metrics
10. API Endpoint Planning
11. Razorpay Integration Boundary
12. Synthetic Data / Testing Plan
13. Failure Handling
14. Final Backend Architecture

**PART C — Low-Level Design: Structure, Patterns & Principles**
1. Project Structure (exceptions isolated)
2. Custom Exception Hierarchy
3. URL Versioning
4. SOLID Principles
5. Layering — Controller / Service / Repository
6. Design Patterns (full reference table)
7. AI Layer — Strategy + Factory
8. Repository Layer — Strategy Pattern (DB portability)
9. Dual Database — PostgreSQL + MongoDB
10. Facade Pattern — Orchestrator
11. Illustrative End-to-End Call Path

**PART D — Low-Level Design: Concurrency, Data & Security**
1. Saga Pattern & Locking
2. PostgreSQL Indexing Plan
3. JWT Authentication
4. Idempotency (Financial Actions)
5. Rate Limiting — Token Bucket
6. URL Protection
7. Swagger / API Docs
8. Code Clarity Guidelines
9. Caching Layer (Redis) + Connection Pooling
10. Observability (Logging, Metrics, Tracing, Health)
11. Migrations Strategy (Alembic)
12. Forward & Reverse Proxy
13. Soft Deletes + Pagination Conventions

**PART E — Consolidated Reference**
1. Updated Directory Skeleton (final)
2. Master Pattern Assignment Table
3. Coverage Checklist
4. Open Items / Next Steps

---

# PART A — Problem, Solution & Product Definition

## A.1 The Problem

Merchants lose revenue for many reasons:
- Payment failures
- Checkout abandonment
- Subscription payment failures
- Overdue invoices
- Repeated payment failures
- Customers intending to pay but not completing payment

Today, these are often handled using fixed rules and separate workflows.

**The problem is:** the system can detect that money was lost, but it doesn't intelligently understand why, choose the best recovery action, execute it, and verify whether the money was actually recovered.

## A.2 Our Solution — AI Revenue Recovery Controller

An AI agent that:

```
Detect revenue at risk → Understand the situation → Investigate the cause
→ Choose recovery strategy → Check merchant policies → Execute action through Razorpay
→ Verify outcome → Measure ₹ recovered → Record complete audit trail
```

We're building **closed-loop revenue recovery**, not just a chatbot or prediction model.

## A.3 Tech Stack

| Layer | Stack |
|---|---|
| Frontend | Next.js, TypeScript, Tailwind CSS, Recharts (analytics), WebSocket/SSE (live agent activity) |
| Backend | FastAPI, Python, Pydantic, SQLAlchemy, PostgreSQL |
| AI / Agent | LLM (Gemini/GPT), LangGraph orchestration, Tool Calling / Structured Outputs, prompt + policy-based reasoning, no custom ML initially |

## A.4 Initial Scope (MVP)

3 scenarios to start — enough variety without making the project enormous:

- **A. Failed payment recovery** — Payment failed → diagnose → retry/payment link → verify
- **B. Checkout abandonment** — Checkout abandoned → understand customer context → generate recovery intervention → payment completed?
- **C. Subscription/payment recovery** — Recurring payment failed → analyze history → choose bounded retry/reminder → verify recovery

## A.5 Core Product Metric

**North Star: ₹ Revenue Recovered**

```
Revenue at risk       ₹5,00,000
Cases analyzed             500
Recovery attempts           300
Successful recoveries       126
Revenue recovered      ₹1,72,400
Recovery rate              34.5%
```

Also tracked: recovery rate, successful interventions, failed interventions, false/unsafe actions prevented, average recovery time, unresolved cases.

## A.6 Safety Principle

The agent never gets unrestricted control over money.

```
LLM Agent → Proposed Action → Policy Engine → [Allowed → Razorpay API] | [Blocked → Human review]
```

Examples: max retry attempts = 2, max transaction = ₹10,000, max customer contacts = 2, recovery window = 7 days.

Addresses the hackathon's **bounded + gated + explainable + auditable** requirement directly.

## A.7 Scenario Detail (A–H)

### A. Failed Payment Recovery
Flow: `Payment failed → Diagnose → Recovery action → Verify`
Tools: get payment details; check merchant-level error frequency; get failure source/reason; get customer/payment history; get order details; decide recovery action; retry/create payment link; check payment status; record result.

### B. Checkout Abandonment
Flow: `Checkout abandoned → Understand customer → Intervention → Verify`
Tools: get checkout/order details; product rejection rate; customer history; cart/product details; previous abandonment/recovery attempts; generate intervention; send message/link; track completion; record outcome.

### C. Subscription/Recurring Payment Recovery
Flow: `Recurring payment failed → Analyze history → Bounded action → Verify`
Tools: get subscription details; failed payment details; customer payment history; previous retry attempts; determine strategy; retry/link/reminder; check status; record outcome.
*Tooling for each problem can be handled differently in different Python files.*

### D. Insurance Premium Recovery
Flow: `Premium AutoPay fails / policy at risk of lapse → Analyze context → Choose bounded intervention → Verify premium payment`
Capabilities: policy/subscription details; failed premium payment details; customer/payment history; previous attempts; determine failure cause; decide intervention (retry/link/reminder/escalation); execute; verify payment; record outcome/policy retained.
**Core objective:** Prevent avoidable policy lapses. 4th recovery scenario — underlying agent/tooling largely reusable.

### E. Protection Plan Churn Recovery *(parked)*
Difference from D: **D** = payment failed → prevent lapse. **E** = customer actively cancelling → understand why and attempt retention.
Broader framing: *Revenue Recovery = recovering money from failed payments AND preventing recurring revenue from disappearing through avoidable churn.*
**Not added to implementation yet** — potential 5th use case, revisit later for hackathon story vs scope tradeoff.

### F. Product Revenue Drop Recovery
Flow: `Revenue anomaly → Diagnose cause → Select intervention → Execute → Measure recovered revenue`
Moves from transaction-level to product/business-level recovery. Mostly LLM + analytics + APIs (statistical thresholds/rules for anomaly detection, not ML).

### G. Customer Churn & Revenue Recovery
Flow: `User activity/revenue drops → Diagnose churn cause → Select bounded retention intervention → User returns → Measure recovered revenue`
More interesting than blanket discounts — e.g. discovering "18% of users who experienced a cancellation fee became inactive" and targeting that cohort specifically.

### H. Transaction Volume / User Activity Recovery
Flow: `Transaction volume drops → Diagnose cause → Target affected users/transactions → Recovery intervention → Measure recovered GMV/revenue`
Expands beyond single payment failures to platform-level volume loss investigation.

## A.8 Illustrative Industry Applications

| Scenario | Revenue at risk | What our AI could do |
|---|---|---|
| 🎥 Content creators | Paid subscriptions/videos | Detect inactive subscribers → understand why → recommend content/renewal reminder → recover subscription |
| ✈️ MakeMyTrip / Cleartrip | Abandoned bookings | Detect abandonment → understand price/availability issue → send reminder/payment link |
| 🚆 IRCTC / travel platforms | Booking drop-off | Detect abandonment → identify friction → recover completed bookings |
| 🎬 Netflix / Prime / JioHotstar | Subscription churn | Detect cancellation risk → understand usage pattern → recommend content/renewal intervention |
| 🎵 Spotify / music platforms | Subscription churn | Detect inactive users → targeted retention intervention → recovery |
| 📚 EdTech | Course/subscription churn | Detect disengagement → relevant content/reminder → recovery |
| 🏋️ Gyms/apps | Membership churn | Detect inactivity → retention intervention → recovery |

## A.9 Razorpay API Analysis (A, B, C)

### A. Failed Payment Recovery

| Required Tool | Provided? | Capability |
|---|---|---|
| Get payment details | ✅ | `GET /v1/payments/:id` |
| Merchant error frequency | ❌ | We calculate from historical data |
| Exact failure source | ✅ | `error_source` |
| Failure/error reason | ✅ | `error_code`, `error_description`, `error_reason`, `error_step` |
| Customer/payment history | ⚠️ Partial | Customer API gives info; history needs our aggregation |
| Order details | ✅ | Orders API |
| Decide recovery action | ❌ | Our LLM agent |
| Retry payment | ⚠️ Not generic | No generic retry API — need a new payment flow |
| Create payment link | ✅ | `POST /v1/payment_links` |
| Check payment status | ✅ | Fetch Payment / Order APIs |
| Record recovery result | ❌ | Our database |

Razorpay exposes `error_code`, `error_description`, `error_source`, `error_step`, `error_reason`, and the `payment.failed` webhook to trigger our agent.

**🔥 Key Differentiator:** Razorpay tells us *why* a payment failed. We determine *how frequently this failure type occurs and what recovery action has historically worked best*:

```
Merchant payment history → Error frequency analysis
  ├── Bank failure rate
  ├── UPI failure rate
  ├── Product failure rate
  ├── Customer failure rate
  └── Time-based failure patterns
→ Context provided to LLM → Recovery decision
```

### B. Checkout Abandonment

| Required Tool | Provided? | What We Do |
|---|---|---|
| Checkout/order details | ✅/⚠️ | Orders API |
| Product rejection frequency | ❌ | Our analytics/database |
| Customer history | ⚠️ Partial | Customer API + our payment history |
| Cart/product details | ❌ | Our merchant-side DB |
| Previous abandonment/recovery attempts | ❌ | Our database |
| Generate recovery intervention | ❌ | LLM |
| Send message/payment link | ⚠️ Partial | Payment Link API + our messaging layer |
| Track completion | ✅ | Payment/Order APIs + webhooks |
| Record outcome | ❌ | Our database |

### C. Subscription / Recurring Payment Recovery

Razorpay already provides quite a lot here.

| Required Tool | Provided? | Capability |
|---|---|---|
| Subscription details | ✅ | `GET /v1/subscriptions/:id` |
| Failed recurring payment details | ✅ | Payment/Invoice APIs + webhooks |
| Customer payment history | ⚠️ Partial | We aggregate |
| Previous retry attempts | ⚠️ Partial | Razorpay state gives some; we track agent attempts |
| Determine recovery strategy | ❌ | Our LLM |
| Retry payment | ✅/⚠️ | Razorpay auto-retries subscription charges |
| Generate payment link | ✅ | Payment Links API |
| Send reminder | ⚠️ | Notification APIs / our messaging layer |
| Check subscription/payment status | ✅ | Subscription/Payment API |
| Record outcome | ❌ | Our database |

---

# PART B — Backend Planning

Scope carried forward as-is: Scenarios A–H, North Star metric, safety principle, and the Razorpay API analysis above. Nothing here adds new scenarios.

## B.1 Backend Responsibilities

**Backend (FastAPI + DB):** receive events (webhooks + analytics jobs); assemble case context; persist cases/attempts/decisions/policies/audit; invoke agent; run Policy Engine; execute allowed actions; verify outcomes; compute analytics; expose REST/WebSocket APIs.

**LLM/Agent:** diagnose *why* revenue is at risk (structured context only); choose strategy from an allowed action set; produce rationale; draft customer-facing content. **Never:** money math, direct Razorpay calls, bypassing policy.

**Razorpay:** source of truth for payments/orders/subscriptions/links; emits webhooks; executes requested money-movement actions.

**Merchant systems:** product/cart/catalog data; engagement/usage data; non-Razorpay messaging channels; business-specific policy inputs.

## B.2 Core Backend Modules

Modular monolith, one FastAPI app, folder-per-domain module:

```
app/
├── core/                 # config, DB session, logging, security
├── events/               # webhook receivers + internal event bus
├── payments/             # (A)
├── checkout/             # (B)
├── subscriptions/        # (C, D)
├── retention/            # (E parked, G) — organizing folder only
├── revenue_intelligence/ # (F, H) — organizing folder only
├── customer/             # profile + aggregated history
├── recovery/             # case lifecycle, state machine, orchestration
├── agent/                # LLM orchestration (LangGraph)
├── policies/             # guardrail engine
├── razorpay_client/      # Razorpay API wrapper
├── notifications/        # message dispatch
├── analytics/            # metrics + anomaly detection
├── audit/                # immutable audit trail
└── api/                  # route aggregation
```

`payments`/`checkout`/`subscriptions` stay separate since their Razorpay surfaces genuinely differ. `revenue_intelligence` and `retention` are organizing folders only — not new scenarios; E stays parked but visible.

## B.3 Database Planning

| Table | Purpose | Key Fields | Relationships |
|---|---|---|---|
| `merchants` | Merchant account + config | id, name, razorpay_key_ref, policy_profile_id | 1—N with everything |
| `customers` | Local customer record | id, merchant_id, razorpay_customer_id, contact_prefs | belongs to merchant |
| `products` | Merchant catalog | id, merchant_id, name, price, category | belongs to merchant |
| `orders` | Order/checkout record | id, merchant_id, customer_id, razorpay_order_id, status, cart_snapshot | FK customer, merchant |
| `payments` | Payment attempt mirror | id, merchant_id, order_id, razorpay_payment_id, status, error_code/reason/source | FK order |
| `subscriptions` | Recurring plan | id, merchant_id, customer_id, razorpay_subscription_id, type, status | FK customer |
| `subscription_charges` | Each charge attempt | id, subscription_id, razorpay_invoice_id, status, attempt_number | FK subscription |
| `recovery_cases` | Central case entity (A–H) | id, merchant_id, scenario_type, source_ref (polymorphic), state, opened_at, closed_at | FK merchant |
| `recovery_attempts` | Each action in a case | id, case_id, attempt_number, action_type, status, executed_at, result | FK recovery_cases |
| `agent_decisions` | LLM diagnosis + action + rationale | id, case_id, input_context_snapshot, diagnosis, proposed_action, confidence, rationale_text | FK recovery_cases |
| `policies` | Merchant guardrail config | id, merchant_id, max_retries, max_txn_amount, max_contacts, recovery_window_days, allowed_actions | FK merchant |
| `policy_evaluations` | Each policy check | id, case_id, attempt_id, decision, reason | FK case, attempt |
| `audit_logs` | Immutable state-change trail | id, case_id, actor, action, before_state, after_state, timestamp | FK case |
| `events` | Raw inbound events | id, merchant_id, source, event_type, payload, processed_at | FK merchant |
| `interventions` | Customer-facing content | id, case_id, channel, content, sent_at, link_ref | FK case |
| `revenue_anomalies` | Detected anomalies (F, H) | id, merchant_id, metric_type, baseline, observed, deviation_pct, detected_at | FK merchant |
| `metrics_snapshots` | Dashboard rollups | id, merchant_id, period, revenue_at_risk, revenue_recovered, recovery_rate, unresolved_cases | FK merchant |

`recovery_cases.source_ref` is polymorphic — one lifecycle table serves all scenarios A–H. Scenario E stays representable in the enum but inactive.

## B.4 Common Tool Layer

Consolidated once, reused across A–H:

- **Razorpay API tools:** `get_payment`, `get_order`, `get_subscription`, `create_payment_link`, `check_payment_status`, `check_subscription_status`
- **Database/analytics tools:** `get_merchant_error_frequency`, `get_product_rejection_rate`, `get_revenue_baseline`, `detect_anomaly` (statistical/rule-based)
- **Customer/context tools:** `get_customer_profile`, `get_customer_payment_history`, `get_previous_recovery_attempts`
- **Recovery-action tools:** `retry_or_create_payment_link` (generic, A/B/C/D), `send_reminder`, `escalate_to_human`
- **Verification tools:** `poll_payment_status`, `confirm_order_completed`, `confirm_subscription_active`
- **Policy/guardrail tools:** `evaluate_policy`, `check_idempotency`
- **Audit tools:** `record_decision`, `record_outcome`

Each scenario module calls into this shared layer with scenario-specific context, rather than owning duplicate tool implementations.

## B.5 Agent Architecture

```
Event → Context Collection → Diagnosis → Reasoning → Proposed Action
      → Policy Check → Execution → Verification → Outcome
```

| Stage | Deterministic / LLM |
|---|---|
| Event ingestion | Deterministic |
| Context collection | Deterministic |
| Diagnosis | **LLM** |
| Reasoning/strategy selection | **LLM** (fixed action enum, not free text) |
| Proposed action | Schema-validated LLM output |
| Policy check | Deterministic |
| Execution | Deterministic |
| Verification | Deterministic |
| Outcome + metrics | Deterministic |

LLM never touches money math or calls Razorpay directly — output constrained to a predefined action enum + structured fields.

## B.6 Event System

| Event | Source |
|---|---|
| `payment.failed` | Razorpay webhook |
| `checkout.abandoned` | Our analytics |
| `subscription.charge.failed` | Razorpay webhook |
| `premium.payment.failed` | Razorpay webhook |
| `churn.cancellation_intent` | Our analytics (parked with E) |
| `revenue.anomaly.product` | Our statistical job (F) |
| `revenue.anomaly.txn_volume` | Our statistical job (H) |
| `churn.activity_drop` | Our analytics job (G) |

Razorpay-native events → webhook → `events` → case pipeline. Analytics-native events → scheduled jobs comparing live metrics to baselines → inserted into `events` the same way, uniform downstream handling.

## B.7 Recovery Case Lifecycle

```
DETECTED → INVESTIGATING → DIAGNOSED → ACTION_PROPOSED → POLICY_CHECK
   → ACTION_EXECUTED → VERIFICATION → (RECOVERED | FAILED | ESCALATED) → CLOSED
```

- `POLICY_CHECK` blocking → `ESCALATED`, not `ACTION_EXECUTED`.
- `VERIFICATION` timeout → `FAILED` (`verification_timeout`), still auditable.
- Attempts loop up to `max_retries` before falling to `FAILED`/`ESCALATED`.

## B.8 Policy / Guardrail Planning

Configurable per merchant (`policies` table):
- Max retry attempts (e.g. 2)
- Max transaction amount (e.g. ₹10,000)
- Max customer contacts (e.g. 2)
- Recovery window (e.g. 7 days)
- Allowed intervention types per scenario
- Human-approval triggers (amount threshold, repeated failures, first-attempt block, churn/retention discounts)
- Idempotency: `check_idempotency` keyed on (case_id, action_type, target_ref)

## B.9 Analytics / Metrics

- **Revenue at risk** = Σ amount entering a `recovery_case` in period
- **Revenue recovered** = Σ confirmed amount of `RECOVERED` cases
- **Recovery rate** = recovered / total cases
- **Intervention success rate** = successful / total attempts
- **Failed interventions** = attempts reaching `FAILED`
- **Unresolved cases** = open past recovery window
- **Average recovery time** = mean(`closed_at` − `opened_at`)
- **Prevented unsafe actions** = count of blocked `policy_evaluations`
- **ROI** = (revenue recovered − intervention cost) / intervention cost

All computed deterministically, rolled into `metrics_snapshots`.

## B.10 API Endpoint Planning (grouped, not implemented)

- **Events:** `POST /webhooks/razorpay`, `POST /events/internal`
- **Cases:** `GET /cases`, `GET /cases/{id}`, `GET /cases/{id}/timeline`
- **Agent:** `GET /cases/{id}/decisions`
- **Policies:** `GET /merchants/{id}/policies`, `PUT /merchants/{id}/policies`
- **Analytics:** `GET /metrics/summary`, `GET /metrics/timeseries`
- **Escalations:** `GET /escalations`, `POST /escalations/{id}/resolve`
- **Audit:** `GET /audit/{case_id}`
- **Live activity:** `WS /live/agent-activity`

Money-moving actions never exposed as direct endpoints — only inside the agent→policy→execution pipeline.

## B.11 Razorpay Integration Boundary

| Category | Detail |
|---|---|
| Already provided | Payment/error fields, Orders/Subscriptions/Payment Links APIs, webhooks, auto subscription retry |
| We aggregate ourselves | Error frequency, payment history, rejection rate, abandonment detection, attempt tracking, case/audit state |
| Razorpay executes | Create link, check statuses, its own auto-retry |
| Our system executes | Non-Razorpay reminders, human escalation, discounts, anomaly response |
| Must simulate in test mode | "Retry this exact payment" (via new linked payment link), realistic failure distributions, churn/anomaly signals |

## B.12 Synthetic Data / Testing Plan

- Failed payments: test-mode card/UPI failure triggers, varied `error_code`/`error_source`
- Abandoned checkouts: test orders left unpaid past threshold
- Recurring failures: test subscriptions with forced charge failures
- Churn: synthetic activity logs with drop-off patterns
- Product revenue drops / transaction volume drops: synthetic time series with injected anomalies
- Ground truth stored alongside each synthetic case for "detected vs actual" demo credibility

## B.13 Failure Handling

| Failure | Handling |
|---|---|
| Razorpay API failure | Retry with backoff, log to audit, alert if repeated |
| Payment stuck pending | Stays in `VERIFICATION` until window elapses → `FAILED` (`stuck_pending`) |
| Recovery action fails | `FAILED`, loop to next attempt or `ESCALATED` |
| Duplicate webhook | Deduped via unique `(source, external_event_id)` |
| LLM gives invalid action | Schema rejects → safe default `ESCALATED` |
| Policy blocks action | `ESCALATED`, reason recorded, human queue |
| Verification timeout | `FAILED` (`verification_timeout`), still counted in metrics |
| Partial recovery | Records actual vs at-risk amount, partial flag/status |

## B.14 Final Backend Architecture

```
Events (Razorpay webhooks + internal analytics)
        ↓
     FastAPI
        ↓
Context + Analytics (deterministic)
        ↓
Agent / LLM (diagnosis + strategy)
        ↓
Policy Engine (deterministic)
   ┌────┴────┐
Allowed    Blocked
   ↓          ↓
Tool Exec   Human Review Queue
(Razorpay/Merchant Systems)
   ↓
Verification
   ↓
Database + Audit Trail
   ↓
Dashboard
```

Modular monolith preserved; bounded/gated/explainable/auditable requirement holds end-to-end; one case lifecycle + one tool layer reused across all eight scenarios.

---

# PART C — Low-Level Design: Structure, Patterns & Principles

## C.1 Project Structure (exceptions isolated)

```
app/
├── core/
│   ├── config.py
│   ├── db.py
│   └── logging.py
│
├── exceptions/                      # ALL custom exceptions — nowhere else
│   ├── __init__.py
│   ├── base.py                      # AppException (root)
│   ├── domain_exceptions.py
│   ├── policy_exceptions.py
│   ├── integration_exceptions.py
│   ├── agent_exceptions.py
│   ├── persistence_exceptions.py
│   └── handlers.py                  # FastAPI exception → HTTP response mapping
│
├── api/
│   ├── v1/
│   │   ├── router.py
│   │   ├── cases.py
│   │   ├── policies.py
│   │   ├── analytics.py
│   │   ├── escalations.py
│   │   ├── audit.py
│   │   └── webhooks.py
│   └── v2/                          # reserved, empty
│
├── payments/  checkout/  subscriptions/  recovery/  agent/
├── policies/  razorpay_client/  notifications/  analytics/  audit/  events/
└── main.py
```

**Rule:** no module raises a bare `Exception` or built-in exception type. Every raise site imports from `app/exceptions/` — every failure is a typed, catchable, loggable object.

## C.2 Custom Exception Hierarchy

```
AppException (base.py)
│
├── DomainException
│   ├── PaymentNotFoundError
│   ├── OrderNotFoundError
│   ├── SubscriptionNotFoundError
│   ├── InvalidCaseStateTransitionError
│   └── DuplicateEventError
│
├── PolicyException
│   ├── PolicyViolationError
│   ├── MaxRetriesExceededError
│   ├── MaxTransactionAmountExceededError
│   ├── MaxContactsExceededError
│   └── RecoveryWindowExpiredError
│
├── IntegrationException
│   ├── RazorpayAPIError
│   ├── RazorpayTimeoutError
│   ├── RazorpayAuthError
│   └── NotificationDeliveryError
│
├── AgentException
│   ├── InvalidAgentOutputError
│   ├── UnsupportedActionTypeError
│   └── LLMProviderError
│
└── PersistenceException
    ├── RecordNotFoundError
    ├── ConcurrentUpdateError
    └── ConstraintViolationError
```

`handlers.py` maps each branch to a consistent JSON error envelope:
```json
{ "error_code": "MAX_RETRIES_EXCEEDED", "message": "...", "case_id": "...", "trace_id": "..." }
```

HTTP mapping: `DomainException` → 404/409; `PolicyException` → 422; `IntegrationException` → 502/504; `AgentException` → 500 (caught internally, routes case to `ESCALATED`, never surfaces raw); `PersistenceException` → 500/409.

## C.3 URL Versioning

- Prefix-based: `/api/v1/...`, `/api/v2/...` reserved from day one, empty.
- `api/v1/router.py` is the only place sub-routers are assembled — domain modules never hardcode version prefixes.
- Webhooks versioned too: `/api/v1/webhooks/razorpay`.
- Domain modules never import from `api/`, only the reverse — versioning stays a presentation-layer concern.

## C.4 SOLID Principles

| Principle | Application |
|---|---|
| **S**ingle Responsibility | Each module owns one concern — `razorpay_client` only talks to Razorpay, `policies` only evaluates rules, `audit` only records/reads. `recovery` orchestrates, doesn't implement domain logic. |
| **O**pen/Closed | New scenarios = new `Strategy` implementation + registration, no edits to existing handlers. New policy rules = new `PolicyRule` classes, not new `if` branches. |
| **L**iskov Substitution | All scenario handlers implement `RecoveryStrategy` (`diagnose()`, `propose_action()`) interchangeably. All Razorpay tool calls implement `PaymentGatewayPort` — mock substitutes cleanly in tests. |
| **I**nterface Segregation | `agent/` depends only on narrow ports it needs (`ContextProviderPort`, `ActionExecutorPort`), not one fat interface. `NotifierPort.send()` is minimal. |
| **D**ependency Inversion | `recovery/` depends on abstractions (`RecoveryStrategy`, `PolicyEngine`, `AuditRecorder`), not concretes. Wired at composition root (`main.py`/`container.py`) — swap LLM providers, sandbox/live mode, or mocks without touching orchestration. |

## C.5 Layering — Controller / Service / Repository

Every domain module follows the same internal shape:

```
payments/
├── controller.py   # FastAPI routes ONLY — no business logic, no DB calls
├── service.py       # Business logic — no DB/ORM code, no HTTP concerns
├── repository.py    # Data access ONLY — no business rules
├── schemas.py        # Pydantic request/response models
├── models.py          # SQLAlchemy ORM models
└── exceptions.py      # re-exports from app/exceptions/ for local discoverability
```

- **Controller** — parses request, calls one service method, returns response.
- **Service** — owns business logic, orchestrates repositories, raises domain exceptions, HTTP-agnostic.
- **Repository** — CRUD/query only, returns domain objects/DTOs, no HTTP errors, no business rules.

Enables independent testing: services with mocked repositories, controllers with mocked services.

## C.6 Design Patterns (full reference table)

| Pattern | Where used | Why |
|---|---|---|
| **Strategy** | `agent/strategies/` — one class per scenario A–H, implementing `RecoveryStrategy` | New scenarios plug in without touching the orchestrator |
| **Factory** | `agent/strategy_factory.py` — resolves `scenario_type` → strategy instance | Orchestrator stays ignorant of concrete classes |
| **Chain of Responsibility** | `policies/rules/` — `MaxRetriesRule`, `MaxAmountRule`, `MaxContactsRule`, `WindowRule`; first block halts the chain | Pluggable, independently configurable guardrails |
| **State** | `recovery/case_state_machine.py` — validates `DETECTED → ... → CLOSED` transitions | Prevents illegal lifecycle jumps at the type level |
| **Observer / Pub-Sub** | `events/` — event bus; `recovery`, `analytics`, `audit` subscribe independently | Decouples producers from consumers |
| **Adapter** | `razorpay_client/` (→ `PaymentGatewayPort`), `notifications/` (→ `NotifierPort`) | Isolates third-party SDK churn, enables mock substitution |
| **Repository** | `*/repository.py` per module, abstracts SQLAlchemy behind domain methods | Domain/service layer never touches ORM directly |
| **Template Method** | `agent/strategies/base.py` — fixed `collect_context() → diagnose() → propose_action()` skeleton | Deterministic pipeline order fixed, customization only where needed |
| **Decorator** | `audit/decorators.py` — `@audited` auto-logs before/after state | Avoids scattering manual audit calls |
| **Singleton (scoped)** | `core/config.py` settings, LLM client instance | Avoid re-instantiating expensive clients per request |
| **Circuit Breaker** | `razorpay_client/`, `agent/llm_client.py` (via `tenacity`) | Prevents hammering a failing external dependency |
| **Facade** | `recovery/orchestrator.py` (see C.10) | Hides multi-component coordination behind one call |
| **Saga** | `recovery/` + `events/` (see Part D.1) | Multi-step external workflow without distributed transactions |

## C.7 AI Layer — Strategy + Factory

```
agent/
├── strategies/
│   ├── base.py                  # RecoveryStrategy (ABC): collect_context(), diagnose(), propose_action()
│   ├── failed_payment.py        # A
│   ├── checkout_abandonment.py  # B
│   ├── subscription_recovery.py # C
│   ├── premium_recovery.py      # D
│   ├── revenue_drop.py          # F
│   ├── churn_recovery.py        # G
│   └── volume_drop.py           # H
│   # E stays unregistered in the factory — parked, not deleted
├── strategy_factory.py          # StrategyFactory.get(scenario_type) -> RecoveryStrategy
├── llm_client.py                # Adapter over Gemini/GPT
├── output_schemas.py            # Pydantic schemas the LLM output must satisfy
└── service.py                   # AgentService — the only entry point other modules call
```

- `StrategyFactory` holds a registry dict `{scenario_type: StrategyClass}`. New scenario = one file + one registry line.
- `AgentService.run(scenario_type, context)` → factory resolves strategy → Template Method skeleton runs → output validated against `output_schemas` → returns structured `ProposedAction` DTO.
- Validation failure → `InvalidAgentOutputError` → orchestrator routes case to `ESCALATED`.

## C.8 Repository Layer — Strategy Pattern (DB portability)

Goal: swap Postgres ↔ MySQL (or add a read-replica strategy) without touching service code.

```
core/db/
├── base_repository.py         # AbstractRepository (ABC): get(), list(), create(), update(), delete()
├── postgres/
│   ├── engine.py
│   └── repository_impl.py     # PostgresRepository(AbstractRepository) — SQLAlchemy + psycopg/asyncpg
├── mysql/
│   ├── engine.py
│   └── repository_impl.py     # MySQLRepository(AbstractRepository) — same interface, different driver
└── repository_factory.py      # returns configured implementation based on settings.DB_ENGINE
```

Every domain repository is written **against `AbstractRepository`**, never against SQLAlchemy directly. Switching engines = one config value change; services never know which engine is active.

## C.9 Dual Database — PostgreSQL + MongoDB

| Store | Used for | Why |
|---|---|---|
| **PostgreSQL** | `merchants`, `customers`, `orders`, `payments`, `subscriptions`, `recovery_cases`, `recovery_attempts`, `agent_decisions`, `policies`, `policy_evaluations` | ACID guarantees, foreign keys, financial correctness |
| **MongoDB** | `audit_logs`, `events` (raw payloads), `agent_decisions.input_context_snapshot` | Append-only, high write volume, variable/nested schema, never updated after write |

```
core/
├── db/postgres/...
└── logging_db/
    ├── mongo_client.py      # Motor/PyMongo async client, single connection pool
    └── audit_repository.py  # AuditRepository — writes/reads audit_logs, events collections
```

- `audit/` talks only to `AuditRepository` (Mongo-backed) — never touches Postgres.
- `recovery_cases` stores a **reference id** to its Mongo audit trail (`audit_ref`), not the trail itself.
- Audit writes never participate in a Postgres transaction/rollback — intentional, so an attempted action is still logged even if the DB transaction rolls back.

## C.10 Facade Pattern — Orchestrator

```
recovery/
├── orchestrator.py     # RecoveryOrchestrator (Facade)
├── (uses) agent.AgentService
├── (uses) policies.PolicyEngine
├── (uses) razorpay_client / notifications
└── (uses) audit.AuditService
```

`RecoveryOrchestrator` is the single facade external callers interact with. Hides coordination across `AgentService`, `PolicyEngine`, `ActionExecutor`, `CaseStateMachine`, `AuditService`.

```
orchestrator.handle_event(event) -> RecoveryCaseResult
```

No caller needs to know about strategies, policy chains, or state machines directly.

## C.11 Illustrative End-to-End Call Path

```
POST /api/v1/webhooks/razorpay
        ↓
events.EventBus.publish("payment.failed", payload)          [Observer]
        ↓
recovery.Orchestrator.handle_event()                          [Facade]
        ↓
strategy = StrategyFactory.get("A") → FailedPaymentStrategy   [Factory → Strategy]
        ↓
strategy.collect_context() → diagnose() → propose_action()    [Template Method]
        ↓
PolicyChain.evaluate(proposed_action)                          [Chain of Responsibility]
   ↓ allowed                              ↓ blocked
ActionExecutor.execute()             raise PolicyViolationError
   ↓ [Adapter → PaymentGatewayPort]         ↓
RazorpayClient.create_payment_link()   handlers.py → 422 + audit log
        ↓
CaseStateMachine.transition(ACTION_EXECUTED)                   [State]
        ↓
@audited → audit_logs entry written                            [Decorator]
```

Every exception raised anywhere in this path is typed (C.2), caught centrally in `exceptions/handlers.py`, turned into an HTTP response and an audit log entry — nothing fails silently.

---

# PART D — Low-Level Design: Concurrency, Data & Security

## D.1 Saga Pattern & Locking

**Saga (choreography-based, via the Observer/event bus):**

```
Step 1: ACTION_PROPOSED   (local DB transaction)
Step 2: POLICY_CHECK      (local, no external call)
Step 3: ACTION_EXECUTED   (external: Razorpay) — on failure: mark FAILED, no dangling side-effects
Step 4: NOTIFICATION_SENT (external: SMS/email) — on failure: log NotificationDeliveryError, proceed to verification anyway (notification failure ≠ payment failure)
Step 5: VERIFICATION      (poll/webhook)
Step 6: OUTCOME_RECORDED  (local DB transaction + Mongo audit write)
```

Each step publishes a domain event (`case.action_executed`, `case.action_failed`); `CaseStateMachine` listens and transitions accordingly. If Step 3 fails, compensation is simply: don't proceed to Step 4, transition to `FAILED`/`ESCALATED` — there's no money to "undo" since we never credit anything until Razorpay confirms it (ties to B.9 — recovered amount uses confirmed payment only).

**2PL (Two-Phase Locking):** Not used — full 2PL doesn't fit a saga spanning external HTTP calls (can't hold a DB lock across a Razorpay request). Instead:
- **Row-level locking** (`SELECT ... FOR UPDATE`) narrowly on `recovery_case` reads immediately before state transitions — prevents double-processing by concurrent workers (webhook retry vs reconciliation job).
- **Optimistic locking** (`version` column + `ConcurrentUpdateError`) everywhere else (`recovery_attempts`, `policy_evaluations`) — lower latency cost for an I/O-bound saga where contention is rare.

**Conclusion:** saga — yes, choreography-based; 2PL — no, replaced by targeted row-level locks + optimistic concurrency.

## D.2 PostgreSQL Indexing Plan

| Table | Index | Reason |
|---|---|---|
| `payments` | `(merchant_id, error_code)` | Powers `get_merchant_error_frequency` |
| `payments` | `razorpay_payment_id` (unique) | Fast webhook lookup/dedup |
| `orders` | `(merchant_id, status, created_at)` | Abandonment detection scan |
| `recovery_cases` | `(merchant_id, state)` | Dashboard filtering |
| `recovery_cases` | `(scenario_type, state)` | Metrics breakdown |
| `recovery_cases` | `source_ref` (btree) | Lookup by originating entity |
| `recovery_attempts` | `(case_id, attempt_number)` unique | Ordering + per-case listing |
| `subscriptions` | `razorpay_subscription_id` (unique) | Webhook lookup |
| `events` | `(source, external_event_id)` unique | Idempotent dedup constraint |
| `policy_evaluations` | `(case_id, attempt_id)` | Audit/debug lookups |
| `metrics_snapshots` | `(merchant_id, period)` unique | Upsert target |

Rule: every FK indexed by default; hot-path `WHERE`/`JOIN` columns get composite indexes matching the query shape — not blanket indexing, to protect write performance on `payments`/`recovery_attempts`.

## D.3 JWT Authentication

```
core/security/
├── jwt_handler.py       # encode/decode (python-jose)
├── auth_dependency.py   # FastAPI Depends() — extracts + validates bearer token
└── rbac.py              # merchant_admin, ops_viewer, system roles
```

- All endpoints except `/webhooks/*` and `/health` require a valid JWT via `Depends(get_current_user)`.
- Webhooks use **Razorpay signature verification** instead — different trust boundary.
- Roles: `merchant_admin` (policy config, full case view), `ops_viewer` (read-only), `system` (internal service accounts).
- Token payload minimal: `sub`, `merchant_id`, `role`, `exp` — no sensitive data.

## D.4 Idempotency (Financial Actions)

**a) Inbound — duplicate webhooks/events:**
- Every event carries `external_event_id` or a generated hash.
- Unique constraint `(source, external_event_id)` — duplicate insert is dropped before reaching the orchestrator.

**b) Outbound — duplicate actions:**
- Idempotency key: `f"{case_id}:{attempt_number}:{action_type}"`.
- `check_idempotency(key)` checks `idempotency_keys` table (unique constraint) before calling Razorpay/notification provider.
- Same key passed through to Razorpay's own idempotency support — a retried HTTP call after a timeout doesn't create a second payment link.
- Directly prevents the double-charge/double-message failure mode (B.13).

## D.5 Rate Limiting — Token Bucket

Chosen over leaky bucket: traffic is bursty-but-legitimate (webhook retry storms), token bucket tolerates bursts up to a cap while enforcing a steady average — better fit than leaky bucket's strict smoothing.

```
core/rate_limit/
├── token_bucket.py    # Redis-backed (atomic INCR/EXPIRE or Lua script)
└── middleware.py       # per-merchant / per-IP / per-JWT-subject
```

- Applied per merchant on dashboard/API endpoints.
- Applied per-source on `/webhooks/razorpay`, sized above legitimate burst volume — a safety net, not a business constraint.
- 429 → `RateLimitExceededError` with `Retry-After` header.

## D.6 URL Protection

- Only `/api/v1/*` exposed; `/internal/*` blocked at reverse-proxy level + requires `role=system` JWT.
- CORS: explicit allow-list, no wildcard.
- Auth on every route by default — global dependency, `/health` and `/webhooks/*` explicitly opted out (secure-by-default).
- Razorpay HMAC signature verification required before trusting any webhook payload, independent of rate limiting/JWT.
- Pydantic validation on every controller rejects malformed payloads before reaching services.

## D.7 Swagger / API Docs

- FastAPI's built-in OpenAPI: `/api/v1/docs` (Swagger UI), `/api/v1/redoc` — gated/disabled in production, open in dev.
- Every Pydantic schema has `Field(..., description=...)` + examples.
- Tags per router matching module boundaries (`payments`, `subscriptions`, `recovery`, `analytics`, ...).

## D.8 Code Clarity Guidelines

- Controllers: ~15 lines max — parse, call service, return.
- Services: one public method per use case, named in business terms (`recover_failed_payment`, not `handle(request)`).
- No function does two things — split diagnose vs execute (matches Template Method).
- Type hints everywhere; Pydantic DTOs across every layer boundary — no raw dicts.
- Docstrings only where "why" isn't obvious from name/types.
- One repository per aggregate root, not per table (e.g. `RecoveryCaseRepository` also handles `recovery_attempts`).

## D.9 Caching Layer (Redis) + Connection Pooling

Redis already used for rate limiting (D.5) — extended for caching, not a second cache tech.

| Data | TTL | Why |
|---|---|---|
| `policies` per merchant | 5 min | Read on every policy check |
| `metrics_snapshots` | 1–5 min | Dashboard polling shouldn't recompute |
| Merchant error-frequency stats | 10 min | Expensive aggregation feeding LLM context |
| JWT blacklist/revoked tokens | until `exp` | Logout/revocation without DB round-trip |

**Not cached:** anything in the money-moving path (`recovery_cases` state, idempotency keys, payment status) — correctness over latency, already indexed for fast reads.

```
core/cache/
├── redis_client.py     # single async Redis pool (redis.asyncio)
└── cache_decorator.py  # @cached(ttl=...)
```

**Connection pooling:** Postgres via SQLAlchemy `QueuePool` (`pool_size`/`max_overflow`); MongoDB via Motor's internal pool (one client at startup); Redis — one pool at startup. All three: created once at app startup (lifespan hook), never per-request.

## D.10 Observability

**Structured Logging:** `structlog`, JSON lines with `trace_id`, `merchant_id`, `case_id`, `event`, `level`. Kept separate from the audit trail — logs are for debugging/ops (verbose, rotatable), Mongo audit is the permanent business record.

**Metrics:** Prometheus-style at `/internal/metrics` (protected). Tracks request latency, case throughput, policy-block rate, LLM call latency/failure rate, Razorpay error rate, rate-limit rejections — operational, distinct from business metrics (B.9) which live in `analytics/`.

**Tracing:** `trace_id` generated at the edge, threaded through controller → service → repository → external calls → audit entry. Propagated via `contextvars` — lightweight for a hackathon, upgradeable to OpenTelemetry later without changing propagation logic.

**Health Checks:**
```
GET /health         → liveness
GET /health/ready    → readiness (Postgres + Mongo + Redis + LLM provider, per-dependency status)
```
`/health` public/unauthenticated; `/health/ready` granular for diagnosing which dependency is down.

## D.11 Migrations Strategy (Alembic)

- Alembic is the single source of schema truth for Postgres — no manual `CREATE TABLE`, no `Base.metadata.create_all()` outside local dev/tests.
- One migration per logical change, not one giant migration per feature.
- **Additive-first:** new columns nullable/defaulted, backfilled, then `NOT NULL` in a follow-up — avoids locking large tables during a demo window.
- MySQL variant migrations generated separately if that strategy is activated (`core/db/mysql/migrations/` mirrors `postgres/migrations/`).
- MongoDB collections are schemaless — no migration tool; a lightweight `schema_version.py` doc convention only if the audit document shape changes.

## D.12 Forward & Reverse Proxy (brief)

- **Reverse Proxy** (Nginx / Traefik, sits in front of FastAPI): terminates TLS/SSL, handles gzip compression, load-balances across multiple FastAPI worker instances, and is the actual public entry point — clients never hit Uvicorn/FastAPI directly. Also enforces the `/internal/*` network-level block mentioned in D.6 (only the reverse proxy's config, not app code, decides whether an internal route is even reachable from outside). Routes `/api/v1/*` and `/api/v2/*` straight through to FastAPI unchanged — versioning stays an app-layer concern (C.3), the proxy doesn't rewrite paths.
- **Forward Proxy** (outbound, e.g. for calls to Razorpay/LLM providers from a restricted network): used only if the deployment environment requires egress control (e.g. corporate network, specific hackathon sandbox with an allow-listed egress IP) — routes our own outbound `razorpay_client`/`llm_client` HTTP calls through a fixed proxy so the destination sees a stable, whitelistable source IP. Not required for a simple cloud deployment with open egress; call this out as environment-dependent rather than a hard requirement.
- Both are **infrastructure-level**, sitting outside `app/` entirely — no application code should assume or hardcode proxy behavior (e.g. don't read client IP from `request.client.host` alone; read `X-Forwarded-For`/`X-Real-IP` set by the reverse proxy, since that's what will be present in production).

---

## D.13 Soft Deletes + Pagination Conventions

**Soft deletes:** nothing in this domain is hard-deleted (financial/compliance relevance).
- `deleted_at TIMESTAMP NULL` on tables where deletion is conceptually possible (`products`, `policies`) — repository `delete()` sets `deleted_at`, never `DELETE FROM`.
- `list()`/`get()` filter `deleted_at IS NULL` by default; `include_deleted=True` only for audit/compliance views.
- Pure event/history tables (`payments`, `recovery_attempts`, `agent_decisions`) have **no delete concept at all**, not even soft — append-only by nature.

**Pagination:** cursor-based (not offset/limit) for all growable list endpoints (`GET /cases`, `GET /audit/{case_id}`) — offset degrades on large, frequently-inserted tables; cursor stays stable during concurrent inserts.
- `GET /api/v1/cases?limit=20&cursor=<opaque_cursor>` → response includes `next_cursor: string | null`.
- Cursor = opaque base64-encoded `(created_at, id)` tuple, backed by indexes already including `created_at` (D.2).
- Dashboard summary/metrics endpoints don't paginate — pre-aggregated, already small.

---

# PART E — Consolidated Reference

## E.1 Updated Directory Skeleton (final)

```
app/
├── core/
│   ├── config.py
│   ├── logging.py
│   ├── security/          # JWT, RBAC
│   ├── rate_limit/         # token bucket
│   ├── cache/               # Redis caching
│   ├── db/
│   │   ├── base_repository.py
│   │   ├── postgres/
│   │   ├── mysql/
│   │   └── repository_factory.py
│   └── logging_db/          # MongoDB client + audit repo
│
├── exceptions/               # custom hierarchy + handlers
│
├── api/
│   ├── v1/
│   └── v2/                   # reserved
│
├── payments/  checkout/  subscriptions/    # each: controller.py, service.py, repository.py, schemas.py, models.py
├── retention/                # organizing folder (E parked, G)
├── revenue_intelligence/     # organizing folder (F, H)
├── customer/
├── recovery/
│   ├── controller.py
│   ├── orchestrator.py       # Facade
│   ├── case_state_machine.py # State
│   └── strategies/ ...
├── agent/
│   ├── strategies/            # Strategy
│   ├── strategy_factory.py    # Factory
│   ├── llm_client.py
│   ├── output_schemas.py
│   └── service.py
├── policies/
│   └── rules/                  # Chain of Responsibility
├── razorpay_client/             # Adapter
├── notifications/                 # Adapter
├── analytics/
├── audit/                         # Mongo-backed, Decorator-instrumented
├── events/                         # Observer/event bus
└── main.py
```

## E.2 Master Pattern Assignment Table

| Requirement | Pattern | Location |
|---|---|---|
| AI layer scenario handling | Strategy + Factory | `agent/strategies/`, `agent/strategy_factory.py` |
| DB engine portability | Strategy | `core/db/base_repository.py` + `postgres/`, `mysql/` |
| Orchestrator simplification | Facade | `recovery/orchestrator.py` |
| Case lifecycle | State | `recovery/case_state_machine.py` |
| Policy guardrails | Chain of Responsibility | `policies/rules/` |
| Multi-step external workflow | Saga (choreography) | `recovery/` + `events/` |
| Concurrency control | Row-level lock + Optimistic lock (not 2PL) | `recovery_cases`, `recovery_attempts` |
| Third-party isolation | Adapter | `razorpay_client/`, `notifications/` |
| Audit logging | Decorator + separate Mongo store | `audit/` |
| Event decoupling | Observer/Pub-Sub | `events/` |
| Repeated skeleton with variation | Template Method | `agent/strategies/base.py` |
| Expensive client reuse | Singleton (scoped) | `core/config.py`, LLM client |
| External dependency protection | Circuit Breaker | `razorpay_client/`, `agent/llm_client.py` |

## E.3 Coverage Checklist

| Area | Status |
|---|---|
| Layering (Controller/Service/Repository) | ✅ C.5 |
| Custom exceptions, isolated directory | ✅ C.1–C.2 |
| URL versioning | ✅ C.3 |
| SOLID | ✅ C.4 |
| Design patterns (full set) | ✅ C.6, C.7, C.10 |
| ORM (SQLAlchemy) | ✅ C.8 |
| Repository strategy pattern (Postgres/MySQL) | ✅ C.8 |
| Dual DB (Postgres + MongoDB) | ✅ C.9 |
| Facade (Orchestrator) | ✅ C.10 |
| Saga + locking (2PL evaluated, rejected) | ✅ D.1 |
| PostgreSQL indexing | ✅ D.2 |
| JWT auth | ✅ D.3 |
| Idempotency (inbound + outbound) | ✅ D.4 |
| Rate limiting (token bucket) | ✅ D.5 |
| URL protection | ✅ D.6 |
| Swagger docs | ✅ D.7 |
| Code clarity rules | ✅ D.8 |
| Caching + connection pooling | ✅ D.9 |
| Observability (logs/metrics/tracing/health) | ✅ D.10 |
| Migrations (Alembic) | ✅ D.11 |
| Forward & reverse proxy | ✅ D.12 |
| Soft deletes + pagination | ✅ D.13 |

## E.4 Open Items / Next Steps

Not yet closed out — worth a decision before implementation:

1. **Secrets management** — `.env` is fine for hackathon; flag if Vault/AWS Secrets Manager should be mentioned even at planning level.
2. **CI/CD outline** — not explicitly asked for, but usually expected alongside LLD in a hackathon submission (test → lint → deploy stages).
3. **Deployment target** — Docker Compose (Postgres + Mongo + Redis + API) vs cloud-managed services — affects how "real" the demo looks to judges.
4. **Exact interface signatures** — `RecoveryStrategy`, `PolicyRule`, `PaymentGatewayPort`, `NotifierPort` — still planning-level, just more granular.
5. **Dependency-injection approach** — native FastAPI `Depends()` graph vs a lightweight container.
6. **Exception → HTTP status + `error_code` string table** — exact mapping, one row per exception subtype.


# AI Revenue Recovery Controller — Frontend

Dashboard for the AI Revenue Recovery Controller: view revenue-at-risk cases, live agent activity, recovery metrics, policy configuration, and escalations for human review.

Status: **Planning stage.** This README describes the intended setup once implementation begins.

---

## Tech Stack

| Concern | Choice |
|---|---|
| Framework | Next.js |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Charts / Analytics | Recharts |
| Live updates | WebSocket / SSE (live agent activity feed) |
| Auth | JWT (issued by backend, stored per app's auth flow) |
| API | Backend FastAPI service, versioned (`/api/v1/...`) |

---

## Prerequisites

- Node.js 18+
- npm / pnpm / yarn (pick one, keep consistent across the team)
- Running instance of the backend API (see backend README) — needed for all data-fetching pages to work locally

---

## Getting Started

```bash
# install dependencies
npm install

# copy environment template and fill in values
cp .env.example .env.local

# run the dev server
npm run dev
```

App runs at `http://localhost:3000` by default.

---

## Environment Variables

```
# .env.local

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_BASE_URL=ws://localhost:8000/api/v1/live
NEXT_PUBLIC_ENV=development
```

- `NEXT_PUBLIC_API_BASE_URL` — points at the backend's versioned REST API.
- `NEXT_PUBLIC_WS_BASE_URL` — points at the live agent-activity WebSocket/SSE endpoint.
- Never put secrets (API keys, DB credentials) in frontend env vars — anything prefixed `NEXT_PUBLIC_` is shipped to the browser.

---

## Project Structure

```
frontend/
├── app/                        # Next.js App Router
│   ├── (dashboard)/
│   │   ├── cases/               # recovery case list + detail views
│   │   ├── analytics/            # ₹ recovered, recovery rate, charts (Recharts)
│   │   ├── escalations/          # human-in-loop review queue
│   │   ├── policies/              # guardrail configuration (per merchant)
│   │   └── audit/                 # audit trail viewer per case
│   ├── login/
│   └── layout.tsx
│
├── components/
│   ├── charts/                    # Recharts wrappers (revenue-at-risk, recovery-rate, etc.)
│   ├── cases/                     # case card, case timeline, state badge
│   ├── live-activity/              # SSE/WebSocket-driven agent activity feed
│   └── ui/                          # shared buttons, tables, modals (Tailwind-based)
│
├── lib/
│   ├── api-client.ts               # thin fetch wrapper, attaches JWT, base URL from env
│   ├── ws-client.ts                # WebSocket/SSE connection handling + reconnect logic
│   └── auth.ts                     # token storage/retrieval, refresh handling
│
├── types/                          # shared TypeScript types mirroring backend Pydantic schemas
│   ├── case.ts
│   ├── policy.ts
│   ├── metrics.ts
│   └── audit.ts
│
├── public/
├── .env.example
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## Key Pages / Views (maps to backend API endpoints)

| Page | Backend endpoint(s) used |
|---|---|
| Case list | `GET /api/v1/cases` (cursor-paginated) |
| Case detail + timeline | `GET /api/v1/cases/{id}`, `GET /api/v1/cases/{id}/timeline` |
| Agent decision view | `GET /api/v1/cases/{id}/decisions` |
| Live agent activity | `WS /api/v1/live/agent-activity` |
| Analytics dashboard | `GET /api/v1/metrics/summary`, `GET /api/v1/metrics/timeseries` |
| Escalations / human review | `GET /api/v1/escalations`, `POST /api/v1/escalations/{id}/resolve` |
| Policy configuration | `GET /api/v1/merchants/{id}/policies`, `PUT /api/v1/merchants/{id}/policies` |
| Audit trail viewer | `GET /api/v1/audit/{case_id}` |

Money-moving actions are never triggered directly from the frontend — the dashboard is read/config-only (matches backend design: API surface stays read/config-heavy, per backend planning §10).

---

## Auth Flow

1. User logs in → backend issues a JWT (`sub`, `merchant_id`, `role`, `exp`).
2. Token stored via `lib/auth.ts` (httpOnly cookie preferred over localStorage where feasible).
3. `lib/api-client.ts` attaches `Authorization: Bearer <token>` to every request.
4. Role-based UI: `merchant_admin` sees policy config + full case view; `ops_viewer` sees read-only dashboard.
5. On 401, redirect to `/login`; on 403, show a permission-denied state rather than a blank page.

---

## Live Agent Activity Feed

- Connects via `lib/ws-client.ts` to the backend's live activity endpoint on dashboard mount.
- Renders each incoming case-state-transition event as an activity item (`components/live-activity/`).
- Reconnects with backoff on disconnect — the feed is a convenience layer; the case list/detail pages always remain the source of truth via REST if the socket drops.

---

## Conventions

- **Type safety**: every API response is typed (`types/`), mirroring backend Pydantic schemas — no `any` on API boundaries.
- **Data fetching**: server components fetch initial data where possible (Next.js App Router); client components handle live updates and interactive filtering.
- **Styling**: Tailwind utility classes only — no ad hoc CSS files unless a third-party component requires it.
- **Charts**: all analytics visuals go through `components/charts/` wrappers around Recharts, not raw Recharts calls scattered across pages — keeps chart styling consistent.
- **No secrets in the frontend** — nothing beyond `NEXT_PUBLIC_*` env vars, and even those contain no credentials.

---

## Scripts

```bash
npm run dev       # start dev server
npm run build     # production build
npm run start     # start production server (after build)
npm run lint       # lint check
```

---

## Notes

- This frontend is a **dashboard only** — it visualizes and lets humans configure/review the backend's closed-loop recovery system. It does not run any recovery logic itself.
- Any new dashboard page should map to an existing backend endpoint (see table above) rather than introduce new client-side business logic — keeps the "backend as single source of truth" principle from the system design intact.# AI Revenue Recovery Controller — Frontend

Dashboard for the AI Revenue Recovery Controller: view revenue-at-risk cases, live agent activity, recovery metrics, policy configuration, and escalations for human review.

Status: **Planning stage.** This README describes the intended setup once implementation begins.

---

## Tech Stack

| Concern | Choice |
|---|---|
| Framework | Next.js |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Charts / Analytics | Recharts |
| Live updates | WebSocket / SSE (live agent activity feed) |
| Auth | JWT (issued by backend, stored per app's auth flow) |
| API | Backend FastAPI service, versioned (`/api/v1/...`) |

---

## Prerequisites

- Node.js 18+
- npm / pnpm / yarn (pick one, keep consistent across the team)
- Running instance of the backend API (see backend README) — needed for all data-fetching pages to work locally

---

## Getting Started

```bash
# install dependencies
npm install

# copy environment template and fill in values
cp .env.example .env.local

# run the dev server
npm run dev
```

App runs at `http://localhost:3000` by default.

---

## Environment Variables

```
# .env.local

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_BASE_URL=ws://localhost:8000/api/v1/live
NEXT_PUBLIC_ENV=development
```

- `NEXT_PUBLIC_API_BASE_URL` — points at the backend's versioned REST API.
- `NEXT_PUBLIC_WS_BASE_URL` — points at the live agent-activity WebSocket/SSE endpoint.
- Never put secrets (API keys, DB credentials) in frontend env vars — anything prefixed `NEXT_PUBLIC_` is shipped to the browser.

---

## Project Structure

```
frontend/
├── app/                        # Next.js App Router
│   ├── (dashboard)/
│   │   ├── cases/               # recovery case list + detail views
│   │   ├── analytics/            # ₹ recovered, recovery rate, charts (Recharts)
│   │   ├── escalations/          # human-in-loop review queue
│   │   ├── policies/              # guardrail configuration (per merchant)
│   │   └── audit/                 # audit trail viewer per case
│   ├── login/
│   └── layout.tsx
│
├── components/
│   ├── charts/                    # Recharts wrappers (revenue-at-risk, recovery-rate, etc.)
│   ├── cases/                     # case card, case timeline, state badge
│   ├── live-activity/              # SSE/WebSocket-driven agent activity feed
│   └── ui/                          # shared buttons, tables, modals (Tailwind-based)
│
├── lib/
│   ├── api-client.ts               # thin fetch wrapper, attaches JWT, base URL from env
│   ├── ws-client.ts                # WebSocket/SSE connection handling + reconnect logic
│   └── auth.ts                     # token storage/retrieval, refresh handling
│
├── types/                          # shared TypeScript types mirroring backend Pydantic schemas
│   ├── case.ts
│   ├── policy.ts
│   ├── metrics.ts
│   └── audit.ts
│
├── public/
├── .env.example
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## Key Pages / Views (maps to backend API endpoints)

| Page | Backend endpoint(s) used |
|---|---|
| Case list | `GET /api/v1/cases` (cursor-paginated) |
| Case detail + timeline | `GET /api/v1/cases/{id}`, `GET /api/v1/cases/{id}/timeline` |
| Agent decision view | `GET /api/v1/cases/{id}/decisions` |
| Live agent activity | `WS /api/v1/live/agent-activity` |
| Analytics dashboard | `GET /api/v1/metrics/summary`, `GET /api/v1/metrics/timeseries` |
| Escalations / human review | `GET /api/v1/escalations`, `POST /api/v1/escalations/{id}/resolve` |
| Policy configuration | `GET /api/v1/merchants/{id}/policies`, `PUT /api/v1/merchants/{id}/policies` |
| Audit trail viewer | `GET /api/v1/audit/{case_id}` |

Money-moving actions are never triggered directly from the frontend — the dashboard is read/config-only (matches backend design: API surface stays read/config-heavy, per backend planning §10).

---

## Auth Flow

1. User logs in → backend issues a JWT (`sub`, `merchant_id`, `role`, `exp`).
2. Token stored via `lib/auth.ts` (httpOnly cookie preferred over localStorage where feasible).
3. `lib/api-client.ts` attaches `Authorization: Bearer <token>` to every request.
4. Role-based UI: `merchant_admin` sees policy config + full case view; `ops_viewer` sees read-only dashboard.
5. On 401, redirect to `/login`; on 403, show a permission-denied state rather than a blank page.

---

## Live Agent Activity Feed

- Connects via `lib/ws-client.ts` to the backend's live activity endpoint on dashboard mount.
- Renders each incoming case-state-transition event as an activity item (`components/live-activity/`).
- Reconnects with backoff on disconnect — the feed is a convenience layer; the case list/detail pages always remain the source of truth via REST if the socket drops.

---

## Conventions

- **Type safety**: every API response is typed (`types/`), mirroring backend Pydantic schemas — no `any` on API boundaries.
- **Data fetching**: server components fetch initial data where possible (Next.js App Router); client components handle live updates and interactive filtering.
- **Styling**: Tailwind utility classes only — no ad hoc CSS files unless a third-party component requires it.
- **Charts**: all analytics visuals go through `components/charts/` wrappers around Recharts, not raw Recharts calls scattered across pages — keeps chart styling consistent.
- **No secrets in the frontend** — nothing beyond `NEXT_PUBLIC_*` env vars, and even those contain no credentials.

---

## Scripts

```bash
npm run dev       # start dev server
npm run build     # production build
npm run start     # start production server (after build)
npm run lint       # lint check
```

---

## Notes

- This frontend is a **dashboard only** — it visualizes and lets humans configure/review the backend's closed-loop recovery system. It does not run any recovery logic itself.
- Any new dashboard page should map to an existing backend endpoint (see table above) rather than introduce new client-side business logic — keeps the "backend as single source of truth" principle from the system design intact.