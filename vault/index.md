# Personal Wiki

Eason Han's personal wiki: portfolio projects, work and school, and the MBA 290T course. Each note is one subject, written by local Gemma from the original sources in `raw/` and then checked against them. Every note lists its sources; see [[Source Catalog]] for where each original came from.

## Projects

_Things built, analysed or shipped — course assignments and portfolio work._

- [[Action Hub]] — Action Hub was built to replace a manual sweep across roughly 200 dashboards for a technical sales organization.
- [[Allowlist Data Access App]] — Allowlist is a constrained application built to replace a shared spreadsheet that governed data access exceptions.
- [[Custom LLM with nanoGPT]] — Building a Custom LLM was an MBA 290T assignment: a small nanoGPT (2 blocks, 4 heads, 64-number embeddings, 48-token context) trained on a classroom corpus and on extended corpora, then scored on a fixed 48-case language eval suite.
- [[DataFest 2023]] — This project involved analyzing data from the American Bar Association's legal advice platform over 48 hours.
- [[Formula 1 Racing Trends]] — This project analyzed thirty-two seasons of Formula 1 data to determine if car speeds have increased over time.
- [[GenAI Adoption Program]] — This project involved designing a gamified adoption program for 1,100 LATAM sellers to drive usage of existing GenAI tooling.
- [[GenAI Target Setting]] — This project involved setting the first annual target for a business with almost no history by forecasting a leading indicator instead of the final goal.
- [[Hazardous Asteroid Screening]] — This project developed a triage filter to prioritize near-Earth asteroids for observation, as space agencies cannot monitor all of them.
- [[Job Search Agent]] — This project is a daily scanner designed to find PM internships for Summer 2027.
- [[Kickstarter Scraper]] — Kickstarter Scraper was an individual extra-credit project for ITAO 40450 at Notre Dame's Mendoza College of Business (Spring 2023). rvest returned an empty result rather than an error, because Kickstarter builds its campaign body in the browser; the fix was a two-stage pipeline: drive a real browser, snapshot the document it builds, then parse the snapshot.
- [[Ms. Pac-Man DQN]] — Ms. Pac-Man DQN was the MBA 290T Class 3 assignment: a Deep Q-Network trained to play Ms. Pac-Man, with exploration 0.10, 300 episodes and learning rate 0.0001 chosen by a measured search.
- [[Pull-Request Automation]] — This project involved building a skill on Amazon's internal OpenClaw platform to automate the mandatory steps between finishing a code change and getting it reviewed.
- [[Secure Networking Tracker]] — Secure Networking Tracker is a private contact tracker for the people met at Berkeley, built at UC Berkeley (Sep 2026) with Next.js 16, Neon Postgres, Better Auth and Vercel.
- [[TripMatch Rides Board]] — TripMatch is a verified, Berkeley-only rides board for a 400-person Haas class that had coordinated rides by scrolling a WhatsApp chat.

## Experience

_Employers, roles and schools._

- [[Amazon Web Services]] — Business Intelligence Engineer in Global Sales Strategy & Analytics at Amazon Web Services, Seattle, from Jul 2023 to May 2026.
- [[IDG Capital]] — Venture Capital Analyst Intern at IDG Capital in Beijing from Jun 2020 to Aug 2020, doing diligence on early-stage SaaS and food-supply companies.
- [[Seaside Sustainability]] — Fundraising Team Lead, a volunteer role, for Seaside Sustainability (clean-shores.org) in Gloucester, MA, from Apr 2025 to Jan 2026: founded and led the fundraising function for a beach-cleaning robot, from concept through launch.
- [[TikTok Internship]] — Ads Risk Integrity Intern at TikTok in Beijing from May 2021 to Aug 2021, working on ad moderation and risk analysis across Data Science, Engineering and Policy.
- [[UC Berkeley]] — A concurrent MBA and M.Eng. in Industrial Engineering & Operations Research at UC Berkeley (Haas School of Business and IEOR), from Aug 2026 to an expected May 2028, taken together so that product judgment and engineering are learned in the same place.
- [[University of Notre Dame]] — B.B.A. in Business Analytics and B.S. in Applied Mathematics at the University of Notre Dame's Mendoza College of Business, Aug 2019 to May 2023: the quantitative methods on one side, the business framing for them on the other.

## Course

_MBA 290T: schedule, assignments and policies._

- [[MBA 290T Syllabus]] — MBA 290T: Fundamental of Agentic AI (Haas School of Business, UC Berkeley, Fall 2026) is a seven-class course that goes from programming foundations to building and evaluating tool-using AI agents.

## Concepts

_Techniques and ideas that show up across several projects._

- [[Deep Learning]] — Deep learning trains layered networks of weights with non-linearities by gradient descent: a loss scores each prediction and the gradient says which way to move every parameter.
- [[Deep Q-Network]] — A Deep Q-Network (DQN) is a reinforcement-learning method in which a neural network estimates how much future reward each possible action is worth, and the agent takes the highest-valued move.
- [[Prioritization Framework]] — A four-gate method for cutting a roadmap, written up as a reconstruction of the one Eason used on the AWS Sales insights platform (the Action Hub); the example features in the write-up are generic, invented for the portfolio.
- [[Time Series Analysis]] — Time-series analysis models how a measurement changes over time; in these sources most of the work is making the points in a series comparable before any model is fitted.

_25 notes. Index rebuilt by `wiki ingest` on 2026-09-28._
