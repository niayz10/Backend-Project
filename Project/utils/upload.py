import os.path



def user_avatar_delete(filename):
    user_avatar_path = os.path.abspath(os.path.join(filename.path, '.'))
    print(user_avatar_path)
    os.remove(user_avatar_path)
