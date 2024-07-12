from typing import Dict
from pyloadover.group import Group, Function
from pyloadover.exceptions import GroupNotFoundError


class Manager:
    def __init__(self):
        self._id_to_group: Dict[str, Group] = {}

    def clear(self):
        self._id_to_group.clear()

    def is_group_exists(self, group_id: str) -> bool:
        return group_id in self._id_to_group

    def get_group(self, group_id: str) -> Group:
        if group_id in self._id_to_group:
            return self._id_to_group[group_id]

        self._id_to_group[group_id] = Group(group_id)
        return self._id_to_group[group_id]

    def register_to_group(self, group_id: str, function: Function):
        self.get_group(group_id).register(function)

    def retrieve_from_existing_group(self, group_id: str, *args, **kwargs) -> Function:
        if not self.is_group_exists(group_id):
            raise GroupNotFoundError(f"Group '{group_id}' does not exist")

        return self.get_group(group_id).find_one_by_arguments(*args, **kwargs)
