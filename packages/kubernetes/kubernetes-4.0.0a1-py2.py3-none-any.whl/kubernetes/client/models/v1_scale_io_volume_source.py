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


class V1ScaleIOVolumeSource(object):
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
        'fs_type': 'str',
        'gateway': 'str',
        'protection_domain': 'str',
        'read_only': 'bool',
        'secret_ref': 'V1LocalObjectReference',
        'ssl_enabled': 'bool',
        'storage_mode': 'str',
        'storage_pool': 'str',
        'system': 'str',
        'volume_name': 'str'
    }

    attribute_map = {
        'fs_type': 'fsType',
        'gateway': 'gateway',
        'protection_domain': 'protectionDomain',
        'read_only': 'readOnly',
        'secret_ref': 'secretRef',
        'ssl_enabled': 'sslEnabled',
        'storage_mode': 'storageMode',
        'storage_pool': 'storagePool',
        'system': 'system',
        'volume_name': 'volumeName'
    }

    def __init__(self, fs_type=None, gateway=None, protection_domain=None, read_only=None, secret_ref=None, ssl_enabled=None, storage_mode=None, storage_pool=None, system=None, volume_name=None):
        """
        V1ScaleIOVolumeSource - a model defined in Swagger
        """

        self._fs_type = None
        self._gateway = None
        self._protection_domain = None
        self._read_only = None
        self._secret_ref = None
        self._ssl_enabled = None
        self._storage_mode = None
        self._storage_pool = None
        self._system = None
        self._volume_name = None
        self.discriminator = None

        if fs_type is not None:
          self.fs_type = fs_type
        self.gateway = gateway
        if protection_domain is not None:
          self.protection_domain = protection_domain
        if read_only is not None:
          self.read_only = read_only
        self.secret_ref = secret_ref
        if ssl_enabled is not None:
          self.ssl_enabled = ssl_enabled
        if storage_mode is not None:
          self.storage_mode = storage_mode
        if storage_pool is not None:
          self.storage_pool = storage_pool
        self.system = system
        if volume_name is not None:
          self.volume_name = volume_name

    @property
    def fs_type(self):
        """
        Gets the fs_type of this V1ScaleIOVolumeSource.
        Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. \"ext4\", \"xfs\", \"ntfs\". Implicitly inferred to be \"ext4\" if unspecified.

        :return: The fs_type of this V1ScaleIOVolumeSource.
        :rtype: str
        """
        return self._fs_type

    @fs_type.setter
    def fs_type(self, fs_type):
        """
        Sets the fs_type of this V1ScaleIOVolumeSource.
        Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. \"ext4\", \"xfs\", \"ntfs\". Implicitly inferred to be \"ext4\" if unspecified.

        :param fs_type: The fs_type of this V1ScaleIOVolumeSource.
        :type: str
        """

        self._fs_type = fs_type

    @property
    def gateway(self):
        """
        Gets the gateway of this V1ScaleIOVolumeSource.
        The host address of the ScaleIO API Gateway.

        :return: The gateway of this V1ScaleIOVolumeSource.
        :rtype: str
        """
        return self._gateway

    @gateway.setter
    def gateway(self, gateway):
        """
        Sets the gateway of this V1ScaleIOVolumeSource.
        The host address of the ScaleIO API Gateway.

        :param gateway: The gateway of this V1ScaleIOVolumeSource.
        :type: str
        """
        if gateway is None:
            raise ValueError("Invalid value for `gateway`, must not be `None`")

        self._gateway = gateway

    @property
    def protection_domain(self):
        """
        Gets the protection_domain of this V1ScaleIOVolumeSource.
        The name of the Protection Domain for the configured storage (defaults to \"default\").

        :return: The protection_domain of this V1ScaleIOVolumeSource.
        :rtype: str
        """
        return self._protection_domain

    @protection_domain.setter
    def protection_domain(self, protection_domain):
        """
        Sets the protection_domain of this V1ScaleIOVolumeSource.
        The name of the Protection Domain for the configured storage (defaults to \"default\").

        :param protection_domain: The protection_domain of this V1ScaleIOVolumeSource.
        :type: str
        """

        self._protection_domain = protection_domain

    @property
    def read_only(self):
        """
        Gets the read_only of this V1ScaleIOVolumeSource.
        Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts.

        :return: The read_only of this V1ScaleIOVolumeSource.
        :rtype: bool
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """
        Sets the read_only of this V1ScaleIOVolumeSource.
        Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts.

        :param read_only: The read_only of this V1ScaleIOVolumeSource.
        :type: bool
        """

        self._read_only = read_only

    @property
    def secret_ref(self):
        """
        Gets the secret_ref of this V1ScaleIOVolumeSource.
        SecretRef references to the secret for ScaleIO user and other sensitive information. If this is not provided, Login operation will fail.

        :return: The secret_ref of this V1ScaleIOVolumeSource.
        :rtype: V1LocalObjectReference
        """
        return self._secret_ref

    @secret_ref.setter
    def secret_ref(self, secret_ref):
        """
        Sets the secret_ref of this V1ScaleIOVolumeSource.
        SecretRef references to the secret for ScaleIO user and other sensitive information. If this is not provided, Login operation will fail.

        :param secret_ref: The secret_ref of this V1ScaleIOVolumeSource.
        :type: V1LocalObjectReference
        """
        if secret_ref is None:
            raise ValueError("Invalid value for `secret_ref`, must not be `None`")

        self._secret_ref = secret_ref

    @property
    def ssl_enabled(self):
        """
        Gets the ssl_enabled of this V1ScaleIOVolumeSource.
        Flag to enable/disable SSL communication with Gateway, default false

        :return: The ssl_enabled of this V1ScaleIOVolumeSource.
        :rtype: bool
        """
        return self._ssl_enabled

    @ssl_enabled.setter
    def ssl_enabled(self, ssl_enabled):
        """
        Sets the ssl_enabled of this V1ScaleIOVolumeSource.
        Flag to enable/disable SSL communication with Gateway, default false

        :param ssl_enabled: The ssl_enabled of this V1ScaleIOVolumeSource.
        :type: bool
        """

        self._ssl_enabled = ssl_enabled

    @property
    def storage_mode(self):
        """
        Gets the storage_mode of this V1ScaleIOVolumeSource.
        Indicates whether the storage for a volume should be thick or thin (defaults to \"thin\").

        :return: The storage_mode of this V1ScaleIOVolumeSource.
        :rtype: str
        """
        return self._storage_mode

    @storage_mode.setter
    def storage_mode(self, storage_mode):
        """
        Sets the storage_mode of this V1ScaleIOVolumeSource.
        Indicates whether the storage for a volume should be thick or thin (defaults to \"thin\").

        :param storage_mode: The storage_mode of this V1ScaleIOVolumeSource.
        :type: str
        """

        self._storage_mode = storage_mode

    @property
    def storage_pool(self):
        """
        Gets the storage_pool of this V1ScaleIOVolumeSource.
        The Storage Pool associated with the protection domain (defaults to \"default\").

        :return: The storage_pool of this V1ScaleIOVolumeSource.
        :rtype: str
        """
        return self._storage_pool

    @storage_pool.setter
    def storage_pool(self, storage_pool):
        """
        Sets the storage_pool of this V1ScaleIOVolumeSource.
        The Storage Pool associated with the protection domain (defaults to \"default\").

        :param storage_pool: The storage_pool of this V1ScaleIOVolumeSource.
        :type: str
        """

        self._storage_pool = storage_pool

    @property
    def system(self):
        """
        Gets the system of this V1ScaleIOVolumeSource.
        The name of the storage system as configured in ScaleIO.

        :return: The system of this V1ScaleIOVolumeSource.
        :rtype: str
        """
        return self._system

    @system.setter
    def system(self, system):
        """
        Sets the system of this V1ScaleIOVolumeSource.
        The name of the storage system as configured in ScaleIO.

        :param system: The system of this V1ScaleIOVolumeSource.
        :type: str
        """
        if system is None:
            raise ValueError("Invalid value for `system`, must not be `None`")

        self._system = system

    @property
    def volume_name(self):
        """
        Gets the volume_name of this V1ScaleIOVolumeSource.
        The name of a volume already created in the ScaleIO system that is associated with this volume source.

        :return: The volume_name of this V1ScaleIOVolumeSource.
        :rtype: str
        """
        return self._volume_name

    @volume_name.setter
    def volume_name(self, volume_name):
        """
        Sets the volume_name of this V1ScaleIOVolumeSource.
        The name of a volume already created in the ScaleIO system that is associated with this volume source.

        :param volume_name: The volume_name of this V1ScaleIOVolumeSource.
        :type: str
        """

        self._volume_name = volume_name

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
        if not isinstance(other, V1ScaleIOVolumeSource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
