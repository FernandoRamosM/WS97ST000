from flask import Flask, session, redirect, render_template, request, jsonify, url_for
from procedure.pSTPE01 import pSTPE01
from procedure.pSTPE02 import pSTPE02
from procedure.pSTPE04 import pSTPE04

app = Flask(__name__)
app.secret_key = 'R:a:m:o:s::218::' 
_db = pSTPE01()
_conn = _db.Conecction()
_sql = pSTPE02(_conn)

# Inicializa
@app.route('/')
def start():
    session.clear()
    session['aut'] = False
    return redirect('/login')

# ..................................................................
# ........................... Login ................................
# ..................................................................


@app.route('/login', methods=['GET', 'POST']) # Inicia sesion
def login():
    if request.method == 'POST':
        try:
            _USER = request.form.get('username')
            _PASS = request.form.get('password')
            isValid = _sql.loginUs((_USER,_PASS))
            if isValid[0]:
                session['aut'] = True
                session['parm'] = (isValid[1])
                return redirect('/home')
            
            session['aut'] = False
            return render_template('login.html',codRet=session['aut'], mensajeQ=isValid[1])
        except Exception as e:
            session['aut'] = False
            return render_template('login.html', codRet=session['aut'], mensajeQ=str(e))
    return render_template('login.html', codRet=None, mensajeQ=None)

@app.route('/recuperar', methods=['POST'])
def recuperar():
    use = request.form.get('usernamefg')
    bir = request.form.get('birthdatefg')
    dni = request.form.get('dnifg')
    try:
        codRet = False
        parm = (use, bir, dni,)
        isValid = _sql.recuperaContraseña(parm)
        if isValid[0]:
            codRet = isValid[0]
            session['parm'] = isValid[1]
            return render_template('login.html', codRet=codRet)
        else:
            return render_template('login.html', codRet=codRet, mensajeQ='Datos incorrectos')
    except RuntimeError as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/nueva-contraseña', methods=['GET', 'POST'])
def upPass():
    codRet = False
    if request.method == 'POST':
        parm = session['parm']
        NPASS = request.form.get('new-password')
        CPASS = request.form.get('confirm-password')
        if NPASS != CPASS:
            return render_template('login.html', codRet=codRet, mensajeQ='Las contraseñas no coinciden')
        _parm = _parm + (NPASS,)
        try:
            isValid = _sql.actualizarContraseña(_parm)
            if isValid:
                return redirect('/')
            else:
                return render_template('login.html', codRet=codRet, mensajeQ='Error interno')
        except Exception as e:
            return render_template('login.html', codRet=codRet, mensajeQ=e)
    else:
        return render_template('login.html', codRet=codRet, mensajeQ="Metodo no permitido")


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/login')


# ..................................................................
# ........................... Fin Login ............................
# ..................................................................

@app.route('/home')
def home():
    if not session['aut']:
        return redirect('/')
    parm = session['parm']
    print(parm[0])
    _USER = parm[0]
    isValid = pSTPE02.localUSuario(_USER)
    if isValid:
        print("Encontro")

    pnom = parm[1].split()
    nom = " ".join(pnom[:2])
    ape = " ".join(pnom[2:])
    return render_template('usuario/home.html', user=(nom,ape))

@app.route('/buscar_producto', methods=['POST'])
def buscar_producto():
    try:
        # Obtener los datos del JSON enviado por el cliente
        data = request.json
        producto_nombre = data.get('nombre', '').strip()

        # Validar que se proporcionó el nombre del producto
        if not producto_nombre:
            return jsonify({"error": "No se proporcionó el nombre del producto"}), 400

        parm = session['parm']
        _parm  = (parm[0])
        pSTPE04.buscaProducto()

        # Consulta SQL para buscar el producto
        cursor.execute("SELECT id, nombre, precio FROM productos WHERE nombre = ?", (producto_nombre,))
        producto = cursor.fetchone()

        conn.close()

        if producto:
            # Si se encuentra el producto, devolver los datos
            return jsonify({
                "id": producto[0],
                "nombre": producto[1],
                "precio": producto[2]
            })
        else:
            # Si no se encuentra el producto
            return jsonify({"error": "Producto no encontrado"}), 404

    except sqlite3.Error as e:
        # Manejo de errores de base de datos
        return jsonify({"error": f"Error de base de datos: {str(e)}"}), 500

    except Exception as e:
        # Manejo de otros errores
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except OSError as e:
        print(f"Error: {e}")
        _conn.close()
        app.run(debug=True, use_reloader=False)