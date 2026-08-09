---
title: Performance Testing Basics (Load, Stress, Spike, k6, Locust & JMeter)
category: 18_PERFORMANCE
subcategory: Performance Testing
keywords:
  - Performance Testing
  - Load Testing
  - Stress Testing
  - Spike Testing
  - Endurance Testing
  - Response Time
  - Throughput
  - k6
  - Locust
  - JMeter
audience:
  - Quality Engineer
  - Performance Specialist
  - SDET
difficulty: intermediate
---

# ⚡ Performance Testing Basics: Metrics & Tooling Guide

## 🎯 Overview: Key Performance Testing Types

Performance testing evaluates system responsiveness, throughput, and stability under workload.

```
  LOAD TESTING      ──> Expected normal peak load (e.g., 1,000 concurrent users for 2 hours).
  STRESS TESTING    ──> Extreme workload breaking point (e.g., Scaling load until system crashes at 8,500 users).
  SPIKE TESTING     ──> Instant sudden traffic surge (e.g., 0 to 5,000 users in 10 seconds during flash sale).
  ENDURANCE TESTING ──> Prolonged sustained load over 24-48 hours (Detects memory leaks and log disk full issues).
```

---

## 📊 Core Performance Metrics

* **Response Time (Latency)**: Time taken to process request (Measure $p_{90}, p_{95}, p_{99}$ percentiles; avoid averages!).
* **Throughput (RPS / TPS)**: Transactions or requests processed per second.
* **Concurrency**: Number of virtual users executing requests simultaneously.

---

## 🛠️ Modern Tooling Comparison (k6 vs. Locust vs. JMeter)

| Tool | Scripting Language | Primary Advantage | Best Use Case |
| :--- | :--- | :--- | :--- |
| **k6** | JavaScript / Go | Developer-friendly, CLI native, low CPU overhead. | API Load Testing in CI/CD pipelines. |
| **Locust** | Python | Expressive Python code, dynamic user behavior. | Python-centric engineering teams. |
| **JMeter** | GUI / XML | Extensive legacy protocol support (SOAP, JMS, FTP). | Enterprise legacy platform load tests. |

---

## 💻 Practical k6 JavaScript Load Test Script (`load_test.js`)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },  # Ramp up to 50 users over 30s
    { duration: '1m', target: 50 },   # Stay at 50 users for 1 minute
    { duration: '10s', target: 0 },   # Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], # 95% of requests must complete under 500ms
  },
};

export default function () {
  const res = http.get('https://staging.erp.client.com/api/v1/health');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

---

## 🔗 Related Topics
* [01. HTTP REST Methods](../06_API_TESTING/01_http_rest_methods_status_codes.md)
* [01. Quality Gates in CI/CD](../02_QA_ENGINEERING/05_quality_gates_and_ci_cd.md)
