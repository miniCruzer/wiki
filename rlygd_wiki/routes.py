import os, json
from flask import Blueprint, render_template
import markdown2

mod = Blueprint("routes", __name__)

# lmao
def render_error(msg):
    return "\n# RENDER ERROR #\n`{}`".format(msg)

def render_markdown(data, extnames=[]):

    try:
        html = markdown2.markdown(data,  extras=extnames)
    except Exception as e:
        data += render_error("Couldn't render with the requested extensions: {}".format(e))
        html = markdown2.markdown(data)

    return html

@mod.route("/")
@mod.route("/<path:path>")
def find_wiki_page(path='/'):

    if path == '/':
        data_path = "data"
    else:
        data_path = os.path.join("data", path)

    data_path = data_path.lower()

    if os.path.isdir(data_path):
        data_path = os.path.join(data_path, "index.txt")
    else:
        data_path += ".txt"

    if not os.path.isfile(data_path):
        return render_template("page.html", info={"title": "nope.jpg"}, wikicontent=None)


    fh = open(data_path, "r")
    data = fh.read()
    fh.close()

    data = data.split('__DATA__', 1)

    if len(data) == 1:
        # no __DATA__ tag found, assume there's no header
        return render_template("page.html", info={}, wikicontent=render_markdown(data[0]))

    info = { }
    md = data[1]
    try:
        info = json.loads(data[0].strip())
    except Exception as e:
        md += render_error("Failed to read header: {}".format(e))

    exts = info.get("extras", [ ])

    return render_template("page.html", info=info, wikicontent=render_markdown(md, exts))
