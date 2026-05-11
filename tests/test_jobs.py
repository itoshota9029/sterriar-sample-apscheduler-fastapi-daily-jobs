"""ジョブ関数のテスト。"""

import logging
from unittest.mock import patch

from src.jobs import daily_report, monthly_summary, weekly_cleanup


def test_daily_report_logging():
    """daily_report がログを出力することを確認する。"""
    with patch.object(logging.getLogger("src.jobs"), "info") as mock_log:
        daily_report()
        mock_log.assert_called_once()
        call_args = mock_log.call_args[0][0]
        assert "Running daily report generation" in call_args


def test_weekly_cleanup_logging():
    """weekly_cleanup がログを出力することを確認する。"""
    with patch.object(logging.getLogger("src.jobs"), "info") as mock_log:
        weekly_cleanup()
        mock_log.assert_called_once()
        call_args = mock_log.call_args[0][0]
        assert "Running weekly cleanup" in call_args


def test_monthly_summary_logging():
    """monthly_summary がログを出力することを確認する。"""
    with patch.object(logging.getLogger("src.jobs"), "info") as mock_log:
        monthly_summary()
        mock_log.assert_called_once()
        call_args = mock_log.call_args[0][0]
        assert "Creating monthly summary" in call_args
