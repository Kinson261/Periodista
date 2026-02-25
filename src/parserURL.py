def parseURLFileUserInput(input: str):
    file = open(input, "r")
    lines = []
    for line in file:
        lines.append(line.strip())
    file.close()
    return lines
