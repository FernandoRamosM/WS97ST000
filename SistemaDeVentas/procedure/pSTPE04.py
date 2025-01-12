from datetime import datetime

today = datetime.now()
fecha = today.strftime("%Y%m%d")
hora = today.strftime("%H:%M:%S")




class pSTPE04:
    def __init__(self, conn):
        self.conn = conn
        self.codret = True
        if not self.conn:
            self.codret = False

# --------------------- PREF9701 ------------------------------
# ----------------------- 9701 --------------------------------
    def buscaProducto(self,parm):
        conn = self.conn
        _COD, _NCOD = parm
        QRY = f"SELECT NOMP,PRIC,UMED FROM STP{_COD} WHERE COD = ? AND NCOD = ?;"
        _PROD = conn.execute(QRY, (_COD,_NCOD,))
        NOMP,PRIC,UMED, = _PROD[0] 
        return (NOMP,PRIC,UMED,)

    def buscaRelacion(self,parm):
        try:
            conn = self.conn
            _COD, _MOD, _TRN, = parm 
            QRY = """
            SELECT REL, STAT
            FROM STP9701
            WHERE COD = ? AND MOD = ? AND TRN = ? AND FECT = ? AND REL = (
                SELECT MAX(REL)
                FROM STP9701
                WHERE COD = ? AND MOD = ? AND TRN = ? AND FECT = ?
            );"""
            _DAT = conn.execute(QRY, (_COD, _MOD, _TRN, fecha, _COD, _MOD, _TRN, fecha,))
            if _DAT:
                if None in _DAT:
                    return  1
                _REL, _STAT = _DAT[0]
                if _STAT == "P":
                    return int(_REL)
                else:
                    _REL = int(_REL) + 1
                    return _REL
            else:
                return 1
        except Exception as e:
            print(f"Error:buscaRelacion {e}")
        
    def _9701_PREF9701(self, Producto): # CREAR STP9701
        try:
            _MOD = 97
            _TRN = 1
            _COD,_NCOD,_NOMP,_CANT,_UMED,_PRIC,_TOTL,_USER = Producto
            _REL = self.buscaRelacion((_COD, _MOD, _TRN,))
            PARM = [_COD, _MOD, _TRN, _REL,_NCOD, _NOMP, _CANT, _UMED, _PRIC, _TOTL, _USER, fecha, hora, 'P',]
            if self.read_PREF9701(PARM):
                if self.update_PREF9701(PARM):
                    return (_COD, _MOD, _TRN, _REL,fecha,)
            else:
                if self.insert_PREF9701(PARM):
                    return (_COD, _MOD, _TRN, _REL,fecha,)
            return False

        except Exception as e:
            print(f"Error:9701_PREF9701 {e}")
            return False

    def _9702_PREF9701(self, parm): # LEE PREFORMATO
        try:
            conn = self.conn
            _MOD = 97
            _TRN = 1
            _USER, _COD, = parm
            _REL = self.buscaRelacion((_COD, _MOD, _TRN,))
            QRY = """
            SELECT COD, MOD, TRN, REL, NCOD, NOMP, CANT, UMED, PRIC, TOTL, USER, FECT, HORT 
            FROM STP9701
            WHERE COD = ? AND MOD = ? AND TRN = ? AND REL = ? AND USER = ? AND FECT = ?;"""
            Producto = conn.execute(QRY, (_COD, _MOD, _TRN, _REL,_USER, fecha,))
            if Producto:
                return Producto
            else:
                return False
        except Exception as e:
            print(f"Error:9702_PREF9701 {e}")


# --------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

    # ------------ MANTENIMIENTO PREF9701 --------------

    # --------------------------------------------------
    # ------------------- INSERT -----------------------
    # --------------------------------------------------
    def insert_PREF9701(self, PARM):
        try:
            conn = self.conn
            QRY = """
                INSERT INTO STP9701 (COD, MOD, TRN, REL, NCOD, NOMP, CANT, UMED, PRIC, TOTL, USER, FECT, HORT,STAT)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
            isValid = conn.execute(QRY, (PARM))
            if isValid:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error:insert_PREF9701 {e}")
            return False
    # --------------------------------------------------
    # ------------------- UPDATE -----------------------
    # --------------------------------------------------
    def update_PREF9701(self, PARM):
        try:
            conn = self.conn
            _COD, _MOD, _TRN, _REL,_NCOD, _NOMP, _CANT, _UMED, _PRIC, _TOTL, _USER, _FECT, _HORT, _STAT, = PARM
            # Obtiene cantidad 
            QRY = """
            SELECT
                CANT
            FROM STP9701
            WHERE COD = ? AND MOD = ? AND TRN = ? AND REL = ? AND NCOD = ? AND FECT = ? AND STAT = ?;"""
            _cantidad = conn.execute(QRY, (_COD, _MOD, _TRN, _REL, _NCOD, _FECT, _STAT,))
            _CANT = float(_cantidad[0][0]) + float(_CANT)
            # Actualiza Cantidad y Precio Total
            _TOTL = round(float(_PRIC) * float(_CANT), 2)   
            QRY = """
            UPDATE STP9701
                SET CANT = ?, TOTL = ?
            WHERE COD = ? AND MOD = ? AND TRN = ? AND REL = ? AND NCOD = ? AND FECT = ? AND STAT = ?;"""
            conn.execute(QRY, (_CANT, _TOTL, _COD, _MOD, _TRN, _REL, _NCOD, _FECT, _STAT,))
            return True
        except Exception as e:
            print(f"Error:update_PREF9701 {e}")
            return False
    # --------------------------------------------------
    # ------------------- DELETE -----------------------
    # --------------------------------------------------
    def delete_PREF9701(self, PARM):
        pass
    # --------------------------------------------------
    # -------------------- READ ------------------------
    # --------------------------------------------------
    def read_PREF9701(self, PARM):
        try:
            conn = self.conn
            # VALIDA SI EXISTE REGISTRO DEL MISMO PRODUCTO
            _COD, _MOD, _TRN, _REL,_NCOD, _NOMP, _CANT, _UMED, _PRIC, _TOTL, _USER, _FECT, _HORT, _STAT, = PARM
            QRY = """
            SELECT 
                CANT
            FROM STP9701
            WHERE COD = ? AND MOD = ? AND TRN = ? AND REL = ? AND NCOD = ? AND FECT = ? AND STAT = ?;"""
            isValid = conn.execute(QRY, (_COD, _MOD, _TRN, _REL, _NCOD, _FECT, _STAT,))
            if isValid:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error:read_PREF9701 {e}")
            return False