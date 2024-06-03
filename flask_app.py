from flask import Flask, request, send_from_directory, render_template, Response
import azimuth

ALLOWED_EXTENSIONS = {"gpx"}

app = Flask(__name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "lines" in request.form:

            lines = list(
                map(
                    str.strip,
                    request.form["lines"]
                    .strip("][")
                    .replace('"', "")
                    .replace("'", "")
                    .split(","),
                )
            )

            lines.append(
                "\nVytvořeno pomocí https://vokymir.eu.pythonanywhere.com/\nAplikace od Vokyho z 55. přední hlídky Royal Rangers Přeštice\nVoky & spol. - https://www.youtube.com/@Voky_spol\n55. ph RR - https://www.facebook.com/prestice.royalrangers\nOmluvuju se za zprávu, nemohl jsem si pomoct."
            )
            text = "\n".join(lines)
            firstName = lines[0].split(">>")[0].strip()
            lastName = lines[-2].split(">>")[1].split(":")[0].strip()
            name = make_valid_filename(f"azim-{firstName}_{lastName}.txt")
            return Response(
                text,
                mimetype="text/plain",
                headers={"Content-disposition": f"attachment; filename={name}"},
            )
        # check if the post request has the file part
        if "file" not in request.files:
            return render_template(
                "done.html",
                lines=[
                    "Asi jste zapomněli vybrat soubor.",
                    "Bez něj nejde hra vytvořit.",
                ],
            )
        request.data.decode("utf-8")
        file = request.files.get("file")

        # check if the filename isnt empty - browser is creating empty file if not uploading anything PRÝ, říkal to někdo na internetu
        if file.filename == "":
            return render_template(
                "done.html",
                lines=[
                    "Asi jste zapomněli vybrat soubor.",
                    "Bez něj nejde hra vytvořit.",
                ],
            )

        # check if the file extension is valid
        if not allowed_file(file.filename):
            return render_template(
                "done.html",
                lines=[
                    "Nepovolená přípona souboru.",
                    "Jediný povolený typ souboru: soubor.gpx",
                ],
            )

        # if file is valid, parse it
        filecontent = file.read()
        content = azimuth.gpx_parse_str_to_list(filecontent)
        return render_template("done.html", lines=content)

    # if not POST method
    return render_template(
        "done.html",
        lines=[
            "Něco se nepovedlo...",
            "Zkuste to znovu, prosím.",
            "Případně zkuste nahrát jiný soubor.",
        ],
    )


def make_valid_filename(string: str) -> str:
    newstr: str = ""

    for char in string:
        charINT = ord(char)
        if (
            charINT >= 48
            and charINT <= 57  # numbers
            or charINT >= 65
            and charINT <= 90  # A-Z
            or charINT >= 97
            and charINT <= 122  # a-z
            or charINT == 46  # dot
            or charINT == 95  # _
            or charINT == 45  # -
        ):
            newstr += char

    return newstr

import git
@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('path/to/git_repo')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400