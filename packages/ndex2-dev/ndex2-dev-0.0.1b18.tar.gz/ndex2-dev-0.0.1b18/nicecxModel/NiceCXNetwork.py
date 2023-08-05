__author__ = 'aarongary'

import json
import sys
import os
import errno
import pandas as pd
import networkx as nx
import ndex2.client as nc
import io
import decimal
import numpy as np
import math
import json
import ijson
import requests
import base64
import nicecxModel.NiceCXStreamer as ncs
from nicecxModel.metadata.MetaDataElement import MetaDataElement
from nicecxModel.cx.aspects.NameSpaces import NameSpaces
from nicecxModel.cx.aspects.NodesElement import NodesElement
from nicecxModel.cx.aspects.EdgesElement import EdgesElement
from nicecxModel.cx.aspects.NodeAttributesElement import NodeAttributesElement
from nicecxModel.cx.aspects.EdgeAttributesElement import EdgeAttributesElement
from nicecxModel.cx.aspects.NetworkAttributesElement import NetworkAttributesElement
from nicecxModel.cx.aspects.SupportElement import SupportElement
from nicecxModel.cx.aspects.CitationElement import CitationElement
from nicecxModel.cx.aspects.AspectElement import AspectElement
from nicecxModel.cx import CX_CONSTANTS
from nicecxModel.cx.aspects import ATTRIBUTE_DATA_TYPE
from nicecxModel.cx import known_aspects, known_aspects_min

if sys.version_info.major == 3:
    from urllib.request import urlopen, Request, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, \
        build_opener, install_opener, HTTPError, URLError
else:
    from urllib2 import urlopen, Request, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, \
        build_opener, install_opener, HTTPError, URLError

class NiceCXNetwork(object):
    def __init__(self, cx=None, server=None, username=None, password=None, uuid=None, networkx_G=None, pandas_df=None, filename=None, data=None, **attr):
        self.metadata = {}
        self.namespaces = NameSpaces()
        self.nodes = {}
        self.node_int_id_generator = set([])
        self.edge_int_id_generator = set([])
        self.node_id_lookup = []
        self.edges = {}
        self.citations = {}
        self.nodeCitations = {}
        self.edgeCitations = {}
        self.edgeSupports = {}
        self.nodeSupports = {}
        self.supports = {}
        self.nodeAttributes = {}
        self.edgeAttributes = {}
        self.edgeAttributeHeader = set([])
        self.nodeAttributeHeader = set([])
        self.networkAttributes = []
        self.nodeAssociatedAspects = {}
        self.edgeAssociatedAspects = {}
        self.opaqueAspects = {}
        self.provenance = None
        self.missingNodes = {}

        if cx:
            self.create_from_cx(cx)
        elif networkx_G:
            self.create_from_networkx(networkx_G)
        elif pandas_df is not None:
            self.create_from_pandas(pandas_df)
        elif filename is not None:
            if os.path.isfile(filename):
                with open(filename, 'rU') as file_cx:
                    #====================================
                    # BUILD NICECX FROM FILE
                    #====================================
                    self.create_from_cx(json.load(file_cx))
            else:
                raise Exception('Input provided is not a valid file')
        else:
            if server and uuid:
                self.create_from_server(server, username, password, uuid)

    def addNode(self, node_element=None, id=None, node_name=None, node_represents=None, json_obj=None):
        if node_element is None:
            node_element = NodesElement(id=id, node_name=node_name, node_represents=node_represents, json_obj=json_obj)

        if type(node_element) is NodesElement:
            self.nodes[node_element.getId()] = node_element

            if type(node_element.getId()) is str:
                self.node_int_id_generator.add(node_element.getId())

            if self.missingNodes.get(node_element.getId()) is not None:
                self.missingNodes.pop(node_element.getId(), None)

            return node_element.getId()
        else:
            raise Exception('Provided input was not of type NodesElement.')

    def addEdge(self, edge_element=None, id=None, edge_source=None, edge_target=None, edge_interaction=None, json_obj=None):
        if edge_element is None:
            edge_element = EdgesElement(id=id, edge_source=edge_source, edge_target=edge_target, edge_interaction=edge_interaction, json_obj=json_obj)

        if type(edge_element) is EdgesElement:
            if edge_element.getId() < 0:
                edge_element.setId(len(self.edges.keys()))
            self.edges[edge_element.getId()] = edge_element

            if self.nodes.get(edge_element.getSource()) is None:
                self.missingNodes[edge_element.getSource()] = 1

            if self.nodes.get(edge_element.getTarget()) is None:
                self.missingNodes[edge_element.getTarget()] = 1

            return edge_element.getId()
        else:
            raise Exception('Provided input was not of type EdgesElement.')

    def addNetworkAttribute(self, network_attribute_element=None, subnetwork=None, property_of=None, name=None, values=None, type=None, json_obj=None):
        if network_attribute_element is None:
            network_attribute_element = NetworkAttributesElement(subnetwork=subnetwork, property_of=property_of,
                                                                 name=name, values=values, type=type, json_obj=json_obj)

        self.networkAttributes.append(network_attribute_element)

    def addNodeAttribute(self, node_attribute_element=None, i=None, subnetwork=None, property_of=None, name=None, values=None, type=None, json_obj=None):
        if node_attribute_element is None:
            node_attribute_element = NodeAttributesElement(subnetwork=subnetwork, property_of=property_of, name=name,
                                                           values=values, type=type, json_obj=json_obj)

        self.nodeAttributeHeader.add(node_attribute_element.getName())
        nodeAttrs = self.nodeAttributes.get(node_attribute_element.getPropertyOf())
        if nodeAttrs is None:
            nodeAttrs = []
            self.nodeAttributes[node_attribute_element.getPropertyOf()] = nodeAttrs

        nodeAttrs.append(node_attribute_element)

    def addEdgeAttribute(self, edge_attribute_element=None, i=None, subnetwork=None, property_of=None, name=None, values=None, type=None, json_obj=None):
        if edge_attribute_element is None:
            edge_attribute_element = EdgeAttributesElement(subnetwork=subnetwork, property_of=property_of, name=name,
                                                           values=values, type=type, json_obj=json_obj)

        self.edgeAttributeHeader.add(edge_attribute_element.getName())
        edgeAttrs = self.edgeAttributes.get(edge_attribute_element.getPropertyOf())
        if edgeAttrs is None:
                edgeAttrs = []
                self.edgeAttributes[edge_attribute_element.getPropertyOf()] = edgeAttrs

        edgeAttrs.append(edge_attribute_element)

    def addSupport(self, support_element):
        if type(support_element) is SupportElement:
            self.supports[support_element.getId()] = support_element
        else:
            raise Exception('Provided input was not of type SupportElement.')

    def addCitation(self, citation_element):
        if type(citation_element) is CitationElement:
            self.citations[citation_element.getId()] = citation_element
        else:
            raise Exception('Provided input was not of type CitationElement.')

    def addNodeCitationsFromCX(self, node_citation_cx):
        self.buildManyToManyRelation('nodeCitations', node_citation_cx, 'citations')

    def addNodeCitations(self, node_id, citation_id):
        node_citation_element = {CX_CONSTANTS.PROPERTY_OF: [node_id], CX_CONSTANTS.CITATIONS: [citation_id]}
        self.buildManyToManyRelation('nodeCitations', node_citation_element, 'citations')

    def addEdgeCitationsFromCX(self, edge_citation_cx):
        self.buildManyToManyRelation('edgeCitations', edge_citation_cx, 'citations')

    def addEdgeCitations(self, edge_id, citation_id):
        edge_citation_element = {CX_CONSTANTS.PROPERTY_OF: [edge_id], CX_CONSTANTS.CITATIONS: [citation_id]}
        self.buildManyToManyRelation('edgeCitations', edge_citation_element, 'citations')

    def addEdgeSupports(self, edge_supports_element):
        self.buildManyToManyRelation('edgeSupports', edge_supports_element, 'supports')

    def buildManyToManyRelation(self, aspect_name, element, relation_name):
        if aspect_name == 'nodeCitations':
            aspect = self.nodeCitations
        elif aspect_name == 'edgeCitations':
            aspect = self.edgeCitations
        elif aspect_name == 'edgeSupports':
            aspect = self.edgeSupports
        else:
            raise Exception('Only nodeCitations, edgeCitations and edgeSupports are supported. ' + aspect_name + ' was supplied')

        for po in element.get(CX_CONSTANTS.PROPERTY_OF):
            po_id = aspect.get(po)
            if po_id is None:
                aspect[po] = element.get(relation_name)
            else:
                aspect[po] += element.get(relation_name)

    def addOpapqueAspect(self, opaque_element):
        if type(opaque_element) is AspectElement:
            aspectElmts = self.opaqueAspects.get(opaque_element.getAspectName())
            if aspectElmts is None:
                aspectElmts = []
                self.opaqueAspects[opaque_element.getAspectName()] = aspectElmts

            aspectElmts.append(opaque_element.getAspectElement())
        else:
            raise Exception('Provided input was not of type AspectElement.')

    def addNodeAssociatedAspectElement(self, nodeId, elmt):
        self.addAssciatatedAspectElement(self.nodeAssociatedAspects, nodeId, elmt)

    def addEdgeAssociatedAspectElement(self, edgeId, elmt):
        self.addAssciatatedAspectElement(self.edgeAssociatedAspects, edgeId, elmt)

    def addAssciatatedAspectElement(self, table, id, elmt):
        aspectElements = table.get(elmt.getAspectName())
        if aspectElements is None:
            aspectElements = {}
            table.put(elmt.getAspectName(), aspectElements)

        elmts = aspectElements.get(id)

        if (elmts is None):
            elmts = []
            aspectElements.put(id, elmts)

        elmts.append(elmt)

    def setName(self, network_name):
        add_this_network_attribute = NetworkAttributesElement(name='name', values=network_name, type=ATTRIBUTE_DATA_TYPE.STRING)

        self.addNetworkAttribute(name='name', values=network_name, type=ATTRIBUTE_DATA_TYPE.STRING)

    def getName(self):
        for net_a in self.networkAttributes:
            if net_a.getName() == 'name':
                return net_a.getValues()

        return None

    def getMetadata(self):
        return self.metadata

    def setMetadata(self, metadata_obj):
        if type(metadata_obj) is dict:
            self.metadata = metadata_obj
        else:
            raise Exception('Set metadata input was not of type <dict>')

    def addMetadata(self, md):
        if type(md) is MetaDataElement:
            #  TODO - alter metadata to match the element counts
            self.metadata[md.getName()] = md
        else:
            raise Exception('Provided input was not of type <MetaDataElement>')

    def addNameSpace(self, prefix, uri):
        self.namespaces[prefix] = uri

    def setNamespaces(self,ns ):
        self.namespaces = ns

    def getNamespaces(self,):
        return self.namespaces

    def getEdges (self):
        return self.edges

    def getNodes(self):
        return self.nodes

    def getOpaqueAspectTable(self):
        return self.opaqueAspects

    def getNetworkAttributes(self):
        return self.networkAttributes

    def getNodeAttributes(self):
        return self.nodeAttributes

    def getEdgeAttributes(self):
        return self.edgeAttributes

    def getEdgeAttributesById(self, id):
        return self.edgeAttributes.get(id)

    def getNodeAssociatedAspects(self):
        return self.nodeAssociatedAspects

    def getEdgeAssociatedAspects(self):
        return self.edgeAssociatedAspects

    def getNodeAssociatedAspect(self, aspectName):
        return self.nodeAssociatedAspects.get(aspectName)

    def getEdgeAssociatedAspect(self, aspectName):
        return self.edgeAssociatedAspects.get(aspectName)

    def getProvenance(self):
        return self.provenance

    def getMissingNodes(self):
        return self.missingNodes

    def setProvenance(self, provenance):
        self.provenance = provenance

    def getEdgeCitations(self):
        return self.edgeCitations

    def getNodeCitations(self):
        return self.nodeCitations

    def apply_template(self, server, username, password, uuid):
        error_message = []
        if not server:
            error_message.append('server')
        if not uuid:
            error_message.append('uuid')

        if server and uuid:
            #===================
            # METADATA
            #===================
            available_aspects = []
            for ae in (o for o in self.streamAspect(uuid, 'metaData', server, username, password)):
                available_aspects.append(ae.get(CX_CONSTANTS.METADATA_NAME))

            #=======================
            # ADD VISUAL PROPERTIES
            #=======================
            for oa in available_aspects:
                if 'visualProperties' in oa:
                    objects = self.streamAspect(uuid, 'visualProperties', server, username, password)
                    obj_items = (o for o in objects)
                    for oa_item in obj_items:
                        aspect_element = AspectElement(oa_item, oa)
                        self.addOpapqueAspect(aspect_element)
                    vis_prop_size = len(self.opaqueAspects.get('visualProperties'))
                    mde = MetaDataElement(elementCount=vis_prop_size, version=1, consistencyGroup=1, name='visualProperties')
                    self.addMetadata(mde)


                if 'cyVisualProperties' in oa:
                    objects = self.streamAspect(uuid, 'cyVisualProperties', server, username, password)
                    obj_items = (o for o in objects)
                    for oa_item in obj_items:
                        aspect_element = AspectElement(oa_item, oa)
                        self.addOpapqueAspect(aspect_element)
                    vis_prop_size = len(self.opaqueAspects.get('cyVisualProperties'))
                    mde = MetaDataElement(elementCount=vis_prop_size, version=1, consistencyGroup=1, name='cyVisualProperties')
                    self.addMetadata(mde)
        else:
            raise Exception(', '.join(error_message) + 'not specified in apply_template')

    def create_from_pandas(self, df, source_field=None, target_field=None, source_node_attr=[], target_node_attr=[], edge_attr=[], edge_interaction=None):
        """
        Constructor that uses a pandas dataframe to build niceCX
        :param df: dataframe
        :type df: Pandas Dataframe
        :param headers:
        :type headers:
        :return: none
        :rtype: n/a
        """

        #====================================================
        # IF NODE FIELD NAME (SOURCE AND TARGET) IS PROVIDED
        # THEN USE THOSE FIELDS OTHERWISE USE INDEX 0 & 1
        #====================================================
        self.setName('Pandas Upload')
        self.add_metadata_stub('networkAttributes')
        count = 0
        if source_field and target_field:
            for index, row in df.iterrows():
                if count % 10000 == 0:
                    print(count)
                count += 1
                #=============
                # ADD NODES
                #=============
                self.addNode(id=row[source_field], node_name=row[source_field], node_represents=row[source_field])
                self.addNode(id=row[target_field], node_name=row[target_field], node_represents=row[target_field])

                #=============
                # ADD EDGES
                #=============
                self.addEdge(id=index, edge_source=row[source_field], edge_target=row[target_field], edge_interaction=row[edge_interaction])

                #==============================
                # ADD SOURCE NODE ATTRIBUTES
                #==============================
                for sp in source_node_attr:
                    attr_type = None
                    if type(row[sp]) is float and math.isnan(row[sp]):
                        row[sp] = ''
                        attr_type = ATTRIBUTE_DATA_TYPE.FLOAT
                    elif type(row[sp]) is float and math.isinf(row[sp]):
                        row[sp] = 'Inf'
                        attr_type = ATTRIBUTE_DATA_TYPE.FLOAT
                    self.addNodeAttribute(property_of=row[source_field], name=sp, values=row[sp], type=attr_type)

                #==============================
                # ADD TARGET NODE ATTRIBUTES
                #==============================
                for tp in target_node_attr:
                    attr_type = None
                    if type(row[tp]) is float and math.isnan(row[tp]):
                        row[tp] = ''
                        attr_type = ATTRIBUTE_DATA_TYPE.FLOAT
                    elif type(row[tp]) is float and math.isinf(row[tp]):
                        row[tp] = 'Inf'
                        attr_type = ATTRIBUTE_DATA_TYPE.FLOAT
                    self.addNodeAttribute(property_of=row[target_field], name=tp, values=row[tp], type=attr_type)

                #==============================
                # ADD EDGE ATTRIBUTES
                #==============================
                for ep in edge_attr:
                    attr_type = None
                    if type(row[ep]) is float and math.isnan(row[ep]):
                        row[ep] = ''
                        attr_type = ATTRIBUTE_DATA_TYPE.FLOAT
                    elif type(row[ep]) is float and math.isinf(row[ep]):
                        row[ep] = 'INFINITY'
                        attr_type = ATTRIBUTE_DATA_TYPE.FLOAT

                    self.addEdgeAttribute(property_of=index, name=ep, values=row[ep], type=attr_type)

        else:
            for index, row in df.iterrows():
                #=============
                # ADD NODES
                #=============
                self.addNode(id=row[0], node_name=row[0], node_represents=row[0])
                self.addNode(id=row[1], node_name=row[1], node_represents=row[1])

                #=============
                # ADD EDGES
                #=============
                if len(row) > 2:
                    self.addEdge(id=index, edge_source=row[0], edge_target=row[1], edge_interaction=row[2])
                else:
                    self.addEdge(id=index, edge_source=row[0], edge_target=row[1], edge_interaction='interacts-with')

        self.add_metadata_stub('nodes')
        self.add_metadata_stub('edges')
        if source_node_attr or target_node_attr:
            self.add_metadata_stub('nodeAttributes')
        if edge_attr:
            self.add_metadata_stub('edgeAttributes')

    def create_from_networkx(self, G):
        """
        Constructor that uses a networkx graph to build niceCX
        :param G: networkx graph
        :type G: networkx graph
        :return: none
        :rtype: none
        """
        self.setName('Networkx Upload')
        self.add_metadata_stub('networkAttributes')
        for n, d in G.nodes_iter(data=True):
            #=============
            # ADD NODES
            #=============
            self.addNode(id=n, node_name=n, node_represents=n)

            #======================
            # ADD NODE ATTRIBUTES
            #======================
            for k,v in d.items():
                self.addNodeAttribute(property_of=n, name=k, values=v)

        index = 0
        for u, v, d in G.edges_iter(data=True):
            #=============
            # ADD EDGES
            #=============
            self.addEdge(id=index, edge_source=u, edge_target=v, edge_interaction=d.get('interaction'))

            #==============================
            # ADD EDGE ATTRIBUTES
            #==============================
            for k,v in d.items():
                self.addEdgeAttribute(property_of=index, name=k, values=v)

            index += 1

        self.add_metadata_stub('nodes')
        self.add_metadata_stub('edges')
        if self.nodeAttributes:
            self.add_metadata_stub('nodeAttributes')
        if self.edgeAttributes:
            self.add_metadata_stub('edgeAttributes')
        #print json.dumps(self.to_json())

    def create_from_server(self, server, username, password, uuid):
        if server and uuid:
            #===================
            # METADATA
            #===================
            available_aspects = []
            for ae in (o for o in self.streamAspect(uuid, 'metaData', server, username, password)):
                available_aspects.append(ae.get(CX_CONSTANTS.METADATA_NAME))
                mde = MetaDataElement(json_obj=ae)
                self.addMetadata(mde)

            opaque_aspects = set(available_aspects).difference(known_aspects_min)

            #====================
            # NETWORK ATTRIBUTES
            #====================
            if 'networkAttributes' in available_aspects:
                objects = self.streamAspect(uuid, 'networkAttributes', server, username, password)
                obj_items = (o for o in objects)
                for network_item in obj_items:
                    #add_this_network_attribute = NetworkAttributesElement(json_obj=network_item)

                    self.addNetworkAttribute(json_obj=network_item)
                self.add_metadata_stub('networkAttributes')

            #===================
            # NODES
            #===================
            if 'nodes' in available_aspects:
                objects = self.streamAspect(uuid, 'nodes', server, username, password)
                obj_items = (o for o in objects)
                for node_item in obj_items:
                    #add_this_node = NodesElement(json_obj=node_item)

                    self.addNode(json_obj=node_item)
                self.add_metadata_stub('nodes')

            #===================
            # EDGES
            #===================
            if 'edges' in available_aspects:
                objects = self.streamAspect(uuid, 'edges', server, username, password)
                obj_items = (o for o in objects)
                for edge_item in obj_items:
                    #add_this_edge = EdgesElement(json_obj=edge_item)

                    self.addEdge(json_obj=edge_item)
                self.add_metadata_stub('edges')

            #===================
            # NODE ATTRIBUTES
            #===================
            if 'nodeAttributes' in available_aspects:
                objects = self.streamAspect(uuid, 'nodeAttributes', server, username, password)
                obj_items = (o for o in objects)
                for att in obj_items:
                    #add_this_node_att = NodeAttributesElement(json_obj=att)

                    self.addNodeAttribute(json_obj=att)
                self.add_metadata_stub('nodeAttributes')

            #===================
            # EDGE ATTRIBUTES
            #===================
            if 'edgeAttributes' in available_aspects:
                objects = self.streamAspect(uuid, 'edgeAttributes', server, username, password)
                obj_items = (o for o in objects)
                for att in obj_items:
                    #add_this_edge_att = EdgeAttributesElement(json_obj=att)

                    self.addEdgeAttribute(json_obj=att)
                self.add_metadata_stub('edgeAttributes')

            #===================
            # CITATIONS
            #===================
            if 'citations' in available_aspects:
                objects = self.streamAspect(uuid, 'citations', server, username, password)
                obj_items = (o for o in objects)
                for cit in obj_items:
                    add_this_citation = CitationElement(json_obj=cit)

                    self.addCitation(add_this_citation)
                self.add_metadata_stub('citations')

            #===================
            # SUPPORTS
            #===================
            if 'supports' in available_aspects:
                objects = self.streamAspect(uuid, 'supports', server, username, password)
                obj_items = (o for o in objects)
                for sup in obj_items:
                    add_this_supports = SupportElement(json_obj=sup)

                    self.addSupport(add_this_supports)
                self.add_metadata_stub('supports')

            #===================
            # EDGE SUPPORTS
            #===================
            if 'edgeSupports' in available_aspects:
                objects = self.streamAspect(uuid, 'edgeSupports', server, username, password)
                obj_items = (o for o in objects)
                for add_this_edge_sup in obj_items:
                    self.addEdgeSupports(add_this_edge_sup)

                self.add_metadata_stub('edgeSupports')

            #===================
            # NODE CITATIONS
            #===================
            if 'nodeCitations' in available_aspects:
                objects = self.streamAspect(uuid, 'nodeCitations', server, username, password)
                obj_items = (o for o in objects)
                for node_cit in obj_items:
                    self.addNodeCitationsFromCX(node_cit)
                self.add_metadata_stub('nodeCitations')

            #===================
            # EDGE CITATIONS
            #===================
            if 'edgeCitations' in available_aspects:
                objects = self.streamAspect(uuid, 'edgeCitations', server, username, password)
                obj_items = (o for o in objects)
                for edge_cit in obj_items:
                    self.addEdgeCitationsFromCX(edge_cit)
                self.add_metadata_stub('edgeCitations')

            #===================
            # OPAQUE ASPECTS
            #===================
            for oa in opaque_aspects:
                objects = self.streamAspect(uuid, oa, server, username, password)
                obj_items = (o for o in objects)
                for oa_item in obj_items:
                    aspect_element = AspectElement(oa_item, oa)
                    self.addOpapqueAspect(aspect_element)
                    self.add_metadata_stub(oa)
        else:
            raise Exception('Server and uuid not specified')

    def create_from_cx(self, cx):
        if cx:
            #===================
            # METADATA
            #===================
            available_aspects = []
            for ae in (o for o in self.get_frag_from_list_by_key(cx, 'metaData')):
                available_aspects.append(ae.get(CX_CONSTANTS.METADATA_NAME))
                mde = MetaDataElement(json_obj=ae)
                self.addMetadata(mde)

            opaque_aspects = set(available_aspects).difference(known_aspects_min)

            #====================
            # NETWORK ATTRIBUTES
            #====================
            if 'networkAttributes' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'networkAttributes')
                obj_items = (o for o in objects)
                for network_item in obj_items:
                    add_this_network_attribute = NetworkAttributesElement(json_obj=network_item)

                    self.addNetworkAttribute(network_attribute_element=add_this_network_attribute)
                self.add_metadata_stub('networkAttributes')

            #===================
            # NODES
            #===================
            if 'nodes' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'nodes')
                obj_items = (o for o in objects)
                for node_item in obj_items:
                    #add_this_node = NodesElement(json_obj=node_item)

                    self.addNode(json_obj=node_item)
                self.add_metadata_stub('nodes')

            #===================
            # EDGES
            #===================
            if 'edges' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'edges')
                obj_items = (o for o in objects)
                for edge_item in obj_items:
                    #add_this_edge = EdgesElement(json_obj=edge_item)

                    self.addEdge(json_obj=edge_item)
                self.add_metadata_stub('edges')

            #===================
            # NODE ATTRIBUTES
            #===================
            if 'nodeAttributes' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'nodeAttributes')
                obj_items = (o for o in objects)
                for att in obj_items:
                    #add_this_node_att = NodeAttributesElement(json_obj=att)

                    self.addNodeAttribute(json_obj=att)
                self.add_metadata_stub('nodeAttributes')

            #===================
            # EDGE ATTRIBUTES
            #===================
            if 'edgeAttributes' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'edgeAttributes')
                obj_items = (o for o in objects)
                for att in obj_items:
                    #add_this_edge_att = EdgeAttributesElement(json_obj=att)

                    self.addEdgeAttribute(json_obj=att)
                self.add_metadata_stub('edgeAttributes')

            #===================
            # CITATIONS
            #===================
            if 'citations' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'citations')
                obj_items = (o for o in objects)
                for cit in obj_items:
                    add_this_citation = CitationElement(json_obj=cit)

                    self.addCitation(add_this_citation)
                self.add_metadata_stub('citations')

            #===================
            # SUPPORTS
            #===================
            if 'supports' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'supports')
                obj_items = (o for o in objects)
                for sup in obj_items:
                    add_this_supports = SupportElement(json_obj=sup)

                    self.addSupport(add_this_supports)
                self.add_metadata_stub('supports')

            #===================
            # EDGE SUPPORTS
            #===================
            if 'edgeSupports' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'edgeSupports')
                obj_items = (o for o in objects)
                for add_this_edge_sup in obj_items:
                    self.addEdgeSupports(add_this_edge_sup)

                self.add_metadata_stub('edgeSupports')

            #===================
            # NODE CITATIONS
            #===================
            if 'nodeCitations' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'nodeCitations')
                obj_items = (o for o in objects)
                for node_cit in obj_items:
                    self.addNodeCitationsFromCX(node_cit)
                self.add_metadata_stub('nodeCitations')

            #===================
            # EDGE CITATIONS
            #===================
            if 'edgeCitations' in available_aspects:
                objects = self.get_frag_from_list_by_key(cx, 'edgeCitations')
                obj_items = (o for o in objects)
                for edge_cit in obj_items:
                    self.addEdgeCitationsFromCX(edge_cit)
                self.add_metadata_stub('edgeCitations')

            #===================
            # OPAQUE ASPECTS
            #===================
            for oa in opaque_aspects:
                objects = self.get_frag_from_list_by_key(cx, oa)
                obj_items = (o for o in objects)
                for oa_item in obj_items:
                    aspect_element = AspectElement(oa_item, oa)
                    self.addOpapqueAspect(aspect_element)
                    self.add_metadata_stub(oa)
        else:
            raise Exception('CX is empty')

    def get_frag_from_list_by_key(self, cx, key):
        for aspect in cx:
            if key in aspect:
                return aspect[key]

        return []

    def to_pandas(self):
        rows = []
        edge_items = None
        if sys.version_info.major == 3:
            edge_items = self.edges.items()
        else:
            edge_items = self.edges.iteritems()

        for k, v in edge_items:
            e_a = self.edgeAttributes.get(k)
            #==========================
            # PROCESS EDGE ATTRIBUTES
            #==========================
            add_this_dict = {}
            if e_a is not None:
                for e_a_item in e_a:
                    if type(e_a_item.getValues()) is list:
                        add_this_dict[e_a_item.getName()] = ','.join(str(e) for e in e_a_item.getValues())
                        add_this_dict[e_a_item.getName()] = '"' + add_this_dict[e_a_item.getName()] + '"'
                    else:
                        add_this_dict[e_a_item.getName()] = e_a_item.getValues()
            #================================
            # PROCESS SOURCE NODE ATTRIBUTES
            #================================
            s_a = self.nodeAttributes.get(v.getSource())
            if s_a is not None:
                for s_a_item in s_a:
                    if type(s_a_item.getValues()) is list:
                        add_this_dict['source_' + s_a_item.getName()] = ','.join(str(e) for e in s_a_item.getValues())
                        add_this_dict['source_' + s_a_item.getName()] = '"' + add_this_dict['source_' + s_a_item.getName()] + '"'
                    else:
                        add_this_dict['source_' + s_a_item.getName()] = s_a_item.getValues()

            #================================
            # PROCESS TARGET NODE ATTRIBUTES
            #================================
            t_a = self.nodeAttributes.get(v.getTarget())
            if t_a is not None:
                for t_a_item in t_a:
                    if type(t_a_item.getValues()) is list:
                        add_this_dict['target_' + t_a_item.getName()] = ','.join(str(e) for e in t_a_item.getValues())
                        add_this_dict['target_' + t_a_item.getName()] = '"' + add_this_dict['target_' + t_a_item.getName()] + '"'
                    else:
                        add_this_dict['target_' + t_a_item.getName()] = t_a_item.getValues()

            if add_this_dict:
                rows.append(dict(add_this_dict, source=self.nodes.get(v.getSource())._node_name, target=self.nodes.get(v.getTarget())._node_name, interaction=v._interaction))
            else:
                rows.append(dict(source=self.nodes.get(v.getSource())._node_name, target=self.nodes.get(v.getTarget())._node_name, interaction=v._interaction))

        nodeAttributeSourceTarget = []
        for n_a in self.nodeAttributeHeader:
            nodeAttributeSourceTarget.append('source_' + n_a)
            nodeAttributeSourceTarget.append('target_' + n_a)

        df_columns = ['source', 'interaction', 'target'] + list(self.edgeAttributeHeader) + nodeAttributeSourceTarget

        return_df = pd.DataFrame(rows, columns=df_columns)

        return return_df

    def add_metadata_stub(self, aspect_name):
        md = self.metadata.get(aspect_name)
        if md is None:
            mde = MetaDataElement(elementCount=0, properties=[], version='1.0', consistencyGroup=1, name=aspect_name)
            self.addMetadata(mde)

    def stream_cx(self):
        """Convert this network to a CX stream

        :return: The CX stream representation of this network.
        :rtype: io.BytesIO

        """
        cx = self.to_cx()

        if sys.version_info.major == 3:
            return io.BytesIO(json.dumps(cx).encode('utf-8'))
        else:
            return_bytes = None
            try:
                return_bytes = io.BytesIO(json.dumps(cx))
            except UnicodeDecodeError as err1:
                print("Detected invalid encoding. Trying latin-1 encoding.")
                return_bytes = io.BytesIO(json.dumps(cx, encoding="latin-1"))
                print("Success")
            except Exception as err2:
                print(err2.message)

            return return_bytes

    def upload_to(self, server, username, password):
        """ Upload this network to the specified server to the account specified by username and password.

        :param server: The NDEx server to upload the network to.
        :type server: str
        :param username: The username of the account to store the network.
        :type username: str
        :param password: The password for the account.
        :type password: str
        :return: The UUID of the network on NDEx.
        :rtype: str

        Example:
            ndexGraph.upload_to('http://test.ndexbio.org', 'myusername', 'mypassword')
        """

        if server and 'http' not in server:
            server = 'http://' + server

        ndex = nc.Ndex2(server,username,password)
        save_this_cx = self.to_json()
        return ndex.save_new_network(save_this_cx)

    def upload_new_network_stream(self, server, username, password):
        response = ncs.postNiceCxStream(self)

        print(response)

    def update_to(self, uuid, server, username, password):
        """ Upload this network to the specified server to the account specified by username and password.

        :param server: The NDEx server to upload the network to.
        :type server: str
        :param username: The username of the account to store the network.
        :type username: str
        :param password: The password for the account.
        :type password: str
        :return: The UUID of the network on NDEx.
        :rtype: str

        Example:
            ndexGraph.upload_to('http://test.ndexbio.org', 'myusername', 'mypassword')
        """
        cx = self.to_json()
        ndex = nc.Ndex2(server,username,password)

        if(len(cx) > 0):
            if(cx[len(cx) - 1] is not None):
                if(cx[len(cx) - 1].get('status') is None):
                    # No STATUS element in the array.  Append a new status
                    cx.append({"status" : [ {"error" : "","success" : True} ]})
                else:
                    if(len(cx[len(cx) - 1].get('status')) < 1):
                        # STATUS element found, but the status was empty
                        cx[len(cx) - 1].get('status').append({"error" : "","success" : True})

            if sys.version_info.major == 3:
                stream = io.BytesIO(json.dumps(cx).encode('utf-8'))
            else:
                stream = io.BytesIO(json.dumps(cx))

            return ndex.update_cx_network(stream, uuid)
        else:
            raise IndexError("Cannot save empty CX.  Please provide a non-empty CX document.")

    def to_networkx(self):
        G = nx.Graph()

        if sys.version_info.major == 3:
            node_items = self.nodes.items()
            edge_items = self.edges.items()
        else:
            node_items = self.nodes.iteritems()
            edge_items = self.edges.iteritems()

        #============================
        # PROCESS NETWORK ATTRIBUTES
        #============================
        for net_a in self.networkAttributes:
            G.graph[net_a.getName()] = net_a.getValues()

        #================================
        # PROCESS NODE & NODE ATTRIBUTES
        #================================
        for k, v in node_items:
            node_attrs = {}
            n_a = self.nodeAttributes.get(k)
            if n_a:
                for na_item in n_a:
                    node_attrs[na_item.getName()] = na_item.getValues()
                    #print(v)
                    my_name = v.getName()
                G.add_node(k, node_attrs, name=v.getName())

        #================================
        # PROCESS EDGE & EDGE ATTRIBUTES
        #================================
        for k, v in edge_items:
            e_a = self.edgeAttributes.get(k)
            add_this_dict = {}
            if e_a is not None:
                for e_a_item in e_a:
                    if type(e_a_item.getValues()) is list:
                        add_this_dict[e_a_item.getName()] = ','.join(str(e) for e in e_a_item.getValues())
                        add_this_dict[e_a_item.getName()] = '"' + add_this_dict[e_a_item.getName()] + '"'
                    else:
                        add_this_dict[e_a_item.getName()] = e_a_item.getValues()

                G.add_edge(v.getSource(), v.getTarget(), add_this_dict)
            else:
                G.add_edge(v.getSource(), v.getTarget())

        #================
        # PROCESS LAYOUT
        #================
        #if hasattr(networkx_G, 'pos'):
        #    G.pos = {node_dict[a] : b for a, b in networkx_G.pos.items()}

        return G

    def __str__(self):
        return json.dumps(self.to_json(), cls=DecimalEncoder)

    def to_json(self):
        output_cx = [{"numberVerification": [{"longNumber": 281474976710655}]}]

        #=====================================================
        # IF THE @ID IS NOT NUMERIC WE NEED TO CONVERT IT TO
        # INT BY USING THE INDEX OF THE NON-NUMERIC VALUE
        #=====================================================
        if self.node_int_id_generator:
            self.node_id_lookup = list(self.node_int_id_generator)

        if self.metadata:
            #output_cx.append(self.generateAspect('metaData'))
            output_cx.append(self.generateMetadataAspect())
        if self.nodes:
            output_cx.append(self.generateAspect('nodes'))
        if self.edges:
            output_cx.append(self.generateAspect('edges'))
        if self.networkAttributes:
            output_cx.append(self.generateAspect('networkAttributes'))
        if self.nodeAttributes:
            output_cx.append(self.generateAspect('nodeAttributes'))
        if self.edgeAttributes:
            output_cx.append(self.generateAspect('edgeAttributes'))
        if self.citations:
            output_cx.append(self.generateAspect('citations'))
        if self.nodeCitations:
            output_cx.append(self.generateAspect('nodeCitations'))
        if self.edgeCitations:
            output_cx.append(self.generateAspect('edgeCitations'))
        if self.supports:
            output_cx.append(self.generateAspect('supports'))
        if self.edgeSupports:
            output_cx.append(self.generateAspect('edgeSupports'))
        if self.nodeSupports:
            output_cx.append(self.generateAspect('nodeSupports'))
        if self.opaqueAspects:
            for oa in self.opaqueAspects:
                output_cx.append({oa: self.opaqueAspects[oa]})
        if self.metadata:
            #===========================
            # UPDATE CONSISTENCY GROUP
            #===========================
            #self.updateConsistencyGroup()
            mt_a = self.generateMetadataAspect()

            #output_cx.append(self.generateAspect('metaData'))
            output_cx.append(self.generateMetadataAspect())

        #print json.dumps(output_cx)

        return output_cx

    def generateAspect(self, aspect_name):
        core_aspect = ['nodes', 'edges','networkAttributes', 'nodeAttributes', 'edgeAttributes', 'citations', 'metaData', 'supports']
        aspect_element_array = []
        element_count = 0
        element_id_max = 0

        use_this_aspect = None
        #=============================
        # PROCESS CORE ASPECTS FIRST
        #=============================
        if aspect_name in core_aspect:
            use_this_aspect = self.string_to_aspect_object(aspect_name)

        if use_this_aspect is not None:
            if type(use_this_aspect) is list:
                for item in use_this_aspect:
                    add_this_element = item.to_json()
                    id = add_this_element.get(CX_CONSTANTS.ID)
                    if id is not None and id > element_id_max:
                        element_id_max = id
                    aspect_element_array.append(add_this_element)
                    element_count +=1
            else:
                items = None
                if sys.version_info.major == 3:
                    items = use_this_aspect.items()
                else:
                    items = use_this_aspect.iteritems()

                for k, v in items:
                    if type(v) is list:
                        for v_item in v:
                            add_this_element = v_item.to_json()
                            id = add_this_element.get(CX_CONSTANTS.ID)
                            if id is not None and id > element_id_max:
                                element_id_max = id

                            if aspect_name == 'nodeAttributes':
                                if self.node_id_lookup:
                                    po_id = self.node_id_lookup.index(add_this_element.get(CX_CONSTANTS.PROPERTY_OF))
                                    add_this_element[CX_CONSTANTS.PROPERTY_OF] = po_id

                            aspect_element_array.append(add_this_element)
                            element_count +=1
                    else:
                        add_this_element = v.to_json()
                        id = add_this_element.get(CX_CONSTANTS.ID)
                        if aspect_name == 'nodes' and type(id) is str:
                            # CONVERT TO INT
                            id = self.node_id_lookup.index(id)
                            add_this_element[CX_CONSTANTS.ID] = id
                        if aspect_name == 'edges' and type(add_this_element.get(CX_CONSTANTS.EDGE_SOURCE_NODE_ID_OR_SUBNETWORK)) is str:
                            s_id = self.node_id_lookup.index(add_this_element.get(CX_CONSTANTS.EDGE_SOURCE_NODE_ID_OR_SUBNETWORK))
                            add_this_element[CX_CONSTANTS.EDGE_SOURCE_NODE_ID_OR_SUBNETWORK] = s_id

                        if aspect_name == 'edges' and type(add_this_element.get(CX_CONSTANTS.EDGE_TARGET_NODE_ID)) is str:
                            t_id = self.node_id_lookup.index(add_this_element.get(CX_CONSTANTS.EDGE_TARGET_NODE_ID))
                            add_this_element[CX_CONSTANTS.EDGE_TARGET_NODE_ID] = t_id

                        if id is not None and id > element_id_max:
                            element_id_max = id
                        aspect_element_array.append(add_this_element)
                        element_count +=1
        else:
            #===========================
            # PROCESS NON-CORE ASPECTS
            #===========================
            use_this_aspect = self.string_to_aspect_object(aspect_name)

            if use_this_aspect is not None:
                if type(use_this_aspect) is dict:
                    items = None
                    if sys.version_info.major == 3:
                        items = use_this_aspect.items()
                    else:
                        items = use_this_aspect.iteritems()

                    for k, v in items:
                        if aspect_name == 'edgeSupports':
                            if type(v) is list:
                                aspect_element_array.append({CX_CONSTANTS.PROPERTY_OF: [k], CX_CONSTANTS.SUPPORTS: v})
                            else:
                                aspect_element_array.append({CX_CONSTANTS.PROPERTY_OF: [k], CX_CONSTANTS.SUPPORTS: [v]})
                        else:
                            if type(v) is list:
                                aspect_element_array.append({CX_CONSTANTS.PROPERTY_OF: [k], CX_CONSTANTS.CITATIONS: v})
                            else:
                                aspect_element_array.append({CX_CONSTANTS.PROPERTY_OF: [k], CX_CONSTANTS.CITATIONS: [v]})
                        element_count +=1
                else:
                    raise Exception('Citation was not in json format')
            else:
                return None

        aspect = {aspect_name: aspect_element_array}
        #============================================
        # UPDATE METADATA ELEMENT COUNTS/ID COUNTER
        #============================================
        md = self.metadata.get(aspect_name)
        if md is not None:
            md.setElementCount(element_count)
            md.setIdCounter(element_id_max)
            #md.incrementConsistencyGroup()
        elif aspect_name != 'metaData':
            mde = MetaDataElement(elementCount=element_count, properties=[], version='1.0', consistencyGroup=1, name=aspect_name)

            if element_id_max != 0:
                mde.setIdCounter(element_id_max)

            self.addMetadata(mde)

        #print('%s ELEMENT COUNT: %s, MAX ID: %s' % (aspect_name, str(element_count), str(element_id_max)))
        return aspect

    def generateMetadataAspect(self):
        aspect_element_array = []
        element_count = 0
        element_id_max = 0

        use_this_aspect = self.string_to_aspect_object('metaData')

        if use_this_aspect is not None:
            if sys.version_info.major == 3:
                items = use_this_aspect.items()
            else:
                items = use_this_aspect.iteritems()

            for k, v in items:
                add_this_element = v.to_json()
                id = add_this_element.get(CX_CONSTANTS.ID)

                if id is not None and id > element_id_max:
                    element_id_max = id
                aspect_element_array.append(add_this_element)
                element_count +=1

        aspect = {'metaData': aspect_element_array}

        return aspect

    def handleMetadataUpdate(self, aspect_name):
        aspect = self.string_to_aspect_object(aspect_name)

        #return_metadata = {
        #    CX_CONSTANTS.CONSISTENCY_GROUP: consistency_group,
        #    CX_CONSTANTS.ELEMENT_COUNT: 1,
        #    CX_CONSTANTS.METADATA_NAME: "@context",
        #    CX_CONSTANTS.PROPERTIES: [],
        #    CX_CONSTANTS.VERSION: "1.0"
        #}

    def updateConsistencyGroup(self):
        consistency_group = 1
        if self.metadata:
            for mi_k, mi_v in self.metadata.items():
                cg = mi_v.getConsistencyGroup()
                if cg > consistency_group:
                    consistency_group = cg

            consistency_group += 1 # bump the consistency group up by one

            for mi_k, mi_v in self.metadata.items():
                #print mi_k
                #print mi_v
                mi_v.setConsistencyGroup(consistency_group)

    def generate_metadata(self, G, unclassified_cx):
        #if self.metadata:
        #    for k, v in self.metadata.iteritems():


        return_metadata = []
        consistency_group = 1
        if(self.metadata_original is not None):
            for mi in self.metadata_original:
                if(mi.get("consistencyGroup") is not None):
                    if(mi.get("consistencyGroup") > consistency_group):
                        consistency_group = mi.get("consistencyGroup")
                else:
                    mi['consistencyGroup'] = 0

            consistency_group += 1 # bump the consistency group up by one

            #print("consistency group max: " + str(consistency_group))

        # ========================
        # @context metadata
        # ========================
        if self.namespaces:
            return_metadata.append(
                {
                    "consistencyGroup": consistency_group,
                    "elementCount": 1,
                    "name": "@context",
                    "properties": [],
                    "version": "1.0"
                }
            )

        #========================
        # Nodes metadata
        #========================
        node_ids = [n[0] for n in G.nodes_iter(data=True)]
        if(len(node_ids) < 1):
            node_ids = [0]
        return_metadata.append(
            {
                "consistencyGroup" : consistency_group,
                "elementCount" : len(node_ids),
                "idCounter": max(node_ids),
                "name" : "nodes",
                "properties" : [ ],
                "version" : "1.0"
            }
        )

        #========================
        # Edges metadata
        #========================
        edge_ids = [e[2]for e in G.edges_iter(data=True, keys=True)]
        if(len(edge_ids) < 1):
            edge_ids = [0]
        return_metadata.append(
            {
                "consistencyGroup" : consistency_group,
                "elementCount" : len(edge_ids),
                "idCounter": max(edge_ids),
                "name" : "edges",
                "properties" : [ ],
                "version" : "1.0"
            }
        )

        #=============================
        # Network Attributes metadata
        #=============================
        if(len(G.graph) > 0):
            return_metadata.append(
                {
                    "consistencyGroup" : consistency_group,
                    "elementCount" : len(G.graph),
                    "name" : "networkAttributes",
                    "properties" : [ ],
                    "version" : "1.0"
                }
            )

        #===========================
        # Node Attributes metadata
        #===========================
        #id_max = 0
        attr_count = 0
        for node_id , attributes in G.nodes_iter(data=True):
            for attribute_name in attributes:
                if attribute_name != "name" and attribute_name != "represents":
                    attr_count += 1



        #
        # for n, nattr in G.nodes(data=True):
        #     if(bool(nattr)):
        #         attr_count += len(nattr.keys())
        #
        #     if(n > id_max):
        #         id_max = n

        if(attr_count > 0):
            return_metadata.append(
                {
                    "consistencyGroup" : consistency_group,
                    "elementCount" : attr_count,
                    #"idCounter": id_max,
                    "name" : "nodeAttributes",
                    "properties" : [ ],
                    "version" : "1.0"
                }
            )

        #===========================
        # Edge Attributes metadata
        #===========================
        #id_max = 0
        attr_count = 0
        for s, t, id, a in G.edges(data=True, keys=True):
            if(bool(a)):
                for attribute_name in a:
                    if attribute_name != "interaction":
                        attr_count += 1
                #attr_count += len(a.keys())

            # if(id > id_max):
            #     id_max = id

        if(attr_count > 0):
            return_metadata.append(
                {
                    "consistencyGroup" : consistency_group,
                    "elementCount" : attr_count,
                    #"idCounter": id_max,
                    "name" : "edgeAttributes",
                    "properties" : [ ],
                    "version" : "1.0"
                }
            )

        #===========================
        # cyViews metadata
        #===========================
        if self.view_id != None:
            return_metadata.append(
                {
                    "elementCount": 1,
                    "name": "cyViews",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )

        #===========================
        # subNetworks metadata
        #===========================
        if self.subnetwork_id != None:
            return_metadata.append(
                {
                    "elementCount": 1,
                    "name": "subNetworks",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )

        #===========================
        # networkRelations metadata
        #===========================
        if self.subnetwork_id != None and self.view_id != None:
            return_metadata.append(
                {
                    "elementCount": 2,
                    "name": "networkRelations",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )

        #===========================
        # citations and supports metadata
        #===========================
        if len(self.support_map) > 0:
            return_metadata.append(
                {
                    "elementCount": len(self.support_map),
                    "name": "supports",
                    "properties": [],
                    "idCounter": max(self.support_map.keys()),
                    "consistencyGroup" : consistency_group
                }
            )

        if len(self.node_support_map) > 0:
            return_metadata.append(
                {
                    "elementCount": len(self.node_support_map),
                    "name": "nodeSupports",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )
        if len(self.edge_support_map) > 0:
            return_metadata.append(
                {
                    "elementCount": len(self.edge_support_map),
                    "name": "edgeSupports",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )

        if len(self.citation_map) > 0:
            return_metadata.append(
                {
                    "elementCount": len(self.citation_map),
                    "name": "citations",
                    "properties": [],
                    "idCounter": max(self.citation_map.keys()),
                    "consistencyGroup" : consistency_group
                }
            )

        if len(self.node_citation_map) > 0:
            return_metadata.append(
                {
                    "elementCount": len(self.node_citation_map),
                    "name": "nodeCitations",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )

        if len(self.edge_citation_map) > 0:
            return_metadata.append(
                {
                    "elementCount": len(self.edge_citation_map),
                    "name": "edgeCitations",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )

        if len(self.function_term_map) > 0:
            return_metadata.append(
                {
                    "elementCount": len(self.function_term_map),
                    "name": "functionTerms",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )

        if len(self.reified_edges) > 0:
            return_metadata.append(
                {
                    "elementCount": len(self.reified_edges),
                    "name": "reifiedEdges",
                    "properties": [],
                    "consistencyGroup" : consistency_group
                }
            )

        #===========================
        # ndexStatus metadata
        #===========================
        return_metadata.append(
            {
                "consistencyGroup": consistency_group,
                "elementCount": 1,
                "name": "ndexStatus",
                "properties": [],
                "version": "1.0"
            }
        )

        #===========================
        # cartesianLayout metadata
        #===========================
        if self.pos and len(self.pos) > 0:
            return_metadata.append(
                {
                    "consistencyGroup": consistency_group,
                    "elementCount": len(self.pos),
                    "name": "cartesianLayout",
                    "properties": [],
                    "version": "1.0"
                }
            )

        #===========================
        # OTHER metadata
        #===========================
        for asp in self.unclassified_cx:
            try:
                aspect_type = asp.iterkeys().next()
                if(aspect_type == "visualProperties"
                   or aspect_type == "cyVisualProperties"
                   or aspect_type == "@context"):
                    return_metadata.append(
                        {
                            "consistencyGroup" : consistency_group,
                            "elementCount":len(asp[aspect_type]),
                            "name":aspect_type,
                            "properties":[]
                         }
                    )
            except Exception as e:
                print(e.message)


        #print {'metaData': return_metadata}

        return [{'metaData': return_metadata}]

    def string_to_aspect_object(self, aspect_name):
        if aspect_name == 'metaData':
            return self.metadata
        elif aspect_name == 'nodes':
            return self.nodes
        elif aspect_name == 'edges':
            return self.edges
        elif aspect_name == 'networkAttributes':
            return self.networkAttributes
        elif aspect_name == 'nodeAttributes':
            return self.nodeAttributes
        elif aspect_name == 'edgeAttributes':
            return self.edgeAttributes
        elif aspect_name == 'citations':
            return self.citations
        elif aspect_name == 'nodeCitations':
            return self.nodeCitations
        elif aspect_name == 'edgeCitations':
            return self.edgeCitations
        elif aspect_name == 'edgeSupports':
            return self.edgeSupports
        elif aspect_name == 'supports':
            return self.supports

    def streamAspect(self, uuid, aspect_name, server, username, password):
        if 'http' not in server:
            server = 'http://' + server
        if aspect_name == 'metaData':
            print(server + '/v2/network/' + uuid + '/aspect')

            s = requests.session()
            if username and password:
                # add credentials to the session, if available
                s.auth = (username, password)
            md_response = s.get(server + '/v2/network/' + uuid + '/aspect')
            json_response = md_response.json()
            return json_response.get('metaData')
        else:
            if username and password:
                base64string = base64.b64encode('%s:%s' % (username, password))
                request = Request(server + '/v2/network/' + uuid + '/aspect/' + aspect_name, headers={"Authorization": "Basic " + base64.encodestring(username + ':' + password).replace('\n', '')})
            else:
                request = Request(server + '/v2/network/' + uuid + '/aspect/' + aspect_name)
            try:
                urlopen_result = urlopen(request) #'http://dev2.ndexbio.org/v2/network/' + uuid + '/aspect/' + aspect_name)
            except HTTPError as e:
                print(e.code)
                return []
            except URLError as e:
                print('Other error')
                print('URL Error %s' % e.message())
                return []

            return ijson.items(urlopen_result, 'item')

class DecimalEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if sys.version_info.major == 3:
            if isinstance(o, np.int64):
                return int(o)
        return super(DecimalEncoder, self).default(o)
