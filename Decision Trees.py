'''
Construction of a decision tree using Gini or Information Gain
Author: Rohit Dandona
'''

import math
import random
import operator
import Test_Accuracy


'''
Function to build decision tree
'''
def decision_tree(instances,attibute_names,class_label_index,non_class_label_index,class_label_types,root_node,measure_type):

    # Check for a leaf node
    temp_list = []
    for value in instances:
        temp_list.append(value[class_label_index])
    class_list = list(set(temp_list))
    if len(class_list) == 1:
        #print ("Leaf Node Found  ","Class Type: ", class_list[0])
        root_node.split_attribute = class_list[0]
        root_node.best_split_threshold = 0
        root_node.is_leaf_node = True

    else:
        temp_value = instances[non_class_label_index]
        for i in range(0,len(instances)):
            if i != class_label_index:
                if instances[i] != temp_value:
                    break
        else:
            #leaf_found = 1
            #leaf = leaf_info(instances,class_label_index)
            #print ("Leaf Node Found  ","Class Type: ", class_list[0])
            root_node.split_attribute = class_list[0]
            root_node.best_split_threshold = 0
            root_node.is_leaf_node = True

    # Continue construction if not a leaf node
    if root_node.is_leaf_node == False:
        attribute_range_measure_list = []
        sorted_information_gain_array = []

        for index in range(0,len(attibute_names)):
            if index != class_label_index:
                sorted_instance_list=sorted(instances, key = operator.itemgetter(index))

                # Compute range values of the attribute's values
                temp_range = []
                attribute_range_list = []
                for each_value in sorted_instance_list:
                    temp_range.append(float(each_value[index]))
                minimum = min(temp_range)
                maximum = max(temp_range)
                step = round(((maximum-minimum)/5),2)
                for j in range(1,5):
                    attribute_range_list.append(round((minimum+(step*j)),2))
                attribute_range_measure_list.extend(compute_attribute_measure_gain(sorted_instance_list,attribute_range_list,index,class_label_index,class_label_types,measure_type))

        sorted_information_gain_array = sorted(attribute_range_measure_list, key = operator.itemgetter(2))
        split = []
        left_split_instances = []
        right_split_instances = []
        split = sorted_information_gain_array[-1]

        for k in range(0,len(instances)):
            if float(instances[k][split[0]])<=split[1]:
                left_split_instances.append(instances[k])
            else:
                right_split_instances.append(instances[k])

        left_split = split[0]
        right_split = split[1]

        # Compute pessimistic error before moving ahead
        result = Test_Accuracy.compute_pessimistic_error(instances, left_split_instances, right_split_instances, class_label_index)

        if result[0] == 1:
            #print ("Leaf Node Found  ","Class Type: ", result[1])
            root_node.split_attribute = result[1]
            root_node.best_split_threshold = 0
            root_node.is_leaf_node = True

        else:
            attribute_index = split[0]
            attribute_value = attibute_names[attribute_index]
            split_value = split[1]
            root_node.attribute_index = attribute_index
            root_node.split_attribute = attribute_value

            root_node.best_split_threshold = split_value
            root_node.children.append(node())
            root_node.children.append(node())

            #print("Split Attribute: ",attribute_value,"  ","Split Value: ",split_value)

            decision_tree(left_split_instances,attibute_names,class_label_index,non_class_label_index,class_label_types,root_node.children[0],measure_type)
            decision_tree(right_split_instances,attibute_names,class_label_index,non_class_label_index,class_label_types,root_node.children[1],measure_type)


'''
Function to calculate Information Gain or Gini based on "measure type" selected by user
'''
def compute_attribute_measure_gain(sorted_instance_list,attribute_range_list,index,class_label_index,class_label_types,measure_type):
    # Compute entropy for parent node
    parent_entropy = 0
    class_list = []
    for each_value in sorted_instance_list:
        class_list.append(each_value[class_label_index])

    distinct_class_type_number = []
    for each_value1 in class_label_types:
        count = 0
        for each_value2 in class_list:
            if each_value1 == each_value2:
                count = count + 1
        distinct_class_type_number.append(count)
    parent_entropy = compute_entropy(distinct_class_type_number,measure_type)

    # Compute entropy for child nodes
    distinct_class_left_count = []
    distinct_class_right_count = []
    attribute_range_measure_list = []
    for each_split_value in attribute_range_list:
        class_array_left = []
        class_array_right = []
        less_than_split_count = 0
        greater_than_split_count = 0
        child_combined_entropy = 0
        for each_sorted_value in sorted_instance_list:
            if float(each_sorted_value[index])<=each_split_value:
                class_array_left.append(each_sorted_value[class_label_index])
                less_than_split_count = less_than_split_count + 1
            else:
                class_array_right.append(each_sorted_value[class_label_index])
                greater_than_split_count = greater_than_split_count + 1

        # Entropy for left child
        distinct_class_left_count = []
        for each_value1 in class_label_types:
            count = 0
            for each_value2 in class_array_left:
                if each_value1 == each_value2:
                    count = count + 1
            distinct_class_left_count.append(count)
        left_child_entropy = compute_entropy(distinct_class_left_count,measure_type)

        # Entropy for left child
        distinct_class_right_count = []
        for each_value1 in class_label_types:
            count = 0
            for each_value2 in class_array_right:
                if each_value1 == each_value2:
                    count = count + 1
            distinct_class_right_count.append(count)
        right_child_entropy = compute_entropy(distinct_class_right_count,measure_type)

        # Total child entropy
        left_sum = 0
        right_sum = 0
        total_sum = 0
        for n1 in distinct_class_left_count:
            left_sum = left_sum + n1
        for n2 in distinct_class_right_count:
            right_sum = right_sum + n2
        total_sum = left_sum + right_sum
        child_entropy = ((left_sum/total_sum)*left_child_entropy)+((right_sum/total_sum)*right_child_entropy)

        # Total gain
        final_measure_gain = parent_entropy - child_entropy

        attribute_range_measure_list.append([index,each_split_value,final_measure_gain])

    return attribute_range_measure_list


'''
Function to calculate Entropy
'''
def compute_entropy(distinct_class_count,measure_type):
    total = 0
    entropy = 0
    gini = 1

    # Procedure for calculating Information Gain
    if int(measure_type) == 0:
        for val1 in distinct_class_count:
            total = total + val1
        for val2 in distinct_class_count:
            if val2 != 0:
                entropy = entropy - ((val2/total) * math.log((val2/total),2))
        return entropy

    # Procedure for calculating Gini
    elif int(measure_type) == 1:
        for val1 in distinct_class_count:
            total = total + val1
        for val2 in distinct_class_count:
            if val2 != 0:
                gini = gini + ((-1) * ((val2/total)**2))
        return gini


# Start of the main function
if __name__ == '__main__':
    # Ask user for inputs
    print("Enter comma seperated attribute names")
    names = input()
    attibute_names = [s.strip() for s in names.strip().split(',')]
    print("Enter class label variable (case sensitive)")
    class_label = input()
    print("Enter measure type: 0 for Information gain and 1 for Gini")
    measure_type = int(input())

    # Find class label index
    index = 0
    for name in attibute_names:
        if name == class_label:
            class_label_index = index
            break
        else:
            index = index + 1

    # Find non class label starting index
    index = 0
    for name in attibute_names:
        if name != class_label:
            non_class_label_index = index
            break
        else:
            index = index + 1

    # Read dataset
    instances = []
    instances_temp = []
    with open("C:\\Users\\rohit\\Desktop\\irisdataset.txt", 'r') as f: # Replace paths for other data sets
        for line in f:
            new_instance = line.strip().split(',') # Replace with delimiter of the respective file
            instances_temp.append([i for i in new_instance])

    random_file=random.sample(range(0,len(instances_temp)),len(instances_temp))

    number_of_test_records = round((len(instances_temp)*10)/100)

    for j in range(0,len(random_file)):
        instances.append(instances_temp[random_file[j]])

    # Class labels types
    types = []
    for values in instances:
        types.append(values[class_label_index])
    class_label_types = list(set(types))

    # Class object definition
    class node(object):
        def __init__(self):
            self.is_leaf_node = False
            self.left_tree_length = 0
            self.right_tree_length = 0
            self.attribute_index = 0
            self.split_attribute = ''
            self.best_split_threshold = 0
            self.children = []

    root_node = node()

    # Dividing into test and training data sets
    test_accuracy_list = []
    accuracy = 0
    for i in range(1,11):
        test_instances = []
        training_instances = []
        for j in range(0,len(instances)):
            if (j+(i-1)*number_of_test_records)<i*number_of_test_records and (j+(i-1)*number_of_test_records)>=(i-1)*number_of_test_records:
                if(j+((i-1)*number_of_test_records)<len(instances)):
                    test_instances.append(instances[j+((i-1)*number_of_test_records)])
        for k in range(0,len(instances)):
            if k<(i-1)*number_of_test_records:
                training_instances.append(instances[k])
            elif k>=(i)*number_of_test_records:
                training_instances.append(instances[k])

        # Construction of tree
        decision_tree(training_instances,attibute_names,class_label_index,non_class_label_index,class_label_types,root_node,measure_type)

        # Capturing accuracy

        test_accuracy_list.append(Test_Accuracy.compute_accuracy(test_instances,root_node,class_label_index))

    # Combined accuracy of the 10 fold validation
    print ("Ten cross fold validation result set :")
    print (test_accuracy_list)
    for value in test_accuracy_list:
        accuracy = accuracy + value
    print(accuracy/len(test_accuracy_list))





