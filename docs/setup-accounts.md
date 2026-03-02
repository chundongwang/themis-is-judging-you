# Account Setup

Before scaffolding the project, you need accounts and credentials on three platforms. This is a one-time setup.

---

## 1. Vercel (frontend hosting)

1. Go to [vercel.com](https://vercel.com) and sign up with your GitHub account (`chundongwang`).
2. Once logged in, no project setup needed yet — we'll connect the repo when the frontend is scaffolded.
3. Install the Vercel CLI locally:
   ```sh
   npm i -g vercel
   vercel login
   ```

---

## 2. Railway (backend hosting + Postgres)

1. Go to [railway.app](https://railway.app) and sign up with your GitHub account.
2. Once logged in, create a new **Project** — name it `themis-is-judging-you`.
3. Inside the project, add a **Postgres** plugin:
   - Click **+ New** → **Database** → **PostgreSQL**
   - Railway will provision a managed Postgres instance and inject `DATABASE_URL` automatically.
4. Note down the `DATABASE_URL` from the Postgres plugin's **Connect** tab — you'll need it for local development.
5. Install the Railway CLI:
   ```sh
   npm i -g @railway/cli
   railway login
   ```

---

## 3. LLM Provider API Key(s)

LiteLLM is model-agnostic — set up whichever providers you want to use. You only need one to start.

| Provider  | Console                              | Env var                |
|-----------|--------------------------------------|------------------------|
| Anthropic | console.anthropic.com → API Keys     | `ANTHROPIC_API_KEY`    |
| Google    | aistudio.google.com → API Keys       | `GEMINI_API_KEY`       |
| OpenAI    | platform.openai.com → API Keys       | `OPENAI_API_KEY`       |

For each provider you sign up with:
1. Create an API key and copy it immediately (shown only once).
2. Set a spend/usage budget in the provider's billing settings to cap dev costs.

---

## 4. Local environment

Create a `.env` file at the project root (never commit this):

```sh
# .env
DATABASE_URL=postgresql://...        # from Railway Postgres Connect tab

# Add keys only for the providers you use
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
OPENAI_API_KEY=sk-...

LITELLM_DEFAULT_MODEL=gemini/gemini-2.0-flash   # swap to whichever is cheapest
```

Add `.env` to `.gitignore`:

```sh
echo ".env" >> .gitignore
```

---

## 5. Railway environment variables

Once the backend is deployed, set the same variables in Railway so the production service can read them:

1. Open your Railway project → select the backend service → **Variables** tab.
2. Add whichever provider API keys you use (`ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, etc.) and `LITELLM_DEFAULT_MODEL`.
3. `DATABASE_URL` is injected automatically by the Postgres plugin — no need to add it manually.

---

## Checklist

- [ ] Vercel account created, CLI installed and logged in
- [ ] Railway account created, project and Postgres provisioned, CLI installed
- [ ] At least one LLM provider API key created and saved
- [ ] Local `.env` file created
- [ ] `.env` added to `.gitignore`
