# 🔧 Predictive Maintenance for Coiled Evaporators

> **Bachelor's Thesis** · Mechanical Engineering · Xavier University

---

## 💡 The Idea

Monitor aircon evaporator health in real time. Sensor data flows from ESP32 nodes through ESP-NOW to a TFT touchscreen, then up to the cloud. Machine learning models predict maintenance needs before failure hits.

---

## ⚡ How It Works

```
  🌡️ Sensors          📡 ESP-NOW           🖥️ TFT + ☁️ Cloud
  ┌──────────┐       ┌──────────┐        ┌──────────────┐
  │ BME280   │──────►│  Sender  │───────►│   Receiver   │
  │ DS18B20  │       │  ESP32   │  P2P   │  ESP32 + TFT │──► Supabase
  │ ×3 probes│       └──────────┘        └──────────────┘
  └──────────┘
```

**Ambient readings** (temp + humidity) + **3 probe temperatures** → calibrated → wireless → displayed + logged.

---

## 🗂️ Repo Map

```
thesis/
│
├── 📄 Thesis Proposal.pdf
│
├── 📂 codes/
│   ├── 📂 prototyping/                 # Final integrated builds
│   │   ├── ambient_module_final/       # Sensor fusion (BME280 + probes)
│   │   ├── now_ambient_sender/         # Wireless data transmitter
│   │   ├── now_receiver_supabase/      # Receiver + cloud pipeline
│   │   └── tft_complete/               # Display firmware (main UI)
│   │
│   ├── 📂 testing/                     # Component experiments
│   │   ├── BME280/  DS18B20/  probes/  i2c_scanner/
│   │   ├── now_sender/  now_receiver/  supabase/
│   │   ├── tft_display/  tft_touch/  tft_ui_demo/
│   │   └── ...                         # 15+ test sketches
│   │
│   └── 📂 python/machine learning/     # Classification experiments
│       ├── 0 perceptron.py
│       ├── 1 logistic_regression.py
│       ├── 2 SVM.py
│       ├── 3 dec_tree.py
│       ├── 4 random_forest.py
│       ├── 5 knn_classifier.py
│       └── pre-processing/
│
├── 📂 schematics/                      # Fritzing — circuits & PCBs
├── 📂 designs/                         # UI mockups, palette, fonts
└── 📂 resources/
```

---

## 🔌 Hardware

| Part | Interface | What It Does |
|------|-----------|--------------|
| ESP32-C3 Super Mini | — | Brains of the operation |
| BME280 | I2C (`0x76`) | Ambient temp + humidity |
| DS18B20 ×3 | OneWire (GPIO10) | Submerged probe temps |
| ST7789 240×320 TFT | SPI | Color display |
| XPT2046 | SPI (shared CLK) | Touch input |

### Calibration

```
BME280 Temp      →  raw × 1.0294412
BME280 Humidity  →  raw × 1.0579399
Probe A          →  1.701471 + 0.984997 × raw
Probe B / C      →  1.637417 + 0.9783362 × raw
```

---

## 🧠 Machine Learning

Six classifiers trained on sensor data — from classic Perceptron to Random Forest:

| # | Script | Model |
|---|--------|-------|
| 0 | `0 perceptron.py` | Perceptron |
| 1 | `1 logistic_regression.py` | Logistic Regression |
| 2 | `2 SVM.py` | Support Vector Machine |
| 3 | `3 dec_tree.py` | Decision Tree |
| 4 | `4 random_forest.py` | Random Forest |
| 5 | `5 knn_classifier.py` | K-Nearest Neighbors |

### Spin Up the Python Env

```bash
cd codes/python/machine learning

python -m venv .venv
# PowerShell:  .venv\Scripts\Activate.ps1
# Git Bash:    source .venv/Scripts/activate

pip install numpy matplotlib scikit-learn pandas

# Need deep learning later? Add PyTorch with CUDA:
pip install torch --index-url https://download.pytorch.org/whl/cu130
```

---

## 📐 Design

The TFT UI follows a **mobile-app navigation pattern** — persistent bottom bar, center arrow for a full-screen menu. Iron Grey palette with light/dark mode. Lora + Montserrat typography.

**Pages:** Main Menu → Pairing → Devices → Units → System

> Full mockups, palette shades, and component specs in `designs/tft_display/design_readme.md`.

---

## 🚀 Quick Start

**Firmware (Arduino)**
```bash
# 1. Arduino IDE + ESP32 board support
# 2. Install: TFT_eSPI, OneWire, DallasTemperature, Adafruit_BME280, esp_now, ESPSupabase
# 3. Open codes/prototyping/now_ambient_sender/
# 4. Board → ESP32-C3 Super Mini → Flash
```

**ML (Python)**
```bash
cd codes/python/machine learning
python -m venv .venv && source .venv/Scripts/activate
pip install numpy matplotlib scikit-learn pandas
python 0 perceptron.py
```

---

---

## 🛠️ Installation

**Git**
- Linux (Debian/Ubuntu): `sudo apt install git`
- macOS: `brew install git` or download from [git-scm.com](https://git-scm.com)
- ChromeOS: enable Linux (Crostini), then `sudo apt install git`
- Windows: download from [git-scm.com](https://git-scm.com)
- Verify: `git --version`

---

## ⚙️ Git Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
git config --global init.defaultBranch main
```

- If using GitHub's privacy feature, use the provided private email: `username@users.noreply.github.com`
- Verify: `git config --global user.name` and `git config --global user.email`
- **macOS:** ignore `.DS_Store` files globally to prevent metadata files from appearing in commits:

```bash
echo ".DS_Store" >> ~/.gitignore_global
git config --global core.excludesFile ~/.gitignore_global
```

---

## 🌐 GitHub Account Setup

- Use a **real email** — required for contribution tracking
- Enable privacy settings: keep email private, block CLI pushes that expose personal email
- Enable **2FA** using a TOTP app (Google Authenticator, Authy, etc.)
  - ⚠️ **Warning:** losing 2FA credentials **and** recovery codes means permanent account lockout — GitHub Support cannot restore access

---

## 🔑 SSH Key Authentication

Check for an existing key:

```bash
ls ~/.ssh/id_ed25519.pub
```

Generate a new Ed25519 key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- Press Enter to accept the default location
- Optional: set a passphrase for extra security

Copy the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

It starts with `ssh-ed25519` and ends with `username@hostname`.

**Add to GitHub:**
1. Settings → SSH and GPG keys → New SSH Key
2. Paste the public key as an **Authentication Key**

Test the connection:

```bash
ssh -T git@github.com
```

- Success: `"Hi username! You've successfully authenticated, but GitHub does not provide shell access."`
- Failure: retry or ask for help in TOP Discord

Multiple SSH keys can be linked to one GitHub account — one per machine.

---

*Built with ☕ and late nights by **Kira (JRon)** · JPSME-XUC · Xavier University*
