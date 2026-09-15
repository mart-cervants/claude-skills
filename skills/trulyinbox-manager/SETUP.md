# Setup — one time

## 1. Get your API key

1. Log in to TrulyInbox.
2. **Settings → API.**
3. Generate and copy the API key.

## 2. Write the config file (outside the skill folder)

```bash
mkdir -p ~/.config/trulyinbox
cp config/config.yaml.example ~/.config/trulyinbox/config.yaml
chmod 600 ~/.config/trulyinbox/config.yaml
```

Edit `~/.config/trulyinbox/config.yaml` and paste the key in place of
`YOUR_TRULYINBOX_API_KEY`.

Optional — point scripts at a different path (add to shell profile to persist):

```bash
export TRULYINBOX_CONFIG_FILE_PATH="$HOME/.config/trulyinbox/config.yaml"
```

## 3. Install dependencies

```bash
cd ~/.claude/skills/trulyinbox-manager
pip install -r requirements.txt
```

(No dedicated venv needed — this API is plain REST over `requests`, unlike
`google-ads-manager`'s heavier SDK. If the system `python3` is externally
managed (Homebrew/PEP 668) and `pip install` refuses, create a light venv the
same way: `python3 -m venv ~/.config/trulyinbox/venv && ~/.config/trulyinbox/venv/bin/pip install -r requirements.txt`,
then run scripts with that interpreter.)

## 4. Verify

```bash
python scripts/doctor.py
```

Fix anything it reports `FAIL`, then try a read-only call:

```bash
python scripts/dashboard.py
```

---

## Security notes

- **Never** put the API key or `config.yaml` inside the skill folder or any
  git repo. Keep it at `~/.config/trulyinbox/config.yaml`, `chmod 600`.
- The API key is a credential — treat it like a password.
