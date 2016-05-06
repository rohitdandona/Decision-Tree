'''
Function to test decision tree with test data set
'''
def compute_accuracy(test_instances,root_node,class_label_index):
    test_class_answers =[]
    count = 0
    for value in test_instances:
        node = root_node
        while node.best_split_threshold!=0:

            if float(value[node.attribute_index])<=node.best_split_threshold:
                node = node.children[0]
            else:
                node = node.children[1]
        test_class_answers.append(node.split_attribute)

    for j in range(0,len(test_instances)):
        if test_class_answers[j] == test_instances[j][class_label_index]:
            count = count + 1
    accuracy = (count/len(test_instances))*100
    return(accuracy)

def compute_pessimistic_error(instances, left_split_instances, right_split_instances, class_label_index):

    # Calculating dominant class label for parent
    parent_class_list = []
    for value1 in instances:
        parent_class_list.append(value1[class_label_index])
    distinct_parent_class_list = list(set(parent_class_list))
    parent_dict = {}
    for item in parent_class_list:
        for class_type in distinct_parent_class_list:
            if item == class_type:
                if class_type in parent_dict:
                    parent_dict[class_type] = parent_dict[class_type] + 1
                else:
                    parent_dict[class_type] = 1
    inverse = [(value, key) for key, value in parent_dict.items()]
    dominant_parent_class = max(inverse)[1]
    dominant_parent_class_count = max(inverse)[0]

    # Calculating dominant class label for left child
    left_child_class_list = []
    for value2 in left_split_instances:
        left_child_class_list.append(value2[class_label_index])
    distinct_left_class_list = list(set(left_child_class_list))
    left_dict = {}
    for item in left_child_class_list:
        for class_type in distinct_left_class_list:
            if item == class_type:
                if class_type in left_dict:
                    left_dict[class_type] = left_dict[class_type] + 1
                else:
                    left_dict[class_type] = 1
    inverse = [(value, key) for key, value in parent_dict.items()]
    dominant_left_child_class_count = max(inverse)[0]

    # Calculating dominant class label for right child
    right_child_class_list = []
    for value3 in right_split_instances:
        right_child_class_list.append(value3[class_label_index])
    distinct_right_class_list = list(set(right_child_class_list))
    right_dict = {}
    for item in right_child_class_list:
        for class_type in distinct_right_class_list:
            if item == class_type:
                if class_type in right_dict:
                    right_dict[class_type] = right_dict[class_type] + 1
                else:
                    right_dict[class_type] = 1
    inverse = [(value, key) for key, value in parent_dict.items()]
    dominant_right_child_class_count = max(inverse)[0]

    result = []
    if ((dominant_left_child_class_count + dominant_right_child_class_count) - dominant_parent_class_count) <= 0:
        result.append(1)
        result.append(dominant_parent_class)
        return result
    else:
        result.append(0)
        return result