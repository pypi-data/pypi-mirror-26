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


class V1CephFSPersistentVolumeSource(object):
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
        'monitors': 'list[str]',
        'path': 'str',
        'read_only': 'bool',
        'secret_file': 'str',
        'secret_ref': 'V1SecretReference',
        'user': 'str'
    }

    attribute_map = {
        'monitors': 'monitors',
        'path': 'path',
        'read_only': 'readOnly',
        'secret_file': 'secretFile',
        'secret_ref': 'secretRef',
        'user': 'user'
    }

    def __init__(self, monitors=None, path=None, read_only=None, secret_file=None, secret_ref=None, user=None):
        """
        V1CephFSPersistentVolumeSource - a model defined in Swagger
        """

        self._monitors = None
        self._path = None
        self._read_only = None
        self._secret_file = None
        self._secret_ref = None
        self._user = None
        self.discriminator = None

        self.monitors = monitors
        if path is not None:
          self.path = path
        if read_only is not None:
          self.read_only = read_only
        if secret_file is not None:
          self.secret_file = secret_file
        if secret_ref is not None:
          self.secret_ref = secret_ref
        if user is not None:
          self.user = user

    @property
    def monitors(self):
        """
        Gets the monitors of this V1CephFSPersistentVolumeSource.
        Required: Monitors is a collection of Ceph monitors More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :return: The monitors of this V1CephFSPersistentVolumeSource.
        :rtype: list[str]
        """
        return self._monitors

    @monitors.setter
    def monitors(self, monitors):
        """
        Sets the monitors of this V1CephFSPersistentVolumeSource.
        Required: Monitors is a collection of Ceph monitors More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :param monitors: The monitors of this V1CephFSPersistentVolumeSource.
        :type: list[str]
        """
        if monitors is None:
            raise ValueError("Invalid value for `monitors`, must not be `None`")

        self._monitors = monitors

    @property
    def path(self):
        """
        Gets the path of this V1CephFSPersistentVolumeSource.
        Optional: Used as the mounted root, rather than the full Ceph tree, default is /

        :return: The path of this V1CephFSPersistentVolumeSource.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path of this V1CephFSPersistentVolumeSource.
        Optional: Used as the mounted root, rather than the full Ceph tree, default is /

        :param path: The path of this V1CephFSPersistentVolumeSource.
        :type: str
        """

        self._path = path

    @property
    def read_only(self):
        """
        Gets the read_only of this V1CephFSPersistentVolumeSource.
        Optional: Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts. More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :return: The read_only of this V1CephFSPersistentVolumeSource.
        :rtype: bool
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """
        Sets the read_only of this V1CephFSPersistentVolumeSource.
        Optional: Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts. More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :param read_only: The read_only of this V1CephFSPersistentVolumeSource.
        :type: bool
        """

        self._read_only = read_only

    @property
    def secret_file(self):
        """
        Gets the secret_file of this V1CephFSPersistentVolumeSource.
        Optional: SecretFile is the path to key ring for User, default is /etc/ceph/user.secret More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :return: The secret_file of this V1CephFSPersistentVolumeSource.
        :rtype: str
        """
        return self._secret_file

    @secret_file.setter
    def secret_file(self, secret_file):
        """
        Sets the secret_file of this V1CephFSPersistentVolumeSource.
        Optional: SecretFile is the path to key ring for User, default is /etc/ceph/user.secret More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :param secret_file: The secret_file of this V1CephFSPersistentVolumeSource.
        :type: str
        """

        self._secret_file = secret_file

    @property
    def secret_ref(self):
        """
        Gets the secret_ref of this V1CephFSPersistentVolumeSource.
        Optional: SecretRef is reference to the authentication secret for User, default is empty. More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :return: The secret_ref of this V1CephFSPersistentVolumeSource.
        :rtype: V1SecretReference
        """
        return self._secret_ref

    @secret_ref.setter
    def secret_ref(self, secret_ref):
        """
        Sets the secret_ref of this V1CephFSPersistentVolumeSource.
        Optional: SecretRef is reference to the authentication secret for User, default is empty. More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :param secret_ref: The secret_ref of this V1CephFSPersistentVolumeSource.
        :type: V1SecretReference
        """

        self._secret_ref = secret_ref

    @property
    def user(self):
        """
        Gets the user of this V1CephFSPersistentVolumeSource.
        Optional: User is the rados user name, default is admin More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :return: The user of this V1CephFSPersistentVolumeSource.
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this V1CephFSPersistentVolumeSource.
        Optional: User is the rados user name, default is admin More info: https://releases.k8s.io/HEAD/examples/volumes/cephfs/README.md#how-to-use-it

        :param user: The user of this V1CephFSPersistentVolumeSource.
        :type: str
        """

        self._user = user

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
        if not isinstance(other, V1CephFSPersistentVolumeSource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
