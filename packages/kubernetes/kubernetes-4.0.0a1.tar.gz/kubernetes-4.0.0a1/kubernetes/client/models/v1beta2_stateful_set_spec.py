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


class V1beta2StatefulSetSpec(object):
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
        'pod_management_policy': 'str',
        'replicas': 'int',
        'revision_history_limit': 'int',
        'selector': 'V1LabelSelector',
        'service_name': 'str',
        'template': 'V1PodTemplateSpec',
        'update_strategy': 'V1beta2StatefulSetUpdateStrategy',
        'volume_claim_templates': 'list[V1PersistentVolumeClaim]'
    }

    attribute_map = {
        'pod_management_policy': 'podManagementPolicy',
        'replicas': 'replicas',
        'revision_history_limit': 'revisionHistoryLimit',
        'selector': 'selector',
        'service_name': 'serviceName',
        'template': 'template',
        'update_strategy': 'updateStrategy',
        'volume_claim_templates': 'volumeClaimTemplates'
    }

    def __init__(self, pod_management_policy=None, replicas=None, revision_history_limit=None, selector=None, service_name=None, template=None, update_strategy=None, volume_claim_templates=None):
        """
        V1beta2StatefulSetSpec - a model defined in Swagger
        """

        self._pod_management_policy = None
        self._replicas = None
        self._revision_history_limit = None
        self._selector = None
        self._service_name = None
        self._template = None
        self._update_strategy = None
        self._volume_claim_templates = None
        self.discriminator = None

        if pod_management_policy is not None:
          self.pod_management_policy = pod_management_policy
        if replicas is not None:
          self.replicas = replicas
        if revision_history_limit is not None:
          self.revision_history_limit = revision_history_limit
        if selector is not None:
          self.selector = selector
        self.service_name = service_name
        self.template = template
        if update_strategy is not None:
          self.update_strategy = update_strategy
        if volume_claim_templates is not None:
          self.volume_claim_templates = volume_claim_templates

    @property
    def pod_management_policy(self):
        """
        Gets the pod_management_policy of this V1beta2StatefulSetSpec.
        podManagementPolicy controls how pods are created during initial scale up, when replacing pods on nodes, or when scaling down. The default policy is `OrderedReady`, where pods are created in increasing order (pod-0, then pod-1, etc) and the controller will wait until each pod is ready before continuing. When scaling down, the pods are removed in the opposite order. The alternative policy is `Parallel` which will create pods in parallel to match the desired scale without waiting, and on scale down will delete all pods at once.

        :return: The pod_management_policy of this V1beta2StatefulSetSpec.
        :rtype: str
        """
        return self._pod_management_policy

    @pod_management_policy.setter
    def pod_management_policy(self, pod_management_policy):
        """
        Sets the pod_management_policy of this V1beta2StatefulSetSpec.
        podManagementPolicy controls how pods are created during initial scale up, when replacing pods on nodes, or when scaling down. The default policy is `OrderedReady`, where pods are created in increasing order (pod-0, then pod-1, etc) and the controller will wait until each pod is ready before continuing. When scaling down, the pods are removed in the opposite order. The alternative policy is `Parallel` which will create pods in parallel to match the desired scale without waiting, and on scale down will delete all pods at once.

        :param pod_management_policy: The pod_management_policy of this V1beta2StatefulSetSpec.
        :type: str
        """

        self._pod_management_policy = pod_management_policy

    @property
    def replicas(self):
        """
        Gets the replicas of this V1beta2StatefulSetSpec.
        replicas is the desired number of replicas of the given Template. These are replicas in the sense that they are instantiations of the same Template, but individual replicas also have a consistent identity. If unspecified, defaults to 1.

        :return: The replicas of this V1beta2StatefulSetSpec.
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """
        Sets the replicas of this V1beta2StatefulSetSpec.
        replicas is the desired number of replicas of the given Template. These are replicas in the sense that they are instantiations of the same Template, but individual replicas also have a consistent identity. If unspecified, defaults to 1.

        :param replicas: The replicas of this V1beta2StatefulSetSpec.
        :type: int
        """

        self._replicas = replicas

    @property
    def revision_history_limit(self):
        """
        Gets the revision_history_limit of this V1beta2StatefulSetSpec.
        revisionHistoryLimit is the maximum number of revisions that will be maintained in the StatefulSet's revision history. The revision history consists of all revisions not represented by a currently applied StatefulSetSpec version. The default value is 10.

        :return: The revision_history_limit of this V1beta2StatefulSetSpec.
        :rtype: int
        """
        return self._revision_history_limit

    @revision_history_limit.setter
    def revision_history_limit(self, revision_history_limit):
        """
        Sets the revision_history_limit of this V1beta2StatefulSetSpec.
        revisionHistoryLimit is the maximum number of revisions that will be maintained in the StatefulSet's revision history. The revision history consists of all revisions not represented by a currently applied StatefulSetSpec version. The default value is 10.

        :param revision_history_limit: The revision_history_limit of this V1beta2StatefulSetSpec.
        :type: int
        """

        self._revision_history_limit = revision_history_limit

    @property
    def selector(self):
        """
        Gets the selector of this V1beta2StatefulSetSpec.
        selector is a label query over pods that should match the replica count. If empty, defaulted to labels on the pod template. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors

        :return: The selector of this V1beta2StatefulSetSpec.
        :rtype: V1LabelSelector
        """
        return self._selector

    @selector.setter
    def selector(self, selector):
        """
        Sets the selector of this V1beta2StatefulSetSpec.
        selector is a label query over pods that should match the replica count. If empty, defaulted to labels on the pod template. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors

        :param selector: The selector of this V1beta2StatefulSetSpec.
        :type: V1LabelSelector
        """

        self._selector = selector

    @property
    def service_name(self):
        """
        Gets the service_name of this V1beta2StatefulSetSpec.
        serviceName is the name of the service that governs this StatefulSet. This service must exist before the StatefulSet, and is responsible for the network identity of the set. Pods get DNS/hostnames that follow the pattern: pod-specific-string.serviceName.default.svc.cluster.local where \"pod-specific-string\" is managed by the StatefulSet controller.

        :return: The service_name of this V1beta2StatefulSetSpec.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Sets the service_name of this V1beta2StatefulSetSpec.
        serviceName is the name of the service that governs this StatefulSet. This service must exist before the StatefulSet, and is responsible for the network identity of the set. Pods get DNS/hostnames that follow the pattern: pod-specific-string.serviceName.default.svc.cluster.local where \"pod-specific-string\" is managed by the StatefulSet controller.

        :param service_name: The service_name of this V1beta2StatefulSetSpec.
        :type: str
        """
        if service_name is None:
            raise ValueError("Invalid value for `service_name`, must not be `None`")

        self._service_name = service_name

    @property
    def template(self):
        """
        Gets the template of this V1beta2StatefulSetSpec.
        template is the object that describes the pod that will be created if insufficient replicas are detected. Each pod stamped out by the StatefulSet will fulfill this Template, but have a unique identity from the rest of the StatefulSet.

        :return: The template of this V1beta2StatefulSetSpec.
        :rtype: V1PodTemplateSpec
        """
        return self._template

    @template.setter
    def template(self, template):
        """
        Sets the template of this V1beta2StatefulSetSpec.
        template is the object that describes the pod that will be created if insufficient replicas are detected. Each pod stamped out by the StatefulSet will fulfill this Template, but have a unique identity from the rest of the StatefulSet.

        :param template: The template of this V1beta2StatefulSetSpec.
        :type: V1PodTemplateSpec
        """
        if template is None:
            raise ValueError("Invalid value for `template`, must not be `None`")

        self._template = template

    @property
    def update_strategy(self):
        """
        Gets the update_strategy of this V1beta2StatefulSetSpec.
        updateStrategy indicates the StatefulSetUpdateStrategy that will be employed to update Pods in the StatefulSet when a revision is made to Template.

        :return: The update_strategy of this V1beta2StatefulSetSpec.
        :rtype: V1beta2StatefulSetUpdateStrategy
        """
        return self._update_strategy

    @update_strategy.setter
    def update_strategy(self, update_strategy):
        """
        Sets the update_strategy of this V1beta2StatefulSetSpec.
        updateStrategy indicates the StatefulSetUpdateStrategy that will be employed to update Pods in the StatefulSet when a revision is made to Template.

        :param update_strategy: The update_strategy of this V1beta2StatefulSetSpec.
        :type: V1beta2StatefulSetUpdateStrategy
        """

        self._update_strategy = update_strategy

    @property
    def volume_claim_templates(self):
        """
        Gets the volume_claim_templates of this V1beta2StatefulSetSpec.
        volumeClaimTemplates is a list of claims that pods are allowed to reference. The StatefulSet controller is responsible for mapping network identities to claims in a way that maintains the identity of a pod. Every claim in this list must have at least one matching (by name) volumeMount in one container in the template. A claim in this list takes precedence over any volumes in the template, with the same name.

        :return: The volume_claim_templates of this V1beta2StatefulSetSpec.
        :rtype: list[V1PersistentVolumeClaim]
        """
        return self._volume_claim_templates

    @volume_claim_templates.setter
    def volume_claim_templates(self, volume_claim_templates):
        """
        Sets the volume_claim_templates of this V1beta2StatefulSetSpec.
        volumeClaimTemplates is a list of claims that pods are allowed to reference. The StatefulSet controller is responsible for mapping network identities to claims in a way that maintains the identity of a pod. Every claim in this list must have at least one matching (by name) volumeMount in one container in the template. A claim in this list takes precedence over any volumes in the template, with the same name.

        :param volume_claim_templates: The volume_claim_templates of this V1beta2StatefulSetSpec.
        :type: list[V1PersistentVolumeClaim]
        """

        self._volume_claim_templates = volume_claim_templates

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
        if not isinstance(other, V1beta2StatefulSetSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
