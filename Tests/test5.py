arr = []
arr.append(1)
arr.append(2)
arr[0] = None
# arr[1] = None
if not None in arr:
    print('None')
else:
    print(type(arr))
