import os

class Utils:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(title):
        print("\n" + "=" * 50)
        print(f"{title:^50}")
        print("=" * 50)

    @staticmethod
    def get_complexity_info():
        return {
            "Bubble Sort": {
                "Complexity": "O(n²)",
                "Explanation": "Algoritma sederhana yang membandingkan elemen bersebelahan. Kurang efisien untuk data besar."
            },
            "Insertion Sort": {
                "Complexity": "O(n²) rata-rata/terburuk, O(n) terbaik",
                "Explanation": "Algoritma yang menyisipkan data pada posisi yang tepat satu per satu. Efisien untuk data kecil atau hampir terurut."
            },
            "Merge Sort": {
                "Complexity": "O(n log n)",
                "Explanation": "Algoritma efisien yang membagi data menjadi dua bagian (Divide & Conquer) secara rekursif dan menggabungkannya kembali."
            },
            "Linear Search": {
                "Complexity": "O(n)",
                "Explanation": "Mencari data dengan memeriksa setiap elemen dari awal sampai akhir pada struktur linear seperti List/Array."
            },
            "Sequential Search": {
                "Complexity": "O(n)",
                "Explanation": "Mencari data secara berurutan dengan menelusuri pointer Node (next) pada struktur Doubly Linked List dari head ke tail."
            },
            "Binary Search": {
                "Complexity": "O(log n)",
                "Explanation": "Mencari data pada list yang sudah terurut dengan membagi rentang pencarian menjadi dua berulang kali."
            }
        }

