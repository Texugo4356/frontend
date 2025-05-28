from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from models.models.py import db, Cuidador, Paciente

app = Flask(__name__)
app.secret_key = 'remory'


user = "postgres"
password = "4356"
host = "localhost"
port = "5432"
dbname = "cadastro"

#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cuidador = Cuidador.query.filter_by(email=email).first()
        if cuidador and check_password_hash(cuidador.senha, senha):
            session['cuidador_id'] = cuidador.id
            return redirect(url_for('dashboard'))
        return "Login inválido!"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('cuidador_id', None)
    return redirect(url_for('login'))

@app.route('/cadastro_cuidador', methods=['GET', 'POST'])
def cadastro_cuidador():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        senha_hash = generate_password_hash(senha)
        novo_cuidador = Cuidador(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_cuidador)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('cadastro_cuidador.html')

@app.route('/dashboard')
def dashboard():
    if 'cuidador_id' not in session:
        return redirect(url_for('login'))

    cuidador = Cuidador.query.get(session['cuidador_id'])
    return render_template('dashboard.html', pacientes=cuidador.pacientes)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if 'cuidador_id' not in session:
        return redirect(url_for('login'))

    cuidador_id = session['cuidador_id']
    dados = request.form

    novo_paciente = Paciente(
        nome=dados['nome_completo'],
        data_nasc=dados['data_nascimento'],
        sexo=dados['sexo'],
        cpf=dados['cpf'],
        tel=dados['telefone'],
        email=dados['email'],
        estado_civil=dados['est_civ'],
        nome_mae=dados['n_mae'],
        nome_pai=dados['n_pai'],
        nacionalidade=dados['nacic'],
        naturalidade=dados['natu'],
        contato_emergencia_nome=dados['n_cont_emr'],
        contato_emergencia_telefone=dados['tel_cont_emr'],
        contato_emergencia_parentesco=dados['paren_cont_emr'],
        endereco=dados['end'],
        cep=dados['cep'],
        tipo_sanguineo=dados['tp_sangue'],
        alergias=dados['alergias'],
        doencas_cronicas=dados['doen_cro'],
        medicamentos_em_uso=dados['medic_uso'],
        cuidador_id=cuidador_id
    )

    db.session.add(novo_paciente)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/form')
def form():
    if 'cuidador_id' not in session:
        return redirect(url_for('login'))
    return render_template('form.html')

@app.route('/pacientes/<int:id>')
def detalhes_pacientes(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return "Paciente não encontrado!", 404
    return render_template('detalhes_pacientes.html', paciente=paciente)


if __name__ == '__main__':
    app.run(debug=True)
