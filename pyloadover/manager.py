from typing import Dict
from pyloadover.config import ConfigReloadable
from pyloadover.groups import Group


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

    def is_group_exists(self, group_id: str) -> bool:
        return group_id in self._id_to_group

    def get_group(self, group_id: str) -> Group:
        if group_id not in self._id_to_group:
            self._id_to_group[group_id] = Group.from_group_id(group_id)

        return self._id_to_group[group_id]


manager = Manager()
