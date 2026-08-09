---
title: Test Case Design Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: Test Design
keywords:
  - Test Design Cheat Sheet
  - BVA Cheat Sheet
  - Equivalence Partitioning
audience:
  - Quality Engineer
  - SDET
difficulty: beginner
---

# 📐 Test Case Design Quick Reference Cheat Sheet

## 📐 Technique Quick Formulas
* **Equivalence Partitioning (EP)**: Pick 1 value per partition (Valid, Invalid-Too-Low, Invalid-Too-High).
* **Boundary Value Analysis (BVA)**: Test edges (Min-1, Min, Min+1, Max-1, Max, Max+1).
* **Decision Tables**: $2^N$ rule combinations for $N$ boolean conditions.
* **State Transition**: Test all valid & invalid state transitions (Draft $\rightarrow$ Pending $\rightarrow$ Approved).
