from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do Banco de Dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definição do Modelo (Tabela)
class Produto(db.Model):
    __tablename__ = 'produto'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria
        }

# Cria o banco de dados e as tabelas
with app.app_context():
    db.create_all()

# Rota para servir o Frontend
@app.route('/')
def index():
    return render_template('index.html')

# Rota GET: Obter todos os produtos (CORRIGIDA: Roda perfeitamente no contexto do Flask)
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    produtos = db.session.execute(db.select(Produto)).scalars().all()
    return jsonify([p.to_dict() for p in produtos])

# Rota POST: Adicionar um novo produto
@app.route('/api/produtos', methods=['POST'])
def add_produto():
    data = request.get_json()
    nome = data.get('nome')
    categoria = data.get('categoria')

    if not nome or not categoria:
        return jsonify({'erro': 'Nome e categoria são obrigatórios.'}), 400

    if Produto.query.filter_by(nome=nome).first():
         return jsonify({'erro': f'O produto "{nome}" já existe na lista!'}), 409

    novo_produto = Produto(nome=nome, categoria=categoria)
    db.session.add(novo_produto)
    db.session.commit()
    
    return jsonify(novo_produto.to_dict()), 201 

@app.route('/api/produtos/<int:produto_id>', methods=['PUT'])
def edit_produto(produto_id):
    data = request.get_json()
    novo_nome = data.get('nome')

    produto = db.session.get(Produto, produto_id)
    if not produto:
        return jsonify({'erro': f'Produto com ID {produto_id} não encontrado.'}), 404

    if not novo_nome:
        return jsonify({'erro': 'O novo nome é obrigatório.'}), 400

    if Produto.query.filter(Produto.nome == novo_nome, Produto.id != produto_id).first():
        return jsonify({'erro': f'O produto "{novo_nome}" já existe na lista!'}), 409
        
    produto.nome = novo_nome
    db.session.commit()

    return jsonify({'mensagem': 'Produto atualizado com sucesso', 'produto': produto.to_dict()}), 200

@app.route('/api/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    
    produto = db.session.get(Produto, produto_id)
    if not produto:
        return jsonify({'erro': f'Produto com ID {produto_id} não encontrado.'}), 404

    db.session.delete(produto)
    db.session.commit()

    return jsonify({'mensagem': 'Produto removido com sucesso.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
