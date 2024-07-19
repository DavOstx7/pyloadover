from typing import Dict
from pyloadover.config import ConfigReloadable
from pyloadover.functions import Function
from pyloadover.groups import Group
from pyloadover.exceptions import GroupNotFoundError


class Manager(ConfigReloadable):
    def __init__(self):
        self._id_to_group: Dict[str, Group] = {}

    @property
    def id_to_group(self) -> Dict[str, Group]:
        # shallow copy (sub objects are modifiable)
        return self._id_to_group.copy()

    def reload_from_config(self):
        for group in self._id_to_group.values():
            group.reload_from_config()

    def clear(self):
        self._id_to_group.clear()

    def is_group_exists(self, _id: str) -> bool:
        return _id in self._id_to_group

    def get_group(self, group_id: str) -> Group:
        if group_id not in self._id_to_group:
            self._id_to_group[group_id] = Group.from_id(group_id)

        return self._id_to_group[group_id]

    def register_function_to_group(self, group_id: str, function: Function):
        self.get_group(group_id).register_function(function)

    def retrieve_function_from_group(self, group_id: str, *args, **kwargs) -> Function:
        if not self.is_group_exists(group_id):
            raise GroupNotFoundError(f"Group '{group_id}' does not exist")

        return self.get_group(group_id).retrieve_function_by_arguments(*args, **kwargs)


manager = Manager()
