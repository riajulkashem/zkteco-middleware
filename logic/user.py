from database_manager import DatabaseManager


class UserManagementLogic:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()

    def add_user(self, name, privilege, password, user_id, group_id, device_id):
        if not all([name, privilege, password, user_id, group_id]):
            return False, "All fields except Device are required."

        try:
            user_id = int(user_id)
            group_id = int(group_id)
            device_id = int(device_id) if device_id else None
        except ValueError:
            return False, "User ID, Group ID, and Device ID must be numbers."

        return self.db_manager.insert_user(
            {
                "name": name,
                "privilege": privilege,
                "password": password,
                "user_id": user_id,
                "group_id": group_id,
                "device_id": device_id,
            }
        )

    def edit_user(
        self, id_user, name, privilege, password, user_id, group_id, device_id
    ):
        try:
            user_id = int(user_id)
            group_id = int(group_id)
            device_id = int(device_id) if device_id else None
        except ValueError:
            return False, "User ID, Group ID, and Device ID must be numbers."

        return self.db_manager.update_user(
            id_user,
            {
                "name": name,
                "privilege": privilege,
                "password": password,
                "user_id": user_id,
                "group_id": group_id,
                "device_id": device_id,
            },
        )

    def delete_user(self, user_id):
        return self.db_manager.delete_user(user_id)

    def get_users(self):
        users = self.db_manager.get_users()
        devices = {d["id"]: d["name"] for d in self.db_manager.get_devices()}
        for user in users:
            user["device_name"] = (
                devices.get(user["device_id"], "") if user["device_id"] else ""
            )
        return users

    def get_devices(self):
        return self.db_manager.get_devices()
