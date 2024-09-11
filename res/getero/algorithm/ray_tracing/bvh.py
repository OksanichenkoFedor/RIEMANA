from numba import njit
import numpy as np

from res.getero.algorithm.dynamic_profile import give_start


#@njit()
def give_edges(border_layer_arr):
    x_start, y_start = give_start(border_layer_arr)
    curr_x, curr_y = x_start, y_start
    num_edges = 0
    while border_layer_arr[curr_x, curr_y, 3] != -1 or border_layer_arr[curr_x, curr_y, 4] != -1:
        num_edges += 1
        curr_x, curr_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    Edges = np.zeros((num_edges, 6))
    # строим массив из ячеек будет 6 точек (x1, x2, y1, y2, xm, ym)
    # print(num_edges1, num_edges)
    curr_x, curr_y = x_start, y_start
    for i in range(num_edges):
        Edges[i, 0], Edges[i, 1] = curr_x, border_layer_arr[curr_x, curr_y, 3]
        Edges[i, 2], Edges[i, 3] = curr_y, border_layer_arr[curr_x, curr_y, 4]
        curr_x, curr_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    Edges[:, 4] = 0.5 * (Edges[:, 0] + Edges[:, 1])
    Edges[:, 5] = 0.5 * (Edges[:, 2] + Edges[:, 3])
    return Edges


@njit()
def build_node_list():
    pass


#@njit()
def build_BVH(border_layer_arr):
    Edges = give_edges(border_layer_arr)
    NodeList = np.zeros((Edges.shape[0]*2-1, 7))
    # массив, описывающий дерево, каждый содержит:
    # (is_fin_node (0,1); child_1, child_2, x_left, x_right, y_left, y_right)
    left_index = 0
    right_index = Edges.shape[0]
    n_nodes = 0
    end_node = build_node(Edges, NodeList, left_index, right_index, n_nodes)
    print(end_node)
    print("---")
    return NodeList


#@njit()
def build_node(curr_edges, NodeList, left_index, right_index, curr_node):
    #print("Start: ",left_index, right_index," size: ",curr_edges.shape[0])#, curr_edges)

    curr_edge = curr_edges[left_index:right_index]
    if right_index-left_index>1:
        left_x, right_x = np.min(curr_edge[:, :2]), np.max(curr_edge[:, :2])
        up_y, down_y = np.min(curr_edge[:, 2:4]), np.max(curr_edge[:, 2:4])

        delta_x = right_x - left_x
        delta_y = down_y - up_y
        do_split_x = delta_x > delta_y
        if delta_x > delta_y:
            #print("do_split_x")
            curr_edge = curr_edge[curr_edge[:, 4].argsort()]
            split_coord = 0.5 * (np.max(curr_edge[:, :2]) + np.min(curr_edge[:, :2]))
        else:

            curr_edge = curr_edge[curr_edge[:, 5].argsort()]
            split_coord = 0.5 * (np.max(curr_edge[:, 2:4]) + np.min(curr_edge[:, 2:4]))

        split_index = find_split_index(curr_edge, do_split_x, split_coord)+left_index

        curr_edges[left_index:right_index] = curr_edge

        node_left = build_node(curr_edges, NodeList, left_index, split_index, curr_node+1)
        node_right = build_node(curr_edges, NodeList, split_index, right_index, node_left+1)
        end_node = node_right
        NodeList[curr_node, 0] = 0 #это не конечный номер
        NodeList[curr_node, 1], NodeList[curr_node, 2] = curr_node+1, node_left+1 #заполнили детей
        NodeList[curr_node, 3], NodeList[curr_node, 4] = left_x, right_x
        NodeList[curr_node, 5], NodeList[curr_node, 6] = up_y, down_y

    else:
        #print("fin_node")
        end_node = curr_node
        NodeList[curr_node, 0] = 1  # это конечный номер
        NodeList[curr_node, 1], NodeList[curr_node, 2] = -1, -1  # детей нет
        NodeList[curr_node, 3], NodeList[curr_node, 4] = curr_edge[0,0], curr_edge[0,1]
        NodeList[curr_node, 5], NodeList[curr_node, 6] = curr_edge[0,2], curr_edge[0,3]
        #остался один элемент

    #возвращаем последний заполненный номер
    return end_node

#@njit()
def find_split_index(curr_edges, do_split_x, split_coord):
    ind = 5
    if do_split_x:
        ind = 4
    left_ind = 0
    right_ind = curr_edges.shape[0]-1
    curr_ind = right_ind - int(0.5*(right_ind-left_ind))
    while right_ind-left_ind>1:
        if curr_edges[curr_ind,ind]>=split_coord:
            right_ind = curr_ind
            curr_ind = right_ind - int(0.5*(right_ind-left_ind))
        else:
            left_ind = curr_ind
            curr_ind = right_ind - int(0.5*(right_ind-left_ind))
    return curr_ind

def bvh_count_collision_point(border_layer_arr, x_ray, y_ray, curr_angle, start_segm_x, start_segm_y):
    pass






