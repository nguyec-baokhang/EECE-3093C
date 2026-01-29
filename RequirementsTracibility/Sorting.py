
def Merge(A, B):
    m = len(A) - 1
    n = len(B) - 1
    i, j, k = 0, 0, 0
    C = [0] * (m + 1 + n + 1)

    while(i<=m and j<=n):
        if (A[i]<B[j]):
            C[k]=A[i]
            k += 1
            i += 1
        else:
            C[k]=B[j]
            k += 1
            j += 1

    for idx in range(i, m + 1):
        C[k] = A[idx]
        k += 1

    for idx in range(j, n + 1):
        C[k] = B[idx]
        k += 1

    return C

def MergeSort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2

    left = MergeSort(arr[:mid])
    right = MergeSort(arr[mid:])

    return Merge(left, right)

if __name__ == "__main__":
    arr = [9, 3, 7, 5, 6, 4, 8, 2]
    arr = MergeSort(arr)
    print(arr)



