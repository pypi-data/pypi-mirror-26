# coding: utf-8

"""
    Kubernetes

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: v1.8.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class V1beta1UserInfo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'extra': 'dict(str, list[str])',
        'groups': 'list[str]',
        'uid': 'str',
        'username': 'str'
    }

    attribute_map = {
        'extra': 'extra',
        'groups': 'groups',
        'uid': 'uid',
        'username': 'username'
    }

    def __init__(self, extra=None, groups=None, uid=None, username=None):
        """
        V1beta1UserInfo - a model defined in Swagger
        """

        self._extra = None
        self._groups = None
        self._uid = None
        self._username = None
        self.discriminator = None

        if extra is not None:
          self.extra = extra
        if groups is not None:
          self.groups = groups
        if uid is not None:
          self.uid = uid
        if username is not None:
          self.username = username

    @property
    def extra(self):
        """
        Gets the extra of this V1beta1UserInfo.
        Any additional information provided by the authenticator.

        :return: The extra of this V1beta1UserInfo.
        :rtype: dict(str, list[str])
        """
        return self._extra

    @extra.setter
    def extra(self, extra):
        """
        Sets the extra of this V1beta1UserInfo.
        Any additional information provided by the authenticator.

        :param extra: The extra of this V1beta1UserInfo.
        :type: dict(str, list[str])
        """

        self._extra = extra

    @property
    def groups(self):
        """
        Gets the groups of this V1beta1UserInfo.
        The names of groups this user is a part of.

        :return: The groups of this V1beta1UserInfo.
        :rtype: list[str]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """
        Sets the groups of this V1beta1UserInfo.
        The names of groups this user is a part of.

        :param groups: The groups of this V1beta1UserInfo.
        :type: list[str]
        """

        self._groups = groups

    @property
    def uid(self):
        """
        Gets the uid of this V1beta1UserInfo.
        A unique value that identifies this user across time. If this user is deleted and another user by the same name is added, they will have different UIDs.

        :return: The uid of this V1beta1UserInfo.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """
        Sets the uid of this V1beta1UserInfo.
        A unique value that identifies this user across time. If this user is deleted and another user by the same name is added, they will have different UIDs.

        :param uid: The uid of this V1beta1UserInfo.
        :type: str
        """

        self._uid = uid

    @property
    def username(self):
        """
        Gets the username of this V1beta1UserInfo.
        The name that uniquely identifies this user among all active users.

        :return: The username of this V1beta1UserInfo.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this V1beta1UserInfo.
        The name that uniquely identifies this user among all active users.

        :param username: The username of this V1beta1UserInfo.
        :type: str
        """

        self._username = username

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, V1beta1UserInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
