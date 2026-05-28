# Brand Guardian — Migration Log

## Purpose

Tracks infrastructure and architectural migration decisions from the Azure-based implementation to the open-source production stack.

---

## Migration Timeline

| Date       | Component       | Old System  | New System  | Status   | Notes                                                              |
| ---------- | --------------- | ----------- | ----------- | -------- | ------------------------------------------------------------------ |
| 2026-05-28 | Baseline Freeze | Azure Stack | Azure Stack | Complete | Stable Azure implementation frozen and tagged as v1.0-azure-stable |

---

## Current Branch Strategy

| Branch        | Purpose                                 |
| ------------- | --------------------------------------- |
| azure-version | Stable Azure reference implementation   |
| main          | Open-source production migration branch |

---

## Migration Principles

1. Preserve orchestration-first architecture
2. Replace infrastructure incrementally
3. Maintain structured output compatibility
4. Prioritize observability and debuggability
5. Avoid premature optimization
6. Keep Azure implementation as rollback reference

---

## Planned Service Replacements

| Azure Service       | Replacement            |
| ------------------- | ---------------------- |
| Azure Video Indexer | Whisper + OCR pipeline |
| Azure AI Search     | Qdrant                 |
| Azure Monitor       | Langfuse               |
| Azure OpenAI        | OpenAI API             |
