import pathlib

import anthropic
import streamlit as st

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


def generate_guide(client: anthropic.Anthropic, app_name: str) -> str:
    messages = [{"role": "user", "content": f"Write the OAuth setup guide for: {app_name}"}]
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}]

    for _ in range(4):  # resume a few times if the server-side search loop pauses
        response = client.beta.messages.create(
            model="claude-opus-5-5",
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=tools,
            output_config={"effort": "medium"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
        if response.stop_reason != "pause_turn":
            break
        messages = [messages[0], {"role": "assistant", "content": response.content}]

    if response.stop_reason == "refusal":
        return "The model declined this request. Try a different app name."
    return "\n".join(block.text for block in response.content if block.type == "text")


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
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        with st.spinner(f"Researching {app_name}..."):
            try:
                guide = generate_guide(client, app_name.strip())
            except anthropic.RateLimitError:
                st.error("Too many requests right now. Please wait a minute and try again.")
                st.stop()
            except anthropic.APIStatusError as e:
                st.error(f"The API returned an error ({e.status_code}). Please try again.")
                st.stop()
            except anthropic.APIConnectionError:
                st.error("Could not reach the API. Check your connection and try again.")
                st.stop()
        st.warning("AI-generated and not yet verified by a human. Check 📄 sources before relying on it.")
        st.markdown(guide)
        st.download_button("Download guide (.md)", guide, file_name=f"{app_name.strip()}.md")
