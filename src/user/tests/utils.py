from django.contrib.auth import get_user_model


# 유틸함수
def create_user(**params):
    """create된 유저를 return함"""
    return get_user_model().objects.create_user(**params)  # type: ignore
