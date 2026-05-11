"""APScheduler のラッパーと管理クラス。"""

import logging
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


class SchedulerManager:
    """APScheduler を管理するシングルトンクラス。"""

    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler(timezone="Asia/Tokyo")
        self._started = False

    def add_job(
        self,
        func: callable,
        trigger: str,
        id: str,
        **trigger_args: Any,
    ) -> None:
        """ジョブを登録する。

        Args:
            func: 実行する関数
            trigger: トリガータイプ ("cron", "interval" など)
            id: ジョブID
            **trigger_args: トリガーの引数 (hour, minute, day_of_week など)
        """
        self.scheduler.add_job(func, trigger, id=id, **trigger_args)
        logger.info(f"Job '{id}' added with trigger '{trigger}' and args {trigger_args}")

    def start(self) -> None:
        """Scheduler を起動する。"""
        if not self._started:
            self.scheduler.start()
            self._started = True
            logger.info("Scheduler started")

    def shutdown(self) -> None:
        """Scheduler を停止する。"""
        if self._started:
            self.scheduler.shutdown(wait=False)
            self._started = False
            logger.info("Scheduler shutdown")

    def get_jobs(self) -> list[dict[str, Any]]:
        """登録されているジョブの一覧を取得する。

        Returns:
            ジョブ情報のリスト
        """
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append(
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run_time": (job.next_run_time.isoformat() if job.next_run_time else None),
                    "trigger": str(job.trigger),
                }
            )
        return jobs

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        """特定のジョブ情報を取得する。

        Args:
            job_id: ジョブID

        Returns:
            ジョブ情報、存在しない場合は None
        """
        job = self.scheduler.get_job(job_id)
        if not job:
            return None
        return {
            "id": job.id,
            "name": job.name,
            "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger),
        }
