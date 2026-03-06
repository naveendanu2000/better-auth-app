from pwdlib import PasswordHash


dummypassword = "asdasdasdad"
password_hash = PasswordHash.recommended()
hashed_dummypassword = password_hash.hash(dummypassword)


def verifyPassword(entered_password: str, saved_password: str | None) -> bool:

    if saved_password:
        return password_hash.verify(entered_password, saved_password)
    else:
        password_hash.verify(entered_password, hashed_dummypassword)
        return False


def hashPassword(unhashed_password: str):
    hashed_password = password_hash.hash(unhashed_password)
    return hashed_password
