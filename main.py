import argparse
import os
from typing import Dict, List

from loader_from_file.ifileloader import IFileLoader
from serializers.iserializer import ISerializer
from settings import settings
from writers_to_file.ifilewriter import IFileWriter


class App:
    def __init__(self, argv):
        self.students_path = argv.students
        self.rooms_path = argv.rooms
        self.output_format = argv.format

    def run(self):
        self._validate_args()
        current_loader: IFileLoader = settings.available_loaders_from_file.get(
            settings.current_loader_format)()

        students_data = current_loader.read(self.students_path)
        rooms_data = current_loader.read(self.rooms_path)
        merge_rooms = self._merge_rooms_and_students(students_data, rooms_data)

        current_serializer: ISerializer = settings.available_serializers.get(
            self.output_format)()
        serialized_data = current_serializer.serialize(merge_rooms)
        text_writer: IFileWriter = settings.available_writers_to_file.get(
            "text")()
        text_writer.write(serialized_data, "result", self.output_format)

    def _validate_args(self):
        if not os.path.isfile(self.students_path):
            raise FileNotFoundError("Путь к файлу студентов некорректен")
        if not os.path.isfile(self.rooms_path):
            raise FileNotFoundError("Путь к файлу комнат некорректен")
        if self.output_format not in settings.available_serializers.keys():
            raise ValueError("Формат файла некорректен")

    def _merge_rooms_and_students(self, students: List[Dict], rooms: List[Dict]) -> List[Dict]:
        for room in rooms:
            room["students"] = []
        for student in students:
            room_id: int = student.get("room")
            room: Dict = rooms[room_id]
            room["students"].append(student.get("id"))
        return rooms


if __name__ == "__main__":
    # init argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("students", help="Path to json file with students")
    parser.add_argument("rooms", help="Path to json file with rooms")
    parser.add_argument("format", help="Format of output file")
    args = parser.parse_args()

    App(args).run()
