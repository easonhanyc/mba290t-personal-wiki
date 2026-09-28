# Ingest rules: how wiki notes are written

You turn one original source into material for a personal wiki that a person browses in Obsidian and a
retrieval program searches. Respond only with the JSON object requested.

## What a note is
- One note is about **one subject**: a project, a job or school, a course, or a concept. It is not about
  a file, a task, or a chunk of text.
- The title names the subject in **2 to 6 words**, the way a person would name the page. Good examples:
  "Ms. Pac-Man DQN", "Secure Networking Tracker", "Row Level Security", "Amazon Web Services",
  "MBA 290T Syllabus".
- Never use file names, export or task titles, full sentences, dates, IDs, hashes or chunk numbers as a
  title. Drop marketing subtitles: "Action Hub — Ranked Alerts with Next Actions" becomes "Action Hub".

## Facts
- Every fact must be stated in the source text you were given. Do not add outside knowledge or infer
  numbers that are not there.
- Keep numbers, names and dates exactly as written.
- Each fact is one self-contained sentence that makes sense without the source next to it.
- `section` must be copied exactly from one of the `## ` headings shown in the source text.

## Folders
- Projects: something built, analysed or shipped (including course assignments).
- Experience: an employer, role, school or program.
- Course: a class, its syllabus, schedule or policies.
- Concepts: a general technique or idea that is useful beyond one project.

## Links and concepts
- `related` may only use titles from the EXISTING NOTES list. Give a one-line reason that says what the
  two subjects actually share. Leave the list empty rather than linking something unrelated.
- `concepts` are general techniques or ideas this source discusses in substance (for example
  "Deep Q-Learning" or "Row Level Security"), not products, people or companies.
