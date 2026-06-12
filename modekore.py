#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""もでコレ - Ollama モデル管理ツール / Ollama model manager (JA/EN)"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import urllib.request
import urllib.error
import json
import os
import threading

OLLAMA_BASE = "http://localhost:11434"
OPENWEBUI_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openwebui_config.json")

# ── 言語 / Language ───────────────────────────────────────────────────────
LANG = "ja"  # "ja" or "en"

TR = {
    "ja": {
        "app_title": "もでコレ 🦙",
        "brand": "🦙 もでコレ",
        "lang_button": "🌐 EN",
        "refresh": "🔄 更新",
        "legend_dup": "■ 同じハッシュ = 同じ実体（重複）",
        "legend_owui": "🌐 = OpenWebUI側にもプロンプト設定済み",
        "list_title": "登録モデル一覧",
        "col_name": "モデル名",
        "col_size": "容量",
        "col_hash": "ハッシュ(先頭12)",
        "col_owui": "WebUI",
        "btn_delete": "🗑️ 削除",
        "btn_copy": "📋 コピー",
        "btn_rename": "✏️ リネーム",
        "btn_derive": "🆕 派生登録",
        "btn_edit": "🖊️ プロンプト編集",
        "detail_title": "モデル詳細",
        "lbl_name": "📛 正式名称",
        "lbl_size": "💾 容量",
        "lbl_hash": "🔑 ハッシュ",
        "lbl_usecase": "🎯 おすすめ用途",
        "lbl_info": "📊 モデル情報",
        "lbl_embedded": "📋 組み込みプロンプト",
        "status_loading": "モデル一覧を取得中...",
        "status_conn_error": "接続エラー: {e}",
        "status_count": "{n} 個のモデル",
        "status_dup": "  ／  重複グループ: {n} 件",
        "loading": "読み込み中...",
        "fetching": "（取得中...）",
        "no_info": "情報なし",
        "fetch_failed": "取得失敗: {e}",
        "info_family": "ファミリー: {v}",
        "info_params": "パラメータ: {v}",
        "info_quant": "量子化: {v}",
        "info_format": "形式: {v}",
        "sys_header": "【SYSTEMプロンプト】\n{v}",
        "no_system": "（システムプロンプトなし）",
        "use_default": "📦 汎用モデル",
        # dialog
        "dlg_base": "ベースモデル",
        "dlg_base_auto": "ベースモデル（自動）",
        "dlg_newname": "新しいモデル名（例: magnum-v2-SD:latest）",
        "dlg_dest": "保存先",
        "dlg_to_ollama": "Ollamaに保存",
        "dlg_to_owui": "OpenWebUIにも反映する",
        "dlg_lock_note": "（新規作成にはOllamaへの保存が必須のため、ここは常にON）",
        "dlg_system": "システムプロンプト",
        "dlg_system_hint": "（空白のままにするとプロンプトなしで登録）",
        "dlg_ok": "✅ 登録する",
        "dlg_cancel": "キャンセル",
        "warn_input": "入力不足",
        "warn_select": "選択不足",
        "warn_need_base": "ベースモデルを選択してください。",
        "warn_need_name": "新しいモデル名を入力してください。",
        "warn_need_dest": "保存先を1つ以上選んでください。",
        "title_derive": "🆕 派生モデル登録",
        "title_edit": "🖊️ プロンプト編集 - {name}",
        "edit_unselected": "編集するモデルを選んでください。",
        "fetch_error_title": "取得エラー",
        "fetch_failed_status": "取得失敗",
        # save
        "saving": "「{name}」を保存中...",
        "saving_ollama": "Ollamaに保存中: {s}",
        "saving_owui": "OpenWebUIに反映中...",
        "save_partial_title": "「{name}」の保存で一部エラー",
        "save_ok_line": "✅ 成功: {oks}\n\n",
        "save_fail_body": "{ok}❌ 失敗:\n{detail}",
        "save_partial": "⚠️ 「{name}」: 一部失敗（成功: {oks}）",
        "save_done": "✅ 「{name}」を保存しました（{oks}）",
        "none": "なし",
        # delete
        "unselected": "未選択",
        "del_unselected": "削除するモデルを選んでください。",
        "del_confirm_title": "削除確認",
        "del_confirm": "「{name}」を削除しますか？\n\nこの操作は取り消せません。",
        "deleting": "削除中...",
        "del_done": "「{name}」を削除しました",
        "del_error_title": "削除エラー",
        "del_failed": "削除失敗",
        # copy
        "copy_unselected": "コピー元のモデルを選んでください。",
        "copy_title": "コピー先の名前",
        "copy_prompt": "「{name}」のコピー先の名前を入力してください。\n形式例:  magnum-v2-SD:latest\n\n※ 容量は増えません（同じファイルを別名で参照するだけ）",
        "nochange_title": "変更なし",
        "nochange": "元の名前と同じです。",
        "copying": "コピー中...",
        "copy_done": "✅ 「{a}」→「{b}」コピー完了",
        "copy_error_title": "コピーエラー",
        "copy_failed": "コピー失敗",
        # rename
        "rename_unselected": "リネームするモデルを選んでください。",
        "rename_title": "新しいモデル名",
        "rename_prompt": "「{name}」の新しい名前を入力してください。\n形式例:  MyModel:latest  または  MyModel:v2",
        "rename_confirm_title": "リネーム確認",
        "rename_confirm": "以下の手順でリネームします：\n\n  ① 「{o}」→「{b}」へバックアップ\n  ② 「{o}」を削除\n  ③ 「{b}」→「{n}」へリネーム\n  ④ 動作確認後、バックアップを削除",
        "rn_step1": "① バックアップ作成中...",
        "rn_step2": "② 元モデルを削除中...",
        "rn_step3": "③ 新しい名前でコピー中...",
        "rn_step4": "④ 動作確認中...",
        "rn_check_fail": "新モデルの確認ができませんでした",
        "rn_done": "✅ 完了！「{o}」→「{n}」",
        "rename_error_title": "リネームエラー",
        "rename_error_body": "{e}\n\nバックアップ「{b}」が残っている場合があります。",
        "rename_failed": "リネーム失敗",
    },
    "en": {
        "app_title": "Modekore 🦙",
        "brand": "🦙 Modekore",
        "lang_button": "🌐 日本語",
        "refresh": "🔄 Refresh",
        "legend_dup": "■ Same hash = same data (duplicate)",
        "legend_owui": "🌐 = Prompt also set on OpenWebUI",
        "list_title": "Installed models",
        "col_name": "Model name",
        "col_size": "Size",
        "col_hash": "Hash (first 12)",
        "col_owui": "WebUI",
        "btn_delete": "🗑️ Delete",
        "btn_copy": "📋 Copy",
        "btn_rename": "✏️ Rename",
        "btn_derive": "🆕 New / Derive",
        "btn_edit": "🖊️ Edit prompt",
        "detail_title": "Model details",
        "lbl_name": "📛 Full name",
        "lbl_size": "💾 Size",
        "lbl_hash": "🔑 Hash",
        "lbl_usecase": "🎯 Suggested use",
        "lbl_info": "📊 Model info",
        "lbl_embedded": "📋 Embedded prompt",
        "status_loading": "Loading model list...",
        "status_conn_error": "Connection error: {e}",
        "status_count": "{n} models",
        "status_dup": "   /   duplicate groups: {n}",
        "loading": "Loading...",
        "fetching": "(loading...)",
        "no_info": "No info",
        "fetch_failed": "Failed to load: {e}",
        "info_family": "Family: {v}",
        "info_params": "Params: {v}",
        "info_quant": "Quantization: {v}",
        "info_format": "Format: {v}",
        "sys_header": "[SYSTEM PROMPT]\n{v}",
        "no_system": "(no system prompt)",
        "use_default": "📦 General-purpose model",
        # dialog
        "dlg_base": "Base model",
        "dlg_base_auto": "Base model (auto)",
        "dlg_newname": "New model name (e.g. magnum-v2-SD:latest)",
        "dlg_dest": "Save to",
        "dlg_to_ollama": "Save to Ollama",
        "dlg_to_owui": "Also apply to OpenWebUI",
        "dlg_lock_note": "(Saving to Ollama is required for new models, so this stays ON.)",
        "dlg_system": "System prompt",
        "dlg_system_hint": "(Leave blank to register with no prompt.)",
        "dlg_ok": "✅ Save",
        "dlg_cancel": "Cancel",
        "warn_input": "Missing input",
        "warn_select": "Nothing selected",
        "warn_need_base": "Please choose a base model.",
        "warn_need_name": "Please enter a new model name.",
        "warn_need_dest": "Please choose at least one destination.",
        "title_derive": "🆕 Register derived model",
        "title_edit": "🖊️ Edit prompt - {name}",
        "edit_unselected": "Please select a model to edit.",
        "fetch_error_title": "Load error",
        "fetch_failed_status": "Load failed",
        # save
        "saving": "Saving \"{name}\"...",
        "saving_ollama": "Saving to Ollama: {s}",
        "saving_owui": "Applying to OpenWebUI...",
        "save_partial_title": "Some errors while saving \"{name}\"",
        "save_ok_line": "✅ Success: {oks}\n\n",
        "save_fail_body": "{ok}❌ Failed:\n{detail}",
        "save_partial": "⚠️ \"{name}\": partly failed (success: {oks})",
        "save_done": "✅ Saved \"{name}\" ({oks})",
        "none": "none",
        # delete
        "unselected": "Nothing selected",
        "del_unselected": "Please select a model to delete.",
        "del_confirm_title": "Confirm delete",
        "del_confirm": "Delete \"{name}\"?\n\nThis cannot be undone.",
        "deleting": "Deleting...",
        "del_done": "Deleted \"{name}\"",
        "del_error_title": "Delete error",
        "del_failed": "Delete failed",
        # copy
        "copy_unselected": "Please select a model to copy.",
        "copy_title": "Copy target name",
        "copy_prompt": "Enter the name for the copy of \"{name}\".\nExample:  magnum-v2-SD:latest\n\n* No extra disk use (it just references the same file under a new name).",
        "nochange_title": "No change",
        "nochange": "Same as the original name.",
        "copying": "Copying...",
        "copy_done": "✅ Copied \"{a}\" -> \"{b}\"",
        "copy_error_title": "Copy error",
        "copy_failed": "Copy failed",
        # rename
        "rename_unselected": "Please select a model to rename.",
        "rename_title": "New model name",
        "rename_prompt": "Enter the new name for \"{name}\".\nExample:  MyModel:latest  or  MyModel:v2",
        "rename_confirm_title": "Confirm rename",
        "rename_confirm": "Rename in these safe steps:\n\n  1. Back up: \"{o}\" -> \"{b}\"\n  2. Delete \"{o}\"\n  3. Rename: \"{b}\" -> \"{n}\"\n  4. After verifying, delete the backup",
        "rn_step1": "1. Creating backup...",
        "rn_step2": "2. Deleting original...",
        "rn_step3": "3. Copying to new name...",
        "rn_step4": "4. Verifying...",
        "rn_check_fail": "Could not verify the new model",
        "rn_done": "✅ Done! \"{o}\" -> \"{n}\"",
        "rename_error_title": "Rename error",
        "rename_error_body": "{e}\n\nThe backup \"{b}\" may still remain.",
        "rename_failed": "Rename failed",
    },
}


def t(key, **kw):
    s = TR.get(LANG, TR["ja"]).get(key) or TR["ja"].get(key, key)
    return s.format(**kw) if kw else s


# モデル名キーワード → 用途（言語別）/ model-name keyword -> use case (per language)
USE_CASES = {
    "maine":     {"ja": "🗣️ 日常会話メイン・日本語お姉さんキャラ・こふでくんサポート",
                  "en": "🗣️ Everyday conversation / friendly assistant persona"},
    "magnum":    {"ja": "✍️ クリエイティブライティング・ストーリー・キャラクター会話・プロンプト生成",
                  "en": "✍️ Creative writing / stories / character chat / prompt generation"},
    "lumimaid":  {"ja": "💬 チャット・ロールプレイ・創作会話・完全フリー",
                  "en": "💬 Chat / role-play / creative dialogue / fully unfiltered"},
    "noob":      {"ja": "🎨 NoobAI向けプロンプト生成・Danbooruタグ形式",
                  "en": "🎨 NoobAI prompt generation / Danbooru tag format"},
    "sd":        {"ja": "🖼️ Stable Diffusion プロンプト生成・画像生成支援",
                  "en": "🖼️ Stable Diffusion prompt generation / image-gen support"},
    "qwen":      {"ja": "🌐 日常会話・テキスト生成・翻訳・多言語対応",
                  "en": "🌐 Everyday chat / text generation / translation / multilingual"},
    "llama":     {"ja": "🤖 汎用テキスト生成・質問応答・コード補助",
                  "en": "🤖 General text generation / Q&A / coding help"},
    "mistral":   {"ja": "🧠 汎用テキスト生成・コード生成・論理的推論",
                  "en": "🧠 General text / code generation / logical reasoning"},
    "codellama": {"ja": "💻 プログラミング支援・コード生成・デバッグ",
                  "en": "💻 Programming help / code generation / debugging"},
    "phi":       {"ja": "⚡ 軽量・高速タスク・要約・簡単な質問応答",
                  "en": "⚡ Lightweight / fast tasks / summaries / simple Q&A"},
    "gemma":     {"ja": "🔍 汎用会話・テキスト分析・Google系モデル",
                  "en": "🔍 General chat / text analysis / Google models"},
    "deepseek":  {"ja": "🧮 数学・コーディング・論理推論",
                  "en": "🧮 Math / coding / logical reasoning"},
    "dolphin":   {"ja": "🐬 無検閲・フリースタイル会話",
                  "en": "🐬 Uncensored / free-style conversation"},
    "stheno":    {"ja": "💬 キャラクター会話・ロールプレイ",
                  "en": "💬 Character chat / role-play"},
    "nemomix":   {"ja": "✨ 創作・フリースタイル・無検閲",
                  "en": "✨ Creative / free-style / uncensored"},
    "goonsai":   {"ja": "🔞 成人向け・無検閲会話",
                  "en": "🔞 Adult / uncensored conversation"},
    "abliterat": {"ja": "🔓 制限解除モデル・フリースタイル",
                  "en": "🔓 Restriction-removed model / free-style"},
}

DUP_COLORS = ["#3b3f6e", "#3b5e4a", "#5e3b3b", "#5e563b", "#4a3b5e"]


def get_use_case(model_name: str) -> str:
    name_lower = model_name.lower()
    for key, desc in USE_CASES.items():
        if key in name_lower:
            return desc.get(LANG, desc["ja"])
    return t("use_default")


def fmt_size(b: int) -> str:
    if b >= 1_000_000_000:
        return f"{b / 1_000_000_000:.2f} GB"
    elif b >= 1_000_000:
        return f"{b / 1_000_000:.1f} MB"
    return f"{b / 1_000:.0f} KB"


def short_hash(digest: str) -> str:
    h = digest.replace("sha256:", "")
    return h[:12] if h else "—"


def ollama_get(path: str):
    url = OLLAMA_BASE + path
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def ollama_post(path: str, data: dict):
    url = OLLAMA_BASE + path
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        content = r.read()
        return json.loads(content) if content.strip() else {}


def ollama_create(model: str, from_model: str, system: str = "", on_progress=None):
    """モデル作成（新API形式: model/from/system）"""
    url = OLLAMA_BASE + "/api/create"
    data = {"model": model, "from": from_model, "stream": True}
    if system:
        data["system"] = system
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        for line in r:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                status = obj.get("status", "")
                if on_progress:
                    on_progress(status)
                if "error" in obj:
                    raise RuntimeError(obj["error"])
            except json.JSONDecodeError:
                pass


def ollama_delete(path: str, data: dict):
    url = OLLAMA_BASE + path
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="DELETE",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status


# ── OpenWebUI 連携 ────────────────────────────────────────────────────────
_openwebui_cfg = None


def load_openwebui_config() -> dict:
    """openwebui_config.json を読み込む（base_url・api_keyを保持。一度読んだらキャッシュ）"""
    global _openwebui_cfg
    if _openwebui_cfg is None:
        with open(OPENWEBUI_CONFIG_PATH, encoding="utf-8") as f:
            _openwebui_cfg = json.load(f)
    return _openwebui_cfg


def _openwebui_request(path: str, method: str = "GET", data=None):
    cfg = load_openwebui_config()
    headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(cfg["base_url"].rstrip("/") + path,
                                 data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read()
        return json.loads(raw) if raw.strip() else {}


def openwebui_get_base_models() -> list:
    """OpenWebUI上の「ベースモデル」一覧を取得（各要素の params.system にプロンプト本体が入る）"""
    data = _openwebui_request("/api/v1/models/base")
    return data if isinstance(data, list) else data.get("data", [])


def openwebui_find_model(model_id: str, models: list = None):
    """id（= Ollama側のモデル名と一致）でエントリを探す"""
    if models is None:
        models = openwebui_get_base_models()
    return next((m for m in models if m.get("id") == model_id), None)


def openwebui_create_model(model_id: str, system: str):
    """OpenWebUI側に未登録のモデルを新規作成する（＝以前は手動だった「初回登録」を自動化）。
    最小ペイロード（id/name/meta/params）で送れば、サーバー側が他フィールドを補完してくれる。
    base_model_id=None ＝ Ollamaのモデルに直結する「ベースモデル」として登録。"""
    payload = {
        "id": model_id,
        "name": model_id,
        "base_model_id": None,
        "meta": {},
        "params": {"system": system},
    }
    return _openwebui_request("/api/v1/models/create", method="POST", data=payload)


def openwebui_update_system_prompt(model_id: str, system: str):
    """OpenWebUI側のsystemプロンプトを書き込む。
    ・既存 → ① 全データ取得 → ② params.system だけ書き換え → ③ 丸ごと送信（他フィールドを壊さない）
    ・未登録 → 自動で新規作成（手動の初回登録＝ハンドシェイクが不要に）"""
    target = openwebui_find_model(model_id)
    if target is None:
        # OpenWebUI側にまだレコードが無い → 自動作成して登録
        return openwebui_create_model(model_id, system)
    target = dict(target)
    params = dict(target.get("params") or {})
    params["system"] = system
    target["params"] = params
    return _openwebui_request("/api/v1/models/model/update", method="POST", data=target)


# ── カラーパレット (Catppuccin Mocha) ─────────────────────────────────────
BG      = "#1e1e2e"
SURFACE = "#313244"
OVERLAY = "#45475a"
TEXT    = "#cdd6f4"
SUBTEXT = "#bac2de"
BLUE    = "#89b4fa"
GREEN   = "#a6e3a1"
YELLOW  = "#f9e2af"
RED     = "#f38ba8"
MAUVE   = "#cba6f7"
TEAL    = "#94e2d5"
PEACH   = "#fab387"
PINK    = "#f5c2e7"


class ModelfileEditor(tk.Toplevel):
    """派生登録・プロンプト編集 共通ダイアログ"""

    def __init__(self, parent, title: str, model_names: list,
                 default_base: str = "", default_name: str = "",
                 default_prompt: str = "", on_save=None, base_readonly: bool = False,
                 lock_to_ollama: bool = False):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.geometry("720x620")
        self.minsize(600, 500)
        self.resizable(True, True)
        self.grab_set()  # モーダル

        self.on_save = on_save
        self.result = None

        self._build(model_names, default_base, default_name, default_prompt,
                    base_readonly, lock_to_ollama)

    def _lbl(self, parent, text, fg=TEXT, font=None, **kw):
        return tk.Label(parent, text=text, bg=BG, fg=fg,
                        font=font or ("Yu Gothic UI", 10), **kw)

    def _chk(self, parent, text, var, enabled=True):
        cb = tk.Checkbutton(
            parent, text=text, variable=var,
            bg=BG, fg=TEXT, selectcolor=SURFACE,
            activebackground=BG, activeforeground=TEXT,
            font=("Yu Gothic UI", 10), relief="flat",
            highlightthickness=0
        )
        if not enabled:
            cb.configure(state="disabled")
        return cb

    def _build(self, model_names, default_base, default_name, default_prompt,
               base_readonly=False, lock_to_ollama=False):
        s = ttk.Style()
        s.configure("DlgOK.TButton",     background=GREEN,  foreground=BG, padding=(10, 5))
        s.map("DlgOK.TButton",           background=[("active", TEAL)])
        s.configure("DlgCancel.TButton", background=OVERLAY, foreground=TEXT, padding=(10, 5))
        s.map("DlgCancel.TButton",       background=[("active", "#585b70")])

        # ボタンを先にbottomで確保（expand=Trueのウィジェットに押し出されないように）
        btn_row = ttk.Frame(self)
        btn_row.pack(side="bottom", fill="x", padx=16, pady=12)
        ttk.Button(btn_row, text=t("dlg_ok"), style="DlgOK.TButton",
                   command=self._ok).pack(side="right", padx=(6, 0))
        ttk.Button(btn_row, text=t("dlg_cancel"), style="DlgCancel.TButton",
                   command=self.destroy).pack(side="right")

        # ベースモデル選択
        row1 = ttk.Frame(self)
        row1.pack(fill="x", padx=16, pady=(12, 4))
        self._base_readonly = base_readonly
        self._base_fixed = default_base  # readonly時はこの値を使う
        if base_readonly:
            self._lbl(row1, t("dlg_base_auto"), fg=BLUE,
                      font=("Yu Gothic UI", 10, "bold")).pack(anchor="w")
            self._lbl(row1, default_base[:90] + ("..." if len(default_base) > 90 else ""),
                      fg=SUBTEXT, font=("Yu Gothic UI", 9)).pack(anchor="w", pady=(2, 0))
            self.cb = None
        else:
            self._lbl(row1, t("dlg_base"), fg=BLUE,
                      font=("Yu Gothic UI", 10, "bold")).pack(anchor="w")
            self.cb = ttk.Combobox(row1, values=model_names, state="readonly", width=50)
            self.cb.pack(fill="x", pady=(4, 0))
            # 描画完了後に選択を反映（after で遅延させないと表示されない）
            if default_base in model_names:
                idx = model_names.index(default_base)
                self.after(50, lambda: self.cb.current(idx))

        # 新しいモデル名
        row2 = ttk.Frame(self)
        row2.pack(fill="x", padx=16, pady=(0, 8))
        self._lbl(row2, t("dlg_newname"), fg=BLUE,
                  font=("Yu Gothic UI", 10, "bold")).pack(anchor="w")
        self.name_var = tk.StringVar(value=default_name)
        tk.Entry(row2, textvariable=self.name_var, bg=SURFACE, fg=TEXT,
                 insertbackground=TEXT, relief="flat", font=("Yu Gothic UI", 10),
                 width=50).pack(fill="x", pady=(4, 0))

        # 保存先（Ollama / OpenWebUI）
        row_dest = ttk.Frame(self)
        row_dest.pack(fill="x", padx=16, pady=(0, 8))
        self._lbl(row_dest, t("dlg_dest"), fg=BLUE,
                  font=("Yu Gothic UI", 10, "bold")).pack(anchor="w")

        self.var_to_ollama    = tk.BooleanVar(value=True)
        self.var_to_openwebui = tk.BooleanVar(value=False)
        self._lock_to_ollama  = lock_to_ollama

        dest_row = ttk.Frame(row_dest)
        dest_row.pack(fill="x", pady=(2, 0))
        self._chk(dest_row, t("dlg_to_ollama"), self.var_to_ollama,
                  enabled=not lock_to_ollama).pack(side="left", padx=(0, 18))
        self._chk(dest_row, t("dlg_to_owui"), self.var_to_openwebui).pack(side="left")

        if lock_to_ollama:
            self._lbl(row_dest, t("dlg_lock_note"),
                      fg=SUBTEXT, font=("Yu Gothic UI", 9)).pack(anchor="w", pady=(2, 0))

        # システムプロンプト（残りスペースをすべて使う）
        row3 = ttk.Frame(self)
        row3.pack(fill="both", expand=True, padx=16, pady=(0, 4))
        self._lbl(row3, t("dlg_system"), fg=BLUE,
                  font=("Yu Gothic UI", 10, "bold")).pack(anchor="w")
        self._lbl(row3, t("dlg_system_hint"), fg=SUBTEXT,
                  font=("Yu Gothic UI", 9)).pack(anchor="w")

        txt_frame = ttk.Frame(row3)
        txt_frame.pack(fill="both", expand=True, pady=(4, 0))
        self.prompt_txt = tk.Text(
            txt_frame, wrap="word", bg=SURFACE, fg=TEXT,
            font=("Yu Gothic UI", 10), relief="flat", padx=8, pady=8,
            insertbackground=TEXT, selectbackground=OVERLAY, undo=True
        )
        vsb = ttk.Scrollbar(txt_frame, orient="vertical", command=self.prompt_txt.yview)
        self.prompt_txt.configure(yscrollcommand=vsb.set)
        self.prompt_txt.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        if default_prompt:
            self.prompt_txt.insert("1.0", default_prompt)

    def _ok(self):
        base   = self._base_fixed if self._base_readonly else (self.cb.get().strip() if self.cb else "")
        name   = self.name_var.get().strip()
        prompt = self.prompt_txt.get("1.0", "end").strip()
        to_ollama    = True if self._lock_to_ollama else self.var_to_ollama.get()
        to_openwebui = self.var_to_openwebui.get()

        if not base:
            messagebox.showwarning(t("warn_input"), t("warn_need_base"), parent=self)
            return
        if not name:
            messagebox.showwarning(t("warn_input"), t("warn_need_name"), parent=self)
            return
        if not to_ollama and not to_openwebui:
            messagebox.showwarning(t("warn_select"), t("warn_need_dest"), parent=self)
            return

        self.result = (base, name, prompt, to_ollama, to_openwebui)
        if self.on_save:
            self.on_save(base, name, prompt, to_ollama, to_openwebui)
        self.destroy()


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(t("app_title"))
        self.root.geometry("1200x760")
        self.root.configure(bg=BG)
        self.root.minsize(950, 620)

        self.models: list = []
        self.selected_model = None
        self.owui_prompt_set: set = set()  # OpenWebUI側でsystem promptが設定済みのモデルID

        self._styles()
        self._build()
        self.refresh()

    def _styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure(".",           background=BG,      foreground=TEXT,   font=("Yu Gothic UI", 10))
        s.configure("TFrame",      background=BG)
        s.configure("TLabel",      background=BG,      foreground=TEXT)
        s.configure("TSeparator",  background=OVERLAY)
        s.configure("TScrollbar",  background=SURFACE, troughcolor=BG,    arrowcolor=SUBTEXT)
        s.configure("TCombobox",   fieldbackground=SURFACE, background=SURFACE,
                    foreground=TEXT, selectbackground=OVERLAY)

        s.configure("TButton",         background=SURFACE, foreground=TEXT,  padding=(8, 5), relief="flat")
        s.map("TButton",               background=[("active", OVERLAY)])
        s.configure("Danger.TButton",  background=RED,    foreground=BG,    padding=(8, 5))
        s.map("Danger.TButton",        background=[("active", "#eba0ac")])
        s.configure("Warn.TButton",    background=YELLOW, foreground=BG,    padding=(8, 5))
        s.map("Warn.TButton",          background=[("active", "#f2cdcd")])
        s.configure("Copy.TButton",    background=PEACH,  foreground=BG,    padding=(8, 5))
        s.map("Copy.TButton",          background=[("active", "#f5c2a0")])
        s.configure("New.TButton",     background=GREEN,  foreground=BG,    padding=(8, 5))
        s.map("New.TButton",           background=[("active", TEAL)])
        s.configure("Edit.TButton",    background=PINK,   foreground=BG,    padding=(8, 5))
        s.map("Edit.TButton",          background=[("active", "#f2a8d8")])

        s.configure("Treeview",
                    background=SURFACE, fieldbackground=SURFACE,
                    foreground=TEXT, rowheight=30, font=("Yu Gothic UI", 10))
        s.configure("Treeview.Heading",
                    background=OVERLAY, foreground=TEXT,
                    font=("Yu Gothic UI", 10, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", "#585b70")])

    def _lbl(self, parent, text, fg=TEXT, font=None, **kw):
        return tk.Label(parent, text=text, bg=BG, fg=fg,
                        font=font or ("Yu Gothic UI", 10), **kw)

    def _info_block(self, parent, label: str, fg: str) -> tk.StringVar:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=(0, 6))
        self._lbl(row, label, fg=BLUE, font=("Yu Gothic UI", 10, "bold")).pack(anchor="w")
        var = tk.StringVar(value="—")
        tk.Label(row, textvariable=var, bg=BG, fg=fg,
                 font=("Yu Gothic UI", 10), wraplength=620, justify="left").pack(anchor="w")
        return var

    def toggle_language(self):
        """日本語 ⇄ 英語を切り替えてUIを作り直す"""
        global LANG
        LANG = "en" if LANG == "ja" else "ja"
        prev = self.selected_model
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title(t("app_title"))
        self._build()
        self._update_tree()  # 取得済みデータで一覧を即再描画
        # 選択中だったモデルを選び直す（→ 詳細欄も新しい言語で再表示される）
        if prev and self.tree.exists(prev):
            self.tree.selection_set(prev)
            self.tree.see(prev)

    def _build(self):
        # ヘッダー
        hdr = ttk.Frame(self.root, padding=(12, 8))
        hdr.pack(fill="x")
        self._lbl(hdr, t("brand"), fg=BLUE,
                  font=("Yu Gothic UI", 14, "bold")).pack(side="left")
        self.status_lbl = self._lbl(hdr, "", fg=GREEN)
        self.status_lbl.pack(side="left", padx=16)

        tk.Label(hdr, text=t("legend_dup"),
                 bg=DUP_COLORS[0], fg=TEXT, font=("Yu Gothic UI", 9),
                 padx=6, pady=2).pack(side="right", padx=(8, 0))
        tk.Label(hdr, text=t("legend_owui"),
                 bg=SURFACE, fg=TEXT, font=("Yu Gothic UI", 9),
                 padx=6, pady=2).pack(side="right", padx=(8, 0))
        ttk.Button(hdr, text=t("refresh"), command=self.refresh).pack(side="right")
        ttk.Button(hdr, text=t("lang_button"),
                   command=self.toggle_language).pack(side="right", padx=(0, 8))

        ttk.Separator(self.root).pack(fill="x")

        body = ttk.Frame(self.root, padding=12)
        body.pack(fill="both", expand=True)

        # ── 左: モデルリスト ──────────────────────────────────────────────
        left = ttk.Frame(body)
        left.pack(side="left", fill="y", padx=(0, 12))

        self._lbl(left, t("list_title"), fg=MAUVE,
                  font=("Yu Gothic UI", 11, "bold")).pack(anchor="w", pady=(0, 6))

        tv_frame = ttk.Frame(left)
        tv_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tv_frame,
                                  columns=("name", "size", "hash", "owui"),
                                  show="headings", selectmode="browse")
        self.tree.heading("name", text=t("col_name"))
        self.tree.heading("size", text=t("col_size"))
        self.tree.heading("hash", text=t("col_hash"))
        self.tree.heading("owui", text=t("col_owui"))
        self.tree.column("name", width=200, stretch=True)
        self.tree.column("size", width=80,  stretch=False)
        self.tree.column("hash", width=110, stretch=False)
        self.tree.column("owui", width=55,  stretch=False, anchor="center")

        vsb = ttk.Scrollbar(tv_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # ボタン 1行目
        btn1 = ttk.Frame(left)
        btn1.pack(fill="x", pady=(10, 3))
        ttk.Button(btn1, text=t("btn_delete"),  style="Danger.TButton",
                   command=self.cmd_delete).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ttk.Button(btn1, text=t("btn_copy"),    style="Copy.TButton",
                   command=self.cmd_copy).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ttk.Button(btn1, text=t("btn_rename"),  style="Warn.TButton",
                   command=self.cmd_rename).pack(side="left", expand=True, fill="x")

        # ボタン 2行目
        btn2 = ttk.Frame(left)
        btn2.pack(fill="x", pady=(0, 0))
        ttk.Button(btn2, text=t("btn_derive"),  style="New.TButton",
                   command=self.cmd_new_derived).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ttk.Button(btn2, text=t("btn_edit"),    style="Edit.TButton",
                   command=self.cmd_edit_prompt).pack(side="left", expand=True, fill="x")

        # ── 右: 詳細 ─────────────────────────────────────────────────────
        right = ttk.Frame(body)
        right.pack(side="left", fill="both", expand=True)

        self._lbl(right, t("detail_title"), fg=MAUVE,
                  font=("Yu Gothic UI", 11, "bold")).pack(anchor="w", pady=(0, 6))

        detail = ttk.Frame(right)
        detail.pack(fill="both", expand=True)

        self.v_name    = self._info_block(detail, t("lbl_name"),    TEXT)
        self.v_size    = self._info_block(detail, t("lbl_size"),    TEXT)
        self.v_hash    = self._info_block(detail, t("lbl_hash"),    PEACH)
        self.v_usecase = self._info_block(detail, t("lbl_usecase"), GREEN)
        self.v_info    = self._info_block(detail, t("lbl_info"),    TEXT)

        self._lbl(detail, t("lbl_embedded"),
                  fg=BLUE, font=("Yu Gothic UI", 10, "bold")).pack(anchor="w")

        txt_frame = ttk.Frame(detail)
        txt_frame.pack(fill="both", expand=True, pady=(4, 0))

        self.prompt_txt = tk.Text(
            txt_frame, wrap="word", bg=SURFACE, fg=TEXT,
            font=("Consolas", 9), relief="flat", padx=8, pady=8,
            state="disabled", selectbackground=OVERLAY, insertbackground=TEXT
        )
        txt_vsb = ttk.Scrollbar(txt_frame, orient="vertical", command=self.prompt_txt.yview)
        self.prompt_txt.configure(yscrollcommand=txt_vsb.set)
        self.prompt_txt.pack(side="left", fill="both", expand=True)
        txt_vsb.pack(side="right", fill="y")

    # ── ステータス ────────────────────────────────────────────────────────
    def set_status(self, msg: str, color: str = GREEN):
        self.status_lbl.configure(text=msg, fg=color)

    # ── 一覧更新 ─────────────────────────────────────────────────────────
    def refresh(self):
        self.set_status(t("status_loading"), YELLOW)

        def fetch():
            try:
                result = ollama_get("/api/tags")
                self.models = sorted(result.get("models", []),
                                     key=lambda m: m.get("name", ""))
            except Exception as e:
                self.root.after(0, lambda: self.set_status(t("status_conn_error", e=e), RED))
                return

            # OpenWebUI側の設定状況も取得（繋がらなくても一覧表示自体は継続する）
            try:
                owui_models = openwebui_get_base_models()
                self.owui_prompt_set = {
                    m.get("id") for m in owui_models
                    if (m.get("params") or {}).get("system")
                }
            except Exception:
                self.owui_prompt_set = set()

            self.root.after(0, self._update_tree)

        threading.Thread(target=fetch, daemon=True).start()

    def _update_tree(self):
        self.tree.delete(*self.tree.get_children())

        from collections import Counter
        digest_count = Counter(short_hash(m.get("digest", "")) for m in self.models)

        dup_color_map: dict = {}
        ci = 0
        for h, count in digest_count.items():
            if count > 1:
                dup_color_map[h] = DUP_COLORS[ci % len(DUP_COLORS)]
                ci += 1

        for i, color in enumerate(DUP_COLORS):
            self.tree.tag_configure(f"dup{i}", background=color, foreground=TEXT)

        for m in self.models:
            name = m.get("name", "")
            size = fmt_size(m.get("size", 0))
            h    = short_hash(m.get("digest", ""))
            owui = "🌐" if name in self.owui_prompt_set else "—"
            tags = ()
            if h in dup_color_map:
                ci = DUP_COLORS.index(dup_color_map[h])
                tags = (f"dup{ci}",)
            self.tree.insert("", "end", iid=name, values=(name, size, h, owui), tags=tags)

        dup_groups = sum(1 for c in digest_count.values() if c > 1)
        msg = t("status_count", n=len(self.models))
        if dup_groups:
            msg += t("status_dup", n=dup_groups)
        self.set_status(msg)

    def _model_names(self) -> list:
        return [m["name"] for m in self.models]

    # ── 選択 ─────────────────────────────────────────────────────────────
    def _on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        self.selected_model = sel[0]
        m = next((x for x in self.models if x["name"] == self.selected_model), {})

        self.v_name.set(self.selected_model)
        self.v_size.set(fmt_size(m.get("size", 0)))
        self.v_hash.set(m.get("digest", "—"))
        self.v_usecase.set(get_use_case(self.selected_model))
        self.v_info.set(t("loading"))
        self._set_prompt(t("fetching"))

        name = self.selected_model

        def fetch():
            try:
                data = ollama_post("/api/show", {"model": name})
                self.root.after(0, lambda: self._show_details(data))
            except Exception as e:
                self.root.after(0, lambda: self.v_info.set(t("fetch_failed", e=e)))

        threading.Thread(target=fetch, daemon=True).start()

    def _show_details(self, data: dict):
        details = data.get("details", {})
        parts = []
        if details.get("family"):
            parts.append(t("info_family", v=details['family']))
        if details.get("parameter_size"):
            parts.append(t("info_params", v=details['parameter_size']))
        if details.get("quantization_level"):
            parts.append(t("info_quant", v=details['quantization_level']))
        if details.get("format"):
            parts.append(t("info_format", v=details['format']))
        self.v_info.set("  |  ".join(parts) if parts else t("no_info"))

        system = data.get("system", "")
        if system:
            content = t("sys_header", v=system)
        else:
            modelfile = data.get("modelfile", "")
            content = modelfile if modelfile else t("no_system")
        self._set_prompt(content)

    def _set_prompt(self, text: str):
        self.prompt_txt.configure(state="normal")
        self.prompt_txt.delete("1.0", "end")
        self.prompt_txt.insert("1.0", text)
        self.prompt_txt.configure(state="disabled")

    def _clear_details(self):
        self.selected_model = None
        for v in (self.v_name, self.v_size, self.v_hash, self.v_usecase, self.v_info):
            v.set("—")
        self._set_prompt("")

    # ── 保存先タグ（新規作成時、名前に強制付与） ──────────────────────────
    def _apply_dest_tag(self, name: str, to_ollama: bool, to_openwebui: bool) -> str:
        """どの保存先向けに作ったかを後から一目で区別できるよう、名前に強制でタグを付ける"""
        if to_ollama and to_openwebui:
            tag = "-OWU-OLM"
        elif to_openwebui:
            tag = "-OWU"
        else:
            tag = "-OLM"

        if ":" in name:
            repo, _, ver = name.partition(":")
            return f"{repo}{tag}:{ver}"
        return f"{name}{tag}"

    # ── モデル作成・プロンプト保存（共通処理：Ollama / OpenWebUI 両対応） ──
    def _save_to_destinations(self, base: str, name: str, prompt: str,
                              to_ollama: bool, to_openwebui: bool):
        """チェックされた保存先へ順番に書き込む（Ollama → OpenWebUI の順）"""
        self.set_status(t("saving", name=name), YELLOW)

        def run():
            results = []  # (保存先名, 成功?, エラー)

            if to_ollama:
                try:
                    def on_progress(status):
                        shown = status[:50] + "..." if len(status) > 50 else status
                        self.root.after(0, lambda: self.set_status(
                            t("saving_ollama", s=shown), YELLOW))

                    ollama_create(name, base, prompt, on_progress)
                    results.append(("Ollama", True, None))
                except Exception as e:
                    results.append(("Ollama", False, e))

            if to_openwebui:
                self.root.after(0, lambda: self.set_status(t("saving_owui"), YELLOW))
                try:
                    openwebui_update_system_prompt(name, prompt)
                    results.append(("OpenWebUI", True, None))
                except Exception as e:
                    results.append(("OpenWebUI", False, e))

            self.root.after(0, lambda: self._finish_save(name, results))

        threading.Thread(target=run, daemon=True).start()

    def _finish_save(self, name: str, results: list):
        oks  = [dest for dest, ok, _ in results if ok]
        errs = [(dest, err) for dest, ok, err in results if not ok]

        if errs:
            detail = "\n\n".join(f"【{dest}】\n{err}" for dest, err in errs)
            ok_msg = t("save_ok_line", oks=" / ".join(oks)) if oks else ""
            messagebox.showwarning(
                t("save_partial_title", name=name),
                t("save_fail_body", ok=ok_msg, detail=detail),
                parent=self.root)
            self.set_status(t("save_partial", name=name,
                              oks=" / ".join(oks) if oks else t("none")),
                            YELLOW if oks else RED)
        else:
            self.set_status(t("save_done", name=name, oks=" / ".join(oks)), GREEN)

        self.refresh()

    # ── 削除 ─────────────────────────────────────────────────────────────
    def cmd_delete(self):
        if not self.selected_model:
            messagebox.showwarning(t("unselected"), t("del_unselected"), parent=self.root)
            return
        name = self.selected_model
        if not messagebox.askyesno(t("del_confirm_title"),
                                   t("del_confirm", name=name),
                                   icon="warning", parent=self.root):
            return
        self.set_status(t("deleting"), YELLOW)

        def run():
            try:
                ollama_delete("/api/delete", {"model": name})
                self.root.after(0, lambda: self.set_status(t("del_done", name=name)))
                self.root.after(0, self._clear_details)
                self.root.after(0, self.refresh)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(t("del_error_title"), str(e), parent=self.root))
                self.root.after(0, lambda: self.set_status(t("del_failed"), RED))

        threading.Thread(target=run, daemon=True).start()

    # ── コピー（プロンプトなしで別名追加） ───────────────────────────────
    def cmd_copy(self):
        if not self.selected_model:
            messagebox.showwarning(t("unselected"), t("copy_unselected"), parent=self.root)
            return
        original = self.selected_model
        new_name = simpledialog.askstring(
            t("copy_title"),
            t("copy_prompt", name=original),
            parent=self.root
        )
        if not new_name or not new_name.strip():
            return
        new_name = new_name.strip()
        if new_name == original:
            messagebox.showinfo(t("nochange_title"), t("nochange"), parent=self.root)
            return

        self.set_status(t("copying"), YELLOW)

        def run():
            try:
                ollama_post("/api/copy", {"source": original, "destination": new_name})
                self.root.after(0, lambda: self.set_status(
                    t("copy_done", a=original, b=new_name), GREEN))
                self.root.after(0, self.refresh)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(t("copy_error_title"), str(e), parent=self.root))
                self.root.after(0, lambda: self.set_status(t("copy_failed"), RED))

        threading.Thread(target=run, daemon=True).start()

    # ── リネーム ─────────────────────────────────────────────────────────
    def cmd_rename(self):
        if not self.selected_model:
            messagebox.showwarning(t("unselected"), t("rename_unselected"), parent=self.root)
            return

        original    = self.selected_model
        backup_name = original.replace(":", "_") + "_backup"

        new_name = simpledialog.askstring(
            t("rename_title"),
            t("rename_prompt", name=original),
            parent=self.root
        )
        if not new_name or not new_name.strip():
            return
        new_name = new_name.strip()
        if new_name == original:
            messagebox.showinfo(t("nochange_title"), t("nochange"), parent=self.root)
            return

        if not messagebox.askyesno(
            t("rename_confirm_title"),
            t("rename_confirm", o=original, b=backup_name, n=new_name),
            parent=self.root
        ):
            return

        def upd(msg, color=YELLOW):
            self.root.after(0, lambda: self.set_status(msg, color))

        def run():
            try:
                upd(t("rn_step1"))
                ollama_post("/api/copy", {"source": original, "destination": backup_name})
                upd(t("rn_step2"))
                ollama_delete("/api/delete", {"model": original})
                upd(t("rn_step3"))
                ollama_post("/api/copy", {"source": backup_name, "destination": new_name})
                upd(t("rn_step4"))
                check = ollama_post("/api/show", {"model": new_name})
                if not check:
                    raise RuntimeError(t("rn_check_fail"))
                ollama_delete("/api/delete", {"model": backup_name})
                upd(t("rn_done", o=original, n=new_name), GREEN)
                self.root.after(0, self._clear_details)
                self.root.after(0, self.refresh)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    t("rename_error_title"), t("rename_error_body", e=e, b=backup_name),
                    parent=self.root))
                upd(t("rename_failed"), RED)
                self.root.after(0, self.refresh)

        threading.Thread(target=run, daemon=True).start()

    # ── 派生登録（ベースモデル + 新プロンプト → 新モデル） ───────────────
    def cmd_new_derived(self):
        default_base = self.selected_model or ""

        def on_save(base, name, prompt, to_ollama, to_openwebui):
            final_name = self._apply_dest_tag(name, to_ollama, to_openwebui)
            self._save_to_destinations(base, final_name, prompt, to_ollama, to_openwebui)

        dlg = ModelfileEditor(
            self.root,
            title=t("title_derive"),
            model_names=self._model_names(),
            default_base=default_base,
            default_name="",
            default_prompt="",
            on_save=on_save,
            lock_to_ollama=True
        )
        self.root.wait_window(dlg)

    # ── プロンプト編集（選択中モデルのプロンプトを書き換えて上書き） ──────
    def cmd_edit_prompt(self):
        if not self.selected_model:
            messagebox.showwarning(t("unselected"), t("edit_unselected"), parent=self.root)
            return

        name = self.selected_model
        self.set_status(t("loading"), YELLOW)

        def fetch():
            try:
                data = ollama_post("/api/show", {"model": name})
                system    = data.get("system", "")
                modelfile = data.get("modelfile", "")

                # modelfile の FROM 行を抽出（blob パスを使うことで循環参照を回避）
                from_line = name  # フォールバック
                for line in modelfile.splitlines():
                    stripped = line.strip()
                    if stripped.upper().startswith("FROM ") and not stripped.startswith("#"):
                        from_line = stripped[5:].strip()
                        break

                self.root.after(0, lambda: self._open_edit_dialog(name, from_line, system))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    t("fetch_error_title"), str(e), parent=self.root))
                self.root.after(0, lambda: self.set_status(t("fetch_failed_status"), RED))

        threading.Thread(target=fetch, daemon=True).start()

    def _open_edit_dialog(self, current_name: str, from_line: str, current_prompt: str):
        self.set_status("")

        def on_save(base_model, new_name, new_prompt, to_ollama, to_openwebui):
            self._save_to_destinations(base_model, new_name, new_prompt, to_ollama, to_openwebui)

        # ベースはモデル名を使う（blobパスより安定）
        ModelfileEditor(
            self.root,
            title=t("title_edit", name=current_name),
            model_names=self._model_names(),
            default_base=current_name,
            default_name=current_name,
            default_prompt=current_prompt,
            on_save=on_save,
            base_readonly=True
        )


if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root = tk.Tk()
    App(root)
    root.mainloop()
