---
title: ERP Workflow & Module Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: ERP
keywords:
  - ERP Cheat Sheet
  - P2P Workflow Cheat Sheet
  - O2C Cheat Sheet
  - 3-Way Match
audience:
  - Quality Engineer
  - ERP Tester
difficulty: beginner-intermediate
---

# 🏭 ERP Workflow & Module Quick Reference Cheat Sheet

## 🔄 Core Workflow Paths
* **Procure-to-Pay (P2P)**: Requisition $\rightarrow$ Approval $\rightarrow$ Purchase Order $\rightarrow$ Goods Receipt $\rightarrow$ Invoice Entry $\rightarrow$ 3-Way Match $\rightarrow$ Payment.
* **Order-to-Cash (O2C)**: Customer Order $\rightarrow$ Credit Check $\rightarrow$ Sales Order $\rightarrow$ Stock Reservation $\rightarrow$ Shipment $\rightarrow$ Invoicing $\rightarrow$ Cash Application.

## ⚖️ 3-Way Match Validation Formula
$$\text{Invoice Qty} == \text{GR Qty} \quad \text{AND} \quad \text{Invoice Price} == \text{PO Price} \pm \text{Tolerance Threshold}$$

## 🔐 Key SoD Restrictions
* **Buyer**: Can create PO $\rightarrow$ Cannot approve own PO or receive goods.
* **Warehouse**: Can post Goods Receipt $\rightarrow$ Cannot approve payments.
* **Finance**: Can approve invoices $\rightarrow$ Cannot modify warehouse inventory or vendor bank details.
