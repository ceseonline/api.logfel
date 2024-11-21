import oracledb

from config_app.walletcredentials import uname, pwd, cdir, wltloc, wltpwd, dsn

def get_connection():

    return oracledb.connect(
        user=uname,
        password=pwd,
        dsn=dsn,
        config_dir=cdir,
        wallet_location=wltloc,
        wallet_password=wltpwd
    )