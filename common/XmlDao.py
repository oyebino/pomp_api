#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/15 10:49
# @Author  : 叶永彬
# @File    : XmlDao.py

from xml.etree.ElementTree import ElementTree,Element
import xml.dom.minidom as Dom
import os

class XmlDao():

    @staticmethod
    def openXml(filename):
        tree = ElementTree()
        tree.parse(filename)
        return tree

    @staticmethod
    def createXml(keyName,value,outPathFile):
        doc = Dom.Document()
        root_node = doc.createElement("root")
        doc.appendChild(root_node)
        case_node = doc.createElement("caseData")
        case_node.setAttribute("name", keyName)
        case_node.setAttribute("value", value)
        root_node.appendChild(case_node)
        f = open(outPathFile, 'w', encoding='utf8')
        doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()

    @staticmethod
    def saveAs(tree,outfile):
        tree.write(outfile, encoding="utf-8",xml_declaration=True)

    @staticmethod
    def add_child_node(nodelist, element):
        '''给一个节点添加子节点
           nodelist: 节点列表
           element: 子节点'''
        print(len(nodelist))
        print(element)
        for node in nodelist:
            node.append(element)

    @staticmethod
    def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
        '''同过属性及属性值定位一个节点，并删除之
           nodelist: 父节点列表
           tag:子节点标签
           kv_map: 属性及属性值列表'''
        for parent_node in nodelist:
            children = parent_node.getchildren()
            for child in children:
                if child.tag == tag and XmlDao.if_match(child, kv_map):
                    parent_node.remove(child)
    @staticmethod
    def create_node(tag, property_map, content=''):
        '''新造一个节点
           tag:节点标签
           property_map:属性及属性值map
           content: 节点闭合标签里的文本内容
           return 新节点'''
        element = Element(tag, property_map)
        element.text = content
        return element
    @staticmethod
    def change_node_text(nodelist, text, is_add=False, is_delete=False):
        '''改变/增加/删除一个节点的文本
           nodelist:节点列表
           text : 更新后的文本'''
        for node in nodelist:
            if is_add:
                node.text += text
            elif is_delete:
                node.text = ""
            else:
                node.text = text
    @staticmethod
    def change_node_properties(nodelist, kv_map, is_delete=False):
        '''修改/增加 /删除 节点的属性及属性值
           nodelist: 节点列表
           kv_map:属性及属性值map'''
        for node in nodelist:
            for key in kv_map:
                if is_delete:
                    if key in node.attrib:
                        del node.attrib[key]
                else:
                    node.set(key, kv_map.get(key))
    @staticmethod
    def get_node_by_keyvalue(nodelist, kv_map):
        '''根据属性及属性值定位符合的节点，返回节点
           nodelist: 节点列表
           kv_map: 匹配属性及属性值map'''
        result_nodes = []
        for node in nodelist:
            if XmlDao.if_match(node, kv_map):
                result_nodes.append(node)
        return result_nodes
    @staticmethod
    def find_nodes(tree, path):
        '''查找某个路径匹配的所有节点
           tree: xml树
           path: 节点路径'''
        # print(tree.findall(path))
        return tree.findall(path)
    @staticmethod
    def if_match(node, kv_map):
        '''判断某个节点是否包含所有传入参数属性
           node: 节点
           kv_map: 属性及属性值组成的map'''
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True

if __name__ == "__main__":
    XmlDao.openXml("../test_data/commonData.xml")
    pass