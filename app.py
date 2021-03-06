from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
# Configuração do banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://orluykns:5zhH2OQdedl8Qm46MrRIsSnTCrRXUvq1@kesavan.db.elephantsql.com/orluykns'
db = SQLAlchemy(app)#usa o alchemy para criar uma um banco de dados em app dentro da variavel db
#  
# Criando objeto 
class Pokemon(db.Model):#parametriza a classe(obejeto), pokemon como uma tabela no db
    # configuração da tabela 'pokemon'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    imagem = db.Column(db.String(500), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(150), nullable=False)

    def __init__(self, nome, imagem, descricao, tipo):
        self.nome = nome
        self.imagem = imagem
        self.descricao = descricao
        self.tipo = tipo
# Rota do inicial 
@app.route('/')
def index():
    pokedex = Pokemon.query.all()
    return render_template('/index.html',pokedex=pokedex )

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        pokemon = Pokemon(
            request.form['nome'],
            request.form['imagem'],
            request.form['descricao'],
            request.form['tipo']
        )
        db.session.add(pokemon)
        db.session.commit()
        return redirect('/')

@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    pokemon = Pokemon.query.get(id)
    pokedex = Pokemon.query.all()
    if request.method == 'POST':
        pokemon.nome = request.form['nome']
        pokemon.imagem = request.form['imagem']
        pokemon.descricao = request.form['descricao']
        pokemon.tipo = request.form['tipo']
        db.session.commit(pokemon)
        return redirect('/')
    return render_template('/index.html', pokemon=pokemon, pokedex=pokedex)

@app.route('/<id>')
def select(id):
    pokemon = Pokemon.query.get(id)
    all = Pokemon.query.all()
    return render_template('index.html', pokemonDelete=pokemon, pokemon=all)
@app.route('/delete/<id>')
def delete(id):
    pokemon = Pokemon.query.get(id)
    db.session.delete(pokemon)
    db.session.commit()
    return redirect('/')

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    tipo = request.form['search']
    pokedex = Pokemon.query.filter(Pokemon.tipo.ilike(f'%{tipo}%')).all()

    return render_template('index.html', pokedex=pokedex)

@app.route('/filter/<param>')
def filterByName(param):
    pokedex = Pokemon.query.filter_by(tipo=param).all()
    return render_template('index.html', pokedex=pokedex)
        
if __name__ == '__main__':
    db.create_all()#Cria as tabelas, se existe atualiza se não existe cria
    app.run(debug=True)