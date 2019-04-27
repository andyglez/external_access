def user_defined():
    return ['user', 'roles', 'show_details', 'quota', 'consumed', 'details', 'headers', 'modify', 'query_sent', 'query_value']

def user_view():
    return ['modify', 'show_details', 'query_sent', 'is_mod_phone']

class Cookies:
    def __init__(self, dictionary):
        self.dictionary = dictionary
    
    def get(self, key):
        return self.dictionary[key]

    def set(self, key, value):
        self.dictionary[key] = value

    def clear(self, key):
        return self.dictionary.pop(key) if key in self.dictionary else 0

    def clear_all(self):
        return [self.clear(cookie) for cookie in user_defined()]

    def contains(self, key):
        return key in self.dictionary

    def reset_all_flags(self, excepted=[]):
        for ck in user_view():
            if ck not in excepted:
                self.dictionary[ck] = False