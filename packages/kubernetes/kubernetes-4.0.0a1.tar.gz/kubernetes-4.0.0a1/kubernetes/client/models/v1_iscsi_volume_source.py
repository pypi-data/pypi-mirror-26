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


class V1ISCSIVolumeSource(object):
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
        'chap_auth_discovery': 'bool',
        'chap_auth_session': 'bool',
        'fs_type': 'str',
        'initiator_name': 'str',
        'iqn': 'str',
        'iscsi_interface': 'str',
        'lun': 'int',
        'portals': 'list[str]',
        'read_only': 'bool',
        'secret_ref': 'V1LocalObjectReference',
        'target_portal': 'str'
    }

    attribute_map = {
        'chap_auth_discovery': 'chapAuthDiscovery',
        'chap_auth_session': 'chapAuthSession',
        'fs_type': 'fsType',
        'initiator_name': 'initiatorName',
        'iqn': 'iqn',
        'iscsi_interface': 'iscsiInterface',
        'lun': 'lun',
        'portals': 'portals',
        'read_only': 'readOnly',
        'secret_ref': 'secretRef',
        'target_portal': 'targetPortal'
    }

    def __init__(self, chap_auth_discovery=None, chap_auth_session=None, fs_type=None, initiator_name=None, iqn=None, iscsi_interface=None, lun=None, portals=None, read_only=None, secret_ref=None, target_portal=None):
        """
        V1ISCSIVolumeSource - a model defined in Swagger
        """

        self._chap_auth_discovery = None
        self._chap_auth_session = None
        self._fs_type = None
        self._initiator_name = None
        self._iqn = None
        self._iscsi_interface = None
        self._lun = None
        self._portals = None
        self._read_only = None
        self._secret_ref = None
        self._target_portal = None
        self.discriminator = None

        if chap_auth_discovery is not None:
          self.chap_auth_discovery = chap_auth_discovery
        if chap_auth_session is not None:
          self.chap_auth_session = chap_auth_session
        if fs_type is not None:
          self.fs_type = fs_type
        if initiator_name is not None:
          self.initiator_name = initiator_name
        self.iqn = iqn
        if iscsi_interface is not None:
          self.iscsi_interface = iscsi_interface
        self.lun = lun
        if portals is not None:
          self.portals = portals
        if read_only is not None:
          self.read_only = read_only
        if secret_ref is not None:
          self.secret_ref = secret_ref
        self.target_portal = target_portal

    @property
    def chap_auth_discovery(self):
        """
        Gets the chap_auth_discovery of this V1ISCSIVolumeSource.
        whether support iSCSI Discovery CHAP authentication

        :return: The chap_auth_discovery of this V1ISCSIVolumeSource.
        :rtype: bool
        """
        return self._chap_auth_discovery

    @chap_auth_discovery.setter
    def chap_auth_discovery(self, chap_auth_discovery):
        """
        Sets the chap_auth_discovery of this V1ISCSIVolumeSource.
        whether support iSCSI Discovery CHAP authentication

        :param chap_auth_discovery: The chap_auth_discovery of this V1ISCSIVolumeSource.
        :type: bool
        """

        self._chap_auth_discovery = chap_auth_discovery

    @property
    def chap_auth_session(self):
        """
        Gets the chap_auth_session of this V1ISCSIVolumeSource.
        whether support iSCSI Session CHAP authentication

        :return: The chap_auth_session of this V1ISCSIVolumeSource.
        :rtype: bool
        """
        return self._chap_auth_session

    @chap_auth_session.setter
    def chap_auth_session(self, chap_auth_session):
        """
        Sets the chap_auth_session of this V1ISCSIVolumeSource.
        whether support iSCSI Session CHAP authentication

        :param chap_auth_session: The chap_auth_session of this V1ISCSIVolumeSource.
        :type: bool
        """

        self._chap_auth_session = chap_auth_session

    @property
    def fs_type(self):
        """
        Gets the fs_type of this V1ISCSIVolumeSource.
        Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: \"ext4\", \"xfs\", \"ntfs\". Implicitly inferred to be \"ext4\" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi

        :return: The fs_type of this V1ISCSIVolumeSource.
        :rtype: str
        """
        return self._fs_type

    @fs_type.setter
    def fs_type(self, fs_type):
        """
        Sets the fs_type of this V1ISCSIVolumeSource.
        Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: \"ext4\", \"xfs\", \"ntfs\". Implicitly inferred to be \"ext4\" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi

        :param fs_type: The fs_type of this V1ISCSIVolumeSource.
        :type: str
        """

        self._fs_type = fs_type

    @property
    def initiator_name(self):
        """
        Gets the initiator_name of this V1ISCSIVolumeSource.
        Custom iSCSI initiator name. If initiatorName is specified with iscsiInterface simultaneously, new iSCSI interface <target portal>:<volume name> will be created for the connection.

        :return: The initiator_name of this V1ISCSIVolumeSource.
        :rtype: str
        """
        return self._initiator_name

    @initiator_name.setter
    def initiator_name(self, initiator_name):
        """
        Sets the initiator_name of this V1ISCSIVolumeSource.
        Custom iSCSI initiator name. If initiatorName is specified with iscsiInterface simultaneously, new iSCSI interface <target portal>:<volume name> will be created for the connection.

        :param initiator_name: The initiator_name of this V1ISCSIVolumeSource.
        :type: str
        """

        self._initiator_name = initiator_name

    @property
    def iqn(self):
        """
        Gets the iqn of this V1ISCSIVolumeSource.
        Target iSCSI Qualified Name.

        :return: The iqn of this V1ISCSIVolumeSource.
        :rtype: str
        """
        return self._iqn

    @iqn.setter
    def iqn(self, iqn):
        """
        Sets the iqn of this V1ISCSIVolumeSource.
        Target iSCSI Qualified Name.

        :param iqn: The iqn of this V1ISCSIVolumeSource.
        :type: str
        """
        if iqn is None:
            raise ValueError("Invalid value for `iqn`, must not be `None`")

        self._iqn = iqn

    @property
    def iscsi_interface(self):
        """
        Gets the iscsi_interface of this V1ISCSIVolumeSource.
        Optional: Defaults to 'default' (tcp). iSCSI interface name that uses an iSCSI transport.

        :return: The iscsi_interface of this V1ISCSIVolumeSource.
        :rtype: str
        """
        return self._iscsi_interface

    @iscsi_interface.setter
    def iscsi_interface(self, iscsi_interface):
        """
        Sets the iscsi_interface of this V1ISCSIVolumeSource.
        Optional: Defaults to 'default' (tcp). iSCSI interface name that uses an iSCSI transport.

        :param iscsi_interface: The iscsi_interface of this V1ISCSIVolumeSource.
        :type: str
        """

        self._iscsi_interface = iscsi_interface

    @property
    def lun(self):
        """
        Gets the lun of this V1ISCSIVolumeSource.
        iSCSI target lun number.

        :return: The lun of this V1ISCSIVolumeSource.
        :rtype: int
        """
        return self._lun

    @lun.setter
    def lun(self, lun):
        """
        Sets the lun of this V1ISCSIVolumeSource.
        iSCSI target lun number.

        :param lun: The lun of this V1ISCSIVolumeSource.
        :type: int
        """
        if lun is None:
            raise ValueError("Invalid value for `lun`, must not be `None`")

        self._lun = lun

    @property
    def portals(self):
        """
        Gets the portals of this V1ISCSIVolumeSource.
        iSCSI target portal List. The portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260).

        :return: The portals of this V1ISCSIVolumeSource.
        :rtype: list[str]
        """
        return self._portals

    @portals.setter
    def portals(self, portals):
        """
        Sets the portals of this V1ISCSIVolumeSource.
        iSCSI target portal List. The portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260).

        :param portals: The portals of this V1ISCSIVolumeSource.
        :type: list[str]
        """

        self._portals = portals

    @property
    def read_only(self):
        """
        Gets the read_only of this V1ISCSIVolumeSource.
        ReadOnly here will force the ReadOnly setting in VolumeMounts. Defaults to false.

        :return: The read_only of this V1ISCSIVolumeSource.
        :rtype: bool
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """
        Sets the read_only of this V1ISCSIVolumeSource.
        ReadOnly here will force the ReadOnly setting in VolumeMounts. Defaults to false.

        :param read_only: The read_only of this V1ISCSIVolumeSource.
        :type: bool
        """

        self._read_only = read_only

    @property
    def secret_ref(self):
        """
        Gets the secret_ref of this V1ISCSIVolumeSource.
        CHAP secret for iSCSI target and initiator authentication

        :return: The secret_ref of this V1ISCSIVolumeSource.
        :rtype: V1LocalObjectReference
        """
        return self._secret_ref

    @secret_ref.setter
    def secret_ref(self, secret_ref):
        """
        Sets the secret_ref of this V1ISCSIVolumeSource.
        CHAP secret for iSCSI target and initiator authentication

        :param secret_ref: The secret_ref of this V1ISCSIVolumeSource.
        :type: V1LocalObjectReference
        """

        self._secret_ref = secret_ref

    @property
    def target_portal(self):
        """
        Gets the target_portal of this V1ISCSIVolumeSource.
        iSCSI target portal. The portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260).

        :return: The target_portal of this V1ISCSIVolumeSource.
        :rtype: str
        """
        return self._target_portal

    @target_portal.setter
    def target_portal(self, target_portal):
        """
        Sets the target_portal of this V1ISCSIVolumeSource.
        iSCSI target portal. The portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260).

        :param target_portal: The target_portal of this V1ISCSIVolumeSource.
        :type: str
        """
        if target_portal is None:
            raise ValueError("Invalid value for `target_portal`, must not be `None`")

        self._target_portal = target_portal

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
        if not isinstance(other, V1ISCSIVolumeSource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
