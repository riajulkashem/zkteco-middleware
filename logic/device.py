from database_manager import DatabaseManager


class DeviceManagementLogic:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()

    def get_devices(self):
        return self.db_manager.get_devices()

    def validate_and_format(self, name, device_model, serial_number, ip, port):
        if not all([name, device_model, serial_number, ip, port]):
            return False, "All fields are required."

        try:
            port = int(port)
            if not (0 <= port <= 65535):
                raise ValueError
        except ValueError:
            return False, "Port must be a number between 0 and 65535."

        return True, {
            "name": name,
            "device_model": device_model,
            "serial_number": serial_number,
            "ip": ip,
            "port": port,
        }

    def add_device(self, **kwargs):
        valid, data_or_msg = self.validate_and_format(**kwargs)
        if not valid:
            return False, data_or_msg
        return self.db_manager.insert_device(data_or_msg)

    def edit_device(self, device_id, **kwargs):
        valid, data_or_msg = self.validate_and_format(**kwargs)
        if not valid:
            return False, data_or_msg
        return self.db_manager.update_device(device_id, data_or_msg)

    def delete_device(self, device_id):
        return self.db_manager.delete_device(device_id)

    def check_connection(self, device_id):
        return False, "Not Connected (stub)"
