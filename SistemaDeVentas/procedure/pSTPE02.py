
from procedure.pSTPE03 import pSTPE03
_pSTPE03 = pSTPE03()

class pSTPE02:
    def __init__(self, conn):
        self.conn = conn
        self.codret = True
        if not self.conn:
            self.codret = False

    def loginUs(self, parm):  # st97pe098 - Usuarios
        try:
            conn = self.conn
            _USER, _AUSE, = parm
            QRY = "SELECT CTST,STAT FROM STP098 WHERE USER = ?;"
            _US = conn.execute(QRY, (_USER,))
            if _US:
                CTST,STAT = _US[0]
                if STAT == 'H':
                    QRY   = "SELECT AUSE FROM STP098a WHERE ACTST = ?;"
                    _US   = conn.execute(QRY, (CTST,))
                    AUSE, = _US[0]
                    if _pSTPE03.validaContraseña(_AUSE, AUSE):
                        return (True, "Credenciales correctas")
                    else:
                        return (False,'Contraseña incorrecta',)
                else:
                    return (False,'Usuario inhabilitado',)
            else:
                return (False,'Usuario no existe',)
        except Exception as e:
            raise RuntimeError(f"Error al ejecutar la consulta: {e}")

    def recuperaContraseña(self, parm):  # Recuperar contraseña
        try:
            conn = self.conn
            _USER,_FNAC,_NDOC = parm
            if _USER.endswith(".STAD"):
                QRY = "SELECT CTST FROM STP098 WHERE USER = ?;"
                _ADM = conn.execute(QRY, (_USER,))
                _CTST, = _ADM[0]    # Obtiene CTST Adm
            else:
                _CTST = ''.join([_CTST for _CTST in _USER if _CTST.isdigit()]) # Obtiene CTST US
            # EndIf #

            QRY = "SELECT COD,PAIS,TDOC,NDOC FROM STP008 WHERE CTST = ?;"
            sql = conn.execute(QRY,(_CTST,))
            COD,PAIS,TDOC,NDOC = sql[0]
            parm = (COD,PAIS,TDOC,NDOC)
            QRY = "SELECT NDOC,FNAC FROM STP001 WHERE COD = ? AND PAIS = ? AND TDOC = ? AND NDOC = ?;"
            sql = conn.execute(QRY, parm)
            if sql:
                NDOC,FNAC = sql[0]
                _FNAC = _FNAC.replace('-','')
                if (NDOC == _NDOC) and (FNAC == _FNAC):
                    return (True, parm,)
                # EndIf #
            # EndIf #
            return (False,)
        # EndTry #
        except Exception as e:
            raise RuntimeError(f"Error al recuperar contraseña: {e}")

    def actualizarContraseña(self, parm):
        try:
            conn = self.conn
            COD,PAIS,TDOC,NDOC,NPASS = parm
            QRY = "SELECT CTST FROM STP008 WHERE COD=? AND PAIS=? AND TDOC=? AND NDOC=?;"
            sql = conn.execute(QRY, (COD,PAIS,TDOC,NDOC,))
            if sql:
                CTST, = sql[0]
                QRYUP  = """
                UPDATE STP098a SET AUSE = ?
                WHERE ACTST = ?; 
                """
                _NPASS = _pSTPE03.generaContraseña(NPASS)
                conn.execute(QRYUP, (_NPASS, CTST,))
                return True
            else:
                return False
        except Exception as e:
            raise RuntimeError(f"Error al actualizar contraseña: {e}")


    def localUsuario(self, _USER):
        try:
            conn = self.conn                                         
            QRY = "SELECT COD,PNOM FROM STP098 WHERE USER = ?;"
            sql = conn.execute(QRY, (_USER,))
            if sql:
                # UBICA LOCAL USUARIO
                NCOD,PNOM = sql[0]
                NCOD = (NCOD*100)+1
                # OBTIENE NOMBRE Y APELLIDOS
                NOM_APE = PNOM.split()
                _NOM = " ".join(NOM_APE[:-2]).upper()
                _APE = " ".join(NOM_APE[-2:]).upper()
                return (True, (_USER,NCOD),(_NOM,_APE))
            else:
                return False
        except Exception as e:
            raise RuntimeError(f"Error al ubicar usuario: {e}")