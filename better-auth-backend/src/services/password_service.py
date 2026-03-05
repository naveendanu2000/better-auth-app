from pwdlib import PasswordHash


dummypassword = "asdasdasdad"
password_hash = PasswordHash.recommended()
hashed_dummypassword = password_hash.hash(dummypassword)


def verifyPassword(new_password, saved_password):
    hashed_new_password = password_hash.hash(new_password)

    return password_hash.verify(hashed_new_password, saved_password)


def hashPassword(unhashed_password):
    hashed_password = password_hash.hash(unhashed_password)
    return hashed_password
