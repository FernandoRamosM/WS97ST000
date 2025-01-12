from flask import Flask, session, redirect, render_template, request, jsonify, url_for
from procedure.pSTPE01 import pSTPE01
from procedure.pSTPE02 import pSTPE02
from procedure.pSTPE04 import pSTPE04

app = Flask(__name__)
app.secret_key = 'R:a:m:o:s::218::' 
_db = pSTPE01()
_conn = _db.Conecction()
_sql = pSTPE02(_conn)
_prod = pSTPE04(_conn)

# Inicializa
@app.route('/')
def start():
    session.clear()             # Session
    session['aut'] = False      # Login Falso
    return redirect('/login')   # Inicia login

# ..................................................................
# ........................... Login ................................
# ..................................................................

@app.route('/login', methods=['GET', 'POST'])               # Inicia sesion
def login():
    if request.method == 'POST':
        try:
            _USER = request.form.get('username')
            _PASS = request.form.get('password')

            isValid = _sql.loginUs((_USER,_PASS,))      
            
            if isValid[0]:  # Valida si exciste Session True
                session['aut'] = isValid[0]     # <-- Sesion True
                session['user'] = (_USER,)      # <-- Pasa Usuario como parametro
                return redirect('/home')    
            # EndIf #
            session['aut'] = isValid[0]         # <-- Sesion Falsa      
            return render_template('login.html',codRet=False, mensajeQ=isValid[1]) # isValid[1] Mensaje de Error 
        # EndTry #
        except Exception as e:  
            session['aut'] = isValid[0]         # <-- Sesion Falsa
            return render_template('login.html', codRet=False, mensajeQ=str(e))
        # EndExecept #
    # EndIf #
    return render_template('login.html', codRet=False, mensajeQ=None)
# EndDef #

@app.route('/recuperar', methods=['POST'])                  # Recupera contraseña
def recuperar():
    _USER = request.form.get('usernamefg')        # Usuario
    _FNAC = request.form.get('birthdatefg')       # Fecha Nacimiento
    _NDOC = request.form.get('dnifg')             # Numero documento

    try:
        codRet = False
        parm = (_USER, _FNAC, _NDOC,)
        isValid = _sql.recuperaContraseña(parm)
        if isValid[0]:
            codRet = isValid[0]
            session['parm'] = isValid[1]
            return render_template('login.html', codRet=codRet)
        else:
            return render_template('login.html', codRet=codRet, mensajeQ='Datos incorrectos')
        # EndIf #
    # EndTry #
    except RuntimeError as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    # EndExcept #
# EndDef #

@app.route('/nueva-contraseña', methods=['GET', 'POST'])    # Genera nueva contraseña
def upPass():
    codRet = False
    try:
        if request.method == 'POST':
            _parm = session['parm']
            NPASS = request.form.get('new-password')
            CPASS = request.form.get('confirm-password')
            if NPASS != CPASS:
                return render_template('login.html', codRet=codRet, mensajeQ='Las contraseñas no coinciden')
            # EndIf #
            _parm = _parm + (NPASS,)
            try:
                isValid = _sql.actualizarContraseña(_parm)
                if isValid:
                    return redirect('/')
                else:
                    return render_template('login.html', codRet=codRet, mensajeQ='Error interno')
                # EndIf #
            except Exception as e:
                return render_template('login.html', codRet=codRet, mensajeQ=e)
            # EndExcept #
        else:
            return render_template('login.html', codRet=codRet, mensajeQ="Metodo no permitido")
        # EndIf #
    except Exception as e:
        return render_template('login.html', codRet=codRet, mensajeQ=f"Error interno {e}")
    # EndExcept #
# EndDef #

@app.route('/logout', methods=['POST'])                     # Limpia la sesion
def logout():
    session.clear()
    return redirect('/login')
# EndDef #

# ..................................................................
# ........................... Fin Login ............................
# ..................................................................

# ..................................................................
# .............................. Home ..............................
# ..................................................................

@app.route('/home')
def home():
    try:
        if not session.get('aut'): 
            return redirect('/')
        # EndIf #
        USER, = session['user']
        isValid = _sql.localUsuario(USER)
        if isValid[0]:
            session['parmLogin'] = (isValid[1])
            session['nombre']   = isValid[2][0]
            session['apellido'] = isValid[2][1]
            NOM = session['nombre'] 
            APE = session['apellido']
            Productos = _prod._9702_PREF9701(isValid[1])
        # EndIf #
        if not Productos:
            return render_template('usuario/home.html', NOM=NOM, APE=APE, Productos=[])
        else:
            
            return render_template('usuario/home.html', NOM=NOM, APE=APE, Productos=Productos, refresh=True)
        # EndIf #
    # EndTry #   
    except Exception as e:
        print(f"Error:home {e}")
        session.clear()
        return redirect('/')
    # EndExcept #
# EndDef #

@app.route('/asigna_ncod', methods=['POST'])
def asigna_ncod():
    try:
        data = request.json
        session['NCOD'] = data.get('NCOD', '').strip()  # Obtiene NCOD Producto
        return redirect('/home')
    # EndTry #
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    # EndExcept #
# EndDef#

@app.route('/PREF9701', methods=['POST'])
def PREF9701():
    try:
        data = request.json
        session['CANT'] = data.get('CANT', '').strip()  # Pbtiene CANT producto+
        _USER, _COD = session['parmLogin']                  # Usuario, localUsuario
        _NCOD,_CANT = session['NCOD'], session['CANT']
        if _NCOD:
            SALE  = _prod.buscaProducto((_COD,_NCOD))
            NOMP,PRIC,UMED, = SALE
        # EndIf #
        if _CANT:
            Producto = [_COD,_NCOD,NOMP,_CANT,UMED,PRIC,(PRIC*float(_CANT)),_USER]
        # EndIf #
        PARM = _prod._9701_PREF9701(Producto) # CREA PREF9701
        if PARM:
            print('Entro')
            session['PREF9701'] = PARM
            print(session['PREF9701'], 'PRIMERO')
            print('Termino')
        return redirect('/home')
    # EndTry #
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    # EndExcept #
# EndDef #

@app.route('/confirmar', methods=['POST'])
def confirmar():
    print(session['PREF9701'],'SEGUNDO')
    return redirect('/home')

@app.route('/cancelar', methods=['POST'])
def cancelar():
    print(session['PREF9701'],'SEGUNDO')
    return redirect('/home')

# ..................................................................
# ............................ Fin Home ............................
# ..................................................................



if __name__ == "__main__":
    try:
        app.run(debug=True)
    except OSError as e:
        print(f"Error: {e}")
        _conn.close()
        app.run(debug=True, use_reloader=False)