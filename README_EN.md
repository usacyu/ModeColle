# ModeColle 🦙

<p align="center"><a href="README.md">日本語</a> ｜ <b>English</b></p>

**A Windows GUI tool for managing your Ollama models with just the mouse.**
Without memorizing any commands (typing into that scary black terminal window), you can
**list, inspect, delete, copy, rename, and edit the prompts** of your models — just pick one and click.

On top of that —

- 🌐 Push the same prompt to **OpenWebUI** in one click (solves the "prompt won't take effect" problem below)
- 📥 Import models you downloaded in **LM Studio** so they show up in the list
- 🎨 Spot **duplicate models** (identical contents) at a glance via color coding

![ModeColle screen](docs/screenshot-main.png)

---

## Try it in 30 seconds (Quick start)

> Assumes **Python** and **Ollama** are installed (→ see [How to install](#how-to-install) for details)

1. In Command Prompt, run `pip install customtkinter` **once**
2. **Double-click** `run.bat` to launch
3. **Click a model** in the left list → details (size, suggested use, built-in prompt) appear on the right
   — that alone already lets you read what's inside each model
4. From there, use the bottom-right buttons to **copy, rename, edit the prompt**, and so on

No commands, ever.

> 💡 Stuck? The **"❓ Help"** button in the header shows how to use the app, right inside it (JA / EN).
>
> ![In-app help](docs/screenshot-help.png)

---

## Why I made it — "I set the system prompt… so why isn't it working?" 🤔

If you've ever edited a model's system prompt in Ollama, opened OpenWebUI, and found your prompt **completely ignored** — you're not imagining it.

OpenWebUI (v0.4+) doesn't read the system prompt baked into an Ollama model. It keeps its **own** copy, in its **own** database. So your carefully written prompt just sits in Ollama, doing nothing.

I lost an evening to this. Even asking AI chatbots didn't surface the real reason. So I built **ModeColle** 🦙 — a small, free Windows tool that writes your system prompt to **both Ollama and OpenWebUI in one click**, so what you set is what you get.

---

## Table of Contents

- [What can it do?](#what-can-it-do)
- [What you need](#what-you-need)
- [How to install](#how-to-install)
- [How to launch](#how-to-launch)
- [Reading the screen](#reading-the-screen)
- [How to use the buttons](#how-to-use-the-buttons)
- [Import from LM Studio](#-import-from-lm-studio)
- [About OpenWebUI integration (important)](#about-openwebui-integration-important)
- [About duplicate-model color coding](#about-duplicate-model-color-coding)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Notes for publishing / distribution](#notes-for-publishing--distribution)

---

## What can it do?

| Feature | Description |
|---|---|
| 📋 **List view** | See all your installed models at a glance |
| 🔍 **Details** | Show size, hash, parameter count, quantization, and the built-in prompt |
| 🎯 **Auto use-case guess** | Suggests a "recommended use" based on the model name |
| 🎨 **Duplicate detection** | Color-codes models with identical contents (registered twice under different names) |
| 🗑️ **Delete** | Remove unwanted models with a confirmation step |
| 📋 **Copy** | Make another model with the same contents under a new name (no extra disk space used) |
| ✏️ **Rename** | Rename safely (backup → verify → swap) |
| 🆕 **Create variant** | Create a new model from an existing one with a new prompt |
| 🖊️ **Edit prompt** | Rewrite and overwrite the system prompt of the selected model |
| 📥 **LM Studio import** | Bring `.gguf` files downloaded in LM Studio into Ollama and the list |
| 🌐 **OpenWebUI sync** | Write the prompt to OpenWebUI as well, not just Ollama |
| ❓ **In-app help** | A "❓ Help" button in the header shows how to use the app on the spot (JA/EN) |
| 🗣️ **Japanese / English toggle** | Switch the UI language with one button in the header |

---

## What you need

| Requirement | Notes |
|---|---|
| **Windows** | Tested on Windows 10 / 11 |
| **Python 3.8+** | Install from [python.org](https://www.python.org/). `tkinter` is bundled with Python by default |
| **CustomTkinter** | Used to draw the UI. Run `pip install customtkinter` once (or use the bundled `requirements.txt`) |
| **Ollama** | Must be running on your PC (listening on `http://localhost:11434`) |
| **OpenWebUI** (optional) | Only needed if you use the sync feature. Everything else works without it |

> 💡 **Run `pip install customtkinter` once before the first launch.** This tool uses CustomTkinter to draw its UI (the standard `tkinter` ships with Python, so it needs no separate install).

---

## How to install

1. **Install Python**
   Download from [python.org](https://www.python.org/downloads/) and install it.
   Tick **"Add Python to PATH"** during setup — it makes everything smoother later.

2. **Install CustomTkinter**
   In Command Prompt (or PowerShell), run this once:
   ```
   pip install customtkinter
   ```
   (Or, using the bundled file: `pip install -r requirements.txt`)

3. **Install and start Ollama**
   Download from [ollama.com](https://ollama.com/), install it, and leave it running.

4. **Put this tool's folder wherever you like**
   You just need `ModeColle.py` and `run.bat` in the same folder.

5. **(Optional) Prepare a config file to use OpenWebUI sync**
   → See [About OpenWebUI integration](#about-openwebui-integration-important) for details.

---

## How to launch

Just double-click **`run.bat`** in the same folder. It starts `ModeColle.py` without showing a black console window.

Once it starts, it automatically begins loading your model list.

> 💡 If the window doesn't appear, make sure you ran `pip install customtkinter` (without it, the app exits silently).
> `run.bat` has a plain ASCII filename, so it launches fine even on systems that can't display Japanese.

---

## Reading the screen

The window has three parts: a **header on top**, a **model list on the left**, and **details on the right**.

### Top: Header

- **🦙 ModeColle** … the title
- **Status** … shows what it's doing right now (loading / success / error) in color
- **📥 Import** … imports LM Studio models into Ollama ([details here](#-import-from-lm-studio))
- **❓ Help** … shows how to use the app, inside the app
- **🌐 EN / 日本語** … toggles the UI language between Japanese and English (switches each time you press it)
- **🔄 Refresh** … reloads the list to the latest state
- **Legend (left side)**
  - 🌐 = a prompt is also set on the OpenWebUI side
  - colored rows = the same underlying model (duplicate contents)

### Left: Registered model list

| Column | Meaning |
|---|---|
| **Model name** | The name registered in Ollama |
| **WebUI** | If 🌐 is shown, a system prompt is also set on the OpenWebUI side |
| **Size** | Disk usage (GB / MB) |

Click a row to see detailed info on the right.

### Right: Model details

- 📛 **Full name**
- 💾 **Size**
- 🎯 **Recommended use** (auto-guessed from the name)
- 🌐 **OpenWebUI** (whether it's set)
- 🔑 **Hash** (the content identifier)
- 📋 **Built-in prompt** (the system prompt embedded in that model)

---

## How to use the buttons

The buttons are at the bottom right. **Select one model from the list first,** then click.

### 🖊️ Edit prompt
Rewrites and overwrites the system prompt of **the currently selected model itself**.
The name does not change. You can choose Ollama / OpenWebUI as the save target.

### 🆕 Create variant
Creates a **separate model** based on an existing one, with a new system prompt.

- Base model … the model to build on
- New model name … the name to create (e.g. `magnum-v2-SD:latest`)
- Save target … see [OpenWebUI integration](#about-openwebui-integration-important)
- System prompt … the instruction text you want to give it

### 📋 Copy
Makes **another model under a different name** with the same contents.
The contents are shared, so **disk usage barely increases** (it just references the same data under a new name).
You'll be asked for the new name (e.g. `magnum-v2-SD:latest`).

### ✏️ Rename
Renames a model. Ollama has no direct "rename" feature, so internally it runs this safe sequence automatically:

1. Copy to a backup name first
2. Delete the original
3. Copy the backup to the new name
4. Delete the backup once verified

If something fails midway, the backup remains so you don't lose data.

### 🗑️ Delete
Deletes the selected model. A confirmation dialog appears. **This cannot be undone,** so be careful.

---

## 📥 Import from LM Studio

Models you downloaded in LM Studio (`.gguf` files) **don't show up in ModeColle (i.e. Ollama) on their own.**
LM Studio and Ollama are separate apps with separate storage, so pressing "🔄 Refresh" won't surface them.

Press **"📥 Import"** in the header and ModeColle **scans your LM Studio folder automatically**, listing what it finds as a checklist.
Tick the ones you want and press **"📥 Import"** — they get imported into Ollama and appear in the list.
A name is suggested automatically and is **editable on the spot** (e.g. `qwen3-coder:q4_k_m`).

> ⚠️ **About disk usage (how it differs from "📋 Copy")**
> - **"📋 Copy"** just points to the **same data under a new name** inside Ollama, so it barely uses extra space.
> - **"📥 Import"** brings an **external file into Ollama as real data**, so it uses disk for the whole model.
>   The original file also stays in LM Studio, so the same model ends up stored in two places.

---

## About OpenWebUI integration (important)

### Why does this feature exist?

**OpenWebUI (v0.4 and later) ignores the system prompt embedded in an Ollama model.**

In other words, even if you correctly save a prompt to Ollama with ModeColle (or with commands),
**it does not show up at all in OpenWebUI's chat.**
To make a prompt take effect in OpenWebUI, you have to write it into OpenWebUI's own setting
(the system prompt field in the admin panel).

To resolve this mismatch, ModeColle lets you **write to both Ollama and OpenWebUI from the same screen.**

### Save-target checkboxes

The "🆕 Create variant" and "🖊️ Edit prompt" dialogs have checkboxes to choose where to save:

- ☑ **Save to Ollama**
- ☑ **Also apply to OpenWebUI**

Check both and save, and it writes to **both in a single action.**
(It processes Ollama → OpenWebUI in order, and if one fails it still reports the other's result clearly.)

> In "Create variant" (new creation), saving to Ollama is mandatory,
> so "Save to Ollama" is always ON (shown grayed out).

### Models brand-new to OpenWebUI are registered automatically

OpenWebUI treats any model you've never touched in its admin panel as an "unknown model."
Because of this, you previously had to **manually save the model once in the OpenWebUI admin panel**
before sending it a prompt for the first time (a so-called "first-time registration").

**ModeColle automates this step.**
If the model you're saving doesn't exist on the OpenWebUI side yet, ModeColle registers it automatically
and then writes the prompt. You don't need to open the admin panel to prepare anything.
Just check the box and save — done.

> 💡 **Saved it, but it doesn't show up in OpenWebUI? → Refresh the page with F5 ♡**
> OpenWebUI's web page does **not automatically re-display** content written by an external tool like ModeColle.
> The moment ModeColle saves it and 🌐 appears, the data is already inside OpenWebUI.
> To check the contents in the admin panel, **reload the page (F5, or reopen the model)**
> and the latest content will be there.

### Automatic name tags (when creating new)

When you **create a new** model via "Create variant," a **mandatory marker tag** is appended to the name
so you can tell at a glance "which side was this made for?" later.

| Save target | Tag added | Example |
|---|---|---|
| Ollama only | `-OLM` | `magnum-v2-OLM:latest` |
| OpenWebUI only | `-OWU` | `magnum-v2-OWU:latest` |
| Both | `-OWU-OLM` | `magnum-v2-OWU-OLM:latest` |

Names that already have a tag like `:latest` are handled too — the marker goes **before** the colon.

> "🖊️ Edit prompt" (overwriting an existing model) **does not change the name,**
> because changing the name could make OpenWebUI lose track of that model.
> Instead, a 🌐 appears in the **WebUI column** of the list to show it's been set.

### Setup (when using the integration)

To use the integration, create an **`openwebui_config.json`** in the same folder as the tool:

```json
{
  "base_url": "http://localhost:3000",
  "api_key": "sk-your-api-key-here"
}
```

- **base_url** … the address of your OpenWebUI (e.g. `http://localhost:3000`)
- **api_key** … an API key issued by OpenWebUI

**How to issue an API key (on the OpenWebUI side):**
Settings → Account → API Keys.

> ⚠️ **If your API key is rejected with a 403 error:**
> Check whether "**API Key Endpoint Restrictions**" is ON under Admin Panel → Settings → General.
> When it's ON, external access is restricted. Turning it OFF resolves the issue.

> 🔒 **`openwebui_config.json` contains your secret key.**
> **Never hand it to anyone or publish it online.**
> (For protection when publishing, see [Notes for publishing / distribution](#notes-for-publishing--distribution).)

---

## About duplicate-model color coding

You can accidentally register the same AI model twice under different names (a waste of disk space).

ModeColle gives rows with the **same hash (content identifier) the same background color** to point this out.
Rows sharing a color have "identical contents = duplicates." Delete the one you don't need to tidy up.

The status bar at the bottom also shows a count like "Duplicate groups: N."

---

## FAQ / Troubleshooting

**Q. It closes immediately when I launch it / the window doesn't appear**
A. Make sure you ran `pip install customtkinter`. `run.bat` launches without a console window, so if the library is missing the app just exits quietly. You can verify Python itself with `python --version`.

**Q. I want the screen in English / back to Japanese**
A. Press the **🌐 button** in the header (labeled "EN" or "日本語") to toggle the UI language.

**Q. I forgot how to use it**
A. Press the **"❓ Help"** button in the header — the usage guide appears inside the app (JA / EN).

**Q. It says "Connection error" / no models show up**
A. Check that Ollama is running (`http://localhost:11434`).

**Q. My LM Studio models don't appear in the list**
A. Import them via **"📥 Import"** in the header. "🔄 Refresh" alone won't show them (LM Studio and Ollama are separate). See [Import from LM Studio](#-import-from-lm-studio).

**Q. 🌐 doesn't appear / it's not reflected in OpenWebUI**
A. Check the following:
- Is `openwebui_config.json` created correctly?
- Is the API key valid? (For 403, check "Endpoint Restrictions" above)
- Does the model exist in Ollama? (ModeColle handles registering it on the OpenWebUI side automatically)

**Q. I saved with ModeColle and 🌐 appeared, but the OpenWebUI screen looks empty**
A. **Reload the OpenWebUI page with F5 ♡**
OpenWebUI's web page does not automatically reflect changes written from outside by ModeColle (a stale view remains).
If 🌐 is showing, the data is already saved in OpenWebUI. Reopen the page and it will display properly.

**Q. Can I use it without OpenWebUI?**
A. Yes. Everything except the integration (list / delete / copy / rename / create variant / prompt editing / LM Studio import)
works without `openwebui_config.json`.

**Q. The rename failed midway**
A. A backup (`originalname_backup`) may remain. Your data is not lost,
so refresh the list and check the state.

---

## Notes for publishing / distribution

When you hand this tool to someone or publish it online, **do not distribute the following file:**

- ❌ **`openwebui_config.json`** … it contains your OpenWebUI address and your **secret API key**

This repository includes a **`.gitignore`** to prevent accidental publication, and an
**`openwebui_config.example.json`** as a template for others to create their settings.
Whoever receives it should copy the example to make their own `openwebui_config.json` and fill in their own key.

---

🦙 *ModeColle — making Ollama × OpenWebUI prompt management simpler.*
