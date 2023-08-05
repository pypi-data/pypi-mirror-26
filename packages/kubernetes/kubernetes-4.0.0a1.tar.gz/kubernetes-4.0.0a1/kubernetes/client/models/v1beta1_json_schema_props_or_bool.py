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


class V1beta1JSONSchemaPropsOrBool(object):
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
        'allows': 'bool',
        'schema': 'V1beta1JSONSchemaProps'
    }

    attribute_map = {
        'allows': 'Allows',
        'schema': 'Schema'
    }

    def __init__(self, allows=None, schema=None):
        """
        V1beta1JSONSchemaPropsOrBool - a model defined in Swagger
        """

        self._allows = None
        self._schema = None
        self.discriminator = None

        self.allows = allows
        self.schema = schema

    @property
    def allows(self):
        """
        Gets the allows of this V1beta1JSONSchemaPropsOrBool.

        :return: The allows of this V1beta1JSONSchemaPropsOrBool.
        :rtype: bool
        """
        return self._allows

    @allows.setter
    def allows(self, allows):
        """
        Sets the allows of this V1beta1JSONSchemaPropsOrBool.

        :param allows: The allows of this V1beta1JSONSchemaPropsOrBool.
        :type: bool
        """
        if allows is None:
            raise ValueError("Invalid value for `allows`, must not be `None`")

        self._allows = allows

    @property
    def schema(self):
        """
        Gets the schema of this V1beta1JSONSchemaPropsOrBool.

        :return: The schema of this V1beta1JSONSchemaPropsOrBool.
        :rtype: V1beta1JSONSchemaProps
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """
        Sets the schema of this V1beta1JSONSchemaPropsOrBool.

        :param schema: The schema of this V1beta1JSONSchemaPropsOrBool.
        :type: V1beta1JSONSchemaProps
        """
        if schema is None:
            raise ValueError("Invalid value for `schema`, must not be `None`")

        self._schema = schema

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
        if not isinstance(other, V1beta1JSONSchemaPropsOrBool):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
