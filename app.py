"""Aplicativo principal do Cadastro de Trecos."""

from pathlib import Path
import sqlite3

from flask import Flask, abort, flash, redirect, render_template, request, url_for

# Caminhos absolutos permitem executar o projeto a partir de qualquer pasta.
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database.db"

# Cria a aplicação Flask e habilita mensagens temporárias (flash).
app = Flask(__name__)
app.config["SECRET_KEY"] = "desenvolvimento-local"


def get_connection():
    """Abre uma conexão com o banco retornando linhas acessíveis por nome."""
    connection = sqlite3.connect(DATABASE)
    # Permite usar content["name"] em vez de content[0].
    connection.row_factory = sqlite3.Row
    return connection


# Página inicial: lista todos os trecos ativos no banco.
@app.route("/")
def index():
    with get_connection() as conn:
        contents = conn.execute(
            """
            SELECT id, name, photo, description, location
            FROM thing
            WHERE status = 'on'
            ORDER BY created_at DESC, id DESC
            """
        ).fetchall()

    # Envia a lista e a quantidade de registros para o template.
    return render_template("index.html", contents=contents, total=len(contents))


# O <int:thing_id> recebe o ID que vem na URL, por exemplo /view/1.
@app.route("/view/<int:thing_id>")
def view(thing_id):
    with get_connection() as conn:
        content = conn.execute(
            "SELECT * FROM thing WHERE status = 'on' AND id = ?", (thing_id,)
        ).fetchone()

    if content is None:
        # Retorna a página padrão de erro quando o ID não existe.
        abort(404)
    return render_template("view.html", content=content)


# GET exibe o formulário; POST recebe e salva seus dados.
@app.route("/new", methods=["GET", "POST"])
def new_thing():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        photo = request.form.get("photo", "").strip()

        # Nome e descrição são campos obrigatórios.
        if not name or not description:
            flash("Informe pelo menos o nome e a descrição do treco.", "error")
            return render_template("new.html")

        if not photo:
            # Gera uma imagem aleatória quando a pessoa não informa uma URL.
            random_photo_id = abs(hash(name)) % 10000
            photo = f"https://picsum.photos/800/500?random={random_photo_id}"

        with get_connection() as conn:
            # Os ? evitam SQL Injection ao inserir os valores do formulário.
            cursor = conn.execute(
                """
                INSERT INTO thing (name, description, location, photo)
                VALUES (?, ?, ?, ?)
                """,
                (name, description, location, photo),
            )
            thing_id = cursor.lastrowid

        # Exibe uma mensagem e encaminha para a página do novo registro.
        flash("Treco cadastrado com sucesso!", "success")
        return redirect(url_for("view", thing_id=thing_id))

    return render_template("new.html")


# Página estática com informações sobre o projeto.
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/termos")
def termos():
    return render_template("termos.html")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Preencha todos os campos do formulário.", "error")
            return render_template("contato.html")

        flash("Formulário recebido. O envio por e-mail ainda não está configurado.", "info")
        return redirect(url_for("contato"))

    return render_template("contato.html")


if __name__ == "__main__":
    # Inicia o servidor somente ao executar este arquivo diretamente.
    app.run(debug=True)
