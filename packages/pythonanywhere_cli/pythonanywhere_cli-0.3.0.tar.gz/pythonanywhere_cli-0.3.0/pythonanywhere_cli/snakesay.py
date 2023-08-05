import textwrap

MESSAGE = "\n".join([
    "",
    "{bubble}",
    "   \\",
    "    ~<:>>>>>>>>>",
    "",
])


def snakesay(*things):
    bubble = "\n".join(speech_bubble_lines(" ".join(things)))
    return MESSAGE.format(bubble=bubble)


def speech_bubble_lines(speech):
    lines, width = rewrap(speech)
    if len(lines) <= 1:
        text = "".join(lines)
        yield "< {} >".format(text)
    else:
        yield "  " + "_" * width
        yield "/ {} \\".format(lines[0])
        for line in lines[1:-1]:
            yield "| {} |".format(line)
        yield r"\ {} /".format(lines[-1])
        yield "  " + "-" * width


def rewrap(speech):
    lines = textwrap.wrap(speech)
    width = max(len(l) for l in lines) if lines else 0
    return [line.ljust(width) for line in lines], width
