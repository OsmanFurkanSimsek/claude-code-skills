# PROJECT.md - invoice-parser

> Single source of truth. A fresh agent reading only this file can continue correctly.

## Goal and definition of done

Parse the three vendor invoice formats (Acme, Globex, Initech) into a normalized table with
line items and totals that match the PDFs to the cent.

## Scope and non-goals

- In: the three vendor formats, totals validation, batch runs over a folder.
- Out: OCR for scanned PDFs, vendor portals, invoice approval workflow.

## Current state and next action

Acme and Initech parsing done. Globex is 80% there - line items parse, totals still off on
multi-page invoices. Next action: fix Globex multi-page totals.

## Decisions locked

- Output format: CSV, one file per vendor, semicolon-separated (finance imports it into Excel).
- pdfplumber for extraction (tried PyPDF2 first, table extraction too weak).

## Plan / workstreams

- [x] Acme parser
- [x] Initech parser
- [~] Globex parser (multi-page totals bug open)
- [ ] Switch output to xlsx? Finance asked informally, not confirmed.
- [ ] Batch runner over the inbox folder.

## Open questions

- Rounding bug: batch totals drift by cents on large invoices - float summation suspected.
- Does finance officially want xlsx instead of CSV?

## Change log

- 2026-07-01: Acme + Initech parsers shipped, totals reconcile.

## Lessons

- PyPDF2 table extraction was too weak for these layouts; pdfplumber handles them (2026-06-20).
