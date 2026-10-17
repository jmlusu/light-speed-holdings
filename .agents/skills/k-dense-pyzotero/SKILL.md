---
name: k-dense-pyzotero
description: Python client for the Zotero Web API v3 for programmatically managing reference libraries—retrieving, creating, updating, and deleting items, collections, tags, and attachments—and exporting citations as BibTeX/CSL-JSON. NOTE: This skill is NOT keyless; it requires either (a) a Zotero API key from your Zotero account, or (b) a local Zotero application installed with your library. Without a key or local Zotero, this skill will fail at runtime. All other k-dense-* skills in this installation are keyless open-API only.
mode: primary
tools:
  - read
  - grep
  - list
permissions:
  - read: open document APIs
  - list: skill catalog
---
