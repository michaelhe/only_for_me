#!/usr/bin/python

# -*- coding=utf-8 -*-
# author : michalemche
# date : 2014-07-03
# version : 0.1


from xml.etree.ElementTree import ElementTree,Element  
  
def read_xml(in_path):  
    '''
       in_path: xml path
       return: ElementTree
    '''  
    tree = ElementTree()  
    tree.parse(in_path)  
    return tree

def write_xml(tree, out_path):  
    ''' 
       tree: xml tree
       out_path: output file '''  
    tree.write(out_path, encoding="utf-8",xml_declaration=False)  
  
def if_match(node, kv_map):  
    ''' 
       node: the node of tree 
       kv_map: key value '''  
    for key in kv_map:  
        if node.get(key) != kv_map.get(key):  
            return False  
    return True  
  
#---------------search -----  
  
def find_nodes(tree, path):  
    return tree.findall(path)  
  
  
def get_node_by_keyvalue(nodelist, kv_map):  
    result_nodes = []  
    for node in nodelist:  
        if if_match(node, kv_map):  
            result_nodes.append(node)  
    return result_nodes  
  
#---------------change -----  
  
def change_node_properties(nodelist, kv_map, is_delete=False):  
    '''
       modified/add/delete node attr and value
       nodelist: the list of select node
       kv_map: a dict of key value
    '''
    for node in nodelist:  
        for key in kv_map:  
            if is_delete:   
                if key in node.attrib:  
                    del node.attrib[key]  
            else:  
                node.set(key, kv_map.get(key))  
              
def change_node_text(nodelist, text, is_add=False, is_delete=False):  
    '''
       modified/add/delete node text 
       nodelist: the list of select node
       text: text
    '''
    for node in nodelist:  
        if is_add:  
            node.text += text  
        elif is_delete:  
            node.text = ""  
        else:  
            node.text = text  
              
def create_node(tag, property_map, content):  
    '''
       tag : node tag
       property_map : key value dict
       content : text
       return : element
       eg: <world id="1" attr="attr value"> world text </world>
    '''
    element = Element(tag, property_map)  
    element.text = content  
    return element  
          
def add_child_node(nodelist, element):  
    '''  
       nodelist: list of node
       element: element
    '''  
    for node in nodelist:  
        node.append(element)  
          
def del_node_by_tagkeyvalue(nodelist, tag, kv_map):  
    '''
      delete a node by tag and key value
      nodelist: the list need to remove
      tag : the tag of children node
      kv_map : the dict of key and value
    '''
    for parent_node in nodelist:  
        children = parent_node.getchildren()  
        for child in children:  
            if child.tag == tag and if_match(child, kv_map):  
                parent_node.remove(child)  

def indent(elem, level=0):
    '''
       format pretty xml
    '''
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem
