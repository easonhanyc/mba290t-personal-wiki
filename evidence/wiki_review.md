# Wiki review log

Every generated note was read against the original passages it cites (`scripts/review_notes.py`). Corrections were made in the wiki, never in `vault/raw/`. This log is written by `scripts/apply_review.py`, which holds each edit and its reason. Notes with no edits below were checked and found accurate.

Reviewed 2026-09-27 01:06 by Claude (Anthropic), for Eason Han; each fact checked against the cited passage.

Totals: 67 facts corrected, 43 facts removed (mostly duplicates after merging sources), 14 summaries rewritten, related links re-checked and re-explained on 23 notes.

## Action Hub

- **fact corrected**: I ran 20 user interviews across segments before writing requirements, then scoped the build from a PRD and Figma prototypes. → 20 user interviews across segments were run before writing requirements; the build was then scoped from a PRD and Figma prototypes.  
  _Why:_ neutral voice
- **fact corrected**: Anything that changed only what a seller *knew* went below the line. → When scope had to be cut, requests that changed only what a seller knew went below the line.  
  _Why:_ added the context of the passage (scope cuts against a fixed launch date)
- **fact corrected**: I under-invested in instrumenting the "action taken" step. → A stated lesson: instrumenting the 'action taken' step was under-invested.  
  _Why:_ neutral voice
- **related links replaced**: Amazon Web Services, Allowlist Data Access App, Job Search Agent  
  _Why:_ each link now states a relationship the sources support

## Allowlist Data Access App

- **related links replaced**: Amazon Web Services, Action Hub, Secure Networking Tracker  
  _Why:_ each link now states a relationship the sources support

## Amazon Web Services

- **summary rewritten**: This role involved working on internal products for over 10,000 sellers within an $80B business. The focus was on transf…  
  _Why:_ clearer, source-checked summary
- **fact removed**: org: Amazon Web Services  
  _Why:_ redundant with the note title
- **fact corrected**: role: Business Intelligence Engineer — Global Sales Strategy & Analytics → Job title: Business Intelligence Engineer — Global Sales Strategy & Analytics.  
  _Why:_ raw front-matter line rewritten as a sentence
- **fact corrected**: location: Seattle, WA → Based in Seattle, WA.  
  _Why:_ front-matter line rewritten as a sentence
- **fact corrected**: start: Jul 2023 → Dates: Jul 2023 to May 2026.  
  _Why:_ start and end combined
- **fact removed**: end: May 2026  
  _Why:_ combined into the dates fact
- **fact corrected**: summary: Internal products for 10,000+ sellers across an $80B business. Three years spent turning a reporting function that produced reports into one that produced decisions. → Built internal products for 10,000+ sellers across an $80B business; three years spent turning a reporting function that produced reports into one that produced decisions.  
  _Why:_ front-matter line rewritten as a sentence
- **fact corrected**: outcomes: Raised on-time delivery of business stakeholder requests from 56% to 82% by establishing recurring roadmap reviews that published the backlog → Raised on-time delivery of business stakeholder requests from 56% to 82% by establishing recurring roadmap reviews that published the backlog.  
  _Why:_ front-matter line rewritten as a sentence
- **fact corrected**: outcomes: Launched a Business-Influence Tracker that lifted customer opportunity coverage 12% and became a standing Monthly Business Review KPI → Launched a Business-Influence Tracker that lifted customer opportunity coverage 12% and became a standing Monthly Business Review KPI.  
  _Why:_ front-matter line rewritten as a sentence
- **related links replaced**: Action Hub, Pull-Request Automation, GenAI Target Setting, Allowlist Data Access App, GenAI Adoption Program  
  _Why:_ each link now states a relationship the sources support

## Custom LLM with nanoGPT

- **summary rewritten**: This project details the process of building and evaluating a custom Large Language Model (LLM) using nanoGPT. Several e…  
  _Why:_ clearer, source-checked summary
- **fact corrected**: nanoGPT has 2 blocks, 4 heads, 64-number embeddings, and a 48-token context. → The model is a nanoGPT with 2 blocks, 4 heads, 64-number embeddings and a 48-token context.  
  _Why:_ the configuration belongs to this project's model, not to nanoGPT in general
- **fact corrected**: Reproduce experiment A can be done using the command python tools/run_experiment.py --experiment starter. → Experiment A is reproduced with `python tools/run_experiment.py --experiment starter`.  
  _Why:_ grammar
- **fact corrected**: Reproduce experiment D requires the command python tools/run_experiment.py --experiment tuned --corpus-dir corpus_seven --lr 0.004. → Experiment D is reproduced with `python tools/run_experiment.py --experiment tuned --corpus-dir corpus_seven --lr 0.004`.  
  _Why:_ grammar
- **fact corrected**: The choice of corpus was classroom; + 4-category; + 7-category; + 7-category with unpaired relations because the assignment requires the first two. → The corpora compared were the classroom corpus alone, plus a 4-category extension, plus a 7-category extension, and the 7-category extension with unpaired relations; the assignment required the first two.  
  _Why:_ Gemma flattened a table row into an unreadable sentence
- **fact removed**: The delivered model D has seven taught categories and a learning rate of 0.004.  
  _Why:_ duplicate of the model D definition fact
- **related links replaced**: MBA 290T Syllabus, Deep Learning, Ms. Pac-Man DQN, Hazardous Asteroid Screening  
  _Why:_ each link now states a relationship the sources support

## DataFest 2023

- **related links replaced**: University of Notre Dame, Formula 1 Racing Trends  
  _Why:_ each link now states a relationship the sources support

## Deep Learning

- **summary rewritten**: Deep Learning involves training layers of weights with non-linearities, guided by gradient descent to minimize predictio…  
  _Why:_ clearer, source-checked summary
- **fact corrected**: The parameters are arranged in layers, including an embedding table, two transformer blocks with 4 attention heads and a small MLP, and an output layer mapping 64 dimensions back to vocabulary scores. → In the project's nanoGPT, the parameters are arranged in layers: an embedding table, two transformer blocks (each with 4 attention heads and a small MLP), and an output layer mapping 64 dimensions back to vocabulary scores.  
  _Why:_ added which model this describes
- **fact corrected**: The learning rate is set to 1e-05 at step 0 because it is part of a 100-step warmup where the initial rate of 0.001 is scaled by (1/100). → The learning rate at step 0 is 1e-05, not 0.001, because step 0 is the first step of a 100-step warmup (0.001 × 1/100).  
  _Why:_ reworded to match the source exactly
- **related links replaced**: Custom LLM with nanoGPT, Deep Q-Network, MBA 290T Syllabus  
  _Why:_ each link now states a relationship the sources support

## Deep Q-Network

- **summary rewritten**: Deep Q-Network is a reinforcement learning technique used to train an agent to play Ms. Pac-Man by observing game screen…  
  _Why:_ clearer, source-checked summary
- **fact removed**: The exploration rate was set to 0.10, which was chosen as the measured sweet spot for the agent's performance.  
  _Why:_ project result, not part of the method; kept in Ms. Pac-Man DQN
- **fact removed**: The training ran for 300 episodes, which was the point where the measured evaluation score peaked.  
  _Why:_ project result, not part of the method; kept in Ms. Pac-Man DQN
- **fact removed**: The learning rate was set to 0.0001, as increasing it made the learning process worse.  
  _Why:_ project result, not part of the method; kept in Ms. Pac-Man DQN
- **fact removed**: The headline result showed the mean evaluation score rose from 492 (untrained) to 906 (trained).  
  _Why:_ project result, not part of the method; kept in Ms. Pac-Man DQN
- **related links replaced**: Ms. Pac-Man DQN, Deep Learning  
  _Why:_ each link now states a relationship the sources support

## Formula 1 Racing Trends

- **related links replaced**: University of Notre Dame, Time Series Analysis, DataFest 2023  
  _Why:_ Removed Gemma's link to Ms. Pac-Man DQN ('both use a Deep Q-Network'), which is false.

## GenAI Adoption Program

- **fact corrected**: Over 75% of 1,100 sellers did participate inside 60 days. → More than 75% of the 1,100 sellers participated within 60 days.  
  _Why:_ grammar
- **related links replaced**: Amazon Web Services, Action Hub  
  _Why:_ Removed a link to Job Search Agent ('both build an automated agent to scan and rank'), which is false for this programme.

## GenAI Target Setting

- **related links replaced**: Amazon Web Services, Time Series Analysis  
  _Why:_ Removed the link to GenAI Adoption Program: one sets a sales target for GenAI business, the other drove sellers' own use of GenAI tools; Gemma's reason conflated the two.

## Hazardous Asteroid Screening

- **fact corrected**: Four models, evaluated on a 30% holdout, included Logistic regression, Random forest, bagged, XGBoost, and XGBoost, tuned. → Four models were evaluated on a 30% holdout: logistic regression, a bagged random forest, XGBoost, and tuned XGBoost.  
  _Why:_ Gemma split the model names in the table into a garbled list
- **fact corrected**: The raw data was 4,687 asteroid records across 40 variables. → The raw data was 4,687 asteroid records across 40 variables, of which seventeen survived as predictors.  
  _Why:_ merged with the next fact, which had no subject
- **fact removed**: Seventeen survived as predictors.  
  _Why:_ merged into the previous fact
- **related links replaced**: University of Notre Dame, Custom LLM with nanoGPT  
  _Why:_ each link now states a relationship the sources support

## IDG Capital

- **summary rewritten**: This role involved serving as a Venture Capital Analyst Intern at IDG Capital in Beijing, China. The responsibilities in…  
  _Why:_ clearer, source-checked summary
- **fact removed**: org: IDG Capital  
  _Why:_ redundant with the note title
- **fact corrected**: role: Venture Capital Analyst Intern → Role: Venture Capital Analyst Intern.  
  _Why:_ front-matter line rewritten
- **fact corrected**: location: Beijing, China → Based in Beijing, China.  
  _Why:_ front-matter line rewritten
- **fact corrected**: start: Jun 2020 → Dates: Jun 2020 to Aug 2020.  
  _Why:_ start and end combined
- **fact removed**: end: Aug 2020  
  _Why:_ combined into the dates fact
- **fact corrected**: summary: Diligence on early-stage SaaS and food-supply companies. → Did diligence on early-stage SaaS and food-supply companies.  
  _Why:_ front-matter line rewritten
- **fact corrected**: outcomes: Evaluated 20+ startups on market position, product differentiation and operations, building a sector database that benchmarked new companies against it; → Evaluated 20+ startups on market position, product differentiation and operations, building a sector database that benchmarked new companies against it.  
  _Why:_ front-matter line rewritten
- **fact corrected**: outcomes: Informed 3 investment decisions by pressure-testing each growth story against executive interviews, industry-expert calls and IPO filings → Informed 3 investment decisions by pressure-testing each growth story against executive interviews, industry-expert calls and IPO filings.  
  _Why:_ front-matter line rewritten
- **related links replaced**: TikTok Internship  
  _Why:_ each link now states a relationship the sources support

## Job Search Agent

- **related links replaced**: Action Hub, TripMatch Rides Board  
  _Why:_ Removed the link to MBA 290T Syllabus; this is a personal project, not course work.

## MBA 290T Syllabus

- **summary rewritten**: This seven-class course guides students from basic programming concepts to building and evaluating tool-using AI agents.…  
  _Why:_ clearer, source-checked summary
- **fact removed**: Concretely, the course targets Level 2 fluency: you do not need a PhD to reason about AI systems, but knowing how to use ChatGPT is not a differentiator either.  
  _Why:_ duplicate of the Level 2 fluency fact (from the merged Agentic AI note)
- **fact corrected**: In seven sessions we go from “what is a variable” to building and evaluating a tool-using AI agent — covering programming foundations, full-stack software systems, machine learning, deep learning and transformers, LLM behavior and retrieval, and agent architecture. → In seven sessions the course goes from “what is a variable” to building and evaluating a tool-using AI agent, covering programming foundations, full-stack software systems, machine learning, deep learning and transformers, LLM behavior and retrieval, and agent architecture.  
  _Why:_ third person instead of the syllabus's 'we'
- **fact corrected**: Attendance is required and is worth 20% of your grade. → Attendance is required and is worth 20% of the grade.  
  _Why:_ third person
- **fact corrected**: You are expected to use AI coding agents (see the AI policy below); you are also expected to understand and be able to explain everything you submit. → Students are expected to use AI coding agents, and also to understand and be able to explain everything they submit.  
  _Why:_ third person; removed a dangling 'see the AI policy below'
- **fact corrected**: The grading framework includes Deliverable quality, Testing & evaluation, and Working result. → Each assignment is scored on deliverable quality (4 points), testing & evaluation (3) and working result (3).  
  _Why:_ added the point values stated in the same table
- **fact corrected**: Performance will be graded with Attendance at 20%, Assignments 1–4 (lowest score dropped) at 50%, and Assignment 5 at 30%. → The final grade weights attendance 20%, Assignments 1–4 50% (lowest score dropped) and Assignment 5 30%.  
  _Why:_ clearer
- **related links replaced**: UC Berkeley, Ms. Pac-Man DQN, Custom LLM with nanoGPT, Deep Learning  
  _Why:_ each link now states a relationship the sources support

## Ms. Pac-Man DQN

- **summary rewritten**: This project details the implementation of a Deep Q-Network (DQN) agent trained to play Ms. Pac-Man. The agent learned t…  
  _Why:_ clearer, source-checked summary
- **fact removed**: The mean evaluation score before training was 492.0 and after training it was 906.0.  
  _Why:_ duplicate of the headline result
- **fact removed**: The trained agent's moves spread across four directions (29.6 / 28.9 / 19.3 / 12.8%) compared to the untrained baseline's 95.4% UPLEFT.  
  _Why:_ duplicate of the action-mix fact
- **fact removed**: Observations consist of four game screens, shrunk to 84x84 and turned grayscale, stacked together.  
  _Why:_ duplicate of the observation fact
- **fact corrected**: Mean score across five fixed evaluation seeds rose from 492 to 906. → The 492 → 906 means are over five fixed evaluation seeds; four of the five seeds improved and one got worse.  
  _Why:_ turned a duplicate into the detail the same passage adds
- **fact removed**: 95.4% of its moves were a single action — UPLEFT.  
  _Why:_ duplicate of the 95.4% UPLEFT fact
- **fact removed**: The trained agent's moves spread across four directions (29.6 / 28.9 / 19.3 / 12.8%).  
  _Why:_ duplicate of the action-mix fact
- **fact corrected**: I expected a bigger replay buffer to be the single largest available win. → A bigger replay buffer was expected to be the largest available win; in the search the 10× larger buffer (50,000 transitions) was worse at three of the four checkpoints.  
  _Why:_ joined the expectation to its outcome
- **fact corrected**: It is violently non-monotonic. → Improvement was violently non-monotonic: the same configuration scored 454, 906 and 656 at 200, 300 and 400 episodes.  
  _Why:_ the sentence had no subject; numbers from the same passage
- **fact removed**: Loss rose, from 0.040 to 0.110, while the score nearly doubled.  
  _Why:_ duplicate of the update-loss fact
- **fact corrected**: I extracted the notebook's exact training and evaluation logic into a standalone harness and searched — 8 runs, roughly 1.6 million agent decisions. → The settings came from a standalone harness that replicates the notebook's training and evaluation logic: 8 runs, roughly 1.6 million agent decisions.  
  _Why:_ neutral voice
- **fact corrected**: My first full run scored +12, not +414. → The first full run (250 episodes instead of 300) scored +12 over the baseline, not +414.  
  _Why:_ added the context from the same passage
- **fact corrected**: Change one setting: decay exploration from 1.0 to about 0.05 across training, instead of holding it at a constant 0.10. → Proposed next experiment: decay exploration from 1.0 to about 0.05 across training instead of holding it at a constant 0.10.  
  _Why:_ labelled as a proposal
- **fact removed**: The three values in the notebook were not guessed. They came from 8 training runs totalling roughly 1.6 million agent decisions, scored with the notebook's own evaluation protocol.  
  _Why:_ duplicate of the harness fact
- **fact corrected**: The target network sync only every 1,000 decisions. → The target network syncs only every 1,000 decisions.  
  _Why:_ grammar
- **fact corrected**: Apple M2, 8 cores, 16 GB RAM, macOS 26.6.2 arm64, Python 3.12.14, PyTorch 2.14.0. → Training ran on an Apple M2 (8 cores, 16 GB RAM, macOS 26.6.2, Python 3.12.14, PyTorch 2.14.0).  
  _Why:_ the fragment had no verb
- **fact removed**: Every learning rate above 1e-4 was worse, monotonically, at the 60-episode mark.  
  _Why:_ duplicate of the learning-rate fact
- **fact removed**: Exploration of 0.05 produced the worst agent in the whole study (224 at 30 episodes).  
  _Why:_ duplicate of the exploration fact
- **fact removed**: The larger buffer was worse at three of the four checkpoints when comparing 5,000 transitions to 50,000 transitions.  
  _Why:_ merged into the replay-buffer fact
- **fact removed**: Episode count is strongly non-monotonic — 454 → 906 → 656 across 200/300/400 episodes.  
  _Why:_ merged into the non-monotonic fact
- **fact removed**: The untrained network is not random — it is stuck.  
  _Why:_ duplicate of the 95.4% UPLEFT fact
- **related links replaced**: Deep Q-Network, MBA 290T Syllabus, Custom LLM with nanoGPT, UC Berkeley  
  _Why:_ each link now states a relationship the sources support

## Pull-Request Automation

- **related links replaced**: Amazon Web Services, Allowlist Data Access App  
  _Why:_ Removed a link to MBA 290T Syllabus that came from the discarded 'Agentic AI' concept note.

## Seaside Sustainability

- **summary rewritten**: This role involved founding and leading the fundraising function for a beach-cleaning robot. The responsibilities spanne…  
  _Why:_ clearer, source-checked summary
- **fact corrected**: org: Clean-shores.org — Seaside Sustainability → Organisation: Clean-shores.org — Seaside Sustainability.  
  _Why:_ front-matter line rewritten
- **fact corrected**: role: Fundraising Team Lead → Role: Fundraising Team Lead (volunteer).  
  _Why:_ role and 'kind: volunteer' combined
- **fact corrected**: location: Gloucester, MA → Based in Gloucester, MA.  
  _Why:_ front-matter line rewritten
- **fact corrected**: start: Apr 2025 → Dates: Apr 2025 to Jan 2026.  
  _Why:_ start and end combined
- **fact removed**: end: Jan 2026  
  _Why:_ combined into the dates fact
- **fact removed**: kind: volunteer  
  _Why:_ combined into the role fact
- **fact corrected**: summary: Founded and led the fundraising function for a beach-cleaning robot, from concept through launch. → Founded and led the fundraising function for a beach-cleaning robot, from concept through launch.  
  _Why:_ front-matter line rewritten
- **fact corrected**: outcomes: Built and led a 6-person team from nothing → Built and led a 6-person team from nothing.  
  _Why:_ front-matter line rewritten
- **fact corrected**: outcomes: Translated strategic objectives into delivery milestones the team could actually work against → Translated strategic objectives into delivery milestones the team could actually work against.  
  _Why:_ front-matter line rewritten
- **related links replaced**: (none)  
  _Why:_ Gemma linked this volunteer role to Amazon Web Services ('a major technology company') and to the GenAI Adoption Program ('adoption of new technologies'); both reasons are false, so both links were removed. No other note shares a subject with this one.

## Secure Networking Tracker

- **summary rewritten**: The Secure Networking Tracker is a private networking tool designed for users at Berkeley to maintain connections. It en…  
  _Why:_ clearer, source-checked summary
- **fact corrected**: A private networking tracker for the people you want to stay connected with at Berkeley is the Secure Networking Tracker. → A private tracker for the people you want to stay connected with at Berkeley: add who you met, where, what they do, how much to prioritise them and what you talked about, then sort, filter and search.  
  _Why:_ the sentence was inverted
- **fact removed**: The project uses Next.js 16 (App Router) as its framework.  
  _Why:_ duplicate of the stack fact
- **fact removed**: Prerequisites for local setup include Node.js 20+ and a free Neon account.  
  _Why:_ setup detail, not about the subject
- **fact removed**: The Neon Console must have Auth (Managed Better Auth) and the Data API enabled on the project.  
  _Why:_ setup detail, not about the subject
- **fact removed**: The rule is that a row belongs to the user whose JWT created it, and only that user can read or change it.  
  _Why:_ duplicate of the three-mechanisms fact
- **fact removed**: The ownership rule states that a row belongs to whoever's JWT created it, and only that user can read or change it.  
  _Why:_ duplicate of the three-mechanisms fact
- **fact removed**: Layer 1 assigns ownership because the API never sends `user_id`, and the value can only come from the verified token.  
  _Why:_ duplicate of the ownership-assignment fact
- **fact removed**: Layer 2 uses Row Level Security policies to filter every statement for the `authenticated` role.  
  _Why:_ duplicate of the RLS fact
- **fact removed**: Returning 404 instead of 403 when a row is not owned is because RLS makes the row invisible, not forbidden.  
  _Why:_ duplicate of the 404-not-403 fact
- **fact removed**: The Secure Networking Tracker is a private contact tracker where ownership is enforced by Postgres itself, not by the API layer.  
  _Why:_ duplicate of the Postgres-ownership fact
- **fact removed**: The project is a networking tracker for Berkeley contacts where one user's list is unreachable to another even if the API layer were bypassed entirely — because the boundary lives in Postgres, not in application code.  
  _Why:_ duplicate of the Postgres-ownership fact
- **fact removed**: The interesting part of the tracker is where the ownership boundary sits, as every contact belongs to exactly one account, and Postgres enforces that below the application through Row Level Security.  
  _Why:_ duplicate of the Postgres-ownership fact
- **fact removed**: RLS filters every statement using four policies for authenticated users covering select, insert, update and delete.  
  _Why:_ duplicate of the RLS fact (which also says RLS is forced)
- **fact corrected**: One thing that could be done differently is implementing keyset pagination instead of loading every matching row. → A stated next step: the list loads every matching row, so at a few thousand contacts it needs keyset pagination.  
  _Why:_ added why, from the same passage
- **related links replaced**: UC Berkeley, Allowlist Data Access App, TripMatch Rides Board  
  _Why:_ Removed Gemma's link to Ms. Pac-Man DQN ('both train an agent using a Deep Q-Network'), which is false.

## TikTok Internship

- **summary rewritten**: This role involved working as an Ads Risk Integrity Intern at TikTok in Beijing, China. The responsibilities focused on …  
  _Why:_ clearer, source-checked summary
- **fact removed**: org: TikTok  
  _Why:_ redundant with the note title
- **fact corrected**: role: Ads Risk Integrity Intern → Role: Ads Risk Integrity Intern.  
  _Why:_ front-matter line rewritten
- **fact corrected**: location: Beijing, China → Based in Beijing, China.  
  _Why:_ front-matter line rewritten
- **fact corrected**: start: May 2021 → Dates: May 2021 to Aug 2021.  
  _Why:_ start and end combined
- **fact removed**: end: Aug 2021  
  _Why:_ combined into the dates fact
- **fact removed**: kind: work  
  _Why:_ adds nothing
- **fact corrected**: summary: Ad moderation and risk analysis, working across Data Science, Engineering and Policy. → Worked on ad moderation and risk analysis across Data Science, Engineering and Policy.  
  _Why:_ front-matter line rewritten
- **fact corrected**: outcomes: Drove a 35% reduction in high-risk ad exposure by analysing flagged ads and presenting risk patterns to weekly cross-functional reviews → Drove a 35% reduction in high-risk ad exposure by analysing flagged ads and presenting risk patterns to weekly cross-functional reviews.  
  _Why:_ front-matter line rewritten
- **fact corrected**: outcomes: Cut unidentified-language ad violations by 95% by partnering with R&D to add 15+ minority-language models and a phrase glossary to the moderation system → Cut unidentified-language ad violations by 95% by partnering with R&D to add 15+ minority-language models and a phrase glossary to the moderation system.  
  _Why:_ front-matter line rewritten
- **related links replaced**: IDG Capital, Amazon Web Services  
  _Why:_ each link now states a relationship the sources support

## Time Series Analysis

- **summary rewritten**: Time Series Analysis involves analyzing data points collected over time, often requiring significant preprocessing to en…  
  _Why:_ clearer, source-checked summary
- **fact corrected**: The variable that wasn't in the data required manual repair because two race times came back in a format inconsistent with the rest, and missing driver and team standings were filled by checking source pages by hand. → The Formula 1 scrape was not clean: two race times came back in a format inconsistent with the rest and had to be repaired, and a missing driver standing and a missing team standing were filled by checking the source pages by hand.  
  _Why:_ Gemma used a section title as the subject and pluralised the missing standings; the source names one of each
- **fact corrected**: The analysis used thirty-two data points, which was considered a thin time series, and the author chose this deliberately because a small valid comparison beats a large invalid one. → Holding the circuit constant left thirty-two data points, a thin time series, chosen deliberately because a small valid comparison beats a large invalid one.  
  _Why:_ clearer subject
- **fact corrected**: The project involved scraping thirty-two seasons from Formula 1's results pages, spanning 1991–2022, and the hardest part was making any two numbers comparable. → The Formula 1 project scraped thirty-two seasons (1991–2022) of results pages; the hard part was making any two numbers comparable.  
  _Why:_ named the project
- **fact corrected**: The quartic exponential model was the one that came out lowest when compared on root mean squared error. → The quartic exponential model had the lowest root mean squared error, but it is the result the author trusts least, because the exponential transform changes the scale on which residuals are measured.  
  _Why:_ added the caveat the same passage gives, so the fact is not misleading
- **fact corrected**: Pipeline creation was forecasted using a least-squares linear trend fitted only on the six months where the category was genuinely active, and then projected forward by region. → In the GenAI target-setting model, pipeline creation was forecast with a least-squares linear trend fitted only on the six months where the category was genuinely active, then projected forward by region.  
  _Why:_ named the project
- **related links replaced**: Formula 1 Racing Trends, GenAI Target Setting  
  _Why:_ each link now states a relationship the sources support

## TripMatch Rides Board

- **summary rewritten**: TripMatch was a verified, Berkeley-only rides board designed to solve the problem of unstructured ride coordination in g…  
  _Why:_ clearer, source-checked summary
- **related links replaced**: UC Berkeley, Secure Networking Tracker, Job Search Agent  
  _Why:_ each link now states a relationship the sources support

## UC Berkeley

- **summary rewritten**: This entry details a concurrent MBA and M.Eng. program at UC Berkeley's Haas School of Business & IEOR. The program is d…  
  _Why:_ clearer, source-checked summary
- **fact corrected**: org: UC Berkeley — Haas School of Business & IEOR → School: UC Berkeley — Haas School of Business & IEOR.  
  _Why:_ front-matter line rewritten
- **fact corrected**: role: MBA / M.Eng., Industrial Engineering & Operations Research → Degrees: MBA / M.Eng., Industrial Engineering & Operations Research.  
  _Why:_ front-matter line rewritten
- **fact corrected**: location: Berkeley, CA → Located in Berkeley, CA.  
  _Why:_ front-matter line rewritten
- **fact corrected**: start: Aug 2026 → Dates: Aug 2026 to an expected May 2028.  
  _Why:_ start and end combined
- **fact removed**: end: Expected May 2028  
  _Why:_ combined into the dates fact
- **fact removed**: kind: education  
  _Why:_ adds nothing
- **fact corrected**: summary: A concurrent MBA and M.Eng., taken together so the product judgment and the engineering are learned in the same place rather than sequentially. → The two degrees are taken together so the product judgment and the engineering are learned in the same place rather than sequentially.  
  _Why:_ front-matter line rewritten
- **related links replaced**: MBA 290T Syllabus, Ms. Pac-Man DQN, Secure Networking Tracker, TripMatch Rides Board  
  _Why:_ each link now states a relationship the sources support

## University of Notre Dame

- **summary rewritten**: This entry details the educational experience at the University of Notre Dame's Mendoza College of Business. The individ…  
  _Why:_ clearer, source-checked summary
- **fact corrected**: The role was B.B.A. Business Analytics · B.S. Applied Mathematics. → Degrees: B.B.A. Business Analytics and B.S. Applied Mathematics.  
  _Why:_ reworded
- **fact corrected**: The location was Notre Dame, IN. → Located in Notre Dame, IN.  
  _Why:_ reworded
- **fact corrected**: The start date was Aug 2019. → Dates: Aug 2019 to May 2023.  
  _Why:_ start and end combined
- **fact removed**: The end date was May 2023.  
  _Why:_ combined into the dates fact
- **fact corrected**: The summary was a double major in business analytics and applied mathematics — the quantitative methods on one side, the business framing for them on the other. → A double major in business analytics and applied mathematics: the quantitative methods on one side, the business framing for them on the other.  
  _Why:_ reworded
- **fact corrected**: The outcomes included winning Best Insight against a field of 10–15 competing teams. → Won Best Insight, against a field of 10–15 competing teams.  
  _Why:_ reworded
- **related links replaced**: DataFest 2023, Formula 1 Racing Trends, Hazardous Asteroid Screening  
  _Why:_ each link now states a relationship the sources support

## Review pass 2026-09-28 15:11

Notes reviewed in this pass: Kickstarter Scraper. Reviewer: Claude (Anthropic), for Eason Han; each fact checked against the cited passage.

### Kickstarter Scraper

- **summary rewritten**: This project addressed the issue where a standard web scraper returned empty results for Kickstarter pages because the c…  
  _Why:_ clearer, source-checked summary
- **fact corrected**: The tool the course taught returns an empty result on this page — and not an error. → On Kickstarter, the tool the course taught (rvest) returned an empty result for the most valuable field, and not an error.  
  _Why:_ named the tool and what came back empty
- **fact corrected**: The project is really about why that happens, and what you do instead: let a real browser execute the page, capture the document it builds, and parse that. → The project is about why that happens and what to do instead: let a real browser execute the page, capture the document it builds, and parse that.  
  _Why:_ neutral voice
- **fact corrected**: Kickstarter's don't. The campaign body — the part carrying the actual pitch — sits under #react-campaign. → Unlike pages that arrive complete, Kickstarter's campaign body (the actual pitch) sits under #react-campaign and is assembled by JavaScript in the visitor's browser after the page loads.  
  _Why:_ the fragment 'Kickstarter's don't.' made no sense without the previous paragraph
- **fact corrected**: html_elements() on a selector matching nothing does not raise. → The failure is silent: html_elements() on a selector that matches nothing does not raise, and html_text() on the empty result returns character(0), so the script exits cleanly and prints nothing.  
  _Why:_ joined two fragments into the point the passage makes
- **fact removed**: html_text() on a zero-length node set returns character(0).  
  _Why:_ merged into the previous fact
- **fact corrected**: Stage one is a real browser. → Stage one: Selenium drives Safari's WebDriver to the project URL, lets the page finish assembling itself, and writes the body's innerHTML to a local file.  
  _Why:_ the fragment had no content
- **fact corrected**: Stage two is the rvest script that was always going to work, pointed at the file on disk instead of at the URL. → Stage two: the unchanged rvest script parses the file on disk instead of the URL, with six selectors for title, pledged amount, pledge goal, backers, location and description.  
  _Why:_ added what it extracts, from the same passage
- **fact corrected**: With the document already on disk, iteration costs nothing and the site sees a single visit. → Splitting fetch from parse means iterating on the selectors costs nothing and the site sees a single visit.  
  _Why:_ added the subject
- **fact corrected**: rvest offers html_text() and html_text2(). → Backers, location and the description use html_text2(), which approximates the rendered text; html_text() returns raw text nodes, layout whitespace and all.  
  _Why:_ the fragment stated no finding
- **fact corrected**: What transfers here is not a library. → The transferable lesson is a question to ask before writing any selector: does the content exist in the server's response, or is it assembled in the browser?  
  _Why:_ the fragment stated no finding
- **fact corrected**: View-source and inspect-element disagree exactly when the answer is assembled. → View-source and inspect-element disagree exactly when the content is assembled: view-source shows what the server sent, the inspector shows what the browser built.  
  _Why:_ completed from the same passage
- **related links replaced**: University of Notre Dame, Formula 1 Racing Trends  
  _Why:_ Removed Gemma's link to MBA 290T Syllabus ('completed as part of MBA 290T'): the source says ITAO 40450 at Notre Dame. A link to the re-created 'Agentic AI' note was removed by the merge (fix 10).

### Formula 1 Racing Trends (already reviewed)

- **related link added**: [[Kickstarter Scraper]] — Same course (ITAO 40450): a browser-snapshot scrape done three days before this one.

### University of Notre Dame (already reviewed)

- **related link added**: [[Kickstarter Scraper]] — An individual extra-credit project for ITAO 40450 (Spring 2023); listed as related work on this entry.

