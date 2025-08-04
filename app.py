from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

BOOTSTRAP_CDN = (
    '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" '
    'rel="stylesheet" integrity="sha384-9ndCyUaI0hJbXn0wXkzXCF3y86IH6Ez7GZm5jWnNQ9sKZCSk1Fv4KfqB0NWnI4vE" crossorigin="anonymous">'
)

@app.get("/")
def home():
    html = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>CI/CD Demo</title>
        {BOOTSTRAP_CDN}
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
