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

## 3. Anthropic (LLM API)

1. Go to [console.anthropic.com](https://console.anthropic.com) and sign in.
2. Navigate to **API Keys** → **Create Key** — name it `themis-prod`.
3. Copy the key immediately (it won't be shown again).
4. Set a usage budget under **Billing → Usage Limits** to avoid surprise bills during development.

---

## 4. Local environment

Create a `.env` file at the project root (never commit this):

```sh
# .env
DATABASE_URL=postgresql://...        # from Railway Postgres Connect tab
ANTHROPIC_API_KEY=sk-ant-...         # from Anthropic console
LITELLM_DEFAULT_MODEL=claude-haiku-4-5-20251001  # cheapest model for development
```

Add `.env` to `.gitignore`:

```sh
echo ".env" >> .gitignore
```

---

## 5. Railway environment variables

Once the backend is deployed, set the same variables in Railway so the production service can read them:

1. Open your Railway project → select the backend service → **Variables** tab.
2. Add `ANTHROPIC_API_KEY` and any other keys.
3. `DATABASE_URL` is injected automatically by the Postgres plugin — no need to add it manually.

---

## Checklist

- [ ] Vercel account created, CLI installed and logged in
- [ ] Railway account created, project and Postgres provisioned, CLI installed
- [ ] Anthropic API key created and saved
- [ ] Local `.env` file created
- [ ] `.env` added to `.gitignore`
