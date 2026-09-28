# Assignment 4 requirements checklist

Source: *Class 5 Assignment: Personal Wiki with Local Gemma + RAG* (MBA 290T, Fall 2026), read in full on
2026-09-26. Assigned Tue 9/22 in Class 5, **due Tue 9/29 at 11:59 pm PT** (syllabus). Scored out of 10:
deliverable quality 4, testing & evaluation 3, working result 3. Each line below maps a requirement to
where this project meets it; the README links the evidence for each.

## Required features

| # | Requirement (from the brief) | Where it is met |
|---|---|---|
| F1 | Own CLI and harness; no cloned sample app; a ready-made document-chat app alone does not count | `src/wiki/` (cli, harness, retrieval, ingest, vault, llm, embed, serve, chat) |
| F2 | Local open-weight Gemma sized for the device, runs offline | Gemma 4 E4B QAT Q4_0 in llama.cpp; `config/settings.toml`; README › Setup |
| F3 | **chat**: personal assistant with a recognizable voice, accurate description of capabilities, brainstorm/draft/plan, uses recent conversation for follow-ups | `instructions/persona.md`, `harness.ChatSession`, `chat.py` |
| F4 | chat retrieves notes only when the request needs them, cites claims from notes, labels proposals as suggestions, never invents personal facts | `ChatSession.route`, `[N#]` tags, persona rules |
| F5 | chat: "what can you help me with?" explains real capabilities; no insufficient-evidence reply, no unrelated passages | mode check M1 |
| F6 | chat: after a draft/plan, "make that shorter" uses the conversation | mode check M2 |
| F7 | **ask**: independent of chat history; retrieves evidence; neutral voice; citations; says so when sources do not support an answer | `harness.ask` (takes no history), `instructions/research-rules.md` |
| F8 | **search**: original passages + source locations; no generated answer; works without the language model running | `wiki search`, `retrieval.Index.search` |
| F9 | **ingest**: read local sources, generate linked wiki pages with local Gemma, update the local index | `wiki ingest`, `ingest.py` |
| F10 | **help**: explains commands, configuration, required inputs; useful errors for missing files or unavailable local model | `wiki --help`, `wiki help <cmd>`, `cli.main` error mapping |
| F11 | Harness shows the model and execution setting; local is the default | header line on every command; `--mode local` default |
| F12 | Research rules and assistant personality kept explicit and separate; harness loads the right one per mode | `instructions/research-rules.md` vs `instructions/persona.md` |
| F13 | Chat history is conversation context, not verified source material; any save-memory feature is explicit and keeps drafts apart from evidence | `/save` writes to `drafts/` (outside the vault, never indexed) |
| F14 | Split long text into passages, keep source path and section; explain how much text goes to Gemma | `retrieval.chunk_*`, README › Design choices |
| F15 | Local retrieval (keyword and/or local embeddings); no hosted embedding API | BM25 + EmbeddingGemma-300M on 127.0.0.1 |
| F16 | Select relevant passages and keep source labels rather than sending the whole wiki | `select_within` token budgets |
| F17 | Save outputs: model/runtime settings, source catalog, wiki pages, retrieval outputs, answers, citations, evidence cards, mode checks; errors recorded | `runs/`, `evidence/`, `data/catalog.json` |
| F18 | Optional online mode through the same harness, clearly labelled, never replaces local | `--mode online` (Gemini API `gemma-4-26b-a4b-it`), no fallback |

## Wiki / Obsidian requirements

| # | Requirement | Where it is met |
|---|---|---|
| W1 | ≥3 original sources in `vault/raw/`, unchanged | 25 originals (website, syllabus, course projects), sha256 in the Source Catalog |
| W2 | Generated pages in `vault/wiki/`; current `vault/index.md` | `wiki ingest` rebuilds both |
| W3 | Short descriptive file names (2–6 words), first heading matches file name | `vault.clean_title`, `naming_problems`, `wiki check` |
| W4 | No export-task titles, full sentences, timestamps, UUIDs, hashes or chunk numbers as names; aliases are not a fix | naming rules enforced in code; lint |
| W5 | Machine IDs and original file names in properties or a source catalog | note properties `sources`, `data/catalog.json`, `vault/Source Catalog.md` |
| W6 | Open `vault/` itself as the vault; raw/, wiki/, attachments/; a few topic folders | `wiki/Projects`, `Experience`, `Course`, `Concepts` |
| W7 | Code, logs, retrieval chunks, embeddings, test answers outside the vault | `data/`, `runs/`, `evidence/`, `tests/` |
| W8 | index.md as a human landing page grouped by topic with short descriptions | `vault.render_index` |
| W9 | One subject per note: summary, details, source references, related notes; merge overlapping notes | note template; subject merge in `Ingester.place` |
| W10 | Meaningful internal links with a reason; no unrelated links for graph density | "Related notes" with one-line reasons; link pass |
| W11 | Graph useful: filter `path:wiki/`, attachments off, readable labels | `vault/.obsidian/graph.json` preset |
| W12 | Check in Obsidian: index → topic → related note → source reference; links and source refs resolve | `wiki check` + screenshots |
| W13 | Review generated summaries against originals; correct the wiki, not the evidence | `evidence/wiki_review.md` |
| W14 | Cleanup (if needed): back up, rename, merge, update incoming links, index, source mappings, retrieval paths; rebuild index; rerun tests | `wiki rename`, `wiki ingest` |
| W15 | Re-ingesting the same source updates the intended notes without duplicates or machine-style names | sha256 skip; catalog-mapped paths; re-ingest check |

## Testing & evaluation requirements

| # | Requirement | Where it is met |
|---|---|---|
| T0 | Write three answerable questions + expected source passages + one unanswerable question **before building retrieval** | `tests/questions.yaml` (written before `retrieval.py`) |
| T1–T3 | Direct question (one source); reworded question; question with known evidence (can connect two sources) | `evidence/offline/ask/T1.md`–`T3.md` |
| T4 | Plausible question with no answer in the wiki → explicit insufficient-evidence | `evidence/offline/ask/T4.md` |
| T5 | Keep test expectations outside the searchable wiki | `tests/` is never indexed |
| T6 | Per test: question, retrieved passages + paths, exact model identity, local/online, answer, citations, assessment | evidence cards |
| T7 | Inspect retrieval first, then the answer; record missing evidence, irrelevant retrieval, invented details, unsupported citations as failures | `evidence/retrieval/`, card assessments |
| T8 | Mode checks: casual chat, conversational follow-up, raw search, ask not using chat claims | `evidence/offline/mode_checks.md` |
| T9 | If a setting changes after a failure: document it, rerun, keep the earlier result | README › Evidence and change log |
| T10 | Measure memory use and response time for local ingestion and an answer | `evidence/metrics/` |

## Offline demonstration

| # | Requirement | Where it is met |
|---|---|---|
| O1 | Download weights, packages, tokenizer, embedding model while online; confirm stored locally | `config/models.lock.json` (sha256 verified against Hugging Face) |
| O2 | Disconnect internet, restart the CLI in local mode, ingest a local source, run all four ask tests and the chat/search checks | `scripts/offline_demo.sh` → `evidence/offline/` |
| O3 | No hosted embeddings, remote search or cloud fallback | local endpoints enforced by `llm.assert_local` |
| O4 | Terminal recording or screenshots + saved evidence cards | `evidence/offline/` transcript + screen recording |

## README must contain

Purpose and sources; setup and device (OS, CPU/chip, total RAM, GPU/VRAM or unified memory, available memory,
free disk, dependencies, model/version, quantization, runtime, downloads, exact CLI commands, model-choice
rationale, measured memory and response time); architecture (model vs retrieval tool vs RAG workflow vs CLI
vs harness, and one traced path from command to result); design choices (passage size, retrieval method,
research rules, personality, context limits, when chat retrieves, note naming/folders, source-ID mapping,
duplicate avoidance, model settings); evidence links (four ask cards, mode checks, offline proof, model and
data used); reflection (one real failure/limitation, cause, one concrete improvement); optional online mode
(how to select, endpoint, what data is sent), kept separate from the offline instructions.

Required Obsidian screenshots: (1) an open note with short descriptive file name, matching heading, source
references and related-note links; (2) the topic-organised page list or index; (3) graph view with readable
labels and meaningful connections (record the filter used). Show the source catalog; trace one note through
a related note back to its original evidence; confirm links work; confirm re-ingest creates no duplicates.
Redact private information.

## Submission

- One **public GitHub repository** (own project, not a sample) with CLI/harness code, README, shareable wiki
  sources and pages, and test evidence. Submitted through the course portal
  (https://submissions-portal-eight.vercel.app). Not a capstone phase.
- Follow the documented setup once more; confirm downloads complete before the offline run.
- Open the repository signed out and confirm README, code, wiki and evidence links work.
- Do not commit model weights or credentials. Give the official download source and exact model identifier.
- Scope: model training, MCP, agents and public deployment are not required. A notebook or web UI is optional.
