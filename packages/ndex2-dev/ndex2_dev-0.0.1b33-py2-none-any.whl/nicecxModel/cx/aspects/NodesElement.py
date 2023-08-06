__author__ = 'aarongary'

import json
from nicecxModel.cx import CX_CONSTANTS

class NodesElement(object):
    def __init__(self, id=None, node_name=None, node_represents=None, json_obj=None):
        self.ASPECT_NAME = 'nodes'

        self._node_name = node_name
        self._node_represents = node_represents
        self._id = None

        if json_obj is not None:
            if type(json_obj) is dict:
                self._node_name = json_obj.get(CX_CONSTANTS.NAME)
                self._node_represents = json_obj.get(CX_CONSTANTS.NODE_REPRESENTS)
                if json_obj.get(CX_CONSTANTS.ID) is not None:
                    self._id = json_obj.get(CX_CONSTANTS.ID)
                else:
                    self._id = self._node_name
            else:
                raise Exception('NodesElement json input provided was not of type json object.')
        else:
            if id is None:
                self._id = node_name
            else:
                self._id = id

    def getAspectName(self):
        return self.ASPECT_NAME

    def getId(self):
        return self._id

    def setId(self, id):
        self._id = id

    def getNodeRepresents(self):
        return self._node_represents

    def setNodeRepresents(self, represents):
        self._node_represents = represents

    def getName(self):
        return self._node_name

    def setNodeName(self, node_name ):
        self._node_name = node_name

    def __eq__ (self, other):
        return self == other or self._id == other._id

    def __str__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        if self._id == -1:
            raise Exception('Edge element does not have a valid ID.  Unable to process this edge - ' + self._node_name)

        node_dict = {
            CX_CONSTANTS.ID: self._id,
            CX_CONSTANTS.NAME: self._node_name
        }

        if self._node_represents is not None:
            node_dict[CX_CONSTANTS.NODE_REPRESENTS] = self._node_represents

        return node_dict



