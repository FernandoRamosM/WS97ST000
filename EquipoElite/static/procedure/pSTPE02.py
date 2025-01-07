class pSTPE02:
    def __init__(self, conn):
        self.conn = conn

    def pSTPE02a(self, user):
        _user = self.conn.execute("""
        Select
        user, nom, stat, tuser
        From ee098
        Where user = ?
        """, (user,))
        return _user[0]
    
    def pSTPE02a1(self,_parm):
        passW = self.conn.execute("""
        Select
        *
        From ee098a
        Where key1 = ?, key2 = ?, key3 = ?, key4 = ?, 
        """, (_parm,))
        return passW[0]