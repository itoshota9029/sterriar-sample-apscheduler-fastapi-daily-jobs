# APScheduler + FastAPI Daily Jobs

[![CI](https://github.com/itoshota9029/sterriar-sample-apscheduler-fastapi-daily-jobs/actions/workflows/ci.yml/badge.svg)](https://github.com/itoshota9029/sterriar-sample-apscheduler-fastapi-daily-jobs/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

FastAPI アプリに APScheduler で日次/週次/月次の cron ジョブを組み込む実装パターン。

## Features

- ⏰ **Cron-based scheduling**: 日次、週次、月次のジョブを cron 式で簡単に定義
- 🚀 **FastAPI integration**: lifespan イベントで scheduler のライフサイクルを管理
- 📊 **Job monitoring**: ジョブの実行状況を REST API で確認可能
- 🧪 **Fully tested**: unittest.mock を使った包括的なテスト

## Installation

```bash
git clone https://github.com/itoshota9029/sterriar-sample-apscheduler-fastapi-daily-jobs.git
cd sterriar-sample-apscheduler-fastapi-daily-jobs
pip install -e ".[dev]"
```

## Quick Start

```python
from src.scheduler import SchedulerManager
from src.app import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

サーバーを起動して以下のエンドポイントにアクセス:

- `GET /` - ヘルスチェック
- `GET /jobs` - 登録されているジョブ一覧
- `GET /jobs/{job_id}` - 特定ジョブの詳細

## Job Configuration

`src/jobs.py` でジョブを定義:

```python
def daily_report():
    """毎日午前9時に実行される日次レポート生成"""
    print("Generating daily report...")

def weekly_cleanup():
    """毎週月曜日午前2時にクリーンアップ"""
    print("Running weekly cleanup...")

def monthly_summary():
    """毎月1日午前0時に月次サマリ生成"""
    print("Creating monthly summary...")
```

## Development

### Run tests

```bash
pytest
```

### Lint & format

```bash
ruff check
ruff format --check
```

## Architecture

- `src/scheduler.py`: APScheduler の初期化とジョブ登録を管理
- `src/jobs.py`: 実行するジョブ関数の定義
- `src/app.py`: FastAPI アプリと lifespan イベントの統合

scheduler は FastAPI の lifespan context manager で起動・停止し、アプリケーションのライフサイクルと完全に同期します。

## License

MIT License - see [LICENSE](LICENSE) for details.
