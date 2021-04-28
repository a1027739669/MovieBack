from django.contrib.auth.hashers import make_password, check_password
sha_pwd = make_password('1234567890', None, 'pbkdf2_sha256')
print(sha_pwd)
isSame = check_password('1234567890', sha_pwd)
print(isSame)