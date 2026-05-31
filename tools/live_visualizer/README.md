# Avida を用いた有性生殖進化シミュレーション研究

## 概要

本リポジトリは、Avida を用いた人工生命シミュレーション環境を研究用に拡張・調整したものです。

主な目的は、**無性生殖集団のみが存在する環境において、どのような条件で有性生殖が出現・定着しうるか**を調べることです。

本研究では、環境変動、タスク難易度、資源条件、突然変異率などを操作し、進化動態や適応の変化を観測します。

特に、**環境変動下における適応度回復と高難度タスク獲得を指標に**、有性生殖の進化的有利性を評価します。

---

## 研究目的

本研究の目的は、Avida を用いて以下の問いを検討することです。

- 有性生殖はどのような環境条件で出現するのか
- 有性生殖はどのような条件で無性生殖より有利になるのか
- 環境変動やタスク難易度の変化は、進化の方向性にどのような影響を与えるのか
- 適応度の低下からの回復速度や高難度タスク獲得率は、生殖様式の違いとどう関係するのか

---

## 実験内容

本研究では、Avida 上で進化シミュレーションを実行し、主に以下を比較・測定します。

### 主な実験条件

- **Dish Size**: 30×30 （基本設定）
- **Mutation Rate**: 2% （操作変数として可変）
- **Offspring Placement**: random / neighbor （条件に応じて変更）
- **実行 Update 数**: 50,000～500,000 （実験ごとに指定）
- **環境変動**: ON / OFF （季節的変動の有無）
- **タスク報酬の難易度設定**: 複数パターン用意
- **資源条件**: 無制限 / 限定あり （実験変数）
- **生殖様式**: 無性のみ / 有性導入後 （主要比較対象）

### 主な測定項目

| 指標 | 説明 |
|------|------|
| **UD (Update)** | シミュレーション進行度 |
| **Gen (Generation)** | 平均世代数 |
| **Fit (Fitness)** | 平均適応度 |
| **Orgs (Organisms)** | 個体数 |
| **高難度タスク獲得率** | 複雑タスク達成個体の割合 |
| **環境変動後の回復時間** | 安定状態復帰までのステップ数 |
| **生殖様式ごとの割合変化** | 有性型・無性型個体の比率推移 |
| **適応度推移と安定性** | 平均適応度の変動係数 |

### 比較対象実験

1. **無性のみ環境** - ベースライン
2. **有性型導入後** - 相互作用効果
3. **限定資源条件** - 資源制限下での生殖戦略
4. **季節変動パターン差** - 環境変動の順序・周期の影響

### 備考

詳細な設定値や条件は、各種 config ファイルや実験用スクリプトを参照してください。

---

## このリポジトリの目的

本リポジトリは、以下を目的としています。

- Avida を用いた研究用シミュレーションコードの管理
- 実験設定ファイルの保存
- 実験の再現性確保
- 可視化ツールや補助スクリプトの管理
- 研究発表・論文執筆のための基盤整理

必要に応じて、本リポジトリは論文付属資料・実験再現用資料としても利用することを想定しています。

---

## リポジトリ構成

```text
.
├─ avida-core/               # Avida 本体コード (submodule)
├─ apps/                     # 関連アプリケーション
├─ libs/                     # 依存ライブラリ (submodule)
├─ documentation/            # 元のドキュメント類
├─ tools/
│  └─ live_visualizer/       # Streamlit による可視化ツール（研究補助用）
├─ build/                    # ローカルビルド生成物
└─ README.md
```

※ `build/` はローカル環境で生成されるため、Git 管理対象外とします。

---

## セットアップ

本研究で最低限必要なセットアップ手順を以下に示します。

### 必要環境

- Windows 10/11
- Visual Studio 2022
- CMake 4.x 以上
- Git (with submodule support)
- Python 3.8+ （可視化ツール利用時）

### Avida 本体のビルド

```powershell
# リポジトリクローン
git clone --recursive https://github.com/mi2yumaru/kenkyu.git
cd kenkyu

# ビルドディレクトリ作成
mkdir build
cd build

# CMake でプロジェクト生成
cmake .. -G "Visual Studio 17 2022" -A x64

# ビルド実行
cmake --build . --config Debug
```

ビルド完了後、`build/bin/Debug/avida.exe` が生成されます。

### 設定ファイルの配置

```powershell
# 設定ファイルをビルド出力ディレクトリにコピー
copy avida-core/support/config/*.cfg build/bin/Debug/
copy avida-core/support/environment/*.env build/bin/Debug/
```

必要な設定ファイル：
- `avida.cfg` - メイン設定
- `environment.cfg` - 環境・タスク定義  
- `instset-*.cfg` - 命令セット定義

### 実行

```powershell
cd build/bin/Debug
.\avida.exe

# カスタム設定ファイルを指定する場合
.\avida.exe -c custom_avida.cfg
```

---

## 可視化ツール（Live Visualizer）

Avida の標準出力をリアルタイム表示するための**研究補助用の可視化ツール**を `tools/live_visualizer/` に配置しています。

### セットアップ

```powershell
cd tools/live_visualizer

# Python 仮想環境作成
python -m venv venv

# パッケージインストール
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 起動

```powershell
cd tools/live_visualizer
.\venv\Scripts\python.exe -m streamlit run app.py
```

ブラウザで `http://localhost:8501` が自動で開きます。

### 機能

- **リアルタイム監視**: Avida の标准出力を監視し、`UD / Gen / Fit / Orgs` を自動抽出
- **グラフ描画**: Gen / Fit / Orgs の3つの折れ線グラフをリアルタイム更新
- **デバッグ情報**: Process PID、Exit Code、Parse 成功/失敗数を表示
- **操作**: Start / Stop / Clear ボタンで簡単操作

---

## 出力

シミュレーション実行によって得られる出力には、以下が含まれます。

- 標準出力ログ
- Fitness / Generation / Organism 数の推移
- 各種設定に基づく実験結果
- 可視化ツール上でのリアルタイム表示

---

## 著者

* **水谷太河** (Taikoh Mizutani)
* 筑波大学大学院理工情報生命学術院システム情報工学研究群情報理工学位プログラム
* 人工生命・進化シミュレーション研究

---

## ライセンス

本リポジトリは Avida をベースにしています。

元の Avida 本体に関する著作権およびライセンスは、Avida の原著作者および元リポジトリのライセンス条件に従います。

本研究のために追加したコード（`tools/live_visualizer/` など）、設定、補助スクリプトについては、研究目的での使用・改変は自由とします。ただし、本研究の結果を参照・引用する場合は著者名と本リポジトリを明記してください。

---

## 参考

* Avida official project: [http://avida.devosoft.org/](http://avida.devosoft.org/)
* Original Avida repository: [https://github.com/devosoft/avida](https://github.com/devosoft/avida)
