import os
from abc import abstractmethod
from typing import Set

from demisto_sdk.commands.common.constants import FileType
from demisto_sdk.commands.common.content.objects.pack_objects.pack import Pack
from demisto_sdk.commands.common.tools import get_yaml
from demisto_sdk.commands.convert.converters.base_converter import \
    BaseConverter


class ClassifierBaseConverter(BaseConverter):
    CLASSIFIER_UP_TO_5_9_9_SCHEMA_PATH = os.path.normpath(os.path.join(__file__, '..', '..', '..', '..',
                                                                       'common/schemas/',
                                                                       f'{FileType.OLD_CLASSIFIER.value}.yml'))

    CLASSIFIER_6_0_0_SCHEMA_PATH = os.path.normpath(os.path.join(__file__, '..', '..', '..', '..',
                                                                 'common/schemas/',
                                                                 f'{FileType.CLASSIFIER.value}.yml'))

    INTERSECTION_FIELDS_TO_EXCLUDE = {'fromVersion', 'toVersion'}

    def __init__(self, pack: Pack):
        super().__init__()
        self.pack = pack

    @abstractmethod
    def convert_dir(self) -> int:
        pass

    def get_classifiers_schema_intersection_fields(self, first_schema_path: str = CLASSIFIER_UP_TO_5_9_9_SCHEMA_PATH,
                                                   second_schema_path: str = CLASSIFIER_6_0_0_SCHEMA_PATH) -> Set[str]:
        """
        TODO test
        Receives schema path of two classifiers, returns the fields intersecting inside mapping field value.
        Args:
            first_schema_path (str): Path to first schema.
            second_schema_path (str): Path to second schema.

        Returns:
            (Set[str]): Set containing all intersecting fields inside mapping field value.
        """
        first_schema_data: dict = get_yaml(first_schema_path).get('mapping', dict())
        second_schema_data: dict = get_yaml(second_schema_path).get('mapping', dict())
        intersecting_fields = first_schema_data.keys() & second_schema_data.keys()
        return {field for field in intersecting_fields if field not in self.INTERSECTION_FIELDS_TO_EXCLUDE}
