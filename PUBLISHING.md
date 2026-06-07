# Publishing Knowledge AI

This document explains how Knowledge AI packages are published to multiple repositories.

## Automated Publishing

Every push to `main` triggers GitHub Actions that:
1. Auto-bumps version (X.Y format)
2. Creates git tag
3. Creates GitHub Release
4. Builds Python packages
5. Publishes to configured repositories

## Publishing Targets

### 1. PyPI (Primary)

**Status:** ✅ Enabled with `PYPI_TOKEN` secret

**Install:**
```bash
pip install knowledge-ai
```

**Setup:**
1. Create PyPI account: https://pypi.org/account/register/
2. Generate API token: https://pypi.org/manage/account/token/
3. Add `PYPI_TOKEN` secret to GitHub repo settings

---

### 2. packagecloud.io (Enterprise)

**Status:** ✅ Enabled with `PACKAGECLOUD_TOKEN` secret

**Install:**
```bash
# One-time setup
pip install --index-url https://packagecloud.io/FlossWare/releases/pypi/simple knowledge-ai

# Or add to requirements.txt
--index-url https://packagecloud.io/FlossWare/releases/pypi/simple
knowledge-ai>=0.1
```

**Setup:**
1. Create packagecloud account: https://packagecloud.io/
2. Create repository: `FlossWare/releases`
3. Generate API token: https://packagecloud.io/api_token
4. Add `PACKAGECLOUD_TOKEN` secret to GitHub repo settings

**Benefits:**
- ✅ Namespaced packages (no conflicts)
- ✅ Private + public repos
- ✅ Multi-language support
- ✅ CDN distribution
- ✅ Free tier available

---

### 3. GitHub Packages (Backup)

**Status:** ✅ Automatic (uses GITHUB_TOKEN)

**Install:**
```bash
pip install knowledge-ai --extra-index-url https://ghcr.io/FlossWare/knowledge-ai
```

**Setup:**
No setup needed - automatic with GitHub Actions.

---

## Repository Structure

```
FlossWare AI Projects:
├── PyPI:            https://pypi.org/project/knowledge-ai/
├── packagecloud:    https://packagecloud.io/FlossWare/releases/packages/python/knowledge-ai
└── GitHub:          https://github.com/FlossWare/knowledge-ai/packages
```

---

## Manual Publishing

If you need to publish manually:

### To PyPI:
```bash
cd python
pip install build twine
python -m build
python -m twine upload dist/*
```

### To packagecloud.io:
```bash
cd python
pip install packagecloud
export PACKAGECLOUD_TOKEN=your-token
package_cloud push FlossWare/releases/python dist/*.whl
package_cloud push FlossWare/releases/python dist/*.tar.gz
```

---

## Installation Methods

### Method 1: PyPI (Recommended)
```bash
pip install knowledge-ai
```

### Method 2: packagecloud.io (Enterprise)
```bash
pip install --index-url https://packagecloud.io/FlossWare/releases/pypi/simple knowledge-ai
```

### Method 3: GitHub Direct
```bash
pip install git+https://github.com/FlossWare/knowledge-ai.git
```

### Method 4: Local Development
```bash
git clone https://github.com/FlossWare/knowledge-ai.git
cd knowledge-ai/python
pip install -e .
```

---

## Version History

All versions follow **X.Y** format (no patches):
- Every merge to main = new minor version
- Tags: `v0.1`, `v0.2`, `v0.3`, etc.
- No `v0.1.0` or patch versions

View releases:
- GitHub: https://github.com/FlossWare/knowledge-ai/releases
- PyPI: https://pypi.org/project/knowledge-ai/#history
- packagecloud: https://packagecloud.io/FlossWare/releases

---

## Secrets Required

Add these to GitHub repository settings → Secrets and variables → Actions:

| Secret | Required | Purpose |
|--------|----------|---------|
| `PYPI_TOKEN` | Optional | Publish to PyPI |
| `PACKAGECLOUD_TOKEN` | Optional | Publish to packagecloud.io |
| `GITHUB_TOKEN` | Automatic | GitHub Releases (auto-provided) |

**Note:** Publishing is optional. Without secrets, packages are still built and attached to GitHub Releases.
