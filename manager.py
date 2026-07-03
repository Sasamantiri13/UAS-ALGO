import time
from models import MahasiswaAktif
from data_structures import DoublyLinkedList, SearchCache

class SortEngine:
    @staticmethod
    def bubbleSort(data, key="nim"):
        """Bubble Sort: O(n²) comparisons and swaps. Berulang kali menukar elemen bersebelahan."""
        n = len(data)
        comparisons = 0
        swaps = 0
        start_time = time.time()
        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1
                if getattr(data[j], key) > getattr(data[j+1], key):
                    data[j], data[j+1] = data[j+1], data[j]
                    swaps += 1
        return comparisons, swaps, time.time() - start_time

    @staticmethod
    def insertionSort(data, key="nim"):
        """Insertion Sort: O(n²) worst/average, O(n) best. Menyisipkan elemen ke posisi yang tepat."""
        n = len(data)
        comparisons = 0
        swaps = 0
        start_time = time.time()
        for i in range(1, n):
            key_item = data[i]
            j = i - 1
            while j >= 0:
                comparisons += 1
                val_j = getattr(data[j], key)
                val_key = getattr(key_item, key)
                if val_j > val_key:
                    data[j + 1] = data[j]
                    swaps += 1 # Perpindahan elemen
                    j -= 1
                else:
                    break
            data[j + 1] = key_item
        return comparisons, swaps, time.time() - start_time

    @staticmethod
    def mergeSort(data, key="nim"):
        """Merge Sort: O(n log n) di semua kasus. Divide & Conquer secara rekursif."""
        comparisons = [0]
        swaps = [0]
        start_time = time.time()

        def _merge_sort(arr):
            if len(arr) > 1:
                mid = len(arr) // 2
                L = arr[:mid]
                R = arr[mid:]
                _merge_sort(L)
                _merge_sort(R)
                i = j = k = 0
                while i < len(L) and j < len(R):
                    comparisons[0] += 1
                    if getattr(L[i], key) < getattr(R[j], key):
                        arr[k] = L[i]
                        i += 1
                    else:
                        arr[k] = R[j]
                        j += 1
                    swaps[0] += 1
                    k += 1
                while i < len(L):
                    arr[k] = L[i]; i += 1; k += 1; swaps[0] += 1
                while j < len(R):
                    arr[k] = R[j]; j += 1; k += 1; swaps[0] += 1

        _merge_sort(data)
        return comparisons[0], swaps[0], time.time() - start_time

class SearchEngine:
    @staticmethod
    def linearSearch(data, value, key="nim"):
        """Linear Search: O(n). Mencari elemen berurutan pada struktur linear (List/Array)."""
        iterations = 0
        for index, item in enumerate(data):
            iterations += 1
            if str(getattr(item, key)).lower() == str(value).lower():
                return index, iterations
        return -1, iterations

    @staticmethod
    def sequentialSearch(linked_list, value, key="nim"):
        """Sequential Search: O(n). Mencari secara berurutan langsung pada pointer node Doubly Linked List."""
        iterations = 0
        current = linked_list.head
        index = 0
        while current:
            iterations += 1
            item = current.data
            if str(getattr(item, key)).lower() == str(value).lower():
                return index, iterations
            current = current.next # Mengikuti penunjuk pointer/reference node
            index += 1
        return -1, iterations

    @staticmethod
    def binarySearch(data, value, key="nim"):
        """Binary Search: O(log n). Membagi rentang pencarian menjadi dua pada data yang sudah terurut."""
        SortEngine.mergeSort(data, key) # Memastikan data terurut terlebih dahulu
        low, high, iterations = 0, len(data) - 1, 0
        while low <= high:
            iterations += 1
            mid = (low + high) // 2
            mid_val = str(getattr(data[mid], key)).lower()
            target_val = str(value).lower()
            if mid_val == target_val: return mid, iterations
            elif mid_val < target_val: low = mid + 1
            else: high = mid - 1
        return -1, iterations

class MahasiswaManager:
    def __init__(self, studentList=None):
        # MENGGUNAKAN DOUBLY LINKED LIST UNTUK PENYIMPANAN
        self.linked_list = DoublyLinkedList()
        if studentList:
            self.linked_list.from_list(studentList)
        
        # MENGGUNAKAN CACHE UNTUK PENCARIAN
        self.search_cache = SearchCache()

    def addStudent(self, student):
        self.linked_list.append(student)
        self.search_cache.clear() # Invalidate cache jika ada mutasi data

    def removeStudent(self, nim):
        success = self.linked_list.remove_by_condition(lambda s: s.nim == nim)
        if success:
            self.search_cache.clear()
        return success

    def updateStudent(self, nim, new_data):
        current = self.linked_list.head
        while current:
            if current.data.nim == nim:
                student = current.data
                if "nama" in new_data: student.nama = new_data["nama"]
                if "jurusan" in new_data: student.jurusan = new_data["jurusan"]
                if "semester" in new_data: student.semester = new_data["semester"]
                if "ipk" in new_data: student.ipk = new_data["ipk"]
                if "status" in new_data:
                    from models import MahasiswaAktif, MahasiswaNonAktif
                    if new_data["status"] == "Non-Aktif" or new_data["status"].lower() == "non":
                        student.__class__ = MahasiswaNonAktif
                        student.status = "Non-Aktif"
                    else:
                        student.__class__ = MahasiswaAktif
                        student.status = "Aktif"
                self.search_cache.clear()
                return True
            current = current.next
        return False

    def getAllStudents(self):
        # Konversi ke Python List untuk mendukung sorting dan rendering tabel
        return self.linked_list.to_list()
    
    def search_with_cache(self, query, key="nim", search_method="sequential"):
        """Pencarian dengan cache untuk kecepatan optimasi."""
        cache_key = f"{key}:{query}:{search_method}"
        cached_result = self.search_cache.get(cache_key)
        if cached_result:
            return cached_result, 0, True # Indikator cached = True
        
        # Eksekusi pencarian sesuai metode yang dipilih
        if search_method == "sequential":
            idx, iters = SearchEngine.sequentialSearch(self.linked_list, query, key)
        elif search_method == "binary":
            data = self.getAllStudents()
            idx, iters = SearchEngine.binarySearch(data, query, key)
        else: # linear
            data = self.getAllStudents()
            idx, iters = SearchEngine.linearSearch(data, query, key)
            
        result = (idx, iters)
        self.search_cache.set(cache_key, result)
        return result, iters, False

