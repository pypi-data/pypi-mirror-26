"""
Auto-generated class for DatasourceResult
"""

from . import client_support


class DatasourceResult(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create():
        """
        :rtype: DatasourceResult
        """

        return DatasourceResult(
        )

    def __init__(self, json=None, **kwargs):
        if json is None and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'DatasourceResult'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
