
def is_uploader(self, user):
    return ((not user.is_superuser) and user.is_authenticated)


def is_approver(self, user):
    return (user.is_superuser and user.is_authenticated)
