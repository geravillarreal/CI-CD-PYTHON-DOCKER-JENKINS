from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    html = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>CI/CD Demo</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-LN+7fdVzj6u52u30Kp6M/trliBMCMKTyK833zpbD+pXdCLuTusPj697FH4R/5mcr" crossorigin="anonymous">
      </head>
      <body class="bg-light">
        <div class="container py-5">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h1 class="display-5">Hello from Flask CI/CD!</h1>
              <p class="lead">This page is served from a Docker container deployed automatically by Jenkins.</p>
              <span class="badge bg-success">Pipeline&nbsp;Green</span>
            </div>
          </div>
        </div>
      </body>
    </html>
    """
    return render_template_string(html), 200


@app.get("/health")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
