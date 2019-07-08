from config import *
import json
from rec import rec


ROOT_NODE = '/'


class KGNode:
    def __init__(self, title):
        self.title = title
        self.children = []

    def add(self, node):
        self.children.append(node)
        node.parent = self


def dfs(json_array, parent, mapping):
    for title_obj in json_array:
        node = None
        if type(title_obj) is str:
            node = KGNode(title_obj)
            mapping[title_obj] = node
        elif type(title_obj) is dict:
            for title_name in title_obj.keys():
                node = KGNode(title_name)
                mapping[title_name] = node
                sub_obj = title_obj[title_name]
                if 'alias' in sub_obj:
                    for alias in sub_obj['alias']:
                        mapping[alias] = node
                if 'children' in sub_obj:
                    dfs(sub_obj['children'], node, mapping)
        parent.add(node)


class KnowledgeGraph:
    def __init__(self, data_path=KG_PATH):
        with rec('KnowledgeGraph initiation'):
            self.root = KGNode(ROOT_NODE)
            self.mapping = {}
            with open(data_path) as f:
                json_str = f.read()
                json_str = json_str.replace('\n', '')
                json_str = json_str.replace(' ', '')

            json_obj = json.loads(json_str)

            dfs(json_obj, self.root, self.mapping)

    def lca(self, title1, title2):
        if title1 not in self.mapping:
            print('Unknown title: ', title1)
            return ROOT_NODE
        if title2 not in self.mapping:
            print('Unknown title: ', title2)
            return ROOT_NODE
        if title1 == title2:
            return title1
        node1 = self.mapping[title1]
        node2 = self.mapping[title2]
        parents1 = []
        while node1.title != ROOT_NODE:
            parents1.append(node1.title)
            node1 = node1.parent
        parents2 = []
        while node2.title != ROOT_NODE:
            parents2.append(node2.title)
            node2 = node2.parent
        ptr1 = len(parents1) - 1
        ptr2 = len(parents2) - 1
        lca = ROOT_NODE
        while ptr1 >= 0 and ptr2 >= 0 and parents1[ptr1] == parents2[ptr2]:
            lca = parents1[ptr1]
            ptr1 -= 1
            ptr2 -= 1
        return lca

    def same_cls(self, title1, title2):
        return self.lca(title1, title2) != ROOT_NODE


if __name__ == '__main__':
    kg = KnowledgeGraph('/Users/wangchenghao1103/Desktop/kg_title_v12.json')
    while True:
        s = input('>> ')
        print(kg.lca(*(s.split())))
