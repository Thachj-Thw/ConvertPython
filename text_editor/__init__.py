import re


def highlight(code: str):

    list_highlight = {
        "key": {
            "#045ccf": ["[Data]", "[Pathex]", "[Option]", "[Setup]", "[Import]", "[Binaries]"],
            "#a918d9": ["Source", "DestDir", "name", "filename"],
            "#cf5804": ["one-file", "no-console", "uac-admin", "Converter", "AppName", "InputFile", "OutputDir", "Icon"]
        },
        "value": {
            "#cf5804": ["NONE", "Default", "PyInstaller"]
        },
        "except": {
            "#c455e6": ["*ThisDir*"],
        }
    }
    highlight_code = code
    strings = re.findall(r"\".*?\"|'.*?'", highlight_code)
    for string in strings:
        _format = re.findall(r"\{.*?}", string)
        str_format = string
        for s in _format:
            str_format = re.sub(
                re.escape(s),
                f'<span style="font-size: 13px; font-weight: 400; color: #cf5804; font-style: normal; white-space: pre-wrap;">{s}</span>',
                str_format
            )
        str_format = re.sub(r"\\", r"\\\\", str_format)
        highlight_code = re.sub(
            re.escape(str_format),
            f'<span style="font-size: 13px; font-weight: 400; color: #438a43; font-style: normal; white-space: pre-wrap;">{str_format}</span>',
            highlight_code
        )
    for color in list_highlight["key"].keys():
        for text in list_highlight["key"][color]:
            es_text = re.escape(text)
            highlight_code = re.sub(
                "(?m)^" + es_text + "(?=\\s)|(?m)^" + es_text + "(?!.)" if "[" == text[0] else "(?m)(?<!.)" + es_text + "(?=\\s)|(?m)(?<!.)" + es_text + "(?!.)|(?m)(?<!.)" + es_text + "(?==)|(?m)(?<=\\s)" + es_text + "(?=\\s)|(?m)(?<=\\s)" + es_text + "(?!.)|(?m)(?<=\\s)" + es_text + "(?==)",
                f'<span style="font-size: 13px; font-weight: 400; color: {color}; font-style: normal; white-space: pre-wrap;">{text}</span>',
                highlight_code
            )
    for color in list_highlight["value"].keys():
        for text in list_highlight["value"][color]:
            highlight_code = re.sub(
                "(?m)(?<==)" + text + "(?=\\s)|(?m)(?<==)" + text + "(?!.)|(?m)(?<=\\s)" + text + "(?=\\s)|(?m)(?<=\\s)" + text + "(?=\\s)",
                f'<span style="font-size: 13px; font-weight: 400; color: {color}; font-style: normal; white-space: pre-wrap;">{text}</span>',
                highlight_code
            )
    for color in list_highlight["except"].keys():
        for text in list_highlight["except"][color]:
            highlight_code = re.sub(re.escape(text), f'<span style="font-size: 13px; font-weight: 400; color: {color}; font-style: normal; white-space: pre-wrap;">{text}</span>', highlight_code)

    cmt_code = []
    for line in highlight_code.split("\n"):
        if line.startswith("#"):
            new_line = '<span style="font-size: 13px; font-weight: 400; color: #7b7580; font-style: normal; white-space: pre-wrap;">' + re.sub(r"<span.*?>|</span>", "", line) + '</span>'
        else:
            new_line = line
        cmt_code.append(new_line)
    highlight_code = "\n".join(cmt_code)
    return '<span style="white-space: pre-wrap;">'+highlight_code+'</span>'
