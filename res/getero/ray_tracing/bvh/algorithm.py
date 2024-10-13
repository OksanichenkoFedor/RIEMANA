from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

from res.getero.algorithm.dynamic_profile import give_start
from res.getero.ray_tracing.bvh.collision_functions import check_rect_collision
from res.getero.ray_tracing.utils import check_collision


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def give_edges(border_layer_arr, is_half):
    x_start, y_start = give_start(border_layer_arr)
    curr_x, curr_y = x_start, y_start
    num_edges = 0
    while border_layer_arr[curr_x, curr_y, 3] != -1 or border_layer_arr[curr_x, curr_y, 4] != -1:
        num_edges += 1
        curr_x, curr_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    if is_half:
        Edges = np.zeros((num_edges+3, 6))
    else:
        Edges = np.zeros((num_edges+2, 6))
    # строим массив из ячеек будет 6 точек (x1, x2, y1, y2, xm, ym)
    # print(num_edges1, num_edges)
    curr_x, curr_y = x_start, y_start
    Edges[0, 0], Edges[0, 1] = curr_x-0.5, curr_x
    Edges[0, 2], Edges[0, 3] = curr_y, curr_y

    for i in range(1, num_edges+1):
        Edges[i, 0], Edges[i, 1] = curr_x, border_layer_arr[curr_x, curr_y, 3]
        Edges[i, 2], Edges[i, 3] = curr_y, border_layer_arr[curr_x, curr_y, 4]
        curr_x, curr_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    #print("bvh: ",curr_x, curr_y, border_layer_arr[curr_x, curr_y])
    Edges[num_edges + 1, 0], Edges[num_edges + 1, 1] = curr_x, curr_x + 0.5
    Edges[num_edges + 1, 2], Edges[num_edges + 1, 3] = curr_y, curr_y

    if is_half:
        Edges[num_edges + 2, 0], Edges[num_edges + 2, 1] = curr_x + 0.5, curr_x + 0.5
        Edges[num_edges + 2, 2], Edges[num_edges + 2, 3] = curr_y, 0

    Edges[:, 4] = 0.5 * (Edges[:, 0] + Edges[:, 1])
    Edges[:, 5] = 0.5 * (Edges[:, 2] + Edges[:, 3])
    return Edges


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def build_node_list():
    pass


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def build_BVH(border_layer_arr, is_half):
    Edges = give_edges(border_layer_arr, is_half)
    NodeList = np.zeros((Edges.shape[0]*2-1, 7))
    # массив, описывающий дерево, каждый содержит:
    # (is_fin_node (0,1); child_1, child_2, x_left, x_right, y_left, y_right)
    left_index = 0
    right_index = Edges.shape[0]
    n_nodes = 0
    end_node = build_node(Edges, NodeList, left_index, right_index, n_nodes)
    #print(end_node)
    #print("---")
    return NodeList




@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
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

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
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

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def bvh_count_collision_point(NodeList, ray_vec, curr_angle, start_segment):
    #print("---")

    found, cross_vec, norm_angle, new_segment, num = check_one_node(NodeList, 0, ray_vec, curr_angle, start_segment)
    #   print(num, int(0.5*(NodeList.shape[0]+1.0)))
    return found, cross_vec, norm_angle, new_segment, num
@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def check_one_node(NodeList, curr_node, ray_vec, curr_angle, start_segment):
    if NodeList[curr_node,0]==0:
        # это не конечный номер
        left_x, right_x = NodeList[curr_node, 3], NodeList[curr_node, 4]
        up_y, down_y = NodeList[curr_node, 5], NodeList[curr_node, 6]
        #print("not end_num: ", left_x, right_x, up_y, down_y)
        is_collide = check_rect_collision(ray_vec,curr_angle,left_x+0.5,right_x+0.5,up_y+0.5,down_y+0.5)
        #print("not end_num: ", left_x, right_x, up_y, down_y, is_collide)
        if is_collide:
            found1, cross_vec1, norm_angle1, new_segment1, num_1 = check_one_node(NodeList, int(NodeList[curr_node, 1]), ray_vec, curr_angle, start_segment)
            found2, cross_vec2, norm_angle2, new_segment2, num_2 = check_one_node(NodeList, int(NodeList[curr_node, 2]), ray_vec, curr_angle, start_segment)

            if found1 and found2:
                # проверяем на расстояние
                dist1 = np.sum((cross_vec1 - ray_vec) * (cross_vec1 - ray_vec))
                dist2 = np.sum((cross_vec2 - ray_vec) * (cross_vec2 - ray_vec))
                if dist1<dist2:
                    return True, cross_vec1, norm_angle1, new_segment1, num_1+num_2
                else:
                    return True, cross_vec2, norm_angle2, new_segment2, num_1+num_2
            # если только один нашёлся
            if found1:
                return True, cross_vec1, norm_angle1, new_segment1, num_1+num_2
            if found2:
                return True, cross_vec2, norm_angle2, new_segment2, num_1+num_2
            # пересечения нет вообще
            return False, np.ones(2), 0.0, np.ones((2, 2))*(-1.0), num_1+num_2
        return False, np.ones(2), 0.0, np.ones((2, 2))*(-1.0), 0
    else:
        # мы пришли к конечному номеру

        x_start, x_end = NodeList[curr_node,3], NodeList[curr_node,4]
        y_start, y_end = NodeList[curr_node,5], NodeList[curr_node,6]

        curr_segment = np.zeros((2, 2))
        curr_segment[0, 0], curr_segment[0, 1] = x_start + 0.5, y_start + 0.5
        curr_segment[1, 0], curr_segment[1, 1] = x_end + 0.5, y_end + 0.5

        is_cross, cross_vec, norm_angle = check_collision(ray_vec, curr_angle, curr_segment)
        #print("end_num: ", x_start, x_end, y_start, y_end, is_cross)

        if is_cross and np.sum(np.abs(start_segment-curr_segment))>0:
            return True, cross_vec, norm_angle, curr_segment, 1
        else:
            return False, np.ones(2), 0.0, np.ones((2, 2))*(-1.0), 0