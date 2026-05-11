"""SchedulerManager のテスト。"""

from unittest.mock import MagicMock, patch

from src.scheduler import SchedulerManager


def test_add_job():
    """ジョブの追加が正しく動作することを確認する。"""
    manager = SchedulerManager()
    mock_func = MagicMock()

    with patch.object(manager.scheduler, "add_job") as mock_add_job:
        manager.add_job(mock_func, "cron", "test_job", hour=9, minute=0)
        mock_add_job.assert_called_once_with(mock_func, "cron", id="test_job", hour=9, minute=0)


def test_start_scheduler():
    """Scheduler の起動が正しく動作することを確認する。"""
    manager = SchedulerManager()

    with patch.object(manager.scheduler, "start") as mock_start:
        manager.start()
        mock_start.assert_called_once()
        assert manager._started is True

        # 2回目の呼び出しでは start が呼ばれないことを確認
        manager.start()
        mock_start.assert_called_once()  # まだ1回のまま


def test_shutdown_scheduler():
    """Scheduler の停止が正しく動作することを確認する。"""
    manager = SchedulerManager()
    manager._started = True

    with patch.object(manager.scheduler, "shutdown") as mock_shutdown:
        manager.shutdown()
        mock_shutdown.assert_called_once_with(wait=False)
        assert manager._started is False


def test_get_jobs():
    """ジョブ一覧の取得が正しく動作することを確認する。"""
    manager = SchedulerManager()

    # モックジョブを作成
    mock_job1 = MagicMock()
    mock_job1.id = "job1"
    mock_job1.name = "Test Job 1"
    mock_job1.next_run_time = None
    mock_job1.trigger = "cron"

    mock_job2 = MagicMock()
    mock_job2.id = "job2"
    mock_job2.name = "Test Job 2"
    mock_job2.next_run_time = MagicMock()
    mock_job2.next_run_time.isoformat.return_value = "2024-01-01T09:00:00"
    mock_job2.trigger = "interval"

    with patch.object(manager.scheduler, "get_jobs", return_value=[mock_job1, mock_job2]):
        jobs = manager.get_jobs()

        assert len(jobs) == 2
        assert jobs[0]["id"] == "job1"
        assert jobs[0]["next_run_time"] is None
        assert jobs[1]["id"] == "job2"
        assert jobs[1]["next_run_time"] == "2024-01-01T09:00:00"


def test_get_job_found():
    """特定のジョブが正しく取得できることを確認する。"""
    manager = SchedulerManager()

    mock_job = MagicMock()
    mock_job.id = "job1"
    mock_job.name = "Test Job"
    mock_job.next_run_time = MagicMock()
    mock_job.next_run_time.isoformat.return_value = "2024-01-01T09:00:00"
    mock_job.trigger = "cron"

    with patch.object(manager.scheduler, "get_job", return_value=mock_job):
        job = manager.get_job("job1")

        assert job is not None
        assert job["id"] == "job1"
        assert job["name"] == "Test Job"
        assert job["next_run_time"] == "2024-01-01T09:00:00"


def test_get_job_not_found():
    """存在しないジョブを取得しようとした場合に None が返ることを確認する。"""
    manager = SchedulerManager()

    with patch.object(manager.scheduler, "get_job", return_value=None):
        job = manager.get_job("nonexistent")
        assert job is None
