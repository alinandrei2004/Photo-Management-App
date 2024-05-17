from Flask import Flask, render_template, redirect, Response

app = Flask("my_website")

@app.route("/")
def serve_template():
    return render_template("index.html", title="FotoHive")

# @app.route("/admin")
# def serve_unauthorized():
#     # Note: 303 is standard HTTP code for See Other redirect
#     return redirect("/login.html", 303, "<h1>Redirecting, please wait...</h1>")
 
# @app.route("/special.xml")
# def serve_special_xml():
#     return Response("<xml><author>Me</author></xml>", mimetype='text/xml')
