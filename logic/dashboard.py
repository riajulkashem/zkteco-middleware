from datetime import datetime
from database_manager import DatabaseManager
from logic.device_control import FingerprintDeviceManager


class DashboardLogic:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()

    def sync_data(self):
        """Sync users and attendance from all devices, return sync timestamp.

        Returns:
            str: Timestamp of the sync in 'YYYY-MM-DD HH:MM:SS' format.
        """
        devices = self.db_manager.get_devices()

        cant_connected_devices = 0
        for device in devices:
            fdm = FingerprintDeviceManager(
                ip=device["ip"], port=device["port"], db_manager=self.db_manager
            )
            success, message = fdm.connect()
            if not success:
                cant_connected_devices += 1
                continue

            # Pull users
            fdm.pull_users_to_db()

            # Pull attendance
            fdm.pull_attendance_to_db()

            fdm.disconnect()
        if cant_connected_devices == len(devices):
            return False
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_card_data(self):
        """Return data for dashboard cards."""
        devices = self.db_manager.get_devices()
        total_devices = len(devices)
        connected_devices = 0

        for device in devices:
            fdm = FingerprintDeviceManager(
                ip=device["ip"], port=device["port"], db_manager=self.db_manager
            )
            success, _ = fdm.connect()
            if success and fdm.is_connected():
                connected_devices += 1
            fdm.disconnect()

        users = self.db_manager.get_users()
        total_users = len(users)

        return [
            {
                "label": "Total Device",
                "value": f"{total_devices}/{connected_devices}",
                "icon": "📟",
                "row": 0,
                "col": 0,
                "font_size": 16,
            },
            {
                "label": "Total Users",
                "value": str(total_users),
                "icon": "👥",
                "row": 0,
                "col": 1,
                "font_size": 16,
            },
        ]
