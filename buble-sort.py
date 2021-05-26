def bubbleSort(inputArray):
    scanLength = len(inputArray) -1 # Scan not apply comparision starting with last item of list (No item to right)
    sorted = False

    while not sorted:
        sorted = True # Break the while loop whenever we have gone through all the values

        for i in range(0,scanLength):
            # if value in list is greater than value directly to the right of it
            if inputArray[i] > inputArray[i+1]:
                sorted = False # These values are unsorted
                inputArray[i], inputArray[i+1] = inputArray[i+1], inputArray[i] #Switch these values
    return inputArray # Return sorted array.

# tests

print(bubbleSort([4,8,1,14,8,2,9,5,7,6,6]))






