from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # chave secreta pra sessão

# Banco de dados fake (em memória, pra teste)
users = {}  # email: { 'password': hash, 'plano': 'nenhum' }

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('loja'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if email in users and check_password_hash(users[email]['password'], senha):
            session['user'] = email
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('loja'))
        flash('Email ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if email in users:
            flash('Email já cadastrado.', 'danger')
        else:
            users[email] = {'password': generate_password_hash(senha), 'plano': 'nenhum'}
            session['user'] = email
            flash('Conta criada! Bem-vindo.', 'success')
            return redirect(url_for('loja'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))

@app.route('/loja')
def loja():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('loja.html', user=session['user'])

@app.route('/minhas-chaves')
def minhas_chaves():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('minhas-chaves.html', user=session['user'])

@app.route('/suporte')
def suporte():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('suporte.html', user=session['user'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
