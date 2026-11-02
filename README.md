# OAuth App Setup Guides

**Live app:** https://oapp-guides-tyksps6mrvs8repxhqm2zw.streamlit.app

Look up an app and see how hard it is to register your own OAuth app with that provider and get it approved: time, effort, requirements, blockers, and which steps an agent can do vs. which you must do yourself. Type any app name and an agent researches it and writes a shareable guide live.

## The problem

<!-- ✍️ WRITE IN YOUR OWN WORDS (3–4 sentences): what an OAuth app is, how it differs from a user's connection, and why developers get stuck. Use your Riya example and what you learned from the Composio managed-auth page. -->

## What I built

- **Guide library**: guides for apps with different setup challenges.
  - `guides/` — written by me from my own setup attempts and the docs
  - `generated/` — produced by the live agent and saved as-is, so they can be checked
- **Live generator**: type an app name or website; an agent (Gemini with Google Search) researches the provider's developer docs and writes a guide in the same format.

Every guide answers the same questions in the same order:
1. Can I skip this for now? (Is a Composio-managed OAuth app available?)
2. How hard is it, and how long until the first test user vs. a public launch?
3. What do I need before starting?
4. Steps, each marked 🤖 agent can do / 🧑 you must do
5. What works right away vs. what needs review
6. Blockers and fixes
7. What is still unknown, and sources

Every claim carries an evidence label: ✅ Tested by me · 📄 Official docs · 🤔 Inferred · ❓ Unknown.

## Key decisions

<!-- ✍️ WRITE 3–4 BULLETS IN YOUR OWN WORDS. Each one: what you decided + why. Ideas from your work:
- Splitting "time to first test user" from "time to public launch"
- Evidence labels on every claim
- Starting each guide with "Can I skip this for now?" after you found GitHub, Gmail, Slack, LinkedIn and Notion all have Composio-managed apps
- Picking apps with different difficulty levels
-->

## What I tested vs. what comes from sources

- ✅ **GitHub**: I registered an OAuth app and completed the consent screen myself (redirect to localhost with an authorization code). I hit a 404 by pasting the client secret instead of the client ID; that is now in the guide's blockers.
- ✅ **Composio toolkit pages**: I checked GitHub, Gmail, Slack, LinkedIn and Notion. All five show "Composio-managed OAuth available". I had assumed LinkedIn would not; I was wrong.
- 📄 / 🤔 **Generated guides**: checked against the provider's docs in [`verification.md`](verification.md).

## Where the agent helps and where you take over

- **Agent can:** find and read the provider's developer docs, summarize requirements, flag review steps, prepare form values (app name, redirect URI, scopes), and build the authorize URL.
- **You must:** sign in to the provider, create the app, store the client secret, verify domains, write a privacy policy, record demo videos, and submit for review.

## Limitations

- The agent can be overconfident: in the first Notion guide it labelled 40 claims as 📄 Docs and none as 🤔 Inferred. I tightened its instructions, but generated guides still need a human check.
- Approval times change and are rarely published; many are marked ❓ Unknown.
- The agent only reads public docs. It cannot log in, create apps, or submit reviews.
- Uses Gemini's free tier, which has daily limits.

## Run it yourself

1. Get a free Gemini API key at https://aistudio.google.com/apikey
2. Locally:
   ```bash
   pip install -r requirements.txt
   mkdir -p .streamlit && cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then paste your key
   streamlit run app.py
   ```
3. Or deploy on https://share.streamlit.io and paste `GEMINI_API_KEY = "..."` into the app's **Settings → Secrets**.

No credentials are stored in this repository.

<!-- ✍️ Optional, recommended: one honest line, e.g. "I used an AI coding assistant to scaffold the app; the testing, guide checks and decisions are my own." -->
