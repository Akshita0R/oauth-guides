import pathlib

import streamlit as st
from google import genai
from google.genai import errors, types

st.set_page_config(page_title="OAuth Setup Guides", page_icon="🔑")

GUIDES_DIR = pathlib.Path(__file__).parent / "guides"

SYSTEM_PROMPT = """You research how a developer creates an OAuth app with a provider and gets it approved for production.
Use web search. Prefer the provider's official developer documentation over blogs or forums.

Write the guide in Markdown using exactly this structure:

# <App name>
- **Difficulty:** 🟢 Easy / 🟡 Medium / 🔴 Hard / ⚫ Gated (partner or invite only)
- **Time to first test user:** ...
- **Time to public launch (including approval wait):** ...

## What you need before starting
## Steps
Mark each step 🤖 (an agent can do or prepare this) or 🧑 (a human must do this, e.g. sign in, verify a domain, pay, submit for review).
## Approval and review
What works right away (testing / development mode) vs what needs review before any user can connect.
## Blockers & fixes
## Still unknown
## Sources

Rules:
- Tag every factual claim: 📄 Docs (official docs say so), 🤔 Inferred (your reasoning or a non-official source), ❓ Unknown.
- Never invent approval times. If no source gives one, write ❓ Unknown.
- Every 📄 Docs claim must be backed by a URL listed under Sources.
- If the app does not seem to offer OAuth for third-party developers, say so clearly at the top.
"""


def generate_guide(client: genai.Client, app_name: str) -> tuple[str, list[tuple[str, str]]]:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Write the OAuth setup guide for: {app_name}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )
    guide = response.text or "The agent could not write a guide. Try a different app name."

    # Pages Google Search actually returned to the agent, so readers can check its claims.
    searched = []
    metadata = response.candidates[0].grounding_metadata if response.candidates else None
    for chunk in (metadata.grounding_chunks or []) if metadata else []:
        if chunk.web and chunk.web.uri:
            searched.append((chunk.web.title or chunk.web.domain or "Source", chunk.web.uri))
    return guide, searched


st.title("🔑 OAuth App Setup Guides")
st.write(
    "How hard is it to get an OAuth app approved for a provider? "
    "See the time, effort, requirements, and blockers before you start."
)
st.caption("Evidence labels: ✅ Tested by me · 📄 Official docs · 🤔 Inferred · ❓ Unknown")

library_tab, generate_tab = st.tabs(["📚 Guide library", "🤖 Generate a new guide"])

with library_tab:
    guide_files = sorted(GUIDES_DIR.glob("*.md"))
    names = [f.stem.replace("_", " ").title() for f in guide_files]
    choice = st.selectbox("Choose an app", names)
    if choice:
        st.markdown(guide_files[names.index(choice)].read_text())

with generate_tab:
    st.write("Enter an app name or website. An agent researches it live (about 1–3 minutes).")
    app_name = st.text_input("App name or website", placeholder="e.g. Notion or notion.so")
    if st.button("Generate guide") and app_name.strip():
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        with st.spinner(f"Researching {app_name}..."):
            try:
                guide, searched = generate_guide(client, app_name.strip())
            except errors.ClientError as e:
                if e.code == 429:
                    st.error("The free daily limit was reached. Please try again later.")
                else:
                    st.error(f"The request was rejected ({e.code}). Check the API key in Streamlit secrets.")
                st.stop()
            except errors.APIError:
                st.error("The AI service had a problem. Please try again in a minute.")
                st.stop()
        st.warning("AI-generated and not yet verified by a human. Check 📄 sources before relying on it.")
        st.markdown(guide)
        if searched:
            with st.expander(f"Pages the agent searched ({len(searched)})"):
                for title, uri in searched:
                    st.markdown(f"- [{title}]({uri})")
        st.download_button("Download guide (.md)", guide, file_name=f"{app_name.strip()}.md")
