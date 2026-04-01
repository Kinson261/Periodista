from typing import List


def parseURLFileUserInput(input_file: str):
    file = open(input_file, "r")
    lines: List[str] = []
    for line in file:
        lines.append(line.strip())
    file.close()
    return lines
