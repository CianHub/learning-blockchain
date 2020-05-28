""" Provides helper methods for returning classes """


class Printable:

    def __repr__(self):
        return str(self.__dict__)
