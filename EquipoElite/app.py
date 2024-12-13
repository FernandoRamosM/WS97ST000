from flask import Flask, render_template, request, redirect, url_for, flash, session
from object.st001.conn import conn

app = Flask(__name__)
app.secret_key = 'Ramos:218:'

_conn = conn()
if conn:
    prueba = _conn.execute("select * from ee098")
    for i in prueba:
        print(i)

# Datos de usuario para prueba (puedes reemplazar esto con una base de datos)
USUARIOS = {
    'admin': '12345',
    'usuario': 'password'
}

@app.route('/')
def home():
    if 'usuario' in session:
        return render_template('user/Equipo-Elite/home.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        
        if usuario in USUARIOS and USUARIOS[usuario] == password:
            session['usuario'] = usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
