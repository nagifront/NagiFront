import re

class NagifrontRouter(object):
    def db_for_read(self, model, **hints):
        """
        The model which has prefix 'nagios', read from nagios database
        """
        if re.match('^nagios.*', model._meta.model_name) is not None:
            return 'nagios'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        No write permission on nagios database
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        No Relations on nagios database
        """
        if re.match('^nagios.*', obj1._meta.model_name) is not None \
                or re.match('^nagios.*', obj2._meta.model_name) is not None:
            return False
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        No migrate permission on nagios database
        """
        if db == 'nagios':
            return False
        return True

    def allow_syncdb(self, db, model):
        """
        Sync is not necessary for nagios database
        """
        if db == 'nagios':
            return False
        return True
