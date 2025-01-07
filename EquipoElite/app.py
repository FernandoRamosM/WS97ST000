from flask import Flask, render_template, request, redirect, url_for, flash, session
from static.procedure.pSTPE00 import conn
from static.procedure.pSTPE01 import pSTPE01
from static.procedure.pSTPE02 import pSTPE02



app = Flask(__name__)
app.secret_key = 'Ramos:218:'
hPass = pSTPE01 # Para validar contraseña 
_conn = conn()  # Conexion SQL
prueba = pSTPE02(_conn)
print(prueba.pSTPE02a('sv73772944'))

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
