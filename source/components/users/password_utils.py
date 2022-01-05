import os

import bcrypt


def get_password_hash(password):
    num_rounds = int(os.environ['BCRYPT_NUM_ROUNDS'])
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=num_rounds)).decode('utf-8')


def check_password(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
