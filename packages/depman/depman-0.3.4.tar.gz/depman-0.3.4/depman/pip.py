from syn.base import create_hook, Attr
from .dependency import Dependency, command, output
from .operation import Combinable
from .relation import Eq, Le

#-------------------------------------------------------------------------------
# Pip Operations

#-----------------------------------------------------------
# pip install


class Install(Combinable):
    def execute(self):
        args = ' '.join(map(str, self))
        command('pip install --upgrade {}'.format(args))


#-------------------------------------------------------------------------------
# Pip


class Pip(Dependency):
    '''Representation of a pip dependency'''
    key = 'pip'
    order = 30

    _attrs = dict(order = Attr(int, order))

    @classmethod
    @create_hook
    def _populate_pkgs(cls):
        if not cls._pkgs:
            try:
                pkgs = output('pip freeze')
                cls._pkgs = dict([tuple(line.split('==')) 
                                  for line in pkgs.split('\n') if line])
            except OSError:
                pass

    def satisfy(self):
        inst = [Install(self.name, order=self.order)]
        instver = [Install('{}=={}'.format(self.name, self.version.rhs),
                           order=self.order)]

        if self.always_upgrade:
            return inst
            
        if not self.check():
            if isinstance(self.version, (Eq, Le)):
                return instver
            return inst
        return []


#-------------------------------------------------------------------------------
# __all__

__all__ = ('Pip',)

#-------------------------------------------------------------------------------
