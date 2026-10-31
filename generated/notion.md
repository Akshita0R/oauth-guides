# Notion

- **Difficulty:** 🟢 Easy 📄 Docs (https://developers.notion.com/docs/authorization)
- **Time to first test user:** ~15 minutes 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration)
- **Time to public launch (including approval wait):** Immediate (no mandatory approval queue required for OAuth distribution) 📄 Docs (https://developers.notion.com/docs/authorization)

---

## What you need before starting

- A Notion user account with permission to create integrations 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).
- Admin access to at least one Notion workspace for testing 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).
- A secure HTTPS redirect URI (callback endpoint) for receiving OAuth authorization codes (`http://localhost` is permitted for local development) 📄 Docs (https://developers.notion.com/docs/authorization).
- A valid Privacy Policy URL and Terms of Service URL (required to distribute as a public OAuth integration) 📄 Docs (https://developers.notion.com/docs/authorization).
- Organization information, including company name, website URL, and support email address 📄 Docs (https://developers.notion.com/docs/authorization).

---

## Steps

### Step 1: Access the Notion Integrations portal 🧑
1. Sign in to your Notion account and navigate to the [Notion Integrations Dashboard](https://www.notion.so/my-integrations) 📄 Docs (https://www.notion.so/my-integrations).
2. Click **+ New integration** 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).

### Step 2: Configure basic integration details 🧑
1. Select the **Associated workspace** where the integration will initially reside 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).
2. Enter an **Integration Name** and upload an app icon 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).

### Step 3: Define API capabilities 🤖
1. Under the **Capabilities** tab, select the content permissions required for your app (e.g., *Read content*, *Update content*, *Insert content*) 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).
2. Select comment permissions (*Read comments*, *Insert comments*) if needed 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).
3. Select user information permissions (*No user information*, *Read user information without email addresses*, or *Read user information with email addresses*) 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).

### Step 4: Convert to a Public Integration (OAuth 2.0) 🧑
1. Navigate to the **Distribution** tab 📄 Docs (https://developers.notion.com/docs/authorization).
2. Toggle the distribution setting from **Internal** to **Public** 📄 Docs (https://developers.notion.com/docs/authorization).
3. Fill in required organization details:
   - Organization / Company name 📄 Docs (https://developers.notion.com/docs/authorization)
   - Homepage URL 📄 Docs (https://developers.notion.com/docs/authorization)
   - Privacy Policy URL 📄 Docs (https://developers.notion.com/docs/authorization)
   - Terms of Service URL 📄 Docs (https://developers.notion.com/docs/authorization)
   - Support email address 📄 Docs (https://developers.notion.com/docs/authorization)
4. Add your **Redirect URIs** (e.g., `https://yourapp.com/auth/notion/callback` or `http://localhost:3000/callback`) 📄 Docs (https://developers.notion.com/docs/authorization).
5. Save the changes 📄 Docs (https://developers.notion.com/docs/authorization).

### Step 5: Retrieve OAuth credentials 🤖
1. Navigate to the **Secrets** section of your integration settings 📄 Docs (https://developers.notion.com/docs/authorization).
2. Copy the **OAuth Client ID** and **OAuth Client Secret** 📄 Docs (https://developers.notion.com/docs/authorization).

### Step 6: Implement the Authorization Code Exchange Flow 🤖
1. Direct users to Notion's authorization URL 📄 Docs (https://developers.notion.com/docs/authorization):
   ```text
   https://api.notion.com/v1/oauth/authorize?owner=user&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code
   ```
2. Upon authorization, handle the callback containing the temporary `code` 📄 Docs (https://developers.notion.com/docs/authorization).
3. Exchange the `code` by issuing a `POST` request to `https://api.notion.com/v1/oauth/token` 📄 Docs (https://developers.notion.com/docs/authorization):
   - **Headers:** `Authorization: Basic {BASE64(CLIENT_ID:CLIENT_SECRET)}`, `Content-Type: application/json`, `Notion-Version: 2022-06-28` 📄 Docs (https://developers.notion.com/docs/authorization).
   - **Body:** `{"grant_type": "authorization_code", "code": "{CODE}", "redirect_uri": "{REDIRECT_URI}"}` 📄 Docs (https://developers.notion.com/docs/authorization).
4. Store the returned `access_token`, `workspace_id`, `workspace_name`, and `bot_id` 📄 Docs (https://developers.notion.com/docs/authorization).

---

## Approval and review

- **Works right away:**
  - **Internal integrations:** Work immediately in the creator's workspace using an internal API secret key 📄 Docs (https://developers.notion.com/docs/create-a-notion-integration).
  - **Public integrations:** As soon as an integration is converted to "Public" with required organization fields and redirect URIs filled out, any external Notion user or workspace admin can authenticate via OAuth 2.0 immediately without prior manual review from Notion 📄 Docs (https://developers.notion.com/docs/authorization).
- **Optional Gallery Listing Review:**
  - Notion offers an optional application process to feature public integrations in the official [Notion Integrations Gallery](https://www.notion.so/integrations) 📄 Docs (https://developers.notion.com/docs/authorization).
  - This review is strictly for directory placement and marketing exposure; it is not required for your OAuth app to function for external users 📄 Docs (https://developers.notion.com/docs/authorization).

---

## Blockers & fixes

- **Redirect URI Mismatch:** Notion strictly validates redirect URIs. Ensure the exact URI passed in the authorization query string matches one of the URIs configured in the integration distribution settings 📄 Docs (https://developers.notion.com/docs/authorization).
- **HTTP vs HTTPS Error:** Notion requires HTTPS endpoints for production redirect URIs; `http://` is rejected unless the host is explicitly `localhost` 📄 Docs (https://developers.notion.com/docs/authorization).
- **Token Request Authentication Failed:** Token exchange requests at `https://api.notion.com/v1/oauth/token` require HTTP Basic Authentication using Base64-encoded `client_id:client_secret` in the `Authorization` header 📄 Docs (https://developers.notion.com/docs/authorization).
- **Missing Resource Access:** When users grant OAuth permission, Notion allows them to select specific pages or entire workspaces. If an endpoint returns 404/403 errors, the user may not have selected or granted access to that specific page during OAuth flow consent 📄 Docs (https://developers.notion.com/docs/authorization).

---

## Still unknown

- Turnaround time for optional Notion Integrations Gallery application approvals ❓ Unknown.

---

## Sources

- https://developers.notion.com/docs/create-a-notion-integration
- https://developers.notion.com/docs/authorization
- https://www.notion.so/my-integrations