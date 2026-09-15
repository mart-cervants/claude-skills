# Setup — one time

This gets you from zero to a working Google Ads API setup using a **service
account with domain-wide delegation** (no per-user OAuth login; survives staff
changes). You need a **Google Workspace** domain you administer.

Work top to bottom, then run `python scripts/doctor.py` to verify.

---

## 1. Get a developer token

1. Sign in to a **Google Ads Manager (MCC) account** (create one at
   https://ads.google.com/home/tools/manager-accounts/ if you don't have one).
2. In the MCC: **Admin → API Center**. Apply for a **developer token**.
3. ⚠️ A new token starts with **Test-account access only** — it can only call
   *test* Ads accounts. To operate on your real account, apply for **Basic
   access** in the same API Center (approval can take a day or more). `doctor.py`
   and the scripts will flag this if you hit it.

Copy the token — it goes in `google-ads.yaml` as `developer_token`.

## 2. Create a Google Cloud project + service account

1. https://console.cloud.google.com → create (or pick) a project.
2. **APIs & Services → Library →** enable **Google Ads API**.
3. **APIs & Services → Credentials → Create credentials → Service account.**
   Give it a name; no project roles are required.
4. Open the new service account → **Keys → Add key → Create new key → JSON**.
   Download it. This is your `json_key_file_path`.
5. On the service account details page, note its **Unique ID (client ID)** and
   enable **domain-wide delegation** (check the box / "Enable G Suite domain-wide
   delegation").

## 3. Authorize the service account in Workspace (domain-wide delegation)

1. Google **Workspace Admin console** (admin.google.com) as a super-admin.
2. **Security → Access and data control → API controls → Domain-wide delegation.**
3. **Add new.** Enter the service account's **client ID** from step 2.5.
4. OAuth scope: `https://www.googleapis.com/auth/adwords`
5. Authorize.

This lets the service account **impersonate** a Workspace user.

## 4. Grant the impersonated user access to the Ads account

The user the service account impersonates (`impersonated_email`) must have
access to the Google Ads account:

1. In Google Ads: **Admin → Access and security**.
2. Add the Workspace user's email with at least **Standard** access.

## 5. Write the config file (outside the skill folder)

```bash
mkdir -p ~/.config/google-ads
cp config/google-ads.yaml.example ~/.config/google-ads/google-ads.yaml
```

Edit `~/.config/google-ads/google-ads.yaml` and fill in:

| Field | Value |
|-------|-------|
| `developer_token` | from step 1 |
| `json_key_file_path` | absolute path to the JSON key from step 2.4 |
| `impersonated_email` | the Workspace user from step 4 |
| `login_customer_id` | your Ads account ID, **digits only, no dashes** |

Then point the scripts at it (add to your shell profile to persist):

```bash
export GOOGLE_ADS_CONFIGURATION_FILE_PATH="$HOME/.config/google-ads/google-ads.yaml"
```

## 6. Install dependencies

```bash
pip install -r requirements.txt
```

## 7. Verify

```bash
python scripts/doctor.py
```

Fix anything it reports `FAIL`. When it passes, try a read-only report:

```bash
python scripts/report.py --preset campaign_spend
```

---

## Fallback: no Workspace / can't do delegation

If you can't enable domain-wide delegation (e.g. the Ads account is on a
personal `@gmail.com`), use the **OAuth refresh-token** flow instead:

1. In Google Cloud, create an **OAuth client ID** of type *Desktop app*.
2. Use Google's `generate_user_credentials.py`
   (https://github.com/googleads/google-ads-python) to produce a refresh token.
3. In `google-ads.yaml`, replace `json_key_file_path` / `impersonated_email`
   with:
   ```yaml
   client_id: "..."
   client_secret: "..."
   refresh_token: "..."
   ```
`doctor.py` recognizes both auth styles.

---

## Security notes

- **Never** put the key file or `google-ads.yaml` inside the skill folder or any
  git repo. Keep them under `~/.config/google-ads/` with tight permissions
  (`chmod 600`).
- The service-account key is a credential — treat it like a password.
