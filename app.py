from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastros.db'
db = SQLAlchemy(app)
@app.route('/')

def index():
    return render_template('inicio.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/cadastro')
def cadastro():
    servicos = request.args.get('servicos')
    return render_template('cadastro.html', servicos=servicos)
class Cadastro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=True)
    servicos = db.Column(db.String(100), nullable=False)
with app.app_context():
    db.create_all()


@app.route('/finalizar', methods=['POST'])
def finalizar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    empresa = request.form.get("empresa")
    servicos = request.form.get("servicos")

    novo_cadastro = Cadastro(nome=nome, email=email, empresa=empresa, servicos=servicos)
    db.session.add(novo_cadastro)
    db.session.commit()

    # Montar mensagem para WhatsApp
    mensagem = (
        f"✨ Cadastro Finalizado! ✨\n\n"
        f"👤 Nome/Empresa: {nome}\n"
        f"📧 Email: {email}\n"
        f"🛠️ Serviço escolhido: {servicos}\n"
        "----------------------------\n"
        "✅ Obrigado pelo contato! Em breve retornaremos."
    )
    mensagem_link = mensagem.replace("\n", "%0A")
    novo_cadastro = Cadastro(nome=nome, email=email, empresa=empresa, servicos=servicos)
    db.session.add(novo_cadastro)
    db.session.commit()

    # Redirecionar direto para WhatsApp
    url = f"https://api.whatsapp.com/send?phone=5548999443394&text={mensagem_link}"
    return redirect(url)
@app.route('/listar')
def listar():
    cadastros = Cadastro.query.all()  # pega todos os registros
    return render_template('listar.html', cadastros=cadastros)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)




    





        