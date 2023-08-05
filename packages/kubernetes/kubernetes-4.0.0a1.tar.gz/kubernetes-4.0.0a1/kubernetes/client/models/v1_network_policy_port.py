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


class V1NetworkPolicyPort(object):
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
        'port': 'object',
        'protocol': 'str'
    }

    attribute_map = {
        'port': 'port',
        'protocol': 'protocol'
    }

    def __init__(self, port=None, protocol=None):
        """
        V1NetworkPolicyPort - a model defined in Swagger
        """

        self._port = None
        self._protocol = None
        self.discriminator = None

        if port is not None:
          self.port = port
        if protocol is not None:
          self.protocol = protocol

    @property
    def port(self):
        """
        Gets the port of this V1NetworkPolicyPort.
        The port on the given protocol. This can either be a numerical or named port on a pod. If this field is not provided, this matches all port names and numbers.

        :return: The port of this V1NetworkPolicyPort.
        :rtype: object
        """
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port of this V1NetworkPolicyPort.
        The port on the given protocol. This can either be a numerical or named port on a pod. If this field is not provided, this matches all port names and numbers.

        :param port: The port of this V1NetworkPolicyPort.
        :type: object
        """

        self._port = port

    @property
    def protocol(self):
        """
        Gets the protocol of this V1NetworkPolicyPort.
        The protocol (TCP or UDP) which traffic must match. If not specified, this field defaults to TCP.

        :return: The protocol of this V1NetworkPolicyPort.
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        """
        Sets the protocol of this V1NetworkPolicyPort.
        The protocol (TCP or UDP) which traffic must match. If not specified, this field defaults to TCP.

        :param protocol: The protocol of this V1NetworkPolicyPort.
        :type: str
        """

        self._protocol = protocol

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
        if not isinstance(other, V1NetworkPolicyPort):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
