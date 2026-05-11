"""FastAPI アプリケーションのテスト。"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import create_app


def test_root_endpoint():
    """ルートエンドポイントが正しく動作することを確認する。"""
    with (
        patch("src.app.scheduler_manager.add_job"),
        patch("src.app.scheduler_manager.start"),
        patch("src.app.scheduler_manager.shutdown"),
    ):
        app = create_app()
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "APScheduler FastAPI Daily Jobs" in data["message"]


def test_list_jobs_endpoint():
    """ジョブ一覧エンドポイントが正しく動作することを確認する。"""
    mock_jobs = [
        {"id": "job1", "name": "Job 1", "next_run_time": None, "trigger": "cron"},
        {
            "id": "job2",
            "name": "Job 2",
            "next_run_time": "2024-01-01T09:00:00",
            "trigger": "interval",
        },
    ]

    with (
        patch("src.app.scheduler_manager.add_job"),
        patch("src.app.scheduler_manager.start"),
        patch("src.app.scheduler_manager.shutdown"),
        patch("src.app.scheduler_manager.get_jobs", return_value=mock_jobs),
    ):
        app = create_app()
        client = TestClient(app)

        response = client.get("/jobs")
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
        assert len(data["jobs"]) == 2
        assert data["jobs"][0]["id"] == "job1"


def test_get_job_endpoint_found():
    """特定のジョブが正しく取得できることを確認する。"""
    mock_job = {
        "id": "daily_report",
        "name": "Daily Report",
        "next_run_time": "2024-01-01T09:00:00",
        "trigger": "cron",
    }

    with (
        patch("src.app.scheduler_manager.add_job"),
        patch("src.app.scheduler_manager.start"),
        patch("src.app.scheduler_manager.shutdown"),
        patch("src.app.scheduler_manager.get_job", return_value=mock_job),
    ):
        app = create_app()
        client = TestClient(app)

        response = client.get("/jobs/daily_report")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "daily_report"
        assert data["name"] == "Daily Report"


def test_get_job_endpoint_not_found():
    """存在しないジョブを取得しようとした場合に404が返ることを確認する。"""
    with (
        patch("src.app.scheduler_manager.add_job"),
        patch("src.app.scheduler_manager.start"),
        patch("src.app.scheduler_manager.shutdown"),
        patch("src.app.scheduler_manager.get_job", return_value=None),
    ):
        app = create_app()
        client = TestClient(app)

        response = client.get("/jobs/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]


def test_lifespan_scheduler_management():
    """lifespan イベントで scheduler が正しく管理されることを確認する。"""
    with (
        patch("src.app.scheduler_manager.add_job") as mock_add,
        patch("src.app.scheduler_manager.start") as mock_start,
        patch("src.app.scheduler_manager.shutdown") as mock_shutdown,
    ):
        app = create_app()
        with TestClient(app):
            # lifespan の起動処理が実行されることを確認
            assert mock_add.call_count == 3  # 3つのジョブが登録される
            mock_start.assert_called_once()

        # lifespan の終了処理が実行されることを確認
        mock_shutdown.assert_called_once()
