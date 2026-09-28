"""The manual review pass, written down as explicit edits so every change is visible and repeatable.

Each generated note was read against the original passages it cites (scripts/review_notes.py prints them
side by side). Corrections go into the wiki note, never into vault/raw. Every edit below carries the
reason it was made, and running this script appends them to evidence/wiki_review.md and marks the note
`reviewed: true` (which also admits it to the retrieval index).

    python scripts/apply_review.py
"""

from __future__ import annotations

import re
import sys
from datetime import datetime

from wiki import config, vault

REVIEWER = "Claude (Anthropic), for Eason Han; each fact checked against the cited passage"
FACT_LINE = re.compile(r"^- (?P<fact>.*?) (?P<ref>\(\[\[raw/[^\]]+\]\]\))$")

# (substring identifying the fact, replacement text or None to delete, reason)
AWS_REASON = "Built in this role at AWS (listed as related work on the website's AWS entry)."
EDITS: dict[str, dict] = {
    "Deep Q-Network": {
        "summary": "A Deep Q-Network (DQN) is a reinforcement-learning method in which a neural network estimates how much "
                   "future reward each possible action is worth, and the agent takes the highest-valued move. In these sources "
                   "it is the algorithm behind the Ms. Pac-Man agent: a convolutional network reads stacked game screens and a "
                   "slower-moving target network supplies the learning target.",
        "facts": [
            ("The exploration rate was set to 0.10", None, "project result, not part of the method; kept in Ms. Pac-Man DQN"),
            ("The training ran for 300 episodes", None, "project result, not part of the method; kept in Ms. Pac-Man DQN"),
            ("The learning rate was set to 0.0001", None, "project result, not part of the method; kept in Ms. Pac-Man DQN"),
            ("The headline result showed", None, "project result, not part of the method; kept in Ms. Pac-Man DQN"),
        ],
        "related": [("Ms. Pac-Man DQN", "The project that applies this method, with its chosen settings and results."),
                    ("Deep Learning", "The Q-network is a convolutional neural network trained on the game screens.")],
    },
    "Deep Learning": {
        "summary": "Deep learning trains layered networks of weights with non-linearities by gradient descent: a loss scores each "
                   "prediction and the gradient says which way to move every parameter. In these sources it is shown concretely "
                   "in the custom nanoGPT project, from turning text into token IDs and embeddings to a single measured weight update.",
        "facts": [
            ("The parameters are arranged in layers",
             "In the project's nanoGPT, the parameters are arranged in layers: an embedding table, two transformer blocks (each "
             "with 4 attention heads and a small MLP), and an output layer mapping 64 dimensions back to vocabulary scores.",
             "added which model this describes"),
            ("The learning rate is set to 1e-05 at step 0",
             "The learning rate at step 0 is 1e-05, not 0.001, because step 0 is the first step of a 100-step warmup "
             "(0.001 × 1/100).", "reworded to match the source exactly"),
        ],
        "related": [("Custom LLM with nanoGPT", "The project these facts come from: a small nanoGPT language model built for MBA 290T."),
                    ("Deep Q-Network", "Another neural-network method in this wiki; there the network estimates action values, not next tokens."),
                    ("MBA 290T Syllabus", "Class 4 of the course covers deep learning and transformers.")],
    },
    "Time Series Analysis": {
        "summary": "Time-series analysis models how a measurement changes over time; in these sources most of the work is making "
                   "the points in a series comparable before any model is fitted. It appears in two projects: a 32-season trend "
                   "in Formula 1 race speeds, and a linear-trend forecast of pipeline creation used to set AWS Sales' first "
                   "Generative AI target.",
        "facts": [
            ("The variable that wasn't in the data required manual repair",
             "The Formula 1 scrape was not clean: two race times came back in a format inconsistent with the rest and had to be "
             "repaired, and a missing driver standing and a missing team standing were filled by checking the source pages by hand.",
             "Gemma used a section title as the subject and pluralised the missing standings; the source names one of each"),
            ("The analysis used thirty-two data points",
             "Holding the circuit constant left thirty-two data points, a thin time series, chosen deliberately because a small "
             "valid comparison beats a large invalid one.", "clearer subject"),
            ("The project involved scraping thirty-two seasons",
             "The Formula 1 project scraped thirty-two seasons (1991–2022) of results pages; the hard part was making any two "
             "numbers comparable.", "named the project"),
            ("The quartic exponential model was the one that came out lowest",
             "The quartic exponential model had the lowest root mean squared error, but it is the result the author trusts least, "
             "because the exponential transform changes the scale on which residuals are measured.",
             "added the caveat the same passage gives, so the fact is not misleading"),
            ("Pipeline creation was forecasted",
             "In the GenAI target-setting model, pipeline creation was forecast with a least-squares linear trend fitted only on "
             "the six months where the category was genuinely active, then projected forward by region.", "named the project"),
        ],
        "related": [("Formula 1 Racing Trends", "Fits six trend models to a 32-point speed series after holding the circuit constant."),
                    ("GenAI Target Setting", "Forecasts a leading indicator (pipeline creation) with a linear trend because the target had no history.")],
    },
    "MBA 290T Syllabus": {
        "summary": "MBA 290T: Fundamental of Agentic AI (Haas School of Business, UC Berkeley, Fall 2026) is a seven-class course "
                   "that goes from programming foundations to building and evaluating tool-using AI agents. It is graded on "
                   "attendance (20%) and five assignments, and it expects students to use AI coding agents while being able to "
                   "explain everything they submit.",
        "facts": [
            ("Concretely, the course targets Level 2 fluency", None, "duplicate of the Level 2 fluency fact (from the merged Agentic AI note)"),
            ("In seven sessions we go from",
             "In seven sessions the course goes from “what is a variable” to building and evaluating a tool-using AI agent, "
             "covering programming foundations, full-stack software systems, machine learning, deep learning and transformers, "
             "LLM behavior and retrieval, and agent architecture.", "third person instead of the syllabus's 'we'"),
            ("Attendance is required and is worth 20% of your grade.",
             "Attendance is required and is worth 20% of the grade.", "third person"),
            ("You are expected to use AI coding agents",
             "Students are expected to use AI coding agents, and also to understand and be able to explain everything they submit.",
             "third person; removed a dangling 'see the AI policy below'"),
            ("The grading framework includes Deliverable quality",
             "Each assignment is scored on deliverable quality (4 points), testing & evaluation (3) and working result (3).",
             "added the point values stated in the same table"),
            ("Performance will be graded with Attendance at 20%",
             "The final grade weights attendance 20%, Assignments 1–4 50% (lowest score dropped) and Assignment 5 30%.", "clearer"),
        ],
        "related": [("UC Berkeley", "A course in the Haas program (Fall 2026)."),
                    ("Ms. Pac-Man DQN", "Built for this course; its README calls it the Class 3 assignment."),
                    ("Custom LLM with nanoGPT", "Built for this course (repository mba290t-custom-llm)."),
                    ("Deep Learning", "Class 4 covers deep learning and transformers.")],
    },
    "Amazon Web Services": {
        "summary": "Business Intelligence Engineer in Global Sales Strategy & Analytics at Amazon Web Services, Seattle, from Jul 2023 "
                   "to May 2026. The role built internal products for 10,000+ sellers across an $80B business, turning a reporting "
                   "function that produced reports into one that produced decisions.",
        "facts": [
            ("org: Amazon Web Services", None, "redundant with the note title"),
            ("role: Business Intelligence Engineer", "Job title: Business Intelligence Engineer — Global Sales Strategy & Analytics.", "raw front-matter line rewritten as a sentence"),
            ("location: Seattle, WA", "Based in Seattle, WA.", "front-matter line rewritten as a sentence"),
            ("start: Jul 2023", "Dates: Jul 2023 to May 2026.", "start and end combined"),
            ("end: May 2026", None, "combined into the dates fact"),
            ("summary: Internal products", "Built internal products for 10,000+ sellers across an $80B business; three years spent turning a "
             "reporting function that produced reports into one that produced decisions.", "front-matter line rewritten as a sentence"),
            ("outcomes: Raised on-time delivery", "Raised on-time delivery of business stakeholder requests from 56% to 82% by establishing "
             "recurring roadmap reviews that published the backlog.", "front-matter line rewritten as a sentence"),
            ("outcomes: Launched a Business-Influence Tracker", "Launched a Business-Influence Tracker that lifted customer opportunity "
             "coverage 12% and became a standing Monthly Business Review KPI.", "front-matter line rewritten as a sentence"),
        ],
        "related": [("Action Hub", "The seller-facing alert screen built in this role."),
                    ("Pull-Request Automation", "An OpenClaw skill built in this role to automate the steps before code review."),
                    ("GenAI Target Setting", "The first Generative AI target model for AWS Sales, built in this role."),
                    ("Allowlist Data Access App", "The data-access exceptions app built in this role."),
                    ("GenAI Adoption Program", "The LATAM GenAI adoption programme run in this role.")],
    },
    "IDG Capital": {
        "summary": "Venture Capital Analyst Intern at IDG Capital in Beijing from Jun 2020 to Aug 2020, doing diligence on early-stage "
                   "SaaS and food-supply companies.",
        "facts": [
            ("org: IDG Capital", None, "redundant with the note title"),
            ("role: Venture Capital Analyst Intern", "Role: Venture Capital Analyst Intern.", "front-matter line rewritten"),
            ("location: Beijing, China", "Based in Beijing, China.", "front-matter line rewritten"),
            ("start: Jun 2020", "Dates: Jun 2020 to Aug 2020.", "start and end combined"),
            ("end: Aug 2020", None, "combined into the dates fact"),
            ("summary: Diligence", "Did diligence on early-stage SaaS and food-supply companies.", "front-matter line rewritten"),
            ("outcomes: Evaluated 20+ startups", "Evaluated 20+ startups on market position, product differentiation and operations, "
             "building a sector database that benchmarked new companies against it.", "front-matter line rewritten"),
            ("outcomes: Informed 3 investment decisions", "Informed 3 investment decisions by pressure-testing each growth story against "
             "executive interviews, industry-expert calls and IPO filings.", "front-matter line rewritten"),
        ],
        "related": [("TikTok Internship", "The other internship in Beijing, a year later (2021).")],
    },
    "Seaside Sustainability": {
        "summary": "Fundraising Team Lead, a volunteer role, for Seaside Sustainability (clean-shores.org) in Gloucester, MA, from "
                   "Apr 2025 to Jan 2026: founded and led the fundraising function for a beach-cleaning robot, from concept through launch.",
        "facts": [
            ("org: Clean-shores.org", "Organisation: Clean-shores.org — Seaside Sustainability.", "front-matter line rewritten"),
            ("role: Fundraising Team Lead", "Role: Fundraising Team Lead (volunteer).", "role and 'kind: volunteer' combined"),
            ("location: Gloucester, MA", "Based in Gloucester, MA.", "front-matter line rewritten"),
            ("start: Apr 2025", "Dates: Apr 2025 to Jan 2026.", "start and end combined"),
            ("end: Jan 2026", None, "combined into the dates fact"),
            ("kind: volunteer", None, "combined into the role fact"),
            ("summary: Founded and led", "Founded and led the fundraising function for a beach-cleaning robot, from concept through launch.",
             "front-matter line rewritten"),
            ("outcomes: Built and led a 6-person team", "Built and led a 6-person team from nothing.", "front-matter line rewritten"),
            ("outcomes: Translated strategic objectives", "Translated strategic objectives into delivery milestones the team could "
             "actually work against.", "front-matter line rewritten"),
        ],
        "related": [],
        "related_note": "Gemma linked this volunteer role to Amazon Web Services ('a major technology company') and to the GenAI "
                        "Adoption Program ('adoption of new technologies'); both reasons are false, so both links were removed. "
                        "No other note shares a subject with this one.",
    },
    "TikTok Internship": {
        "summary": "Ads Risk Integrity Intern at TikTok in Beijing from May 2021 to Aug 2021, working on ad moderation and risk "
                   "analysis across Data Science, Engineering and Policy.",
        "facts": [
            ("org: TikTok", None, "redundant with the note title"),
            ("role: Ads Risk Integrity Intern", "Role: Ads Risk Integrity Intern.", "front-matter line rewritten"),
            ("location: Beijing, China", "Based in Beijing, China.", "front-matter line rewritten"),
            ("start: May 2021", "Dates: May 2021 to Aug 2021.", "start and end combined"),
            ("end: Aug 2021", None, "combined into the dates fact"),
            ("kind: work", None, "adds nothing"),
            ("summary: Ad moderation", "Worked on ad moderation and risk analysis across Data Science, Engineering and Policy.",
             "front-matter line rewritten"),
            ("outcomes: Drove a 35% reduction", "Drove a 35% reduction in high-risk ad exposure by analysing flagged ads and presenting "
             "risk patterns to weekly cross-functional reviews.", "front-matter line rewritten"),
            ("outcomes: Cut unidentified-language ad violations", "Cut unidentified-language ad violations by 95% by partnering with "
             "R&D to add 15+ minority-language models and a phrase glossary to the moderation system.", "front-matter line rewritten"),
        ],
        "related": [("IDG Capital", "The earlier internship in Beijing (2020)."),
                    ("Amazon Web Services", "The next industry role, full-time from Jul 2023.")],
    },
    "UC Berkeley": {
        "summary": "A concurrent MBA and M.Eng. in Industrial Engineering & Operations Research at UC Berkeley (Haas School of "
                   "Business and IEOR), from Aug 2026 to an expected May 2028, taken together so that product judgment and "
                   "engineering are learned in the same place.",
        "facts": [
            ("org: UC Berkeley", "School: UC Berkeley — Haas School of Business & IEOR.", "front-matter line rewritten"),
            ("role: MBA / M.Eng.", "Degrees: MBA / M.Eng., Industrial Engineering & Operations Research.", "front-matter line rewritten"),
            ("location: Berkeley, CA", "Located in Berkeley, CA.", "front-matter line rewritten"),
            ("start: Aug 2026", "Dates: Aug 2026 to an expected May 2028.", "start and end combined"),
            ("end: Expected May 2028", None, "combined into the dates fact"),
            ("kind: education", None, "adds nothing"),
            ("summary: A concurrent MBA", "The two degrees are taken together so the product judgment and the engineering are learned "
             "in the same place rather than sequentially.", "front-matter line rewritten"),
        ],
        "related": [("MBA 290T Syllabus", "A course in this program (Haas, Fall 2026)."),
                    ("Ms. Pac-Man DQN", "An MBA 290T project built here (Sep 2026); listed as related work on this entry."),
                    ("Secure Networking Tracker", "Built at UC Berkeley (Sep 2026) for Berkeley contacts; listed as related work on this entry."),
                    ("TripMatch Rides Board", "A rides board for the Haas class (Aug 2026); listed as related work on this entry.")],
    },
    "University of Notre Dame": {
        "summary": "B.B.A. in Business Analytics and B.S. in Applied Mathematics at the University of Notre Dame's Mendoza College of "
                   "Business, Aug 2019 to May 2023: the quantitative methods on one side, the business framing for them on the other.",
        "facts": [
            ("The role was B.B.A.", "Degrees: B.B.A. Business Analytics and B.S. Applied Mathematics.", "reworded"),
            ("The location was Notre Dame, IN.", "Located in Notre Dame, IN.", "reworded"),
            ("The start date was Aug 2019.", "Dates: Aug 2019 to May 2023.", "start and end combined"),
            ("The end date was May 2023.", None, "combined into the dates fact"),
            ("The summary was a double major", "A double major in business analytics and applied mathematics: the quantitative methods "
             "on one side, the business framing for them on the other.", "reworded"),
            ("The outcomes included winning Best Insight", "Won Best Insight, against a field of 10–15 competing teams.", "reworded"),
        ],
        "related": [("DataFest 2023", "A 48-hour data competition led as team lead (2023); listed as related work on this entry."),
                    ("Formula 1 Racing Trends", "An individual project for ITAO 40450 at the Mendoza College of Business (Spring 2023)."),
                    ("Hazardous Asteroid Screening", "A project for ITAO 40420 (Spring 2022); listed as related work on this entry.")],
    },
    "Action Hub": {
        "facts": [
            ("I ran 20 user interviews", "20 user interviews across segments were run before writing requirements; the build was then "
             "scoped from a PRD and Figma prototypes.", "neutral voice"),
            ("Anything that changed only what a seller", "When scope had to be cut, requests that changed only what a seller knew went "
             "below the line.", "added the context of the passage (scope cuts against a fixed launch date)"),
            ("I under-invested in instrumenting", "A stated lesson: instrumenting the 'action taken' step was under-invested.", "neutral voice"),
        ],
        "related": [("Amazon Web Services", "Built in this role at AWS Global Sales Strategy & Analytics."),
                    ("Allowlist Data Access App", "Both scope what each seller may see through the territory and account assignments."),
                    ("Job Search Agent", "Both rank a long list and cap it on purpose: fifty alerts per seller here, two roles per company there.")],
    },
    "Allowlist Data Access App": {
        "related": [("Amazon Web Services", AWS_REASON),
                    ("Action Hub", "Both scope what each seller may see through the territory and account assignments."),
                    ("Secure Networking Tracker", "The same question, who may see which records, answered with database policies instead "
                     "of a logged exception register.")],
    },
    "Custom LLM with nanoGPT": {
        "summary": "Building a Custom LLM was an MBA 290T assignment: a small nanoGPT (2 blocks, 4 heads, 64-number embeddings, "
                   "48-token context) trained on a classroom corpus and on extended corpora, then scored on a fixed 48-case language "
                   "eval suite. The delivered model D reached 40/48 on that suite and 12/16 on a held-out suite written after the "
                   "corpus was frozen.",
        "facts": [
            ("nanoGPT has 2 blocks", "The model is a nanoGPT with 2 blocks, 4 heads, 64-number embeddings and a 48-token context.",
             "the configuration belongs to this project's model, not to nanoGPT in general"),
            ("Reproduce experiment A can be done", "Experiment A is reproduced with `python tools/run_experiment.py --experiment starter`.", "grammar"),
            ("Reproduce experiment D requires", "Experiment D is reproduced with `python tools/run_experiment.py --experiment tuned "
             "--corpus-dir corpus_seven --lr 0.004`.", "grammar"),
            ("The choice of corpus was classroom", "The corpora compared were the classroom corpus alone, plus a 4-category extension, "
             "plus a 7-category extension, and the 7-category extension with unpaired relations; the assignment required the first two.",
             "Gemma flattened a table row into an unreadable sentence"),
            ("The delivered model D has seven taught categories", None, "duplicate of the model D definition fact"),
        ],
        "related": [("MBA 290T Syllabus", "Built for this course (repository mba290t-custom-llm)."),
                    ("Deep Learning", "The concepts this project demonstrates: embeddings, attention, loss and gradient steps."),
                    ("Ms. Pac-Man DQN", "The other MBA 290T model-training assignment; both tune a learning rate against a fixed evaluation."),
                    ("Hazardous Asteroid Screening", "Both confront leakage: here the corpus was audited for eval leakage; there NASA's "
                     "definition sat in two input columns.")],
    },
    "DataFest 2023": {
        "related": [("University of Notre Dame", "Done at Notre Dame (2023) as team lead; listed as related work on the Notre Dame entry."),
                    ("Formula 1 Racing Trends", "Another Notre Dame analytics project from 2023.")],
    },
    "Formula 1 Racing Trends": {
        "related": [("University of Notre Dame", "An individual project for ITAO 40450 at the Mendoza College of Business (Spring 2023)."),
                    ("Time Series Analysis", "The concept note on its trend models and the comparability work behind them."),
                    ("DataFest 2023", "Another Notre Dame analytics project from 2023.")],
        "related_note": "Removed Gemma's link to Ms. Pac-Man DQN ('both use a Deep Q-Network'), which is false.",
    },
    "GenAI Adoption Program": {
        "facts": [("Over 75% of 1,100 sellers did participate", "More than 75% of the 1,100 sellers participated within 60 days.", "grammar")],
        "related": [("Amazon Web Services", "Run in this role at AWS (2024)."),
                    ("Action Hub", "Another AWS Sales product from the same role, aimed at what sellers do each day.")],
        "related_note": "Removed a link to Job Search Agent ('both build an automated agent to scan and rank'), which is false for "
                        "this programme.",
    },
    "GenAI Target Setting": {
        "related": [("Amazon Web Services", "Built in this role at AWS (2024)."),
                    ("Time Series Analysis", "Its forecast is a least-squares linear trend on six months of pipeline history.")],
        "related_note": "Removed the link to GenAI Adoption Program: one sets a sales target for GenAI business, the other drove "
                        "sellers' own use of GenAI tools; Gemma's reason conflated the two.",
    },
    "Hazardous Asteroid Screening": {
        "facts": [
            ("Four models, evaluated on a 30% holdout", "Four models were evaluated on a 30% holdout: logistic regression, a bagged "
             "random forest, XGBoost, and tuned XGBoost.", "Gemma split the model names in the table into a garbled list"),
            ("The raw data was 4,687 asteroid records", "The raw data was 4,687 asteroid records across 40 variables, of which seventeen "
             "survived as predictors.", "merged with the next fact, which had no subject"),
            ("Seventeen survived as predictors.", None, "merged into the previous fact"),
        ],
        "related": [("University of Notre Dame", "A project for ITAO 40420 (Spring 2022); listed as related work on the Notre Dame entry."),
                    ("Custom LLM with nanoGPT", "Both confront leakage: here NASA's definition sat in two input columns; there the "
                     "training corpus was audited for eval leakage.")],
    },
    "Job Search Agent": {
        "related": [("Action Hub", "Both rank a long list and cap it on purpose: two roles per company here, fifty alerts per seller there."),
                    ("TripMatch Rides Board", "Another independent project from Aug–Sep 2026, built end to end alone.")],
        "related_note": "Removed the link to MBA 290T Syllabus; this is a personal project, not course work.",
    },
    "Ms. Pac-Man DQN": {
        "summary": "Ms. Pac-Man DQN was the MBA 290T Class 3 assignment: a Deep Q-Network trained to play Ms. Pac-Man, with "
                   "exploration 0.10, 300 episodes and learning rate 0.0001 chosen by a measured search. Its mean evaluation score "
                   "rose from 492 to 906 (+84%), but the untrained baseline was stuck repeating one move 95.4% of the time, so the "
                   "headline number flatters the result.",
        "facts": [
            ("The mean evaluation score before training was 492.0", None, "duplicate of the headline result"),
            ("The trained agent's moves spread across four directions (29.6 / 28.9 / 19.3 / 12.8%) compared", None, "duplicate of the action-mix fact"),
            ("Observations consist of four game screens", None, "duplicate of the observation fact"),
            ("Mean score across five fixed evaluation seeds rose from 492 to 906.",
             "The 492 → 906 means are over five fixed evaluation seeds; four of the five seeds improved and one got worse.",
             "turned a duplicate into the detail the same passage adds"),
            ("95.4% of its moves were a single action", None, "duplicate of the 95.4% UPLEFT fact"),
            ("The trained agent's moves spread across four directions (29.6 / 28.9 / 19.3 / 12.8%).", None, "duplicate of the action-mix fact"),
            ("I expected a bigger replay buffer", "A bigger replay buffer was expected to be the largest available win; in the search the "
             "10× larger buffer (50,000 transitions) was worse at three of the four checkpoints.", "joined the expectation to its outcome"),
            ("It is violently non-monotonic.", "Improvement was violently non-monotonic: the same configuration scored 454, 906 and 656 at "
             "200, 300 and 400 episodes.", "the sentence had no subject; numbers from the same passage"),
            ("Loss rose, from 0.040 to 0.110", None, "duplicate of the update-loss fact"),
            ("I extracted the notebook's exact training", "The settings came from a standalone harness that replicates the notebook's "
             "training and evaluation logic: 8 runs, roughly 1.6 million agent decisions.", "neutral voice"),
            ("My first full run scored +12", "The first full run (250 episodes instead of 300) scored +12 over the baseline, not +414.",
             "added the context from the same passage"),
            ("Change one setting: decay exploration", "Proposed next experiment: decay exploration from 1.0 to about 0.05 across training "
             "instead of holding it at a constant 0.10.", "labelled as a proposal"),
            ("The three values in the notebook were not guessed", None, "duplicate of the harness fact"),
            ("The target network sync only every 1,000 decisions.", "The target network syncs only every 1,000 decisions.", "grammar"),
            ("Apple M2, 8 cores", "Training ran on an Apple M2 (8 cores, 16 GB RAM, macOS 26.6.2, Python 3.12.14, PyTorch 2.14.0).",
             "the fragment had no verb"),
            ("Every learning rate above 1e-4 was worse", None, "duplicate of the learning-rate fact"),
            ("Exploration of 0.05 produced the worst agent", None, "duplicate of the exploration fact"),
            ("The larger buffer was worse at three of the four checkpoints", None, "merged into the replay-buffer fact"),
            ("Episode count is strongly non-monotonic", None, "merged into the non-monotonic fact"),
            ("The untrained network is not random — it is stuck.", None, "duplicate of the 95.4% UPLEFT fact"),
        ],
        "related": [("Deep Q-Network", "The algorithm the agent uses."),
                    ("MBA 290T Syllabus", "Built for this course; the README calls it the Class 3 assignment."),
                    ("Custom LLM with nanoGPT", "The other MBA 290T model-training assignment; both tune a learning rate against a fixed evaluation."),
                    ("UC Berkeley", "Built at UC Berkeley (Sep 2026).")],
    },
    "Pull-Request Automation": {
        "related": [("Amazon Web Services", "Built in this role on Amazon's internal OpenClaw platform."),
                    ("Allowlist Data Access App", "Another internal tool from the same AWS role.")],
        "related_note": "Removed a link to MBA 290T Syllabus that came from the discarded 'Agentic AI' concept note.",
    },
    "Secure Networking Tracker": {
        "summary": "Secure Networking Tracker is a private contact tracker for the people met at Berkeley, built at UC Berkeley (Sep 2026) "
                   "with Next.js 16, Neon Postgres, Better Auth and Vercel. Every contact belongs to exactly one account, and three "
                   "independent mechanisms enforce that ownership, with Postgres Row Level Security as the real boundary.",
        "facts": [
            ("A private networking tracker for the people you want to stay connected with",
             "A private tracker for the people you want to stay connected with at Berkeley: add who you met, where, what they do, "
             "how much to prioritise them and what you talked about, then sort, filter and search.", "the sentence was inverted"),
            ("The project uses Next.js 16 (App Router)", None, "duplicate of the stack fact"),
            ("Prerequisites for local setup include", None, "setup detail, not about the subject"),
            ("The Neon Console must have Auth", None, "setup detail, not about the subject"),
            ("The rule is that a row belongs to the user whose JWT created it", None, "duplicate of the three-mechanisms fact"),
            ("The ownership rule states that a row belongs", None, "duplicate of the three-mechanisms fact"),
            ("Layer 1 assigns ownership because", None, "duplicate of the ownership-assignment fact"),
            ("Layer 2 uses Row Level Security policies", None, "duplicate of the RLS fact"),
            ("Returning 404 instead of 403", None, "duplicate of the 404-not-403 fact"),
            ("The Secure Networking Tracker is a private contact tracker where ownership", None, "duplicate of the Postgres-ownership fact"),
            ("The project is a networking tracker for Berkeley contacts", None, "duplicate of the Postgres-ownership fact"),
            ("The interesting part of the tracker is where the ownership boundary sits", None, "duplicate of the Postgres-ownership fact"),
            ("RLS filters every statement using four policies", None, "duplicate of the RLS fact (which also says RLS is forced)"),
            ("One thing that could be done differently is implementing keyset pagination",
             "A stated next step: the list loads every matching row, so at a few thousand contacts it needs keyset pagination.",
             "added why, from the same passage"),
        ],
        "related": [("UC Berkeley", "Built at UC Berkeley (Sep 2026) for Berkeley contacts."),
                    ("Allowlist Data Access App", "The same question, who may see which records, answered with a logged exception "
                     "register instead of database policies."),
                    ("TripMatch Rides Board", "Another Berkeley-only tool where access control is the core design question.")],
        "related_note": "Removed Gemma's link to Ms. Pac-Man DQN ('both train an agent using a Deep Q-Network'), which is false.",
    },
    "TripMatch Rides Board": {
        "summary": "TripMatch is a verified, Berkeley-only rides board for a 400-person Haas class that had coordinated rides by "
                   "scrolling a WhatsApp chat. It went from PRD to public board in six days (August 22–27, 2026); V1 stored the whole "
                   "board as one JSON document, and a rebuild moved storage behind an API on GitHub Pages, a Cloudflare Worker and D1.",
        "related": [("UC Berkeley", "Built for the Haas class; listed as related work on the UC Berkeley entry."),
                    ("Secure Networking Tracker", "Another Berkeley-only tool where access control is the core design question."),
                    ("Job Search Agent", "Another independent project from Aug–Sep 2026, built end to end alone.")],
    },
}


# Review pass 2 (2026-09-28): the note ingested during the offline demonstration.
EDITS["Kickstarter Scraper"] = {
    "summary": "Kickstarter Scraper was an individual extra-credit project for ITAO 40450 at Notre Dame's Mendoza College of "
               "Business (Spring 2023). rvest returned an empty result rather than an error, because Kickstarter builds its "
               "campaign body in the browser; the fix was a two-stage pipeline: drive a real browser, snapshot the document it "
               "builds, then parse the snapshot.",
    "facts": [
        ("The tool the course taught returns an empty result", "On Kickstarter, the tool the course taught (rvest) returned an "
         "empty result for the most valuable field, and not an error.", "named the tool and what came back empty"),
        ("The project is really about why that happens", "The project is about why that happens and what to do instead: let a "
         "real browser execute the page, capture the document it builds, and parse that.", "neutral voice"),
        ("Kickstarter's don't.", "Unlike pages that arrive complete, Kickstarter's campaign body (the actual pitch) sits under "
         "#react-campaign and is assembled by JavaScript in the visitor's browser after the page loads.",
         "the fragment 'Kickstarter's don't.' made no sense without the previous paragraph"),
        ("html_elements() on a selector matching nothing does not raise.", "The failure is silent: html_elements() on a selector "
         "that matches nothing does not raise, and html_text() on the empty result returns character(0), so the script exits "
         "cleanly and prints nothing.", "joined two fragments into the point the passage makes"),
        ("html_text() on a zero-length node set returns character(0).", None, "merged into the previous fact"),
        ("Stage one is a real browser.", "Stage one: Selenium drives Safari's WebDriver to the project URL, lets the page finish "
         "assembling itself, and writes the body's innerHTML to a local file.", "the fragment had no content"),
        ("Stage two is the rvest script", "Stage two: the unchanged rvest script parses the file on disk instead of the URL, with six "
         "selectors for title, pledged amount, pledge goal, backers, location and description.", "added what it extracts, from the same passage"),
        ("With the document already on disk", "Splitting fetch from parse means iterating on the selectors costs nothing and the site "
         "sees a single visit.", "added the subject"),
        ("rvest offers html_text() and html_text2().", "Backers, location and the description use html_text2(), which approximates the "
         "rendered text; html_text() returns raw text nodes, layout whitespace and all.", "the fragment stated no finding"),
        ("What transfers here is not a library.", "The transferable lesson is a question to ask before writing any selector: does the "
         "content exist in the server's response, or is it assembled in the browser?", "the fragment stated no finding"),
        ("View-source and inspect-element disagree", "View-source and inspect-element disagree exactly when the content is assembled: "
         "view-source shows what the server sent, the inspector shows what the browser built.", "completed from the same passage"),
    ],
    "related": [("University of Notre Dame", "An individual extra-credit project for ITAO 40450 at the Mendoza College of Business "
                 "(Spring 2023); listed as related work on the Notre Dame entry."),
                ("Formula 1 Racing Trends", "Same course (ITAO 40450), scraped three days later; that archive arrived complete, so it "
                 "was rate-limited with polite::bow() instead of snapshotted in a browser.")],
    "related_note": "Removed Gemma's link to MBA 290T Syllabus ('completed as part of MBA 290T'): the source says ITAO 40450 at Notre "
                    "Dame. A link to the re-created 'Agentic AI' note was removed by the merge (fix 10).",
}

# Links added to notes that were already reviewed, so the new note has meaningful incoming links.
ADD_RELATED = {
    "University of Notre Dame": [("Kickstarter Scraper", "An individual extra-credit project for ITAO 40450 (Spring 2023); listed "
                                  "as related work on this entry.")],
    "Formula 1 Racing Trends": [("Kickstarter Scraper", "Same course (ITAO 40450): a browser-snapshot scrape done three days before "
                                 "this one.")],
}


def add_related(note: vault.Note, links: list, log: list) -> None:
    for title, why in links:
        if f"[[{title}]]" in note.body:
            continue
        note.body = re.sub(r"(## Related notes\n(?:- .*\n)*)", lambda m: m.group(1) + f"- [[{title}]] — {why}\n", note.body, count=1)
        log.append(("related link added", title, why))


def apply(note: vault.Note, spec: dict, log: list) -> None:
    body = note.body
    if "summary" in spec:
        parts = body.split("\n\n", 2)  # "# Title", summary paragraph, rest
        old = parts[1]
        parts[1] = spec["summary"]
        body = "\n\n".join(parts)
        note.meta["summary"] = vault.first_sentence(spec["summary"])
        log.append(("summary rewritten", old[:120] + ("…" if len(old) > 120 else ""), "clearer, source-checked summary"))
    lines = body.split("\n")
    for needle, new, why in spec.get("facts", []):
        hit = [i for i, l in enumerate(lines) if l is not None and l.startswith("- ") and needle in l and FACT_LINE.match(l)]
        if len(hit) != 1:
            raise SystemExit(f"{note.title}: expected one fact containing {needle!r}, found {len(hit)}")
        m = FACT_LINE.match(lines[hit[0]])
        if new is None:
            log.append(("fact removed", m.group("fact"), why))
            lines[hit[0]] = None
        else:
            log.append(("fact corrected", f"{m.group('fact')} → {new}", why))
            lines[hit[0]] = f"- {new} {m.group('ref')}"
    body = "\n".join(l for l in lines if l is not None)
    body = re.sub(r"\n### From [^\n]+\n(?=\n|### |## )", "\n", body)  # drop source groups left empty
    if "related" in spec:
        rel = "\n".join(f"- [[{t}]] — {w}" for t, w in spec["related"]) or \
              "- None. No other note in this wiki shares a subject with this one."
        body = re.sub(r"(## Related notes\n)(.*?)(\n## )", lambda m: m.group(1) + rel + "\n" + m.group(3), body, flags=re.S)
        log.append(("related links replaced", ", ".join(t for t, _ in spec["related"]) or "(none)",
                    spec.get("related_note", "each link now states a relationship the sources support")))
    note.body = body
    note.meta["reviewed"] = True
    note.meta["reviewed_by"] = REVIEWER
    note.meta["reviewed_at"] = datetime.now().isoformat(timespec="minutes")


def main() -> int:
    """Review notes that are not yet reviewed; append the changes to evidence/wiki_review.md."""
    settings = config.load()
    notes = {n.title: n for n in vault.all_notes(settings)}
    log_path = settings.root / "evidence" / "wiki_review.md"
    todo = [t for t in sorted(notes) if not notes[t].meta.get("reviewed")]
    extra = [t for t in sorted(ADD_RELATED) if t in notes and notes[t].meta.get("reviewed")]
    if not todo and not any(f"[[{x}]]" not in notes[t].body for t in extra for x, _ in ADD_RELATED[t]):
        print("nothing to review")
        return 0
    report = [f"## Review pass {datetime.now():%Y-%m-%d %H:%M}", "",
              f"Notes reviewed in this pass: {', '.join(todo) or 'none'}. Reviewer: {REVIEWER}.", ""]
    counts = {"removed": 0, "corrected": 0, "summaries": 0, "links": 0}
    for title in todo:
        note = notes[title]
        log: list = []
        apply(note, EDITS.get(title, {}), log)
        vault.write_note(note)
        report += [f"### {title}", ""]
        if not log:
            report.append("Checked against its sources; no changes needed.")
        for kind, what, why in log:
            report.append(f"- **{kind}**: {what}  \n  _Why:_ {why}")
            counts["removed" if "removed" in kind else "corrected" if "corrected" in kind else "summaries" if "summary" in kind else "links"] += 1
        report.append("")
    for title in extra:
        log = []
        add_related(notes[title], ADD_RELATED[title], log)
        if log:
            notes[title].meta["reviewed_at"] = datetime.now().isoformat(timespec="minutes")
            vault.write_note(notes[title])
            report += [f"### {title} (already reviewed)", ""] + [f"- **{k}**: [[{w}]] — {y}" for k, w, y in log] + [""]
    text = log_path.read_text() if log_path.exists() else "# Wiki review log\n"
    log_path.write_text(text.rstrip() + "\n\n" + "\n".join(report) + "\n")
    vault.render_index(settings)
    print(f"reviewed {todo}; {counts}; links added to {extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
