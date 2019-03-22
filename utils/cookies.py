def user_defined():
    return ['user', 'roles', 'show_details', 'quota', 'consumed', 'details', 'headers', 'modify', 'query_sent']

def user_view():
    return ['modify', 'show_details', 'query_sent']

class Cookies:
    def __init__(self, dictionary):
        self.dictionary = dictionary
    
    def get(self, key):
        return self.dictionary[key]

    def set(self, key, value):
        self.dictionary[key] = value

    def clear(self, key):
        return self.dictionary.pop(key)

    def clear_all(self):
        return [self.clear(cookie) for cookie in user_defined()]

    def contains(self, key):
        return key in self.dictionary

    def reset_all_flags(self, excepted=''):
        for ck in user_view():
            if ck != excepted:
                self.dictionary[ck] = False