import bcrypt

class pSTPE03:
    def generaContraseña(self, _pass: str) -> str: # IN:CONTRASEÑA
        passw = bcrypt.hashpw(_pass.encode('utf-8'), bcrypt.gensalt())
        return passw.decode('utf-8')

    def validaContraseña(self, _pass: str, passw: str) -> bool: # IN:CONTRASEÑA IN:CONTRASEÑA_INPUT OUT:VALIDA
        return bcrypt.checkpw(_pass.encode('utf-8'), passw.encode('utf-8'))

