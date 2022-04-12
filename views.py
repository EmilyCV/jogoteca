import time
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from App.models.jogo import Jogo
from App.models.usuario import Usuario
from helpers import deleta_arquivo, recupera_imagem
from jogoteca import app
from persistence.database.dao import JogoDao, UsuarioDao
from persistence.database.database import Session
from werkzeug.security import generate_password_hash, check_password_hash

jogo_dao = JogoDao(Session)
usuario_dao = UsuarioDao(Session)


@app.route('/')
def index():
    lista = jogo_dao.listar()
    usuario_logado = False
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template('lista.html', titulo='Jogos', jogos=lista, usuario = usuario_logado)
    else:
        usuario_logado = True
        return render_template('lista.html', titulo='Jogos', jogos=lista, usuario = usuario_logado)


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo='Novo Usuário')


@app.route('/cadastrar', methods=['POST', ])
def cadastrar():
    nome_user = request.form['usuario']
    nome_completo = request.form['nome']
    email = request.form['email']
    senha = request.form['password']
    
    if usuario_dao.buscar_por_id(nome_user):
        flash('Nome de Usuário já cadastrado.')
        return redirect(url_for('cadastro'))
    if usuario_dao.buscar_por_email(email):
        flash('E-mail já cadastrado.')
        return redirect(url_for('cadastro'))
    else:  
        senha_hash = generate_password_hash(senha, method='sha256')
        usuario = Usuario(nome_user, nome_completo, email, senha_hash)
        usuario = usuario_dao.salvar(usuario)
        return redirect(url_for('index'))


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']

    ultimo_id = jogo_dao.listar()[-1]

    timestamp = time.time()

    arquivo.save(
        f"{upload_path}/capa-{ultimo_id.id}-{timestamp}.jpg")

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=nome_imagem)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo = jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']

    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa-{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if check_password_hash(usuario.senha,request.form['senha']) == False:
            flash('Usuário ou senha inválidos.')
            return redirect(url_for('login'))
        elif check_password_hash(usuario.senha,request.form['senha']):
            session['usuario_logado'] = usuario.nome
            flash(usuario.nome +
                  ' logado(a) com sucesso!')
            return redirect(url_for('index'))
    else:
        flash('Usuário não existe!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
