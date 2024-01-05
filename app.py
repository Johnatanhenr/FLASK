from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

class SistemaGestaoProjetosTarefas:
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos (
          id INTEGER PRIMARY KEY,
          nome TEXT,
          descricao TEXT,
          data_inicio TEXT,
          data_prazo TEXT        
        )
    ''')
    conn.commit()
    conn.close()

    def criar_projeto(self, nome, descricao, data_inicio, data_prazo):
        conn = sqlite3.connect("gestao_projetos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projetos (nome, descricao, data_inicio, data_prazo) VALUES (?, ?, ?, ?)",
                       (nome, descricao, data_inicio, data_prazo))
        conn.commit()
        conn.close()
    
    def listar_projetos(self):
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome FROM projetos')
        projetos = cursor.fetchall()
        return projetos
    
    def limpar_banco_dados(self):
        conn = sqlite3.connect("gestao_projetos.db")
        conn.execute("DELETE FROM projetos")
        conn.commit()
        conn.close()



sistema = SistemaGestaoProjetosTarefas()


@app.route('/' , methods=['GET','POST'])
def index():
    if request.method =='POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']     
        data_prazo = request.form['data_prazo']
        sistema.criar_projeto(nome, descricao, data_inicio, data_prazo)
    
    projetos = sistema.listar_projetos()

    return render_template('index.html', projetos=projetos)


@app.route('/limpar_banco', methods=['POST'])
def limpar_banco():
    sistema.limpar_banco_dados()
    projetos = sistema.listar_projetos()
    return render_template('index.html' , projetos=projetos)


if __name__ == '__main__':
    app.run(debug=True)
