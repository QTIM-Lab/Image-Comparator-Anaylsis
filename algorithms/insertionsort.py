# Python program for implementation of Insertion Sort
 
# Function to do insertion sort
def insertionSort(arr):
     # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        # pdb.set_trace()
        key = arr[i]
 
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        print(f"pair: [{key}, {arr[j]}]")
        # get_annotator_result(key, arr[j])
        while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = key
        print(arr)


# Driver code to test above
# arr = [12, 11, 13, 5, 6]
# insertionSort(arr)
# for i in range(len(arr)):
#     print ("% d" % arr[i])