
class pSTPE04:
    def __init__(self, conn):
        self.conn = conn
        self.codret = True
        if not self.conn:
            self.codret = False

    def buscaProducto(self,parm):
        conn = self.conn
        COD, NCOD = parm
        COD = COD * 100 + 1
        QRY = f"SELECT NOMP,PRIC FROM STP{COD} WHERE COD = ? AND NCOD = ?;"
        _PROD = conn.execute(QRY, (COD,NCOD,))
        print(_PROD[0]) 

        