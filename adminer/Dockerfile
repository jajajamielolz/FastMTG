FROM adminer

# This defines the password! The $password_hash is the hashed version of the password
# If you want to change the password, go to https://www.writephponline.com and enter
# `password_hash("PASSWORD", PASSWORD_DEFAULT)`, get the result and then replace the
# value. More information here -> https://nerdpress.org/2019/10/23/adminer-for-sqlite-in-docker
# Why do we need this? adminer needs a password and sqlite doesn't have a password
# Sooo, adminer *requries* you to set a password.

RUN echo -e "\
<?php \n\
require_once('plugins/login-password-less.php'); \n\
 \n\
/** Set allowed password \n\
        * @param string result of password_hash \n\
        */ \n\
return new AdminerLoginPasswordLess( \n\
        \$password_hash = '\$2y\$10\$vyb7I5XoSLa0b6gtm.Dy6.7gmnTvCDR73437.t/pzvVzaO0g4gIzG' \n\
); \n\
?> \
" > /var/www/html/plugins-enabled/login-password-less.php
