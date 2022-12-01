#!/usr/bin/env python3

def datareader(filename, translate=int):
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


data = datareader("day1.txt", translate=str)
elfs = []
elf = 0
for line in data:
    # print(f"line {linenumber} data: '{line}'")
    if line == '':
        elfs.append(elf)
        elf = 0
        continue
    elf += int(line)
elfs.append(elf)

print(f"max elf {max(elfs)}")
print(f"max 3 elfs {sum(sorted(elfs)[-3:])}")
