def make_valid_filename(string: str) -> str:
    newstr: str = ""
    for char in string:
        charINT = ord(char)
        if (
            charINT >= 48
            and charINT <= 57
            or charINT >= 65
            and charINT <= 90
            or charINT >= 97
            and charINT <= 122
        ):
            newstr += char
    print(newstr)

    return newstr


txt = "asdfga54545šřčřžýýždfg"
make_valid_filename(txt)
