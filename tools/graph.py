# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 16:58
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : graph.py
# @Software: PyCharm

class Edge(object):
    def __init__(self, start, end, weight):
        self.startNodeId = start
        self.endNodeId = end
        self.weight = weight

class Node(object):
    def __init__(self, nodeId, edgeList):
        self.nodeId = nodeId
        self.edgeList = edgeList

class Path(object):
    def __init__(self, curNodeId):
        self.visited = False
        self.weight = 8888
        self.curNodeId = curNodeId
        self.routeList = []

class Graph(object):
    def __init__(self, nodeList):
        self.nodeList = nodeList
        self.pathDic = {}

    def initPaths(self, originNodeId):
        self.pathDic = {}
        originNode = None
        for node in self.nodeList:
            if node.nodeId == originNodeId:
                originNode = node
            self.pathDic[node.nodeId] = Path(node.nodeId)

        if originNode is None:
            print("originNode is none")
            return
        else:
            for edge in originNode.edgeList:
                path = self.pathDic[edge.endNodeId]
                if path is None:
                    print("path is None")
                    return
                else:
                    path.weight = edge.weight
                    path.routeList.append(originNodeId)

        path = self.pathDic[originNodeId]
        path.weight = 0
        path.visit = True
        path.routeList.append(originNodeId)

    def getMinPath(self, originNodeId):
        destNode = None
        weight = 8888
        for node in self.nodeList:
            path = self.pathDic[node.nodeId]
            if path.visited == False and path.weight < weight:
                weight = path.weight
                destNode = node
        return destNode

    def dijkstra(self, originNodeId, destNodeId):
        self.initPaths(originNodeId)
        curNode = self.getMinPath(originNodeId)
        while curNode is not None:
            curPath = self.pathDic[curNode.nodeId]
            curPath.visited = True

            for edge in curNode.edgeList:
                minPath = self.pathDic[edge.endNodeId]
                if minPath.weight > (curPath.weight + edge.weight):
                    minPath.weight = curPath.weight + edge.weight
                    minPath.routeList = curPath.routeList + [curNode.nodeId]

            curNode = self.getMinPath(originNodeId)

        route = self.pathDic[destNodeId].routeList
        if route == []:
            return route
        else:
            return route + [destNodeId]

edge11 = Edge("A", "B", 1)
edge12 = Edge("A", "C", 1)
edge13 = Edge("A", "E", 1)

edge21 = Edge("B", "C", 1)
edge22 = Edge("B", "E", 1)

edge31 = Edge("C", "D", 1)

edge51 = Edge("E", "D", 1)

node1 = Node("A", [edge11, edge12, edge13])
node2 = Node("B", [edge21, edge22])
node3 = Node("C", [edge31])
node4 = Node("D", [])
node5 = Node("E", [edge51])

graph = Graph([node1, node2, node3, node4, node5])

startNodeId = "A"
endNodeId = "D"

print("最短路径:", graph.dijkstra(startNodeId, endNodeId))

