"""FastAPI アプリケーションと APScheduler の統合。"""

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException

from src.jobs import daily_report, monthly_summary, weekly_cleanup
from src.scheduler import SchedulerManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

scheduler_manager = SchedulerManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI の lifespan イベントで scheduler を管理する。"""
    # 起動時: ジョブを登録して scheduler を開始
    scheduler_manager.add_job(
        daily_report,
        trigger="cron",
        id="daily_report",
        hour=9,
        minute=0,
    )
    scheduler_manager.add_job(
        weekly_cleanup,
        trigger="cron",
        id="weekly_cleanup",
        day_of_week="mon",
        hour=2,
        minute=0,
    )
    scheduler_manager.add_job(
        monthly_summary,
        trigger="cron",
        id="monthly_summary",
        day=1,
        hour=0,
        minute=0,
    )
    scheduler_manager.start()
    logger.info("Application startup: scheduler started")

    yield

    # 終了時: scheduler を停止
    scheduler_manager.shutdown()
    logger.info("Application shutdown: scheduler stopped")


def create_app() -> FastAPI:
    """FastAPI アプリケーションを作成する。

    Returns:
        FastAPI アプリケーションインスタンス
    """
    app = FastAPI(title="APScheduler FastAPI Daily Jobs", lifespan=lifespan)

    @app.get("/")
    async def root() -> dict[str, str]:
        """ヘルスチェックエンドポイント。"""
        return {"status": "ok", "message": "APScheduler FastAPI Daily Jobs is running"}

    @app.get("/jobs")
    async def list_jobs() -> dict[str, list[dict[str, Any]]]:
        """登録されているジョブの一覧を取得する。"""
        jobs = scheduler_manager.get_jobs()
        return {"jobs": jobs}

    @app.get("/jobs/{job_id}")
    async def get_job(job_id: str) -> dict[str, Any]:
        """特定のジョブの詳細を取得する。"""
        job = scheduler_manager.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")
        return job

    return app
