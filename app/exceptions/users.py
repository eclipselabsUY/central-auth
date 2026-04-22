# Empty, i know

# When a user's password is wrong:
class UserWrongPassword(Exception):
    pass

# When a user is not verified and tried to log in (succesfully):
class UserNotVerified(Exception):
    pass

# When a user is verified and tried to log in (succesfully) but account is locked:
class UserLocked(Exception):
    pass

