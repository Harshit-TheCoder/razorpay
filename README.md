# AI Revenue Recovery Controller — Full Planning Document

Status: **Planning phase only. No implementation code.**

---

# PART 1 — Problem, Solution & Differentiator

## 1. The Problem

Merchants lose revenue for many reasons:

- Payment failures
- Checkout abandonment
- Subscription payment failures
- Overdue invoices
- Repeated payment failures
- Customers intending to pay but not completing payment

Today, these are often handled using fixed rules and separate workflows.

**The problem is:** the system can detect that money was lost, but it doesn't intelligently understand why, choose the best recovery action, execute it, and verify whether the money was actually recovered.

---

## 2. Our Solution — AI Revenue Recovery Controller

An AI agent that:

```
Detect revenue at risk
        ↓
Understand the situation
        ↓
Investigate the cause
        ↓
Choose recovery strategy
        ↓
Check merchant policies
        ↓
Execute action through Razorpay
        ↓
Verify outcome
        ↓
Measure ₹ recovered
        ↓
Record complete audit trail
```

So we're building **closed-loop revenue recovery**, not just a chatbot or prediction model.

---

## 3. Tech Stack

**Frontend**
- Next.js
- TypeScript
- Tailwind CSS
- Recharts — recovery/revenue analytics
- WebSocket / SSE — live agent activity

**Backend**
- FastAPI
- Python
- Pydantic
- SQLAlchemy
- PostgreSQL

**AI / Agent Layer**
- LLM: Gemini / GPT
- LangGraph — agent orchestration
- Tool Calling / Structured Outputs
- Prompt + policy-based reasoning
- No custom ML initially

---

## 4. Initial Scope

Don't try to solve every revenue problem. For the MVP, 3 scenarios:

**A. Failed payment recovery**
Payment failed → diagnose → retry / payment link → verify

**B. Checkout abandonment**
Checkout abandoned → understand customer context → generate recovery intervention → payment completed?

**C. Subscription/payment recovery**
Recurring payment failed → analyze history → choose bounded retry/reminder → verify recovery

This gives us enough variety without making the project enormous.

---

## 5. The Core Product Metric

**North Star metric: ₹ Revenue Recovered**

Example:

```
Revenue at risk       ₹5,00,000
Cases analyzed             500
Recovery attempts           300
Successful recoveries       126

Revenue recovered      ₹1,72,400
Recovery rate              34.5%
```

We'll also track:
- Recovery rate
- Successful interventions
- Failed interventions
- False/unsafe actions prevented
- Average recovery time
- Unresolved cases

---

## 6. The Safety Principle

The agent never gets unrestricted control over money.

```
                 LLM Agent
                     ↓
              Proposed Action
                     ↓
              Policy Engine
                     ↓
          ┌──────────┴──────────┐
          ↓                     ↓
       Allowed               Blocked
          ↓                     ↓
    Razorpay API          Human review
```

Examples:
- Maximum retry attempts = 2
- Maximum transaction = ₹10,000
- Maximum customer contacts = 2
- Recovery window = 7 days

This directly addresses the hackathon's **bounded + gated + explainable + auditable** requirement.

---

## 7. Methods Required (Scenario Detail)

### A. Failed Payment Recovery

Flow: `Payment failed → Diagnose → Recovery action → Verify`

Required tools:
- Get payment details
- Check whether this error happens often with this merchant or not
- Get the exact failure source
- Get failure/error reason
- Get customer/payment history
- Get order details
- Decide recovery action
- Retry payment / create payment link
- Check payment status
- Record recovery result

### B. Checkout Abandonment

Flow: `Checkout abandoned → Understand customer → Intervention → Verify`

Required tools:
- Get checkout/order details
- Check how often the specific product is rejected
- Get customer history
- Get cart/product details
- Check previous abandonment/recovery attempts
- Generate recovery intervention
- Send recovery message/payment link
- Track whether checkout/payment completed
- Record outcome

### C. Subscription/Recurring Payment Recovery

Flow: `Recurring payment failed → Analyze history → Bounded action → Verify`

Required tools:
- Get subscription details
- Get failed recurring payment details
- Get customer payment history
- Get previous retry attempts
- Determine recovery strategy
- Retry / generate payment link / send reminder
- Check subscription/payment status
- Record outcome

*The tooling for each problem can be handled differently in different Python files.*

### D. Insurance Premium Recovery

Flow: `Premium AutoPay fails / policy at risk of lapse → Analyze customer & payment context → Choose bounded intervention → Verify premium payment`

Required capabilities:
- Get policy/subscription details
- Get failed premium payment details
- Analyze customer/payment history
- Check previous recovery attempts
- Determine why premium payment failed
- Decide intervention — retry, payment link, reminder, escalation
- Execute bounded recovery action
- Check whether premium was paid
- Record outcome / policy retained

**Core objective:** Prevent avoidable policy lapses by recovering failed recurring premium payments. This becomes our 4th recovery scenario, while the underlying agent/tooling remains largely reusable.

### E. Protection Plan Churn Recovery

The key difference from D:
- **D:** Premium payment failed → prevent policy lapse.
- **E:** Customer is actively cancelling → understand why and attempt retention.

This introduces a broader concept:

> Revenue Recovery = recovering money from failed payments AND preventing recurring revenue from disappearing through avoidable churn.

**We should not add it to the implementation yet.** Kept as a potential 5th use case, to be revisited on whether it strengthens the hackathon story or makes scope too broad.

### F. Product Revenue Drop Recovery

Flow: `Revenue anomaly → Diagnose cause → Select intervention → Execute → Measure recovered revenue`

This moves us from transaction-level recovery to product/business-level revenue recovery. It can still be mostly LLM + analytics + APIs (not ML) if we use statistical thresholds/rules for anomaly detection and let the LLM handle investigation and action planning.

### G. Customer Churn & Revenue Recovery

Flow: `User activity/revenue drops → Diagnose churn cause → Select bounded retention intervention → User returns → Measure recovered revenue`

More interesting than simply giving discounts. Example: 18% of users who experienced a cancellation fee became inactive. The agent could discover that pattern, identify the affected cohort, and recommend a bounded retention campaign.

### H. Transaction Volume / User Activity Recovery

Flow: `Transaction volume drops → Diagnose cause → Target affected users/transactions → Recovery intervention → Measure recovered GMV/revenue`

Expands beyond "a payment failed" to: "The merchant/platform is losing transaction volume — find out why and recover it."

---

## 8. Illustrative Industry Applications

| Scenario | Revenue at risk | What our AI could do |
|---|---|---|
| 🎥 Content creators | Paid subscriptions / paid videos | Detect inactive subscribers → understand why → recommend relevant content / renewal reminder → recover subscription |
| ✈️ MakeMyTrip / Cleartrip | Abandoned bookings | Detect abandoned booking → understand price/availability issue → send relevant reminder/payment link |
| 🚆 IRCTC / travel platforms | Search → booking drop-off | Detect booking abandonment → identify friction → recover completed bookings |
| 🎬 Netflix / Prime / JioHotstar | Subscription churn | Detect cancellation risk → understand usage pattern → recommend relevant content / renewal intervention |
| 🎵 Spotify / music platforms | Subscription churn | Detect inactive users → targeted retention intervention → subscription recovery |
| 📚 EdTech | Course/subscription churn | Detect disengagement → relevant content/reminder → recover subscription |
| 🏋️ Gyms/apps | Membership churn | Detect inactivity → retention intervention → recover membership |

---

## 9. Razorpay API Analysis (A, B, C)

### A. Failed Payment Recovery

| Required Tool | Razorpay Already Provides? | Razorpay Capability |
|---|---|---|
| Get payment details | ✅ | `GET /v1/payments/:id` |
| Check whether this error happens often with merchant | ❌ | We calculate this from historical payment data |
| Get exact failure source | ✅ | `error_source` |
| Get failure/error reason | ✅ | `error_code`, `error_description`, `error_reason`, `error_step` |
| Get customer/payment history | ⚠️ Partial | Customer API provides customer information; payment history needs our aggregation |
| Get order details | ✅ | Orders API |
| Decide recovery action | ❌ | Our LLM agent |
| Retry payment | ⚠️ Not generic | Razorpay does not provide a generic "retry this failed payment" API; we need an appropriate new payment flow |
| Create payment link | ✅ | `POST /v1/payment_links` |
| Check payment status | ✅ | Fetch Payment / Order APIs |
| Record recovery result | ❌ | Our database |

Razorpay's Payments API supports fetching payment details and exposes fields such as `error_code`, `error_description`, `error_source`, `error_step`, `error_reason`. Razorpay also provides the `payment.failed` webhook, which can trigger our recovery agent when a payment fails.

**🔥 Key Differentiator:** Razorpay can tell us *why* a particular payment failed. Our system should determine: *"How frequently does this type of failure occur, and what recovery action has historically worked best?"*

```
Merchant payment history
        ↓
Error frequency analysis
        ↓
├── Bank failure rate
├── UPI failure rate
├── Product failure rate
├── Customer failure rate
└── Time-based failure patterns
        ↓
Context provided to LLM
        ↓
Recovery decision
```

### B. Checkout Abandonment

| Required Tool | Razorpay Already Provides? | What We Do |
|---|---|---|
| Get checkout/order details | ✅/⚠️ | Orders API gives order data |
| Check how often product is rejected | ❌ | Our analytics/database |
| Get customer history | ⚠️ Partial | Customer API + our payment history |
| Get cart/product details | ❌ | Our merchant-side DB |
| Check previous abandonment/recovery attempts | ❌ | Our database |
| Generate recovery intervention | ❌ | LLM |
| Send recovery message/payment link | ⚠️ Partial | Payment Link API + our messaging layer |
| Track whether payment completed | ✅ | Payment/Order APIs + webhooks |
| Record outcome | ❌ | Our database |

### C. Subscription / Recurring Payment Recovery

Razorpay already provides quite a lot of functionality here.

| Required Tool | Razorpay Already Provides? | Razorpay Capability |
|---|---|---|
| Get subscription details | ✅ | `GET /v1/subscriptions/:id` |
| Get failed recurring payment details | ✅ | Payment/Invoice APIs + webhooks |
| Get customer payment history | ⚠️ Partial | We aggregate payment history |
| Get previous retry attempts | ⚠️ Partial | Razorpay subscription state/retry behavior provides some data; we track agent attempts |
| Determine recovery strategy | ❌ | Our LLM |
| Retry payment | ✅/⚠️ | Razorpay already automatically retries subscription charges |
| Generate payment link | ✅ | Payment Links API |
| Send reminder | ⚠️ | Payment Link notification APIs / our messaging layer |
| Check subscription status | ✅ | Subscription API |
| Check payment status | ✅ | Payment API |
| Record outcome | ❌ | Our database |

---

# PART 2 — Backend Planning

Scope carried forward as-is: Scenarios A–H, North Star metric (₹ Revenue Recovered), safety principle (bounded + gated + explainable + auditable), and the Razorpay API analysis above for A/B/C. Nothing below adds new scenarios.

## 1. Backend Responsibilities

**Backend (FastAPI + DB) is responsible for:**
- Receiving events (webhooks + internal analytics jobs)
- Assembling context for a case (customer, payment, product, history)
- Persisting recovery cases, attempts, decisions, policies, audit logs
- Invoking the agent with structured context, receiving a structured proposed action
- Running the proposed action through the deterministic Policy Engine
- Executing allowed actions via Razorpay/merchant tools
- Verifying outcomes (poll/webhook) and closing the loop
- Computing all analytics/metrics
- Exposing REST/WebSocket APIs to the dashboard

**LLM/Agent is responsible for:**
- Diagnosing *why* revenue is at risk, given structured context (not raw DB access)
- Choosing a recovery strategy from an allowed action set
- Producing an explanation/rationale (for audit + dashboard)
- Drafting customer-facing message content (where applicable)
- Never: computing money math, never directly calling Razorpay, never bypassing policy

**Razorpay is responsible for:**
- Source of truth for payments, orders, subscriptions, payment links
- Emitting webhooks (`payment.failed`, `subscription.charged`, etc.)
- Executing the actual money-movement action we request (payment link creation, subscription retry behavior, status checks)

**Merchant's own systems/data are responsible for:**
- Product/cart/catalog data
- Customer engagement/usage data (for churn, content, activity scenarios)
- Any messaging/notification channel not native to Razorpay (email/SMS/WhatsApp/push)
- Business-specific policy inputs (discount limits, brand tone, escalation contacts)

---

## 2. Core Backend Modules

Modular monolith, one FastAPI app, folder-per-domain module.

```
app/
├── core/                 # config, DB session, logging, security
├── events/               # webhook receivers + internal event bus
├── payments/             # payment fetch, error parsing, one-off recovery (A)
├── checkout/             # checkout/order/abandonment logic (B)
├── subscriptions/        # subscription + recurring/premium recovery (C, D)
├── retention/            # churn / cancellation intent handling (E, G) — flagged, not built yet for E
├── revenue_intelligence/ # product revenue drop, txn volume drop (F, H)
├── customer/             # customer profile + aggregated history
├── recovery/             # recovery case lifecycle, state machine, orchestration
├── agent/                # LLM orchestration (LangGraph), prompts, context assembly
├── policies/             # policy/guardrail engine, config, evaluation
├── razorpay_client/      # thin wrapper over Razorpay APIs (payments, orders, subs, links)
├── notifications/        # payment link delivery, reminders, message dispatch
├── analytics/            # metrics computation, anomaly detection (rule/statistical)
├── audit/                # immutable audit trail writer/reader
└── api/                  # route aggregation for dashboard/frontend
```

Rationale: `payments`, `checkout`, `subscriptions` stay separate because their Razorpay surfaces genuinely differ (per the API table above). `revenue_intelligence` and `retention` are new **only as organizing folders**, not new scenarios — they group F/H and E/G respectively so scope stays visible and E remains clearly parked.

---

## 3. Database Planning

| Table | Purpose | Key Fields | Relationships |
|---|---|---|---|
| `merchants` | Merchant account + config | id, name, razorpay_key_ref, policy_profile_id | 1—N with everything else |
| `customers` | Local customer record, mirrors Razorpay customer | id, merchant_id, razorpay_customer_id, contact_prefs | belongs to merchant |
| `products` | Merchant catalog (for checkout/product-drop use) | id, merchant_id, name, price, category | belongs to merchant |
| `orders` | Order/checkout record | id, merchant_id, customer_id, razorpay_order_id, status, cart_snapshot | FK customer, merchant |
| `payments` | Local mirror of payment attempts | id, merchant_id, order_id, razorpay_payment_id, status, error_code, error_reason, error_source | FK order |
| `subscriptions` | Subscription/policy-linked recurring plan | id, merchant_id, customer_id, razorpay_subscription_id, type (`generic`/`insurance_premium`), status | FK customer |
| `subscription_charges` | Each recurring charge attempt | id, subscription_id, razorpay_invoice_id, status, attempt_number | FK subscription |
| `recovery_cases` | Central case entity — one per "revenue at risk" event | id, merchant_id, scenario_type (A–H), source_ref (payment/order/subscription/anomaly id), state, opened_at, closed_at | FK merchant, polymorphic ref |
| `recovery_attempts` | Each action taken within a case | id, case_id, attempt_number, action_type, status, executed_at, result | FK recovery_cases |
| `agent_decisions` | LLM diagnosis + proposed action + rationale, per attempt | id, case_id, input_context_snapshot, diagnosis, proposed_action, confidence, rationale_text | FK recovery_cases |
| `policies` | Merchant-configurable guardrail set | id, merchant_id, max_retries, max_txn_amount, max_contacts, recovery_window_days, allowed_actions, requires_human_approval_rules | FK merchant |
| `policy_evaluations` | Record of each policy check (allow/block) | id, case_id, attempt_id, decision (allowed/blocked), reason | FK case, attempt |
| `audit_logs` | Immutable full trail of every state change | id, case_id, actor (agent/system/policy/human), action, before_state, after_state, timestamp | FK case |
| `events` | Raw inbound events (webhooks + internal) | id, merchant_id, source (razorpay/analytics), event_type, payload, processed_at | FK merchant |
| `interventions` | Customer-facing action content (message, link) | id, case_id, channel, content, sent_at, link_ref | FK case |
| `revenue_anomalies` | Detected product/volume-level anomalies (F, H) | id, merchant_id, metric_type, baseline, observed, deviation_pct, detected_at | FK merchant |
| `metrics_snapshots` | Periodic rollups for dashboard (avoids recompute) | id, merchant_id, period, revenue_at_risk, revenue_recovered, recovery_rate, unresolved_cases | FK merchant |

Notes:
- `recovery_cases.source_ref` is polymorphic (payment_id / order_id / subscription_id / revenue_anomaly_id) — one lifecycle table serves all scenarios A–H, avoiding per-scenario case tables.
- Scenario E stays representable in `recovery_cases.scenario_type` enum but is not activated in MVP logic.

---

## 4. Common Tool Layer

Consolidated once, reused across A–H (no per-scenario duplicates).

**Razorpay API tools**
- `get_payment(payment_id)`
- `get_order(order_id)`
- `get_subscription(subscription_id)`
- `create_payment_link(...)`
- `check_payment_status(payment_id)`
- `check_subscription_status(subscription_id)`

**Database / analytics tools**
- `get_merchant_error_frequency(merchant_id, error_code)`
- `get_product_rejection_rate(product_id)`
- `get_revenue_baseline(merchant_id, metric)`
- `detect_anomaly(metric_series)` (statistical/rule-based, not ML)

**Customer/context tools**
- `get_customer_profile(customer_id)`
- `get_customer_payment_history(customer_id)`
- `get_previous_recovery_attempts(case_id or customer_id)`

**Recovery-action tools**
- `retry_or_create_payment_link(...)` (generic — covers A/B/C/D)
- `send_reminder(customer_id, channel, template)`
- `escalate_to_human(case_id, reason)`

**Verification tools**
- `poll_payment_status(payment_id, timeout)`
- `confirm_order_completed(order_id)`
- `confirm_subscription_active(subscription_id)`

**Policy/guardrail tools**
- `evaluate_policy(merchant_id, proposed_action, case_history)`
- `check_idempotency(case_id, action_type)`

**Audit tools**
- `record_decision(case_id, decision_payload)`
- `record_outcome(case_id, outcome_payload)`

Each scenario module (A–H) calls into this shared tool layer with scenario-specific context, rather than owning its own tool implementations — matching the earlier note that "tooling can be handled differently in different files" while keeping underlying calls shared.

---

## 5. Agent Architecture

```
Event → Context Collection → Diagnosis → Reasoning → Proposed Action
      → Policy Check → Execution → Verification → Outcome
```

| Stage | Deterministic or LLM | Detail |
|---|---|---|
| Event ingestion | Deterministic | Webhook parsing, validation, dedup |
| Context collection | Deterministic | Tool calls fetch structured data only |
| Diagnosis | **LLM** | Given structured context, LLM infers root cause |
| Reasoning / strategy selection | **LLM** | Chooses from a fixed enum of allowed actions, not free text |
| Proposed action | LLM output, schema-validated | Structured output (Pydantic-enforced) |
| Policy check | Deterministic | Policy Engine only, no LLM involved |
| Execution | Deterministic | Tool call to Razorpay/merchant system |
| Verification | Deterministic | Poll/webhook confirmation |
| Outcome + metrics | Deterministic | Pure calculation, written to DB |

The LLM never touches money math, never calls Razorpay directly, and its output space is constrained to a predefined action enum + structured fields — this is what makes the loop explainable and auditable.

---

## 6. Event System

| Event | Source |
|---|---|
| `payment.failed` | Razorpay webhook |
| `checkout.abandoned` | Our own analytics (order created, not completed within threshold) |
| `subscription.charge.failed` | Razorpay webhook |
| `premium.payment.failed` | Razorpay webhook (subscription type = insurance) |
| `churn.cancellation_intent` | Our own analytics/product signal (parked with scenario E) |
| `revenue.anomaly.product` | Our own statistical job (F) |
| `revenue.anomaly.txn_volume` | Our own statistical job (H) |
| `churn.activity_drop` | Our own analytics job (G) |

Razorpay-native events arrive via webhook and go straight into `events` then the case pipeline. Analytics-native events are produced by scheduled jobs in `analytics/` comparing live metrics against rolling baselines, then inserted into `events` the same way — so downstream handling is uniform regardless of origin.

---

## 7. Recovery Case Lifecycle

```
DETECTED → INVESTIGATING → DIAGNOSED → ACTION_PROPOSED → POLICY_CHECK
   → ACTION_EXECUTED → VERIFICATION → (RECOVERED | FAILED | ESCALATED) → CLOSED
```

- `POLICY_CHECK` blocking sends the case to `ESCALATED` (human review) instead of `ACTION_EXECUTED`.
- `VERIFICATION` timeout (no confirmation within window) routes to `FAILED` with reason `verification_timeout`, still auditable.
- Multiple attempts can loop `ACTION_PROPOSED → ... → VERIFICATION` up to `max_retries` before falling to `FAILED`/`ESCALATED`.

---

## 8. Policy / Guardrail Planning

Configurable per merchant in `policies` table:
- Maximum retry attempts (e.g. 2)
- Maximum transaction amount eligible for automated action (e.g. ₹10,000)
- Maximum customer contacts per case (e.g. 2)
- Recovery window (e.g. 7 days from detection)
- Allowed intervention types per scenario (retry / payment link / reminder / escalation — some scenarios may exclude certain types, e.g. no auto-retry on premium above a threshold)
- Human-approval triggers: amount above threshold, repeated failure of same customer, blocked policy on 1st attempt, scenario = churn/retention (discount-bearing actions)
- Idempotency: `check_idempotency` keyed on (case_id, action_type, target_ref) before every execution to prevent duplicate webhook or duplicate agent runs from double-charging or double-messaging

---

## 9. Analytics / Metrics

- **Revenue at risk** = Σ amount of all payments/orders/subscriptions entering a `recovery_case` in period
- **Revenue recovered** = Σ amount of cases that reach `RECOVERED` state, using the actually-confirmed payment amount (not proposed amount)
- **Recovery rate** = recovered cases / total cases in period
- **Intervention success rate** = successful attempts / total attempts (attempt-level, finer grain than case-level recovery rate)
- **Failed interventions** = attempts reaching `FAILED`
- **Unresolved cases** = cases still open past recovery window
- **Average recovery time** = mean(`closed_at` − `opened_at`) for `RECOVERED` cases
- **Prevented unsafe actions** = count of `policy_evaluations` with decision = blocked
- **ROI of interventions** = (revenue recovered − cost of interventions, e.g. messaging/discount cost) / cost of interventions

All computed by deterministic SQL/aggregation jobs in `analytics/`, rolled into `metrics_snapshots` for dashboard performance.

---

## 10. API Endpoint Planning (grouped, not implemented)

- **Events**: `POST /webhooks/razorpay`, `POST /events/internal`
- **Cases**: `GET /cases`, `GET /cases/{id}`, `GET /cases/{id}/timeline`
- **Agent**: `GET /cases/{id}/decisions` (read-only, for audit view)
- **Policies**: `GET /merchants/{id}/policies`, `PUT /merchants/{id}/policies`
- **Analytics**: `GET /metrics/summary`, `GET /metrics/timeseries`
- **Escalations**: `GET /escalations`, `POST /escalations/{id}/resolve` (human-in-loop action)
- **Audit**: `GET /audit/{case_id}`
- **Live activity**: `WS /live/agent-activity` (SSE/WebSocket feed for dashboard)

API surface stays read/config-heavy; money-moving actions never exposed as direct external endpoints — they only happen inside the agent→policy→execution pipeline.

---

## 11. Razorpay Integration Boundary

| Category | Detail |
|---|---|
| Already provided by Razorpay | Payment details + error fields, Orders API, Subscriptions API, Payment Links API, `payment.failed`/subscription webhooks, automatic subscription retry behavior |
| We must aggregate ourselves | Merchant-level error frequency, customer payment history, product rejection rate, abandonment detection, previous-attempt tracking, all case/audit state |
| Actions Razorpay can execute | Create payment link, check payment/order/subscription status, (its own) automatic subscription retry |
| Actions our system executes outside Razorpay | Sending reminders via non-Razorpay channels, escalation to human, discount/retention offers, product-level anomaly response |
| Must simulate in test mode | "Retry this exact failed payment" (no generic retry API exists — simulate via new payment link + mark linked to original failure), realistic failure distributions, churn/activity signals, revenue anomalies |

---

## 12. Synthetic Data / Testing Plan

- **Failed payments**: generate payments in Razorpay test mode using documented test card/UPI failure triggers; vary `error_code`/`error_source` to build realistic frequency distributions
- **Abandoned checkouts**: create orders via test mode, deliberately leave a percentage unpaid past a threshold window
- **Recurring payment failures**: create test subscriptions, force charge failures on selected cycles
- **Churn**: synthetic activity logs with engineered drop-off patterns (not built into MVP execution, but data model should support it for demo)
- **Product revenue drops**: synthetic daily revenue series per product with injected anomalies (sudden drop, gradual decline)
- **Transaction volume drops**: synthetic overall transaction count series with injected dips
- Ground truth for each synthetic case stored alongside so demo can show "detected vs actual" for judging credibility

---

## 13. Failure Handling

| Failure | Handling |
|---|---|
| Razorpay API failure | Retry with backoff; case stays in current state; log to audit; alert if repeated |
| Payment remains pending | Case stays in `VERIFICATION` until window elapses, then `FAILED` with reason `stuck_pending` |
| Recovery action fails | Attempt marked `FAILED`, case loops to next attempt if under `max_retries`, else `ESCALATED` |
| Duplicate webhook | Deduped via `events` table unique constraint on (source, external_event_id) before case creation |
| LLM gives invalid action | Schema validation rejects it; case falls back to a safe default (`ESCALATED`) rather than retrying LLM indefinitely |
| Policy blocks action | Case → `ESCALATED`, `policy_evaluations` records reason, human review queue |
| Verification timeout | Case → `FAILED` with `verification_timeout`, still counted in metrics as unresolved/failed, not silently dropped |
| Partial recovery | e.g. partial payment captured — case records actual recovered amount vs at-risk amount, state reflects partial (`RECOVERED` with partial flag, or dedicated status if needed) |

---

## 14. Final Backend Architecture

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
                     ┌────────┴────────┐
                     ↓                 ↓
                  Allowed           Blocked
                     ↓                 ↓
              Tool Execution     Human Review Queue
           (Razorpay / Merchant
                 Systems)
                     ↓
                Verification
                     ↓
           Database + Audit Trail
                     ↓
                  Dashboard
```

This keeps the modular monolith intact, preserves the bounded/gated/explainable/auditable requirement end-to-end, and reuses one case lifecycle + one tool layer across all eight scenarios without introducing new scope.