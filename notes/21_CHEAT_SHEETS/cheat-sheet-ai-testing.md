---
title: AI Prompting for QA Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: AI Testing
keywords:
  - AI Prompt Cheat Sheet
  - Prompt Engineering
  - QA AI Prompts
audience:
  - Quality Engineer
  - SDET
difficulty: beginner
---

# 🤖 AI Prompting for QA Quick Reference Cheat Sheet

## 💡 Key Rules
1. **Never input secrets**: Redact API keys, JWT tokens, passwords, and patient PII before prompting.
2. **Review all generated code**: Validate locators, remove hardcoded sleep, verify assertions.

## 📝 High-Yield Prompt Format
> "ROLE: SDET Architect. CONTEXT: Testing ERP API. INSTRUCTION: Generate 5 negative test JSON payloads for [Schema]. CONSTRAINTS: Include expected HTTP status code for each."
