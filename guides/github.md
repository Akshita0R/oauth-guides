# GitHub

- **Difficulty:** 🟢 Easy
- **Time to first test user:** ~5 minutes ✅ Tested
- **Time to public launch:** ~5 minutes, no approval needed ✅ Tested
- **Last checked:** October 2026

## What you need before starting
- A GitHub account
- An app name, a homepage URL, and a redirect URI (`http://localhost` works for testing) ✅ Tested
- No company, domain, privacy policy, or payment needed ✅ Tested

## Steps
1. 🧑 Go to Settings → Developer settings → OAuth Apps → New OAuth App
2. 🤖 Fill in app name, homepage URL, redirect URI (an agent can prepare these values)
3. 🧑 Click Register application
4. 🧑 Generate a client secret and store it safely (it is shown only once)
5. 🤖 Build the authorize URL and test the consent screen

## Blockers & fixes
- **404 page on the authorize URL** → you probably used the client *secret* instead of the client *ID*. The Client ID starts with `Ov23li`. ✅ Tested (I hit this myself)

## Still unknown
- Rate limits for apps with many users (not tested)

## Sources
- My own test, October 2026
- https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app 📄 Docs
