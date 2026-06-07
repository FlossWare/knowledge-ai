# Native Package Installation

Knowledge AI is available as native packages for multiple operating systems.

## Supported Package Formats

- **RPM** - RHEL, CentOS, Fedora, Rocky Linux, AlmaLinux
- **DEB** - Debian, Ubuntu, Linux Mint
- **Python (pip)** - All platforms (fallback)
- **BSD Ports** - FreeBSD, OpenBSD, NetBSD (coming soon)

---

## RPM-based Systems (Red Hat, Fedora, CentOS)

### RHEL 8/9, CentOS 8/9, Rocky Linux, AlmaLinux

```bash
# Add packagecloud.io repository
curl -s https://packagecloud.io/install/repositories/FlossWare/releases/script.rpm.sh | sudo bash

# Install
sudo yum install python3-knowledge-ai
sudo yum install python3-semantic-search-ai
sudo yum install python3-knowledge-ai
sudo yum install python3-consensus-ai
```

### Fedora 39/40+

```bash
# Add packagecloud.io repository
curl -s https://packagecloud.io/install/repositories/FlossWare/releases/script.rpm.sh | sudo bash

# Install
sudo dnf install python3-knowledge-ai
sudo dnf install python3-semantic-search-ai
sudo dnf install python3-knowledge-ai
sudo dnf install python3-consensus-ai
```

---

## DEB-based Systems (Debian, Ubuntu)

### Ubuntu 20.04 (Focal), 22.04 (Jammy), 24.04 (Noble)

```bash
# Add packagecloud.io repository
curl -s https://packagecloud.io/install/repositories/FlossWare/releases/script.deb.sh | sudo bash

# Install
sudo apt-get install python3-knowledge-ai
sudo apt-get install python3-semantic-search-ai
sudo apt-get install python3-knowledge-ai
sudo apt-get install python3-consensus-ai
```

### Debian 11 (Bullseye), 12 (Bookworm)

```bash
# Add packagecloud.io repository
curl -s https://packagecloud.io/install/repositories/FlossWare/releases/script.deb.sh | sudo bash

# Install
sudo apt-get install python3-knowledge-ai
sudo apt-get install python3-semantic-search-ai
sudo apt-get install python3-knowledge-ai
sudo apt-get install python3-consensus-ai
```

---

## BSD Systems

### FreeBSD (via Ports - Coming Soon)

```bash
# Install from ports
cd /usr/ports/devel/py-knowledge-ai
make install clean

# Or via pkg (when available)
pkg install py39-knowledge-ai
```

### OpenBSD (via Ports - Coming Soon)

```bash
# Install from ports
cd /usr/ports/devel/py-knowledge-ai
make install

# Or via pkg_add (when available)
pkg_add py3-knowledge-ai
```

### NetBSD (via pkgsrc - Coming Soon)

```bash
# Install from pkgsrc
cd /usr/pkgsrc/devel/py-knowledge-ai
make install

# Or via pkg (when available)
pkg_add py39-knowledge-ai
```

---

## Package Names

| System | Package Name |
|--------|-------------|
| **RHEL/CentOS/Fedora** | `python3-knowledge-ai` |
| **Debian/Ubuntu** | `python3-knowledge-ai` |
| **FreeBSD** | `py39-knowledge-ai` |
| **OpenBSD** | `py3-knowledge-ai` |
| **NetBSD** | `py39-knowledge-ai` |
| **Python/pip** | `knowledge-ai` |

---

## Verify Installation

After installing via native package:

```bash
python3 -c "from vectordb_ai import VectorStoreFactory; print('✅ Knowledge AI installed')"
```

---

## Why Use Native Packages?

✅ **No pip required** - Uses system Python  
✅ **Automatic updates** - Via system package manager  
✅ **Dependency resolution** - OS handles dependencies  
✅ **Enterprise-friendly** - Standard deployment method  
✅ **Container-ready** - Easy Docker/Podman integration  

---

## Supported Platforms

### Tier 1 (Full Support)
- ✅ RHEL 8, 9
- ✅ CentOS 8, 9
- ✅ Rocky Linux 8, 9
- ✅ AlmaLinux 8, 9
- ✅ Fedora 39, 40
- ✅ Ubuntu 20.04, 22.04, 24.04
- ✅ Debian 11, 12

### Tier 2 (Coming Soon)
- 🔄 FreeBSD 13, 14
- 🔄 OpenBSD 7.x
- 🔄 NetBSD 9, 10

### All Platforms
- ✅ Python pip (works everywhere)

---

## Building Custom Packages

See [PACKAGING.md](PACKAGING.md) for building custom RPM/DEB packages.
