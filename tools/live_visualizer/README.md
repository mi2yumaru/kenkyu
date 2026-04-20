# Avida Live Visualizer

Avida シミュレーションの標準出力をリアルタイムで可視化する最小構成のダッシュボード。

## 特徴

- 🧬 **Avida 本体を改造なし** で外側から可視化
- 📊 **4つのメトリクス** をリアルタイムグラフ表示
  - `UD` (Update)
  - `Gen` (Generation)
  - `Fit` (Fitness)
  - `Orgs` (Population Size)
- ⏯️ **Start / Stop ボタン** で簡単操作
- 📈 **matplotlib** で高速・安定した描画
- 🪟 **Windows 対応**

## 前提条件

- Windows 10/11
- Python 3.8+
- Avida 実行ファイル: `C:\avida\build\bin\Debug\avida.exe` が実行可能
- Avida 設定ファイル: `C:\avida\build\bin\Debug\` に `avida.cfg` 等が配置済み

## セットアップ手順

### 1. Python 仮想環境作成

```powershell
cd C:\avida\tools\live_visualizer
python -m venv venv
```

### 2. 仮想環境を有効化

```powershell
# PowerShell の場合
.\venv\Scripts\Activate.ps1

# (もしエラーが出たら: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)
```

### 3. パッケージをインストール

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## 実行方法

### 1. 仮想環境を有効化（未実行の場合）

```powershell
cd C:\avida\tools\live_visualizer
.\venv\Scripts\Activate.ps1
```

### 2. Streamlit アプリを起動

```powershell
streamlit run app.py
```

ブラウザが自動で開き、`http://localhost:8501` にアクセスします。

### 3. シミュレーション実行

- **▶ Start Simulation** ボタンをクリック
- グラフがリアルタイムで更新される
- **⏹ Stop Simulation** で停止

## ディレクトリ構成

```
C:\avida\tools\live_visualizer\
├─ app.py              # メインアプリケーション
├─ requirements.txt    # 依存パッケージ
├─ README.md           # このファイル
└─ venv\               # 仮想環境（生成後）
```

## トラブルシューティング

### Avida.exe が見つからない

- `C:\avida\build\bin\Debug\avida.exe` が存在するか確認
- `avida.cfg` が `C:\avida\build\bin\Debug\` に存在するか確認
- Avida が正常にビルドされているか確認

### グラフが表示されない

- **Start** ボタンをクリック後、十分に待つ（最初のデータが来るまで数秒かかる場合あり）
- Avida が標準出力を正しく出力しているか確認（コマンドプロンプトで直接実行してみる）

### Streamlit がエラーで落ちる

- 仮想環境が正しく有効化されているか確認
- `pip install -r requirements.txt` で再インストール
- ブラウザのキャッシュをクリアして再度アクセス

### データが解析されない

- Avida の出力フォーマットが変わった可能性
- `app.py` の `parse_avida_line()` 関数をデバッグ
- PowerShell で直接 `avida.exe -r` を実行して出力を確認

## 動作確認手順

```powershell
# 1. Avida が実行できるか確認
cd C:\avida\build\bin\Debug
.\avida.exe -h

# 2. 出力形式を確認（最初の数行を見る）
# UD, Gen, Fit, Orgs の順で数値が並んでいることを確認
```

## 今後の拡張

- Avida 設定ファイル選択ダイアログ
- 複数実験の同時比較
- データのCSV エクスポート
- より詳細な統計情報
- カスタム可視化

## ライセンス

Avida 本体と同じライセンスに従う。

---

**作成日**: 2026-04-21  
**環境**: Windows 10/11, Python 3.8+, Streamlit 1.28+
