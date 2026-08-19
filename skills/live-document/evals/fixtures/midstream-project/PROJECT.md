# invoice-parser

so the idea here is we take PDF invoices from vendors and pull out line items + totals into a CSV.
started this like 3 weeks ago.

## goal
parse invoices. get the numbers out. originally was just for one vendor (Acme) but now we have like
4 vendors and they all have different layouts which is annoying.

## what we did
- week 1: built a regex based parser for Acme invoices. worked ok.
- then tried to add Globex invoices and the regex approach totally fell apart because their layout
  is two-column. spent 2 days fighting it.
- decided to switch to a layout-aware approach using the pdfplumber word boxes instead of raw text.
- Acme works again with the new approach. Globex like 80% there.
- Initech and Umbrella not started yet.
- oh also we decided early on to output CSV but honestly the user (finance team) wants xlsx with one
  sheet per vendor. need to change that.

## decisions
- use pdfplumber not PyPDF2 (PyPDF2 mangled the layout)
- python not node for this part even though rest of stack is node, because pdf libs are better in py
- output was going to be CSV

## todo
- finish Globex
- Initech
- Umbrella
- switch output to xlsx
- the totals sometimes off by a penny due to rounding, need to fix

## random notes
- vendor sends invoices to invoices@ inbox, someone forwards them, eventually we want to auto-pull
- the rounding bug is because we sum floats, should use Decimal
- finance team only cares about: vendor, invoice date, line items, total. nothing else.
- deadline is end of quarter for at least Acme + Globex working in production
