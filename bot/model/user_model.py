import database

class UserModel(object):
    """docstring for UserModel"""
    def __init__(self, db):
        super(UserModel, self).__init__()
        self.db = db

    def get(self, user_id = None):
        if not user_id:
            return self.db.get('user')
        return self.db.get_where('user', {'id': user_id})

    def set(self, args):
        data = {
            'id':args.id,
            'is_bot':1 if args.is_bot else 0,
            'first':args.first_name,
            'last':args.last_name,
            'username':args.username
        }
        return self.db.insert('user', data)