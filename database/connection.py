import os
import oracledb
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    conn = oracledb.connect(
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        dsn=os.getenv('DSN'),
        config_dir=os.getenv('CONFIG_DIR'),
        wallet_location=os.getenv('WALLET_DIR'),
        wallet_password=os.getenv('WALLET_PASS')
    )
    return conn