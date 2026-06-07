# Publishing to PyPI

Complete guide to publish FlossWare AI projects to PyPI (Python Package Index).

## Quick Setup (5 Minutes)

### Step 1: Create PyPI Account

1. **Go to:** https://pypi.org/account/register/
2. **Fill out:**
   - Username
   - Email
   - Password
3. **Verify email** (check your inbox)
4. **Done!**

---

### Step 2: Generate API Token

1. **Log in** to https://pypi.org/
2. **Go to:** https://pypi.org/manage/account/token/
3. **Click:** "Add API token"
4. **Fill out:**
   - Token name: `FlossWare-GitHub-Actions`
   - Scope: `Entire account` (or specific project after first upload)
5. **Click:** "Add token"
6. **COPY THE TOKEN** - You'll only see it once!
   - Format: `pypi-AgEIcHlwaS5vcmc...` (long string)

**⚠️ IMPORTANT:** Save this token somewhere safe! You can't see it again!

---

### Step 3: Add Token to GitHub

1. **Go to:** https://github.com/FlossWare/knowledge-ai/settings/secrets/actions
2. **Click:** "New repository secret"
3. **Fill out:**
   - Name: `PYPI_TOKEN`
   - Secret: `pypi-AgEIcHlwaS5vcmc...` (paste your token)
4. **Click:** "Add secret"

**Repeat for all 4 projects:**
- https://github.com/FlossWare/knowledge-ai/settings/secrets/actions
- https://github.com/FlossWare/semantic-search-ai/settings/secrets/actions
- https://github.com/FlossWare/knowledge-ai/settings/secrets/actions
- https://github.com/FlossWare/consensus-ai/settings/secrets/actions

**OR** add at organization level (once for all repos):
- https://github.com/organizations/FlossWare/settings/secrets/actions

---

### Step 4: Done! Automation Handles the Rest

**Next push to `main` will automatically:**

1. ✅ Bump version (v0.2 → v0.3)
2. ✅ Build Python packages
3. ✅ **Publish to PyPI** ← NEW!
4. ✅ Publish to packagecloud.io
5. ✅ Create GitHub Release

**No manual steps needed!**

---

## What Happens After Publishing

### Your packages appear on PyPI:

- https://pypi.org/project/knowledge-ai/
- https://pypi.org/project/semantic-search-ai/
- https://pypi.org/project/knowledge-ai/
- https://pypi.org/project/consensus-ai/

### Anyone can install with pip:

```bash
pip install knowledge-ai
pip install semantic-search-ai
pip install knowledge-ai
pip install consensus-ai
```

**No extra URLs needed!** Standard pip install.

---

## Verification

After your first successful publish:

### Check PyPI

Visit: https://pypi.org/project/knowledge-ai/

You should see:
- ✅ Your package listed
- ✅ Current version
- ✅ Download stats
- ✅ README displayed

### Test Installation

```bash
# Create fresh virtualenv
python3 -m venv test-env
source test-env/bin/activate

# Install from PyPI
pip install knowledge-ai

# Verify
python -c "from vectordb_ai import VectorStoreFactory; print('✅ Works!')"
```

---

## Troubleshooting

### "Package name already taken"

If someone already registered the name on PyPI:

**Option 1:** Contact PyPI support to claim it (if inactive)
- Email: admin@pypi.org
- Show them your GitHub repo

**Option 2:** Use a different name
- `flossware-knowledge-ai`
- `knowledge-ai-flossware`

Update `setup.py`:
```python
setup(
    name="flossware-knowledge-ai",  # Changed
    ...
)
```

### "Invalid token"

- Make sure token starts with `pypi-`
- Copy the ENTIRE token (very long)
- No extra spaces

### "Permission denied"

For scope, use:
- **First upload:** "Entire account"
- **After first upload:** Scope to specific project

---

## Manual Publishing (if needed)

If you need to publish manually:

```bash
cd python/

# Install tools
pip install build twine

# Build packages
python -m build

# Upload to PyPI
python -m twine upload dist/*
# Enter username: __token__
# Enter password: pypi-AgEIcHlwaS5vcmc... (your token)
```

---

## PyPI vs packagecloud.io

| Feature | PyPI | packagecloud.io |
|---------|------|-----------------|
| **Discoverability** | ⭐⭐⭐⭐⭐ Standard | ⭐⭐⭐ Requires URL |
| **Installation** | `pip install X` | `pip install --index-url ...` |
| **Name conflicts** | ❌ Global namespace | ✅ Namespaced |
| **Private packages** | ❌ No (paid tier) | ✅ Yes (free tier) |
| **Native packages** | ❌ Python only | ✅ RPM, DEB, Python |
| **Enterprise** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Better |

**Recommendation:** Publish to BOTH!
- PyPI for discoverability
- packagecloud.io for enterprise deployments

---

## Security Best Practices

### Use Scoped Tokens (After First Upload)

1. After first successful upload to PyPI
2. Go back to: https://pypi.org/manage/account/token/
3. Delete the "Entire account" token
4. Create new token scoped to **specific project**
   - Name: `knowledge-ai-only`
   - Scope: `Project: knowledge-ai`
5. Update GitHub secret with new token

**Benefits:**
- ✅ Token can only upload to one project
- ✅ Limits damage if token leaks
- ✅ Security best practice

### Rotate Tokens Regularly

Update tokens every 6-12 months:
1. Generate new token
2. Update GitHub secret
3. Delete old token

---

## Organization vs Personal Account

### Personal Account (pypi.org/user/yourname/)
- ✅ Simple
- ❌ Tied to your account
- ❌ Single owner

### Organization (Recommended)
1. Create PyPI organization: https://pypi.org/manage/organizations/
2. Add team members
3. Shared ownership

**For FlossWare:** Create `FlossWare` organization on PyPI

---

## Monitoring

### After publishing, monitor:

**Download stats:**
- https://pypistats.org/packages/knowledge-ai

**Security alerts:**
- PyPI will email you about vulnerabilities

**User feedback:**
- GitHub issues
- PyPI project page comments

---

## Next Steps

1. ✅ Create PyPI account
2. ✅ Generate API token
3. ✅ Add `PYPI_TOKEN` to GitHub secrets
4. 🚀 Push to main → Auto-publish!

That's it! **Your packages will be on PyPI automatically!** 🎉
