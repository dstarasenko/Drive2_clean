import datetime

class Logger():
    file_name = f"logs\\log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"


    @classmethod
    def write_log_to_file(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf=8') as logger_file:
            logger_file.write(data)

    @classmethod
    def start_logs(cls):
        data_to_add = f"\n-----\n"
        data_to_add += f"Время начала: {str(datetime.datetime.now())}\n"
        data_to_add += "\n"
        cls.write_log_to_file(data_to_add)

    @classmethod
    def add_logs(cls, txt: str):
        data_to_add = f"{txt}\n"
        cls.write_log_to_file(data_to_add)

    @classmethod
    def end_logs(cls):
        data_to_add = f"\n-----\n"
        data_to_add += f"Время окончания: {str(datetime.datetime.now())}\n"
        data_to_add += "\n"
        cls.write_log_to_file(data_to_add)

