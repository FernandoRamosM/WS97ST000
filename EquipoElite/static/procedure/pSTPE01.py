from passlib.hash import pbkdf2_sha256

class pSTPE01():
    def __init__(self):
        pass

    # Hashear una contraseña
    def pSTPE01a(_pass):
        h_pass = pbkdf2_sha256.hash(_pass)
        return h_pass

    # Verificar una contraseña
    def pSTPE01b(h_pass, _pass):
        return pbkdf2_sha256.verify(_pass, h_pass)
    

'''contraseña = pSTPE01
hash = contraseña.pSTPE01a('Ramos218')
print('44: < ',contraseña.pSTPE01a('44'),' >')
print('29: < ',contraseña.pSTPE01a('44'),' >')
print('77: < ',contraseña.pSTPE01a('44'),' >')
print('73: < ',contraseña.pSTPE01a('44'),' >')'''