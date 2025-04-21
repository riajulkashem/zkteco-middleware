from zk import ZK, const
from database_manager import DatabaseManager
from datetime import datetime


class FingerprintDeviceManager:
    """Manages communication with a ZKTeco fingerprint device using pyzk."""

    def __init__(self, ip="192.168.1.201", port=4370, password=0, db_manager=None):
        """Initialize the device manager with connection details and database manager.

        Args:
            ip (str): Device IP address (default: '192.168.1.201').
            port (int): Device port (default: 4370).
            password (int): Device password (default: 0).
            db_manager (DatabaseManager): Database manager instance (optional).
        """
        self.ip = ip
        self.port = port
        self.password = password
        self.db_manager = db_manager or DatabaseManager()
        self.zk = ZK(
            ip,
            port=port,
            timeout=5,
            password=password,
            force_udp=False,
            ommit_ping=False,
        )
        self.conn = None
        self.is_connect = False

    def is_connected(self):
        """Check if the device is connected.

        Returns:
            bool: True if connected, False otherwise.
        """
        if not self.is_connect or not self.conn:
            return False
        try:
            # Test connection by getting device time
            self.conn.get_time()
            return True
        except Exception:
            self.is_connect = False
            return False

    def connect(self):
        """Connect to the device and disable it for operations.

        Returns:
            tuple: (success: bool, message: str)
        """
        if self.is_connect:
            return True, "Already connected."
        try:
            self.conn = self.zk.connect()
            self.conn.disable_device()  # Disable device to prevent user activity
            self.is_connect = True
            self.conn.test_voice(index=0)  # Play 'Thank You' to confirm connection
            return True, "Connected successfully."
        except Exception as e:
            self.is_connect = False
            self.conn = None
            return False, f"Failed to connect: {str(e)}"

    def disconnect(self):
        """Disconnect from the device and re-enable it.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_connect or not self.conn:
            return True, "Not connected."
        try:
            self.conn.enable_device()  # Re-enable device
            self.conn.disconnect()
            self.is_connect = False
            self.conn = None
            return True, "Disconnected successfully."
        except Exception as e:
            return False, f"Failed to disconnect: {str(e)}"

    def create_user(self, uid, name, privilege, password, user_id, group_id="", card=0):
        """Create a new user on the device.

        Args:
            uid (int): Unique ID for the user on the device.
            name (str): User name.
            privilege (str): 'User' or 'Admin' (maps to const.USER_DEFAULT or const.USER_ADMIN).
            password (str): User password.
            user_id (str): User ID string for the device.
            group_id (str): Group ID (optional, default '').
            card (int): Card number (optional, default 0).

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_connected():
            return False, "Device not connected."
        try:
            privilege_val = (
                const.USER_ADMIN if privilege.lower() == "admin" else const.USER_DEFAULT
            )
            self.conn.set_user(
                uid=uid,
                name=name,
                privilege=privilege_val,
                password=password,
                group_id=group_id,
                user_id=str(user_id),
                card=card,
            )
            return True, "User created successfully."
        except Exception as e:
            return False, f"Failed to create user: {str(e)}"

    def get_users(self):
        """Retrieve all users from the device.

        Returns:
            tuple: (success: bool, users: list, message: str)
            users: List of dicts with keys: uid, name, privilege, password, group_id, user_id, card
        """
        if not self.is_connected():
            return False, [], "Device not connected."
        try:
            users = self.conn.get_users()
            user_list = [
                {
                    "uid": user.uid,
                    "name": user.name,
                    "privilege": "Admin"
                    if user.privilege == const.USER_ADMIN
                    else "User",
                    "password": user.password,
                    "group_id": user.group_id,
                    "user_id": user.user_id,
                    "card": user.card,
                }
                for user in users
            ]
            return True, user_list, "Users retrieved successfully."
        except Exception as e:
            return False, [], f"Failed to get users: {str(e)}"

    def update_user(
        self,
        uid,
        name=None,
        privilege=None,
        password=None,
        user_id=None,
        group_id=None,
        card=None,
    ):
        """Update an existing user on the device.

        Args:
            uid (int): Unique ID of the user to update.
            name (str, optional): New name.
            privilege (str, optional): 'User' or 'Admin'.
            password (str, optional): New password.
            user_id (str, optional): New user ID.
            group_id (str, optional): New group ID.
            card (int, optional): New card number.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_connected():
            return False, "Device not connected."
        try:
            # Get current user data
            users = self.conn.get_users()
            user = next((u for u in users if u.uid == uid), None)
            if not user:
                return False, "User not found."

            # Prepare updated data
            updated_data = {
                "uid": uid,
                "name": name if name is not None else user.name,
                "privilege": const.USER_ADMIN
                if privilege and privilege.lower() == "admin"
                else const.USER_DEFAULT
                if privilege
                else user.privilege,
                "password": password if password is not None else user.password,
                "group_id": group_id if group_id is not None else user.group_id,
                "user_id": str(user_id) if user_id is not None else user.user_id,
                "card": card if card is not None else user.card,
            }

            self.conn.set_user(**updated_data)
            return True, "User updated successfully."
        except Exception as e:
            return False, f"Failed to update user: {str(e)}"

    def delete_user(self, uid=None, user_id=None):
        """Delete a user from the device by UID or user_id.

        Args:
            uid (int, optional): Unique ID of the user.
            user_id (str, optional): User ID string.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_connected():
            return False, "Device not connected."
        if not uid and not user_id:
            return False, "UID or user_id required."
        try:
            self.conn.delete_user(uid=uid, user_id=user_id)
            return True, "User deleted successfully."
        except Exception as e:
            return False, f"Failed to delete user: {str(e)}"

    def pull_users_to_db(self):
        """Pull all users from the device and insert/update them in the User table.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_connected():
            return False, "Device not connected."
        try:
            success, users, message = self.get_users()
            if not success:
                return False, message

            device = next(
                (d for d in self.db_manager.get_devices() if d["ip"] == self.ip), None
            )
            device_id = device["id"] if device else None

            for user in users:
                user_data = {
                    "name": user["name"],
                    "privilege": user["privilege"],
                    "password": user["password"],
                    "user_id": int(user["user_id"]),
                    "group_id": int(user["group_id"]) if user["group_id"] else 0,
                    "device_id": device_id,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
                # Check if user exists by user_id
                existing_user = next(
                    (
                        u
                        for u in self.db_manager.get_users()
                        if u["user_id"] == user_data["user_id"]
                    ),
                    None,
                )
                if existing_user:
                    # Update existing user
                    self.db_manager.update_user(existing_user["id"], user_data)
                else:
                    # Insert new user
                    self.db_manager.insert_user(user_data)

            return True, f"{len(users)} users pulled and synced to database."
        except Exception as e:
            return False, f"Failed to pull users: {str(e)}"

    def pull_attendance_to_db(self):
        """Pull attendance records from the device and insert them into the Attendance table.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_connected():
            return False, "Device not connected."
        try:
            attendances = self.conn.get_attendance()
            if not attendances:
                return True, "No new attendance records found."

            count = 0
            for att in attendances:
                # Map status (pyzk uses integers: 0=check-in, 1=check-out, etc.)
                status_map = {0: "in", 1: "out"}
                status = status_map.get(att.status, None)  # Only store 'in' or 'out'

                attendance_data = {
                    "user_id": int(att.user_id),
                    "timestamp": att.timestamp,
                    "status": status,
                    "device_ip": self.ip,
                    "synced": False,
                    "created_at": datetime.now(),
                }

                # Check if attendance record exists (by user_id and timestamp)
                existing_att = next(
                    (
                        a
                        for a in self.db_manager.get_attendance()
                        if a["user_id"] == attendance_data["user_id"]
                        and a["timestamp"] == attendance_data["timestamp"]
                    ),
                    None,
                )
                if not existing_att:
                    success, message = self.db_manager.insert_attendance(
                        attendance_data
                    )
                    if success:
                        count += 1

            # Optionally clear attendance records from device
            # self.conn.clear_attendance()

            return True, f"{count} new attendance records inserted."
        except Exception as e:
            return False, f"Failed to pull attendance: {str(e)}"
