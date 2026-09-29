# Chat checks in online mode (optional extension)

Run 2026-09-28 at about 19:54–19:56 with the internet on and `--mode online`: hosted `gemma-4-26b-a4b-it` through the
Gemini API. Retrieval, the chat router's rules and the vault stayed on this laptop. The same scripted turns as the
local checks ([`tests/chat_scripts/`](../../tests/chat_scripts/)), run as `wiki chat --mode online --script <file>`.
Transcripts are saved verbatim; each ends with the path of its full log under `runs/`. M3 (search with the model
stopped) involves no model, so there is nothing online to check.

| Check | Transcript | What happened | Assessment |
|---|---|---|---|
| M1 casual chat, capabilities | [before fix 13](chat/M1_capabilities-before-fix13.txt) | no notes lookup for either turn; the command list is right (`/notes`, `wiki ask`, `/save` to `drafts/`), but Wren said *"Since I live on your laptop"*, *"I don't have internet access"* and *"Since I'm running locally"*: false in online mode | Failed (kept as evidence) |
| M1 after the fix | [after fix 13](chat/M1_capabilities.txt) | no notes lookup; capabilities explained with no claim about where it runs | Pass |
| M2 conversational follow-up | [M2](chat/M2_followup.txt) | the week plan was drafted without a lookup, and "make that shorter" condensed the same plan from the conversation. Minor: it said it did not have the Assignment 4 deadline "in my notes yet", but it had not looked (the syllabus note has it) | Pass |
| M4 ask ignores chat history | [chat](chat/M4_claim.txt) · [ask](chat/M4_ask.txt) | chat acknowledged "my favorite programming language is Rust" with no lookup; the separate `wiki ask … --mode online` answered `Insufficient evidence`, and its saved prompt (`runs/ask-20260928-195513-308.json`) does not contain "Rust" | Pass |

**Fix 13** ([changes.md](../changes.md)): the persona said Wren runs "entirely on his laptop as a small local model"
in every mode. That sentence is now filled in per mode. The local wording is unchanged byte for byte, so the offline
evidence still matches the code; the online wording says the conversation is sent to Google. Regression test:
`tests/test_harness.py::test_persona_states_where_the_model_runs`.
