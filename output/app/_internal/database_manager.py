from peewee import *
from datetime import datetime

database = SqliteDatabase("app_data.db")


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    privilege = CharField()
    password = CharField()
    user_id = IntegerField(unique=True)
    group_id = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    device = ForeignKeyField(
        "self", backref="users", null=True, column_name="device_id"
    )

    class Meta:
        table_name = "users"


class Device(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    device_model = CharField()
    serial_number = CharField(unique=True)
    ip = CharField()
    port = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "devices"


class Attendance(BaseModel):
    id = AutoField()
    user_id = ForeignKeyField(
        User, field=User.user_id, backref="attendance", on_delete="CASCADE"
    )
    timestamp = DateTimeField()
    status = CharField(null=True)  # "in" or "out", optional
    device_ip = CharField()
    synced = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        indexes = (
            # Index on user_id and timestamp for efficient queries
            (("user_id", "timestamp"), False),
        )


class DatabaseManager:
    def __init__(self):
        self.database = database
        self._connect_once()

    def _connect_once(self):
        print("Connecting...")
        if not self.database.is_closed():
            return
        self.database.connect(reuse_if_open=True)

    def check_connection(self):
        try:
            self._connect_once()
            self.database.execute_sql(
                "SELECT 1"
            )  # Simple query to ensure DB is responsive
            return True, "Database connection is active."
        except Exception as e:
            return False, f"Database connection failed: {str(e)}"

    def initialize_tables(self):
        print("Initializing tables...")
        try:
            self._connect_once()
            User._meta.database = self.database
            Device._meta.database = self.database
            Attendance._meta.database = self.database

            self.database.create_tables([Device, User, Attendance], safe=True)
            print("Tables initialized.")
            return True, "Database and tables created successfully!"
        except Exception as e:
            return False, f"Failed to create database: {str(e)}"

    def insert_user(self, user_data):
        self._connect_once()
        with self.database.atomic():
            try:
                user = User.create(
                    name=user_data["name"],
                    privilege=user_data["privilege"],
                    password=user_data["password"],
                    user_id=user_data["user_id"],
                    group_id=user_data["group_id"],
                    device_id=user_data.get("device_id"),
                    updated_at=datetime.now(),
                )
                return True, user.id
            except IntegrityError as e:
                return False, f"Failed to insert user: {str(e)}"

    def get_users(self):
        self._connect_once()
        return [
            {
                "id": user.id,
                "name": user.name,
                "privilege": user.privilege,
                "password": user.password,
                "user_id": user.user_id,
                "group_id": user.group_id,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "device_id": user.device_id,
            }
            for user in User.select()
        ]

    def update_user(self, id_user, user_data):
        self._connect_once()
        with self.database.atomic():
            user = User.get_or_none(User.id == id_user)
            if user:
                try:
                    user.name = user_data["name"]
                    user.privilege = user_data["privilege"]
                    user.password = user_data["password"]
                    user.user_id = user_data["user_id"]
                    user.group_id = user_data["group_id"]
                    user.device_id = user_data.get("device_id")
                    user.updated_at = datetime.now()
                    user.save()
                    return True, "User updated successfully!"
                except IntegrityError as e:
                    return False, f"Failed to update user: {str(e)}"
            return False, "User not found."

    def delete_user(self, id_user):
        self._connect_once()
        with self.database.atomic():
            user = User.get_or_none(User.id == id_user)
            if user:
                user.delete_instance()
                return True, "User deleted successfully!"
            return False, "User not found."

    def insert_device(self, device_data):
        self._connect_once()
        with self.database.atomic():
            try:
                device = Device.create(
                    name=device_data["name"],
                    device_model=device_data["device_model"],
                    serial_number=device_data["serial_number"],
                    ip=device_data["ip"],
                    port=device_data["port"],
                    updated_at=datetime.now(),
                )
                return True, device.id
            except IntegrityError as e:
                return False, f"Failed to insert device: {str(e)}"

    def get_devices(self):
        self._connect_once()
        return [
            {
                "id": device.id,
                "name": device.name,
                "device_model": device.device_model,
                "serial_number": device.serial_number,
                "ip": device.ip,
                "port": device.port,
                "created_at": device.created_at,
                "updated_at": device.updated_at,
            }
            for device in Device.select()
        ]

    def update_device(self, device_id, device_data):
        self._connect_once()
        with self.database.atomic():
            device = Device.get_or_none(Device.id == device_id)
            if device:
                try:
                    device.name = device_data["name"]
                    device.device_model = device_data["device_model"]
                    device.serial_number = device_data["serial_number"]
                    device.ip = device_data["ip"]
                    device.port = device_data["port"]
                    device.updated_at = datetime.now()
                    device.save()
                    return True, "Device updated successfully!"
                except IntegrityError as e:
                    return False, f"Failed to update device: {str(e)}"
            return False, "Device not found."

    def delete_device(self, device_id):
        self._connect_once()
        with self.database.atomic():
            device = Device.get_or_none(Device.id == device_id)
            if device:
                device.delete_instance()
                return True, "Device deleted successfully!"
            return False, "Device not found."

    def insert_attendance(self, attendance_data):
        try:
            with self.database.atomic():
                Attendance.create(**attendance_data)
                return True, "Attendance recorded successfully."
        except Exception as e:
            return False, f"Failed to record attendance: {str(e)}"

    def update_attendance(self, attendance_id, attendance_data):
        try:
            with self.database.atomic():
                attendance = Attendance.get_or_none(Attendance.id == attendance_id)
                if not attendance:
                    return False, "Attendance record not found."
                for key, value in attendance_data.items():
                    setattr(attendance, key, value)
                attendance.save()
                return True, "Attendance updated successfully."
        except Exception as e:
            return False, f"Failed to update attendance: {str(e)}"

    def delete_attendance(self, attendance_id):
        try:
            with self.database.atomic():
                attendance = Attendance.get_or_none(Attendance.id == attendance_id)
                if not attendance:
                    return False, "Attendance record not found."
                attendance.delete_instance()
                return True, "Attendance deleted successfully."
        except Exception as e:
            return False, f"Failed to delete attendance: {str(e)}"

    def get_attendance(self):
        try:
            attendance = Attendance.select().dicts()
            return list(attendance)
        except Exception:
            return []

    def close(self):
        if not self.database.is_closed():
            self.database.close()
