#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""もでコレ - Ollama モデル管理ツール / Ollama model manager (JA/EN)"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import urllib.request
import urllib.error
import json
import os
import re
import hashlib
import threading
import customtkinter as ctk

OLLAMA_BASE = "http://localhost:11434"
OPENWEBUI_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openwebui_config.json")

# ── 言語 / Language ───────────────────────────────────────────────────────
LANG = "ja"  # "ja" or "en"

TR = {
    "ja": {
        "app_title": "もでコレ 🦙",
        "brand": "🦙 もでコレ",
        "lang_button": "🌐 EN",
        "help_button": "❓ ヘルプ",
        "help_title": "❓ もでコレの使い方",
        "help_close": "閉じる",
        "import_button": "📥 取り込み",
        "import_title": "📥 LM Studio から取り込み",
        "import_note": "⚠️ 取り込むと Ollama 側にも実体がコピーされます（LM Studio とで容量が二重になります）。",
        "import_col_name": "取り込み後の名前（編集できます）",
        "import_select_all": "全選択",
        "import_clear_all": "全解除",
        "import_do": "📥 取り込む",
        "import_close": "閉じる",
        "import_already": "既にOllamaにあります",
        "import_no_folder": "LM Studio のモデルフォルダが見つかりませんでした。\nLM Studio をインストールし、モデルをダウンロードしているか確認してください。",
        "import_none_found": "LM Studio に取り込めるモデル（.gguf）が見つかりませんでした。",
        "import_nothing_checked": "取り込むモデルにチェックを入れてください。",
        "import_bad_name": "名前が空のモデルがあります。名前を入れてください。",
        "import_found": "{n} 個のモデルが見つかりました（容量の小さい順ではありません）",
        "import_progress": "[{i}/{n}] {name} … {status}",
        "import_row_done": "✅ 完了",
        "import_row_fail": "❌ 失敗: {e}",
        "import_finished": "✅ 取り込み完了：成功 {ok} 件／失敗 {fail} 件",
        "import_status_done": "✅ LM Studio から {ok} 件取り込みました",
        "import_cancel": "⏹ 中止",
        "import_cancelling": "中止中…",
        "import_importing": "取り込み中…",
        "import_del_source": "取り込んだら LM Studio の元ファイルも削除（容量を2倍にしない）",
        "import_confirm_title": "取り込みの確認",
        "import_confirm": "{n} 個のモデル（合計 {size}）を Ollama に取り込みます。\n\n⚠️ Ollama 側に実体がコピーされるので、その分ディスクを使います。\n\n取り込みますか？",
        "import_confirm_delsrc": "\n\n🗑 取り込み後、LM Studio の元ファイルも削除します（戻せません）。",
        "import_cancelled": "⏹ 中止しました（成功 {ok} 件／失敗 {fail} 件）",
        "refresh": "🔄 更新",
        "legend_dup": "■ 同じハッシュ = 同じ実体（重複）",
        "legend_owui": "🌐 = OpenWebUI側にもプロンプト設定済み",
        "search_ph": "モデルを検索…",
        "legend_hint": "🌐 = OpenWebUI同期済み　／　色付き＝中身が重複",
        "empty_detail": "← 左の一覧からモデルを選んでね",
        "ready": "準備OK",
        "lbl_owui_row": "🌐 OpenWebUI",
        "owui_yes": "同期済み",
        "owui_no": "未設定",
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
        "app_title": "ModeColle 🦙",
        "brand": "🦙 ModeColle",
        "lang_button": "🌐 日本語",
        "help_button": "❓ Help",
        "help_title": "❓ How to use ModeColle",
        "help_close": "Close",
        "import_button": "📥 Import",
        "import_title": "📥 Import from LM Studio",
        "import_note": "⚠️ Importing copies the model into Ollama as well (it uses disk space in both LM Studio and Ollama).",
        "import_col_name": "Name in Ollama (editable)",
        "import_select_all": "Select all",
        "import_clear_all": "Clear",
        "import_do": "📥 Import",
        "import_close": "Close",
        "import_already": "already in Ollama",
        "import_no_folder": "Could not find the LM Studio models folder.\nMake sure LM Studio is installed and you have downloaded a model.",
        "import_none_found": "No importable models (.gguf) were found in LM Studio.",
        "import_nothing_checked": "Please check at least one model to import.",
        "import_bad_name": "Some models have an empty name. Please enter a name.",
        "import_found": "Found {n} model(s)",
        "import_progress": "[{i}/{n}] {name} … {status}",
        "import_row_done": "✅ done",
        "import_row_fail": "❌ failed: {e}",
        "import_finished": "✅ Import finished: {ok} succeeded / {fail} failed",
        "import_status_done": "✅ Imported {ok} model(s) from LM Studio",
        "import_cancel": "⏹ Cancel",
        "import_cancelling": "Cancelling…",
        "import_importing": "Importing…",
        "import_del_source": "Delete the LM Studio source file after import (avoid doubling disk)",
        "import_confirm_title": "Confirm import",
        "import_confirm": "Import {n} model(s) ({size} total) into Ollama.\n\n⚠️ The data is copied into Ollama, using that much disk.\n\nProceed?",
        "import_confirm_delsrc": "\n\n🗑 The LM Studio source files will be deleted after import (cannot be undone).",
        "import_cancelled": "⏹ Cancelled ({ok} succeeded / {fail} failed)",
        "refresh": "🔄 Refresh",
        "legend_dup": "■ Same hash = same data (duplicate)",
        "legend_owui": "🌐 = Prompt also set on OpenWebUI",
        "search_ph": "Search models…",
        "legend_hint": "🌐 = synced to OpenWebUI  /  tinted = duplicate content",
        "empty_detail": "← Pick a model from the list",
        "ready": "Ready",
        "lbl_owui_row": "🌐 OpenWebUI",
        "owui_yes": "Synced",
        "owui_no": "Not set",
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


# アプリ内ヘルプの本文（見出し, 本文）のリスト。LANG連動でHelpDialogが表示する。
HELP_SECTIONS = {
    "ja": [
        ("もでコレって何？",
         "Ollama に入れた AI モデルを、コマンドを覚えなくても一覧から選んでボタン操作で管理できる "
         "Windows ツールです。さらに OpenWebUI 側のシステムプロンプトも、同じ画面から直接読み書きできます。"),
        ("使い方は3ステップ",
         "① 左の「登録モデル一覧」から、操作したいモデルをクリックして選ぶ\n"
         "② 右の「モデル詳細」に、容量・おすすめ用途・組み込みプロンプトなどが表示される\n"
         "③ 右下のボタンで、編集・コピー・リネーム・削除などを実行する"),
        ("ボタンの意味",
         "🖊️ プロンプト編集 … 選んだモデルのシステムプロンプトを書き換える\n"
         "🆕 派生登録 … 既存モデルをベースに、別プロンプトの新しいモデルを作る\n"
         "📋 コピー … 同じ中身を別名でもう1つ作る（容量は増えない）\n"
         "✏️ リネーム … 安全な手順（バックアップ→確認→入れ替え）で名前を変える\n"
         "🗑️ 削除 … いらないモデルを確認つきで消す\n"
         "🔄 更新 … 一覧を最新に読み直す　／　🌐 … 日本語⇄英語の切替"),
        ("OpenWebUI連携（ここが肝心）",
         "編集・派生のダイアログで「☑ OpenWebUIにも反映する」を入れると、Ollama と OpenWebUI の "
         "両方へ一度に書き込みます。\n"
         "⚠️ OpenWebUI は Ollama に埋め込んだプロンプトを読みません（自分専用の別の場所に持つため）。"
         "だからこのツールで両方に書くのが大事。これがもでコレを作った理由です。\n"
         "💡 保存しても OpenWebUI の画面は自動で更新されません。F5 で再読み込みしてね。\n"
         "🌐 バッジ … そのモデルが OpenWebUI 側にもプロンプト設定済みの印。"),
        ("色分け（重複の発見）",
         "一覧で同じ色がついたモデル同士は、中身（ハッシュ）が同じ＝別名で二重登録されているという印です。"
         "容量を節約したいときの、整理の目印になります。"),
        ("LM Studio のモデルを取り込む",
         "LM Studio でダウンロードしたモデル（.gguf）は、そのままでは ModeColle に出てきません"
         "（別アプリで保管場所が違うため）。\n"
         "一覧の上の「📥 取り込み」ボタンを押すと、LM Studio のモデルを自動で探して一覧表示します。"
         "取り込みたいものにチェック→「📥 取り込む」で Ollama に取り込まれ、一覧に出ます（名前はその場で編集可）。\n"
         "⚠️ 取り込むと Ollama 側にも実体がコピーされるので、LM Studio とで容量が二重になります。"),
        ("困ったとき",
         "・モデルが出てこない → Ollama が起動しているか確認（http://localhost:11434）\n"
         "・LM Studioのモデルが無い → 上の「📥 取り込み」で取り込む（更新だけでは出ません）\n"
         "・OpenWebUI に繋がらない → 本体と同じフォルダの openwebui_config.json の URL と API キーを確認\n"
         "・起動しない → 「pip install customtkinter」を実行したか確認"),
    ],
    "en": [
        ("What is ModeColle?",
         "A Windows tool that lets you manage the AI models in Ollama from a list with button "
         "clicks - no commands to memorize. It can also read and write the system prompts on the "
         "OpenWebUI side from the same screen."),
        ("Three simple steps",
         "1. Click a model in the \"Installed models\" list on the left to select it\n"
         "2. Its size, suggested use, embedded prompt and more appear under \"Model details\" on the right\n"
         "3. Use the buttons at the bottom right to edit, copy, rename or delete it"),
        ("What the buttons do",
         "🖊️ Edit prompt … rewrite the selected model's system prompt\n"
         "🆕 New / Derive … make a new model from an existing one with a different prompt\n"
         "📋 Copy … make another copy under a new name (no extra disk use)\n"
         "✏️ Rename … rename safely (back up -> verify -> swap)\n"
         "🗑️ Delete … remove a model you don't need, with confirmation\n"
         "🔄 Refresh … reload the list  /  🌐 … switch Japanese <-> English"),
        ("OpenWebUI integration (the key part)",
         "In the edit / derive dialog, tick \"☑ Also apply to OpenWebUI\" to write to both Ollama "
         "and OpenWebUI at once.\n"
         "⚠️ OpenWebUI does NOT read the prompt embedded in an Ollama model (it keeps its own copy "
         "elsewhere). That's why writing to both with this tool matters - it's the reason ModeColle exists.\n"
         "💡 After saving, the OpenWebUI page won't refresh on its own. Press F5 to reload it.\n"
         "🌐 badge … marks a model that also has its prompt set on OpenWebUI."),
        ("Color coding (spotting duplicates)",
         "Models that share the same color in the list have the same content (same hash) = registered "
         "twice under different names. A handy marker when you want to clean up and save space."),
        ("Import models from LM Studio",
         "Models you downloaded in LM Studio (.gguf) don't show up in ModeColle on their own "
         "(it's a separate app with its own storage).\n"
         "Click the \"📥 Import\" button above the list to auto-detect LM Studio models. Check the "
         "ones you want and press \"📥 Import\" - they get imported into Ollama and appear in the list "
         "(you can edit the name on the spot).\n"
         "⚠️ Importing copies the model into Ollama too, so it uses disk space in both LM Studio and Ollama."),
        ("Troubleshooting",
         "- No models show up -> check that Ollama is running (http://localhost:11434)\n"
         "- An LM Studio model is missing -> import it with \"📥 Import\" above (Refresh alone won't show it)\n"
         "- Can't reach OpenWebUI -> check the URL and API key in openwebui_config.json (same folder as the app)\n"
         "- App won't start -> make sure you ran \"pip install customtkinter\""),
    ],
}


# モデル名キーワード → 用途（言語別）/ model-name keyword -> use case (per language)
USE_CASES = {
    "maine":     {"ja": "🗣️ 日常会話メイン・日本語お姉さんキャラ・パーソナルアシスタント",
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


# ── LM Studio からの取り込み ────────────────────────────────────────────────
# LM Studio は GGUF ファイルを独自フォルダに保管する（Ollama とは別管理）。
# ここでそのフォルダを走査し、見つけた .gguf を Ollama へ取り込む（blob→create）。

def lmstudio_models_dir():
    """LM Studio のモデル保管フォルダを返す（無ければ None）。"""
    home = os.path.expanduser("~")
    for c in (os.path.join(home, ".lmstudio", "models"),
              os.path.join(home, ".cache", "lm-studio", "models")):
        if os.path.isdir(c):
            return c
    return None


_QUANT_RE = re.compile(r'(?i)((?:UD[-_])?(?:IQ|Q|TQ)\d[0-9a-z_]*|f16|bf16|fp16)')


def _sanitize_name(s: str) -> str:
    """Ollama のモデル名に使える形へ（小文字・記号は - に）。"""
    s = re.sub(r'[^a-z0-9._-]+', '-', s.lower()).strip('-.')
    s = re.sub(r'-{2,}', '-', s)
    return s or "model"


def suggest_ollama_name(repo: str, filename: str) -> str:
    """リポジトリ名＋量子化から取り込み後の名前を提案（例: magnum-12b-v2:q5_k_m）。"""
    base = re.sub(r'[-_]?gguf$', '', repo, flags=re.IGNORECASE)
    base = _sanitize_name(base)
    stem = os.path.splitext(filename)[0]
    m = _QUANT_RE.search(stem)
    tag = _sanitize_name(m.group(1)) if m else "latest"
    return f"{base}:{tag}"


def scan_lmstudio_models():
    """LM Studio フォルダ内の .gguf を一覧化。フォルダが無ければ None を返す。
    mmproj（マルチモーダル補助ファイル＝モデル本体ではない）は除外する。"""
    root_dir = lmstudio_models_dir()
    if not root_dir:
        return None
    found = []
    for root, _dirs, files in os.walk(root_dir):
        for fn in files:
            low = fn.lower()
            if not low.endswith(".gguf") or low.startswith("mmproj"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, root_dir)
            parts = rel.split(os.sep)
            publisher = parts[0] if len(parts) >= 2 else ""
            repo = parts[-2] if len(parts) >= 2 else os.path.basename(root)
            try:
                size = os.path.getsize(path)
            except OSError:
                size = 0
            found.append({"path": path, "publisher": publisher, "repo": repo,
                          "filename": fn, "size": size,
                          "suggested": suggest_ollama_name(repo, fn)})
    found.sort(key=lambda x: (x["repo"].lower(), x["filename"].lower()))
    return found


def ollama_blob_upload(path: str) -> str:
    """ファイルを sha256 で blob 登録し、digest を返す。大きいファイルもストリーム送信。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    digest = h.hexdigest()
    url = OLLAMA_BASE + "/api/blobs/sha256:" + digest
    # 既にサーバ側にある blob は再送しない（送るとサーバが即応答して接続リセットになる＆無駄）
    try:
        urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30).close()
        return digest
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        req = urllib.request.Request(url, data=f, method="POST")
        req.add_header("Content-Type", "application/octet-stream")
        req.add_header("Content-Length", str(size))
        urllib.request.urlopen(req, timeout=3600).close()
    return digest


def _ollama_models_dir():
    """Ollama のモデル保管フォルダ（OLLAMA_MODELS 環境変数 か ~/.ollama/models）。"""
    d = os.environ.get("OLLAMA_MODELS")
    if d and os.path.isdir(d):
        return d
    d = os.path.join(os.path.expanduser("~"), ".ollama", "models")
    return d if os.path.isdir(d) else None


def _cleanup_orphan_blob(digest: str):
    """取り込み時にアップロードした元 blob が、Ollama の変換後どのモデルからも参照されていなければ
    削除して容量を戻す。Ollama には blob 削除 API が無いためファイルを直接消す。
    localhost 運用前提・best-effort（失敗しても取り込み自体は成功）。"""
    try:
        md = _ollama_models_dir()
        if not md:
            return
        manifests = os.path.join(md, "manifests")
        if os.path.isdir(manifests):
            for root, _d, files in os.walk(manifests):
                for fn in files:
                    try:
                        with open(os.path.join(root, fn), encoding="utf-8", errors="ignore") as f:
                            if digest in f.read():
                                return  # まだどこかのモデルが使っている＝消さない
                    except OSError:
                        pass
        blob = os.path.join(md, "blobs", "sha256-" + digest)
        if os.path.isfile(blob):
            os.remove(blob)
    except Exception:
        pass


class ImportCancelled(Exception):
    """取り込みがユーザーにより中止された。"""


def ollama_import_gguf(name: str, gguf_path: str, on_progress=None, should_cancel=None):
    """GGUF ファイルを Ollama に取り込む（blob アップロード → create → 孤児blob掃除）。
    should_cancel() が True を返したら ImportCancelled を投げて中断する
    （※巨大ファイルの blob アップロード中は中断できず、その後の create 段階から効く）。"""
    if on_progress:
        on_progress("uploading")
    digest = ollama_blob_upload(gguf_path)
    if should_cancel and should_cancel():
        raise ImportCancelled()
    fname = os.path.basename(gguf_path)
    data = {"model": name, "files": {fname: "sha256:" + digest}, "stream": True}
    body = json.dumps(data).encode()
    req = urllib.request.Request(OLLAMA_BASE + "/api/create", data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=3600) as r:
        for line in r:
            if should_cancel and should_cancel():
                raise ImportCancelled()
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if on_progress and obj.get("status"):
                    on_progress(obj["status"])
                if "error" in obj:
                    raise RuntimeError(obj["error"])
            except json.JSONDecodeError:
                pass
    # 変換でアップロード元 blob が孤児化していたら掃除（参照が残っていれば消さない）
    _cleanup_orphan_blob(digest)


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


# ── 配色（ぷろんぷたん family: 白基調・パステル・角丸） ───────────────────
ctk.set_appearance_mode("light")

WIN_BG    = "#faf6fb"
CARD      = "#ffffff"
BORDER    = "#ece4f0"
TXT       = "#3d3447"
TXT_MUT   = "#9a8ea6"
TXT_HINT  = "#bcb1c6"
PINK      = "#EA4C9D"   # ブランド基準ピンク（CTA/ロゴ/選択中）
PINK_HOV  = "#D43A87"   # ホバー＝一段濃いピンク
PINK_TXT  = "#7c2b50"
PINK_SOFT = "#FBE3F1"   # 選択行・淡ピンク面（ブランド共通トークン）
PINK_FLASH = "#fbeef5"
LAV       = "#8B7EE8"   # ブランド基準ラベンダー（副アクセント）
LAV_HOV   = "#F3EFFC"   # 淡ラベンダー面（ゴーストhover）
LAV_TXT   = "#6E5FD0"   # ラベンダー文字
RED       = "#e06d6d"
RED_HOV   = "#fbeaea"
RED_BD    = "#eeb4b4"
GHOST_BD  = "#e6dcec"
GHOST_HOV = "#f4eef7"
CHIP_BG   = "#F3EFFC"   # WebUI同期バッジ＝ラベンダー淡ピル（青→ブランド統一）
CHIP_TX   = "#6E5FD0"
OK_GREEN  = "#3a9e78"
WARN_AMBER = "#c98a2a"

DUP_TINTS = ["#f3edfb", "#e9f6ef", "#fdeef1", "#fef6e6", "#eaf2fb"]


class ModelfileEditor(ctk.CTkToplevel):
    """派生登録・プロンプト編集 共通ダイアログ（CustomTkinter）"""

    def __init__(self, parent, title, model_names, default_base="", default_name="",
                 default_prompt="", on_save=None, base_readonly=False, lock_to_ollama=False):
        super().__init__(parent)
        self.title(title)
        self.configure(fg_color=WIN_BG)
        self.geometry("680x640")
        self.minsize(560, 520)
        self.update_idletasks()
        try:
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            self.geometry(f"680x640+{px + (pw - 680) // 2}+{py + (ph - 640) // 2}")
        except Exception:
            pass
        self.on_save = on_save
        self.result = None
        self._base_readonly = base_readonly
        self._base_fixed = default_base
        self._lock_to_ollama = lock_to_ollama
        self._build(model_names, default_base, default_name, default_prompt,
                    base_readonly, lock_to_ollama)
        self.transient(parent)
        self.after(60, self._grab)

    def _grab(self):
        try:
            self.grab_set()
            self.lift()
            self.focus_force()
        except Exception:
            pass

    def _build(self, model_names, default_base, default_name, default_prompt,
               base_readonly, lock_to_ollama):
        fb = ctk.CTkFont("Yu Gothic UI", 12, "bold")
        fn = ctk.CTkFont("Yu Gothic UI", 11)
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=18, pady=16)

        # ベースモデル（元の名前）は常に大きく明示する
        ctk.CTkLabel(wrap, text=(t("dlg_base_auto") if base_readonly else t("dlg_base")),
                     font=fb, text_color=LAV_TXT, anchor="w").pack(fill="x")
        if base_readonly:
            box = ctk.CTkFrame(wrap, fg_color=PINK_SOFT, corner_radius=10)
            box.pack(fill="x", pady=(4, 10))
            ctk.CTkLabel(box, text=default_base, font=ctk.CTkFont("Yu Gothic UI", 13, "bold"),
                         text_color=PINK_TXT, anchor="w", justify="left",
                         wraplength=560).pack(fill="x", padx=12, pady=8)
            self.cb = None
        else:
            self.cb = ctk.CTkComboBox(wrap, values=model_names, state="readonly", font=fn,
                                      fg_color=CARD, border_color=BORDER, button_color=LAV,
                                      button_hover_color=LAV_TXT, dropdown_fg_color=CARD,
                                      text_color=TXT, corner_radius=10)
            self.cb.pack(fill="x", pady=(4, 10))
            self.cb.set(default_base if default_base in model_names else "")

        ctk.CTkLabel(wrap, text=t("dlg_newname"), font=fb, text_color=LAV_TXT,
                     anchor="w").pack(fill="x")
        self.name_var = tk.StringVar(value=default_name)
        ctk.CTkEntry(wrap, textvariable=self.name_var, font=fn, fg_color=CARD,
                     border_color=BORDER, text_color=TXT, corner_radius=10,
                     height=34).pack(fill="x", pady=(4, 10))

        ctk.CTkLabel(wrap, text=t("dlg_dest"), font=fb, text_color=LAV_TXT,
                     anchor="w").pack(fill="x")
        self.var_to_ollama = tk.BooleanVar(value=True)
        self.var_to_openwebui = tk.BooleanVar(value=False)
        drow = ctk.CTkFrame(wrap, fg_color="transparent")
        drow.pack(fill="x", pady=(4, 2))
        c1 = ctk.CTkCheckBox(drow, text=t("dlg_to_ollama"), variable=self.var_to_ollama,
                             font=fn, text_color=TXT, fg_color=PINK, hover_color=PINK_HOV,
                             border_color=LAV)
        c1.pack(side="left", padx=(0, 18))
        if lock_to_ollama:
            c1.configure(state="disabled")
        ctk.CTkCheckBox(drow, text=t("dlg_to_owui"), variable=self.var_to_openwebui,
                        font=fn, text_color=TXT, fg_color=PINK, hover_color=PINK_HOV,
                        border_color=LAV).pack(side="left")
        if lock_to_ollama:
            ctk.CTkLabel(wrap, text=t("dlg_lock_note"), font=fn, text_color=TXT_MUT,
                         anchor="w").pack(fill="x", pady=(2, 6))

        ctk.CTkLabel(wrap, text=t("dlg_system"), font=fb, text_color=LAV_TXT,
                     anchor="w").pack(fill="x", pady=(8, 0))
        ctk.CTkLabel(wrap, text=t("dlg_system_hint"), font=fn, text_color=TXT_MUT,
                     anchor="w").pack(fill="x")
        self.prompt_txt = ctk.CTkTextbox(wrap, font=ctk.CTkFont("Yu Gothic UI", 12),
                                         fg_color=CARD, border_color=BORDER, border_width=1,
                                         text_color=TXT, wrap="word", corner_radius=10)
        self.prompt_txt.pack(fill="both", expand=True, pady=(4, 12))
        if default_prompt:
            self.prompt_txt.insert("1.0", default_prompt)

        brow = ctk.CTkFrame(wrap, fg_color="transparent")
        brow.pack(fill="x")
        ctk.CTkButton(brow, text=t("dlg_ok"), command=self._ok,
                      font=ctk.CTkFont("Yu Gothic UI", 13, "bold"), fg_color=PINK,
                      hover_color=PINK_HOV, text_color="#ffffff", corner_radius=20,
                      height=40).pack(side="right", padx=(8, 0))
        ctk.CTkButton(brow, text=t("dlg_cancel"), command=self.destroy,
                      font=ctk.CTkFont("Yu Gothic UI", 13), fg_color="transparent",
                      hover_color=GHOST_HOV, text_color=TXT_MUT, border_width=1,
                      border_color=GHOST_BD, corner_radius=20, height=40).pack(side="right")

    def _ok(self):
        base = self._base_fixed if self._base_readonly else (self.cb.get().strip() if self.cb else "")
        name = self.name_var.get().strip()
        prompt = self.prompt_txt.get("1.0", "end").strip()
        to_ollama = True if self._lock_to_ollama else self.var_to_ollama.get()
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


class AskNameDialog(ctk.CTkToplevel):
    """初期値を入れられるテーマ統一の入力ダイアログ。文字列 or None を返す。"""

    def __init__(self, parent, title, body, default=""):
        super().__init__(parent)
        self.title(title)
        self.configure(fg_color=WIN_BG)
        self.geometry("470x250")
        self.resizable(False, False)
        self.result = None
        self.update_idletasks()
        try:
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            self.geometry(f"470x250+{px + (pw - 470) // 2}+{py + (ph - 250) // 2}")
        except Exception:
            pass
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=18, pady=16)
        ctk.CTkLabel(wrap, text=body, font=ctk.CTkFont("Yu Gothic UI", 11), text_color=TXT,
                     anchor="w", justify="left", wraplength=430).pack(fill="x", pady=(0, 10))
        self.var = tk.StringVar(value=default)
        self.entry = ctk.CTkEntry(wrap, textvariable=self.var,
                                  font=ctk.CTkFont("Yu Gothic UI", 12), fg_color=CARD,
                                  border_color=BORDER, text_color=TXT, corner_radius=10,
                                  height=36)
        self.entry.pack(fill="x")
        brow = ctk.CTkFrame(wrap, fg_color="transparent")
        brow.pack(fill="x", pady=(16, 0))
        ctk.CTkButton(brow, text="OK", command=self._ok,
                      font=ctk.CTkFont("Yu Gothic UI", 13, "bold"), fg_color=PINK,
                      hover_color=PINK_HOV, text_color="#ffffff", corner_radius=20,
                      height=38, width=110).pack(side="right", padx=(8, 0))
        ctk.CTkButton(brow, text="キャンセル", command=self._cancel,
                      font=ctk.CTkFont("Yu Gothic UI", 13), fg_color="transparent",
                      hover_color=GHOST_HOV, text_color=TXT_MUT, border_width=1,
                      border_color=GHOST_BD, corner_radius=20, height=38, width=110).pack(side="right")
        self.transient(parent)
        self.bind("<Return>", lambda e: self._ok())
        self.bind("<Escape>", lambda e: self._cancel())
        self.after(60, self._post_init)

    def _post_init(self):
        try:
            self.grab_set()
            self.lift()
            self.focus_force()
            self.entry.focus_set()
            self.entry._entry.select_range(0, "end")
        except Exception:
            pass

    def _ok(self):
        self.result = self.var.get().strip()
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()


class HelpDialog(ctk.CTkToplevel):
    """使い方をアプリ内で表示するヘルプ窓。日英はLANG連動（開いた時点の言語で表示）。"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title(t("help_title"))
        self.configure(fg_color=WIN_BG)
        W, H = 640, 680
        self.geometry(f"{W}x{H}")
        self.minsize(520, 460)
        self.update_idletasks()
        try:
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            self.geometry(f"{W}x{H}+{px + (pw - W) // 2}+{py + (ph - H) // 2}")
        except Exception:
            pass

        ctk.CTkLabel(self, text=t("help_title"),
                     font=ctk.CTkFont("Yu Gothic UI", 18, "bold"),
                     text_color=PINK_TXT).pack(anchor="w", padx=20, pady=(16, 8))

        body = ctk.CTkScrollableFrame(self, fg_color=CARD, corner_radius=14,
                                      border_width=1, border_color=BORDER)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        for i, (heading, text_body) in enumerate(HELP_SECTIONS.get(LANG, HELP_SECTIONS["ja"])):
            ctk.CTkLabel(body, text=heading,
                         font=ctk.CTkFont("Yu Gothic UI", 14, "bold"), text_color=LAV_TXT,
                         anchor="w", justify="left", wraplength=560
                         ).pack(fill="x", padx=14, pady=(16 if i else 12, 2))
            ctk.CTkLabel(body, text=text_body,
                         font=ctk.CTkFont("Yu Gothic UI", 12), text_color=TXT,
                         anchor="w", justify="left", wraplength=560
                         ).pack(fill="x", padx=14, pady=(0, 2))

        brow = ctk.CTkFrame(self, fg_color="transparent")
        brow.pack(fill="x", padx=18, pady=(0, 14))
        ctk.CTkButton(brow, text=t("help_close"), command=self.destroy,
                      font=ctk.CTkFont("Yu Gothic UI", 13, "bold"), fg_color=PINK,
                      hover_color=PINK_HOV, text_color="#ffffff", corner_radius=20,
                      height=38, width=120).pack(side="right")
        self.transient(parent)
        self.bind("<Escape>", lambda e: self.destroy())
        self.after(60, self._post_init)

    def _post_init(self):
        try:
            self.lift()
            self.focus_force()
            _ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modecole.ico")
            if os.path.isfile(_ico):
                self.iconbitmap(_ico)
        except Exception:
            pass


class ImportDialog(ctk.CTkToplevel):
    """LM Studio の GGUF を選んで Ollama に取り込むダイアログ。"""

    def __init__(self, parent, models, existing_names, on_done):
        super().__init__(parent)
        self.existing = existing_names
        self.on_done = on_done
        self.rows = []
        self.importing = False
        self._cancel = False
        self.del_source = tk.BooleanVar(value=False)
        self.title(t("import_title"))
        self.configure(fg_color=WIN_BG)
        W, H = 780, 640
        self.geometry(f"{W}x{H}")
        self.minsize(640, 480)
        self.update_idletasks()
        try:
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            self.geometry(f"{W}x{H}+{px + (pw - W) // 2}+{py + (ph - H) // 2}")
        except Exception:
            pass

        ctk.CTkLabel(self, text=t("import_title"),
                     font=ctk.CTkFont("Yu Gothic UI", 18, "bold"),
                     text_color=PINK_TXT).pack(anchor="w", padx=20, pady=(16, 0))
        ctk.CTkLabel(self, text=t("import_found", n=len(models)),
                     font=ctk.CTkFont("Yu Gothic UI", 11), text_color=TXT_MUT,
                     anchor="w").pack(anchor="w", padx=20, pady=(2, 0))
        ctk.CTkLabel(self, text=t("import_note"), font=ctk.CTkFont("Yu Gothic UI", 11),
                     text_color=WARN_AMBER, anchor="w", justify="left",
                     wraplength=W - 60).pack(anchor="w", padx=20, pady=(4, 8))

        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.pack(fill="x", padx=18)
        ctk.CTkButton(topbar, text=t("import_select_all"), command=lambda: self._set_all(True),
                      font=ctk.CTkFont("Yu Gothic UI", 11), fg_color="transparent",
                      hover_color=GHOST_HOV, text_color=TXT_MUT, border_width=1,
                      border_color=GHOST_BD, corner_radius=14, height=28,
                      width=80).pack(side="left", padx=(0, 6))
        ctk.CTkButton(topbar, text=t("import_clear_all"), command=lambda: self._set_all(False),
                      font=ctk.CTkFont("Yu Gothic UI", 11), fg_color="transparent",
                      hover_color=GHOST_HOV, text_color=TXT_MUT, border_width=1,
                      border_color=GHOST_BD, corner_radius=14, height=28, width=80).pack(side="left")

        body = ctk.CTkScrollableFrame(self, fg_color=CARD, corner_radius=14,
                                      border_width=1, border_color=BORDER)
        body.pack(fill="both", expand=True, padx=18, pady=(8, 8))
        for m in models:
            self._add_row(body, m)

        self.chk_del = ctk.CTkCheckBox(self, text=t("import_del_source"), variable=self.del_source,
                                       font=ctk.CTkFont("Yu Gothic UI", 11), fg_color=RED,
                                       hover_color=RED_BD, border_color=GHOST_BD,
                                       checkmark_color="#ffffff", text_color=TXT_MUT)
        self.chk_del.pack(anchor="w", padx=20, pady=(2, 2))

        self.status_lbl = ctk.CTkLabel(self, text="", font=ctk.CTkFont("Yu Gothic UI", 11),
                                       text_color=OK_GREEN, anchor="w", justify="left",
                                       wraplength=W - 60)
        self.status_lbl.pack(fill="x", padx=20, pady=(0, 4))

        brow = ctk.CTkFrame(self, fg_color="transparent")
        brow.pack(fill="x", padx=18, pady=(0, 14))
        self.btn_import = ctk.CTkButton(brow, text=t("import_do"), command=self._start,
                                        font=ctk.CTkFont("Yu Gothic UI", 13, "bold"),
                                        fg_color=PINK, hover_color=PINK_HOV, text_color="#ffffff",
                                        corner_radius=20, height=40, width=150)
        self.btn_import.pack(side="right", padx=(8, 0))
        self.btn_close = ctk.CTkButton(brow, text=t("import_close"), command=self._close,
                                       font=ctk.CTkFont("Yu Gothic UI", 13), fg_color="transparent",
                                       hover_color=GHOST_HOV, text_color=TXT_MUT, border_width=1,
                                       border_color=GHOST_BD, corner_radius=20, height=40, width=110)
        self.btn_close.pack(side="right")

        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.after(60, self._post_init)

    def _post_init(self):
        try:
            self.lift()
            self.focus_force()
            _ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modecole.ico")
            if os.path.isfile(_ico):
                self.iconbitmap(_ico)
        except Exception:
            pass

    def _add_row(self, parent, m):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=6, pady=3)
        var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(row, text="", variable=var, width=24, fg_color=PINK,
                        hover_color=PINK_HOV, border_color=GHOST_BD,
                        checkmark_color="#ffffff").pack(side="left", padx=(2, 6))
        status_lbl = ctk.CTkLabel(row, text="", font=ctk.CTkFont("Yu Gothic UI", 11),
                                  text_color=TXT_MUT, width=90, anchor="w")
        status_lbl.pack(side="right", padx=(6, 2))
        name_var = tk.StringVar(value=m["suggested"])
        ctk.CTkEntry(row, textvariable=name_var, width=200, height=30,
                     font=ctk.CTkFont("Consolas", 11), fg_color=WIN_BG, border_color=BORDER,
                     text_color=TXT, corner_radius=8).pack(side="right", padx=(6, 0))
        label = f"{m['repo']}  /  {m['filename']}   ({fmt_size(m['size'])})"
        if m["suggested"] in self.existing:
            label += "   ⚠" + t("import_already")
        ctk.CTkLabel(row, text=label, font=ctk.CTkFont("Yu Gothic UI", 11), text_color=TXT,
                     anchor="w", justify="left").pack(side="left", fill="x", expand=True)
        self.rows.append({"data": m, "var": var, "name_var": name_var, "status": status_lbl})

    def _set_all(self, val):
        if self.importing:
            return
        for r in self.rows:
            r["var"].set(val)

    def _start(self):
        if self.importing:
            return
        chosen = [r for r in self.rows if r["var"].get()]
        if not chosen:
            messagebox.showwarning(t("import_title"), t("import_nothing_checked"), parent=self)
            return
        for r in chosen:
            if not r["name_var"].get().strip():
                messagebox.showwarning(t("import_title"), t("import_bad_name"), parent=self)
                return
        # 実行前の確認（個数・合計容量・元ファイル削除の有無を提示）
        total = sum(r["data"]["size"] for r in chosen)
        msg = t("import_confirm", n=len(chosen), size=fmt_size(total))
        if self.del_source.get():
            msg += t("import_confirm_delsrc")
        if not messagebox.askyesno(t("import_confirm_title"), msg, parent=self):
            return
        self.importing = True
        self._cancel = False
        self.chk_del.configure(state="disabled")
        self.btn_import.configure(state="disabled", text=t("import_importing"))
        self.btn_close.configure(state="normal", text=t("import_cancel"), command=self._cancel_import,
                                 text_color=RED, border_color=RED_BD, hover_color=RED_HOV)
        threading.Thread(target=self._worker, args=(chosen,), daemon=True).start()

    def _cancel_import(self):
        if not self.importing:
            return
        self._cancel = True
        self.btn_close.configure(state="disabled", text=t("import_cancelling"))

    def _worker(self, chosen):
        ok = fail = 0
        cancelled = False
        n = len(chosen)
        for i, r in enumerate(chosen, 1):
            if self._cancel:
                cancelled = True
                break
            name = r["name_var"].get().strip()
            path = r["data"]["path"]

            def prog(status, i=i, name=name, r=r):
                self.after(0, lambda: self.status_lbl.configure(
                    text=t("import_progress", i=i, n=n, name=name, status=status), text_color=LAV_TXT))
                self.after(0, lambda: r["status"].configure(text=status, text_color=LAV_TXT))

            try:
                ollama_import_gguf(name, path, on_progress=prog, should_cancel=lambda: self._cancel)
                ok += 1
                # 「元ファイルも削除」がONなら、取り込み成功後に LM Studio の .gguf を消す
                if self.del_source.get():
                    try:
                        os.remove(path)
                    except OSError:
                        pass
                self.after(0, lambda r=r: r["status"].configure(text=t("import_row_done"),
                                                                text_color=OK_GREEN))
            except ImportCancelled:
                cancelled = True
                self.after(0, lambda r=r: r["status"].configure(text="", text_color=TXT_MUT))
                break
            except Exception as e:
                fail += 1
                msg = str(e)
                self.after(0, lambda r=r, msg=msg: r["status"].configure(
                    text=t("import_row_fail", e=msg[:24]), text_color=RED))
        self.after(0, lambda: self._finish(ok, fail, cancelled))

    def _finish(self, ok, fail, cancelled=False):
        self.importing = False
        self._cancel = False
        self.chk_del.configure(state="normal")
        self.btn_import.configure(state="normal", text=t("import_do"))
        self.btn_close.configure(state="normal", text=t("import_close"), command=self._close,
                                 text_color=TXT_MUT, border_color=GHOST_BD, hover_color=GHOST_HOV)
        if cancelled:
            self.status_lbl.configure(text=t("import_cancelled", ok=ok, fail=fail), text_color=WARN_AMBER)
        else:
            self.status_lbl.configure(text=t("import_finished", ok=ok, fail=fail),
                                      text_color=OK_GREEN if fail == 0 else WARN_AMBER)
        if self.on_done:
            self.on_done(ok)

    def _close(self):
        if self.importing:
            self._cancel_import()  # 取り込み中の×は「中止」として扱う（窓は中止完了後に手動で閉じる）
            return
        self.destroy()


def copy_suggest(name):
    """コピー/派生のたたき台名（元の名前の末尾に -copy）。"""
    return f"{name}-copy"


def ask_name(parent, title, body, default=""):
    dlg = AskNameDialog(parent, title, body, default)
    parent.wait_window(dlg)
    return dlg.result


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(t("app_title"))
        self.root.geometry("1140x760")
        self.root.minsize(960, 640)
        self.root.configure(fg_color=WIN_BG)
        _ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modecole.ico")
        if os.path.isfile(_ico):
            self.root.iconbitmap(_ico)
            self.root.after(200, lambda: self.root.iconbitmap(_ico))
        self.models = []
        self.selected_model = None
        self.owui_prompt_set = set()
        self.row_widgets = {}
        self._fonts()
        self._build()
        self.refresh()

    def _fonts(self):
        self.f_brand = ctk.CTkFont("Yu Gothic UI", 20, "bold")
        self.f_sub = ctk.CTkFont("Yu Gothic UI", 11)
        self.f_h = ctk.CTkFont("Yu Gothic UI", 13, "bold")
        self.f_row = ctk.CTkFont("Yu Gothic UI", 13)
        self.f_size = ctk.CTkFont("Yu Gothic UI", 11)
        self.f_chip = ctk.CTkFont("Yu Gothic UI", 11)
        self.f_lbl = ctk.CTkFont("Yu Gothic UI", 11, "bold")
        self.f_val = ctk.CTkFont("Yu Gothic UI", 13)
        self.f_btn = ctk.CTkFont("Yu Gothic UI", 13, "bold")
        self.f_mono = ctk.CTkFont("Consolas", 11)
        self.f_mut = ctk.CTkFont("Yu Gothic UI", 11)
        self.f_big = ctk.CTkFont("Yu Gothic UI", 16, "bold")

    def show_help(self):
        HelpDialog(self.root)

    def toggle_language(self):
        global LANG
        LANG = "en" if LANG == "ja" else "ja"
        prev = self.selected_model
        self.selected_model = None
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title(t("app_title"))
        self._build()
        self._render_list()
        if prev and prev in self.row_widgets:
            self._select(prev)

    def _build(self):
        hdr = ctk.CTkFrame(self.root, fg_color="transparent")
        hdr.pack(fill="x", padx=18, pady=(14, 6))
        left = ctk.CTkFrame(hdr, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text=t("brand"), font=self.f_brand,
                     text_color=PINK_TXT).pack(side="left")
        self.status_lbl = ctk.CTkLabel(left, text="", font=self.f_sub, text_color=OK_GREEN)
        self.status_lbl.pack(side="left", padx=14)

        right = ctk.CTkFrame(hdr, fg_color="transparent")
        right.pack(side="right")
        self.search_entry = ctk.CTkEntry(right, placeholder_text=t("search_ph"),
                                         placeholder_text_color="#ab9fb8", font=self.f_row,
                                         width=210, height=34, fg_color=CARD,
                                         border_color=BORDER, text_color=TXT, corner_radius=18)
        self.search_entry.pack(side="left", padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", lambda e: self._render_list())
        ctk.CTkButton(right, text=t("help_button"), command=self.show_help, font=self.f_row,
                      fg_color="transparent", hover_color=LAV_HOV, text_color=LAV_TXT,
                      border_width=1, border_color=LAV, corner_radius=18, height=34,
                      width=96).pack(side="left", padx=(0, 8))
        ctk.CTkButton(right, text=t("lang_button"), command=self.toggle_language,
                      font=self.f_row, fg_color="transparent", hover_color=GHOST_HOV,
                      text_color=TXT_MUT, border_width=1, border_color=GHOST_BD,
                      corner_radius=18, height=34, width=88).pack(side="left", padx=(0, 8))
        ctk.CTkButton(right, text=t("refresh"), command=self.refresh, font=self.f_row,
                      fg_color=LAV, hover_color=LAV_TXT, text_color="#ffffff",
                      corner_radius=18, height=34, width=94).pack(side="left")

        main = ctk.CTkFrame(self.root, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=18, pady=(6, 14))

        # 左: モデル一覧（ボタンは置かない＝視点を散らさない）
        left_panel = ctk.CTkFrame(main, fg_color="transparent", width=430)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)
        lh = ctk.CTkFrame(left_panel, fg_color="transparent")
        lh.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(lh, text=t("list_title"), font=self.f_h,
                     text_color=LAV_TXT).pack(side="left")
        self.count_lbl = ctk.CTkLabel(lh, text="", font=self.f_mut, text_color=TXT_MUT)
        self.count_lbl.pack(side="left", padx=8)
        ctk.CTkButton(lh, text=t("import_button"), command=self.cmd_import_lmstudio,
                      font=self.f_mut, fg_color="transparent", hover_color=LAV_HOV,
                      text_color=LAV_TXT, border_width=1, border_color=LAV,
                      corner_radius=14, height=28, width=98).pack(side="right")
        ctk.CTkLabel(left_panel, text=t("legend_hint"), font=self.f_mut,
                     text_color=TXT_MUT, anchor="w").pack(fill="x", pady=(0, 4))
        self.list_frame = ctk.CTkScrollableFrame(left_panel, fg_color=CARD, corner_radius=14,
                                                 border_width=1, border_color=BORDER)
        self.list_frame.pack(fill="both", expand=True)

        # 右: 詳細 ＋ 操作ボタン（選んだモデルの真下で完結＝視線移動を最小化）
        right_panel = ctk.CTkFrame(main, fg_color="transparent")
        right_panel.pack(side="left", fill="both", expand=True, padx=(14, 0))
        ctk.CTkLabel(right_panel, text=t("detail_title"), font=self.f_h,
                     text_color=LAV_TXT, anchor="w").pack(fill="x", pady=(0, 4))

        act = ctk.CTkFrame(right_panel, fg_color="transparent")
        act.pack(side="bottom", fill="x", pady=(10, 0))
        ctk.CTkButton(act, text=t("btn_edit"), command=self.cmd_edit_prompt, font=self.f_btn,
                      fg_color=PINK, hover_color=PINK_HOV, text_color="#ffffff",
                      corner_radius=20, height=42, width=150).pack(side="left", padx=(0, 8))
        ctk.CTkButton(act, text=t("btn_derive"), command=self.cmd_new_derived, font=self.f_btn,
                      fg_color="transparent", hover_color=LAV_HOV, text_color=LAV_TXT,
                      border_width=1, border_color=LAV, corner_radius=20, height=42,
                      width=132).pack(side="left", padx=(0, 8))
        ctk.CTkButton(act, text=t("btn_copy"), command=self.cmd_copy, font=self.f_row,
                      fg_color="transparent", hover_color=GHOST_HOV, text_color=TXT_MUT,
                      border_width=1, border_color=GHOST_BD, corner_radius=20, height=42,
                      width=96).pack(side="left", padx=(0, 8))
        ctk.CTkButton(act, text=t("btn_rename"), command=self.cmd_rename, font=self.f_row,
                      fg_color="transparent", hover_color=GHOST_HOV, text_color=TXT_MUT,
                      border_width=1, border_color=GHOST_BD, corner_radius=20, height=42,
                      width=110).pack(side="left")
        ctk.CTkButton(act, text=t("btn_delete"), command=self.cmd_delete, font=self.f_row,
                      fg_color="transparent", hover_color=RED_HOV, text_color=RED,
                      border_width=1, border_color=RED_BD, corner_radius=20, height=42,
                      width=96).pack(side="right")

        self.detail_card = ctk.CTkFrame(right_panel, fg_color=CARD, corner_radius=16,
                                        border_width=1, border_color=BORDER)
        self.detail_card.pack(fill="both", expand=True)
        self._build_detail()

    def _build_detail(self):
        self.detail_empty = ctk.CTkFrame(self.detail_card, fg_color="transparent")
        ctk.CTkLabel(self.detail_empty, text="🦙",
                     font=ctk.CTkFont("Yu Gothic UI", 40)).pack(pady=(0, 6))
        ctk.CTkLabel(self.detail_empty, text=t("empty_detail"), font=self.f_val,
                     text_color=TXT_HINT).pack()

        self.detail_filled = ctk.CTkFrame(self.detail_card, fg_color="transparent")
        pad = ctk.CTkFrame(self.detail_filled, fg_color="transparent")
        pad.pack(fill="both", expand=True, padx=18, pady=16)
        self.d_name = ctk.CTkLabel(pad, text="", font=self.f_big, text_color=PINK_TXT,
                                   anchor="w", justify="left", wraplength=520)
        self.d_name.pack(fill="x")
        self.d_meta = ctk.CTkLabel(pad, text="", font=self.f_mut, text_color=TXT_MUT,
                                   anchor="w")
        self.d_meta.pack(fill="x", pady=(2, 10))
        self.d_size = self._kv(pad, t("lbl_size"))
        self.d_use = self._kv(pad, t("lbl_usecase"))
        self.d_webui = self._kv(pad, t("lbl_owui_row"))
        self.d_hash = self._kv(pad, t("lbl_hash"), mono=True)
        ctk.CTkLabel(pad, text=t("lbl_embedded"), font=self.f_lbl, text_color=LAV_TXT,
                     anchor="w").pack(fill="x", pady=(8, 4))
        self.prompt_box = ctk.CTkTextbox(pad, font=self.f_mono, fg_color="#fbf8fc",
                                         border_color=BORDER, border_width=1, text_color=TXT,
                                         wrap="word", corner_radius=10)
        self.prompt_box.pack(fill="both", expand=True)
        self.prompt_box.configure(state="disabled")
        self._show_empty()

    def _kv(self, parent, label, mono=False):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=label, font=self.f_lbl, text_color=TXT_MUT, width=118,
                     anchor="w").pack(side="left")
        val = ctk.CTkLabel(row, text="—", font=(self.f_mono if mono else self.f_val),
                           text_color=TXT, anchor="w", justify="left", wraplength=360)
        val.pack(side="left", fill="x", expand=True)
        return val

    def _show_empty(self):
        self.detail_filled.pack_forget()
        self.detail_empty.pack(expand=True)
        try:
            self.detail_card.configure(border_color=BORDER, border_width=1)
        except Exception:
            pass

    def _show_filled(self):
        self.detail_empty.pack_forget()
        self.detail_filled.pack(fill="both", expand=True)
        try:
            self.detail_card.configure(border_color=PINK, border_width=2)
        except Exception:
            pass

    def _flash_detail(self):
        try:
            self.detail_card.configure(fg_color=PINK_FLASH)
            self.root.after(200, lambda: self.detail_card.configure(fg_color=CARD))
        except Exception:
            pass

    def set_status(self, msg, color=None):
        self.status_lbl.configure(text=msg, text_color=color or OK_GREEN)

    def _model_names(self):
        return [m["name"] for m in self.models]

    def cmd_import_lmstudio(self):
        models = scan_lmstudio_models()
        if models is None:
            messagebox.showwarning(t("import_title"), t("import_no_folder"))
            return
        if not models:
            messagebox.showinfo(t("import_title"), t("import_none_found"))
            return
        ImportDialog(self.root, models, set(self._model_names()), on_done=self._after_import)

    def _after_import(self, ok):
        if ok:
            self.set_status(t("import_status_done", ok=ok), OK_GREEN)
        self.refresh()

    def refresh(self):
        self.set_status(t("status_loading"), WARN_AMBER)

        def fetch():
            try:
                result = ollama_get("/api/tags")
                self.models = sorted(result.get("models", []),
                                     key=lambda m: m.get("name", ""))
            except Exception as e:
                self.root.after(0, lambda: self.set_status(t("status_conn_error", e=e), RED))
                return
            try:
                owui = openwebui_get_base_models()
                self.owui_prompt_set = {m.get("id") for m in owui
                                        if (m.get("params") or {}).get("system")}
            except Exception:
                self.owui_prompt_set = set()
            self.root.after(0, self._render_list)

        threading.Thread(target=fetch, daemon=True).start()

    def _render_list(self):
        if not hasattr(self, "list_frame"):
            return
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.row_widgets = {}
        flt = self.search_entry.get().strip().lower() if hasattr(self, "search_entry") else ""

        from collections import Counter
        dc = Counter(short_hash(m.get("digest", "")) for m in self.models)
        dup_map = {}
        ci = 0
        for h, c in dc.items():
            if c > 1:
                dup_map[h] = DUP_TINTS[ci % len(DUP_TINTS)]
                ci += 1

        for m in self.models:
            name = m.get("name", "")
            if flt and flt not in name.lower():
                continue
            base = dup_map.get(short_hash(m.get("digest", "")), "transparent")
            row = ctk.CTkFrame(self.list_frame, fg_color=base, corner_radius=10)
            row.pack(fill="x", padx=4, pady=3)
            inner = ctk.CTkFrame(row, fg_color="transparent")
            inner.pack(fill="x", padx=10, pady=7)
            nl = ctk.CTkLabel(inner, text=name, font=self.f_row, text_color=TXT,
                              anchor="w", justify="left", wraplength=250)
            nl.pack(side="left", fill="x", expand=True)
            rt = ctk.CTkFrame(inner, fg_color="transparent")
            rt.pack(side="right")
            if name in self.owui_prompt_set:
                ctk.CTkLabel(rt, text=" 🌐 WebUI ", font=self.f_chip, fg_color=CHIP_BG,
                             text_color=CHIP_TX, corner_radius=8).pack(side="left", padx=(0, 8))
            ctk.CTkLabel(rt, text=fmt_size(m.get("size", 0)), font=self.f_size,
                         text_color=TXT_MUT).pack(side="left")
            self.row_widgets[name] = {"row": row, "name_label": nl, "base": base}
            self._bind_click(row, name)

        dup_groups = sum(1 for c in dc.values() if c > 1)
        cnt = t("status_count", n=len(self.models))
        if dup_groups:
            cnt += t("status_dup", n=dup_groups)
        self.count_lbl.configure(text=cnt)
        self.set_status(t("ready"), OK_GREEN)
        if self.selected_model in self.row_widgets:
            self._highlight(self.selected_model)

    def _bind_click(self, widget, name):
        widget.bind("<Button-1>", lambda e, n=name: self._select(n))
        for ch in widget.winfo_children():
            self._bind_click(ch, name)

    def _highlight(self, name):
        for n, info in self.row_widgets.items():
            if n == name:
                info["row"].configure(fg_color=PINK_SOFT)
                info["name_label"].configure(text_color=PINK_TXT)
            else:
                info["row"].configure(fg_color=info["base"])
                info["name_label"].configure(text_color=TXT)

    def _select(self, name):
        if name not in self.row_widgets:
            return
        self.selected_model = name
        self._highlight(name)
        self._show_filled()
        self._flash_detail()
        m = next((x for x in self.models if x["name"] == name), {})
        synced = name in self.owui_prompt_set
        self.d_name.configure(text=name)
        self.d_meta.configure(text=t("loading"))
        self.d_size.configure(text=fmt_size(m.get("size", 0)))
        self.d_use.configure(text=get_use_case(name))
        self.d_webui.configure(text=(t("owui_yes") if synced else t("owui_no")),
                               text_color=(CHIP_TX if synced else TXT_MUT))
        self.d_hash.configure(text=m.get("digest", "—"))
        self._set_prompt(t("fetching"))

        def fetch():
            try:
                data = ollama_post("/api/show", {"model": name})
                self.root.after(0, lambda: self._show_details(data))
            except Exception as e:
                self.root.after(0, lambda: self.d_meta.configure(text=t("fetch_failed", e=e)))

        threading.Thread(target=fetch, daemon=True).start()

    def _show_details(self, data):
        details = data.get("details", {})
        parts = []
        for k in ("family", "parameter_size", "quantization_level", "format"):
            if details.get(k):
                parts.append(str(details[k]))
        self.d_meta.configure(text=("  ·  ".join(parts) if parts else t("no_info")))
        system = data.get("system", "")
        if system:
            content = t("sys_header", v=system)
        else:
            modelfile = data.get("modelfile", "")
            content = modelfile if modelfile else t("no_system")
        self._set_prompt(content)

    def _set_prompt(self, text):
        self.prompt_box.configure(state="normal")
        self.prompt_box.delete("1.0", "end")
        self.prompt_box.insert("1.0", text)
        self.prompt_box.configure(state="disabled")

    def _clear_details(self):
        self.selected_model = None
        self._show_empty()
        self._highlight("__none__")

    def _apply_dest_tag(self, name, to_ollama, to_openwebui):
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

    def _save_to_destinations(self, base, name, prompt, to_ollama, to_openwebui):
        self.set_status(t("saving", name=name), WARN_AMBER)

        def run():
            results = []
            if to_ollama:
                try:
                    def on_progress(status):
                        shown = status[:50] + "..." if len(status) > 50 else status
                        self.root.after(0, lambda: self.set_status(
                            t("saving_ollama", s=shown), WARN_AMBER))
                    ollama_create(name, base, prompt, on_progress)
                    results.append(("Ollama", True, None))
                except Exception as e:
                    results.append(("Ollama", False, e))
            if to_openwebui:
                self.root.after(0, lambda: self.set_status(t("saving_owui"), WARN_AMBER))
                try:
                    openwebui_update_system_prompt(name, prompt)
                    results.append(("OpenWebUI", True, None))
                except Exception as e:
                    results.append(("OpenWebUI", False, e))
            self.root.after(0, lambda: self._finish_save(name, results))

        threading.Thread(target=run, daemon=True).start()

    def _finish_save(self, name, results):
        oks = [dest for dest, ok, _ in results if ok]
        errs = [(dest, err) for dest, ok, err in results if not ok]
        if errs:
            detail = "\n\n".join(f"【{dest}】\n{err}" for dest, err in errs)
            ok_msg = t("save_ok_line", oks=" / ".join(oks)) if oks else ""
            messagebox.showwarning(t("save_partial_title", name=name),
                                   t("save_fail_body", ok=ok_msg, detail=detail),
                                   parent=self.root)
            self.set_status(t("save_partial", name=name,
                              oks=" / ".join(oks) if oks else t("none")),
                            WARN_AMBER if oks else RED)
        else:
            self.set_status(t("save_done", name=name, oks=" / ".join(oks)), OK_GREEN)
        self.refresh()

    def cmd_delete(self):
        if not self.selected_model:
            messagebox.showwarning(t("unselected"), t("del_unselected"), parent=self.root)
            return
        name = self.selected_model
        if not messagebox.askyesno(t("del_confirm_title"), t("del_confirm", name=name),
                                   icon="warning", parent=self.root):
            return
        self.set_status(t("deleting"), WARN_AMBER)

        def run():
            try:
                ollama_delete("/api/delete", {"model": name})
                self.root.after(0, lambda: self.set_status(t("del_done", name=name)))
                self.root.after(0, self._clear_details)
                self.root.after(0, self.refresh)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(t("del_error_title"), str(e),
                                                                parent=self.root))
                self.root.after(0, lambda: self.set_status(t("del_failed"), RED))

        threading.Thread(target=run, daemon=True).start()

    def cmd_copy(self):
        if not self.selected_model:
            messagebox.showwarning(t("unselected"), t("copy_unselected"), parent=self.root)
            return
        original = self.selected_model
        new_name = ask_name(self.root, t("copy_title"), t("copy_prompt", name=original),
                            default=copy_suggest(original))
        if not new_name or not new_name.strip():
            return
        new_name = new_name.strip()
        if new_name == original:
            messagebox.showinfo(t("nochange_title"), t("nochange"), parent=self.root)
            return
        self.set_status(t("copying"), WARN_AMBER)

        def run():
            try:
                ollama_post("/api/copy", {"source": original, "destination": new_name})
                self.root.after(0, lambda: self.set_status(
                    t("copy_done", a=original, b=new_name), OK_GREEN))
                self.root.after(0, self.refresh)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(t("copy_error_title"), str(e),
                                                                parent=self.root))
                self.root.after(0, lambda: self.set_status(t("copy_failed"), RED))

        threading.Thread(target=run, daemon=True).start()

    def cmd_rename(self):
        if not self.selected_model:
            messagebox.showwarning(t("unselected"), t("rename_unselected"), parent=self.root)
            return
        original = self.selected_model
        backup_name = original.replace(":", "_") + "_backup"
        new_name = ask_name(self.root, t("rename_title"), t("rename_prompt", name=original),
                            default=original)
        if not new_name or not new_name.strip():
            return
        new_name = new_name.strip()
        if new_name == original:
            messagebox.showinfo(t("nochange_title"), t("nochange"), parent=self.root)
            return
        if not messagebox.askyesno(t("rename_confirm_title"),
                                   t("rename_confirm", o=original, b=backup_name, n=new_name),
                                   parent=self.root):
            return

        def upd(msg, color=WARN_AMBER):
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
                upd(t("rn_done", o=original, n=new_name), OK_GREEN)
                self.root.after(0, self._clear_details)
                self.root.after(0, self.refresh)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    t("rename_error_title"), t("rename_error_body", e=e, b=backup_name),
                    parent=self.root))
                upd(t("rename_failed"), RED)
                self.root.after(0, self.refresh)

        threading.Thread(target=run, daemon=True).start()

    def cmd_new_derived(self):
        default_base = self.selected_model or ""

        def on_save(base, name, prompt, to_ollama, to_openwebui):
            final_name = self._apply_dest_tag(name, to_ollama, to_openwebui)
            self._save_to_destinations(base, final_name, prompt, to_ollama, to_openwebui)

        ModelfileEditor(self.root, title=t("title_derive"), model_names=self._model_names(),
                        default_base=default_base,
                        default_name=(copy_suggest(default_base) if default_base else ""),
                        default_prompt="", on_save=on_save, lock_to_ollama=True)

    def cmd_edit_prompt(self):
        if not self.selected_model:
            messagebox.showwarning(t("unselected"), t("edit_unselected"), parent=self.root)
            return
        name = self.selected_model
        self.set_status(t("loading"), WARN_AMBER)

        def fetch():
            try:
                data = ollama_post("/api/show", {"model": name})
                system = data.get("system", "")
                modelfile = data.get("modelfile", "")
                from_line = name
                for line in modelfile.splitlines():
                    stripped = line.strip()
                    if stripped.upper().startswith("FROM ") and not stripped.startswith("#"):
                        from_line = stripped[5:].strip()
                        break
                self.root.after(0, lambda: self._open_edit_dialog(name, from_line, system))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(t("fetch_error_title"), str(e),
                                                                parent=self.root))
                self.root.after(0, lambda: self.set_status(t("fetch_failed_status"), RED))

        threading.Thread(target=fetch, daemon=True).start()

    def _open_edit_dialog(self, current_name, from_line, current_prompt):
        self.set_status("")

        def on_save(base_model, new_name, new_prompt, to_ollama, to_openwebui):
            self._save_to_destinations(base_model, new_name, new_prompt, to_ollama, to_openwebui)

        ModelfileEditor(self.root, title=t("title_edit", name=current_name),
                        model_names=self._model_names(), default_base=current_name,
                        default_name=current_name, default_prompt=current_prompt,
                        on_save=on_save, base_readonly=True)


if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    root = ctk.CTk()
    App(root)
    root.mainloop()
