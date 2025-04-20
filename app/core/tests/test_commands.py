from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.test import TestCase
from psycopg2 import OperationalError
from io import StringIO


class WaitForDbCommandTests(TestCase):
    """
    🧪 Test suite for the wait_for_db management command
    """

    @patch("time.sleep", return_value=None)  # ⏰ avoid actual delay
    @patch("psycopg2.connect")  # 🔌 mock database connection
    def test_wait_for_db_retries_then_succeeds(self, mock_connect, mock_sleep):
        """
        ✅ Ensures the command retries on OperationalError and succeeds eventually.
        Test flow:
        1. 🔄 First 3 connection attempts fail
        2. ✨ 4th attempt succeeds
        3. 📝 Verify retry count and success message
        """

        # 🚫 Simulate 3 failures then a successful connection
        mock_connect.side_effect = [OperationalError] * 3 + [MagicMock()]

        # 📥 Capture output printed by the command
        out = StringIO()
        call_command("wait_for_db", stdout=out)

        # ✔️ Assert connection was attempted 4 times
        self.assertEqual(mock_connect.call_count, 4)

        # 🔍 Check that final success message is in output
        self.assertIn("Database is ready!", out.getvalue())
