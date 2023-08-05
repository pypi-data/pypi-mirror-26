
class Animal(object):
    name = ''

    def get_name(self):
        return self.name

    def print_name(self):
        print(self.name)

    def set_name(self, name):
        self.name = name or ''
