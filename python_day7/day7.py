#!/usr/bin/env python3

from ast import parse


class Directory:

    def __init__(self, directory_name, parent_directory=None):
        self.directory_name = directory_name
        self.parent_directory = parent_directory
        self.directories = {}
        self.files = {}
        self.storage_usage = 0

    def add_directory(self, directory_name):
        self.directories[directory_name] = Directory(directory_name, self)
        return self.directories[directory_name]

    def add_file(self, filesize, filename):
        self.files[filename] = int(filesize)

    def calculate_storage(self):
        storage_usage = sum([x for x in self.files.values()])
        storage_usage += sum([x.calculate_storage()
                             for x in self.directories.values()])
        self.storage_usage = storage_usage
        return storage_usage

    def find_directories_with_filter(self, filter):
        # print(f"Checking directory {root_location}")
        if filter(self.storage_usage):
            # print(f"{root_location.directory_name} is under {max_size}")
            yield self
        # print(f"checking subdirectories")
        for directory in self.directories.values():
            yield from directory.find_directories_with_filter(filter)

    def __str__(self):
        return f"\n\tdirectory: {self.directory_name} total:{self.storage_usage}{', '.join([str(x) for x in self.directories.values()])}\n\t{self.files} "


def datareader(filename, translate=int):
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def parse_commands(data):
    current_directory = None

    for command_line in data:
        commands = command_line.split()
        command = commands.pop(0)
        # print(f"'{command}'")
        if command != '$':
            if command == 'dir':
                current_directory.add_directory(commands.pop(0))
            else:
                current_directory.add_file(int(command), commands.pop(0))
            continue

        # print(f"command found {command[1:]}")
        command_type = commands.pop(0)

        # No need to do anything with 'ls' commands
        if command_type != 'cd':
            continue

        command_parameter = commands.pop(0)
        if command_parameter == '..':
            current_directory = current_directory.parent_directory
        elif command_parameter == "/":
            if not current_directory:
                current_directory = Directory(command_parameter)
            else:
                while current_directory.parent_directory:
                    current_directory = current_directory.parent_directory
        elif current_directory:
            # print(f"{command[2]}")
            current_directory = current_directory.directories[command_parameter]

    # Rewind to root-node
    while current_directory.parent_directory:
        current_directory = current_directory.parent_directory

    # Update storage usage
    current_directory.calculate_storage()
    return current_directory


if __name__ == '__main__':
    data = datareader("../day7.txt", str)
    current_directory = parse_commands(data)

    total_sum = sum([x.storage_usage for x in current_directory.find_directories_with_filter(
        lambda x: x <= 100000)])

    print(f"End sum part 1: {total_sum}")

    max_space = 70000000
    needed_space = 30000000
    current_space = max_space - current_directory.storage_usage

    storage_need = needed_space - current_space

    enought_to_remove = min([x.storage_usage for x in current_directory.find_directories_with_filter(
        lambda x: x >= storage_need)])

    print(f"Smallest amount to remove for part2 is: {enought_to_remove}")

    # print(f"{current_directory}")
