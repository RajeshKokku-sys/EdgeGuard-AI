from database.db_manager import DatabaseManager


class EmployeeManager:

    def __init__(self):

        self.db = DatabaseManager()

    def enroll(

        self,

        employee_id,

        name,

        department,

        designation,

        embedding

    ):

        self.db.add_employee(

            employee_id,

            name,

            department,

            designation,

            embedding

        )

    def list_employees(self):

        return self.db.get_all_employees()