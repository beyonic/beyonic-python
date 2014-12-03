'''
' API related resources
'''
import sys, json


class GenericObject(dict):
    def __init__(self, id=None, api_key=None, **params):
        super(GenericObject, self).__init__()
        self._params = params
        object.__setattr__(self, 'api_key', api_key)

        if id:
            self['id'] = id

    """
    Generic object class
    """

    @classmethod
    def from_json(cls, json_string):
        """
        Parses the given json_string, returning GenericObject instance/s.
        """
        return json.loads(json_string, object_hook=cls)

    def __setattr__(self, prop, val):
        if prop[0] == '_' or prop in self.__dict__:
            return super(GenericObject, self).__setattr__(prop, val)
        else:
            self[prop] = val

    def __getattr__(self, prop):
        if prop in self:
            return self[prop]
        else:
            raise AttributeError

    def __delitem__(self, prop):
        # on delete, setting value to None
        if prop in self:
            self[prop] = None

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('id'), dict):
            sid = self.get('id').get('id')
            ident_parts.append('id=%s' % (sid,))
        elif isinstance(self.get('id'), basestring):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> : %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        if isinstance(self.get('id'), dict):
            self = self.get('id')
        return json.dumps(self, sort_keys=True, indent=2)

