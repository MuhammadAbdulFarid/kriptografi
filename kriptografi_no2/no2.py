import string
from collections import Counter
from typing import Dict, Tuple, List

class AdvancedCaesarAnalyzer:
    """
    Kelas penganalisis Caesar Cipher Multi-Bahasa.
    Menampilkan seluruh 26 iterasi Brute-Force, lalu menyaring Top 3 hasil terbaik.
    """
    
    # Distribusi frekuensi huruf Bahasa Inggris standar
    EN_FREQ = {
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228,
        'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
        'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987,
        'S': 6.327, 'T': 9.056, 'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150,
        'Y': 1.974, 'Z': 0.074
    }

    # Distribusi frekuensi huruf Bahasa Indonesia standar (Perkiraan)
    ID_FREQ = {
        'A': 19.34, 'B': 2.58, 'C': 1.48, 'D': 4.15, 'E': 8.52, 'F': 0.82,
        'G': 4.10, 'H': 2.29, 'I': 8.86, 'J': 0.79, 'K': 4.31, 'L': 4.01,
        'M': 4.41, 'N': 9.35, 'O': 2.05, 'P': 3.03, 'Q': 0.01, 'R': 5.34,
        'S': 5.33, 'T': 5.05, 'U': 5.23, 'V': 0.30, 'W': 0.42, 'X': 0.01,
        'Y': 1.63, 'Z': 0.10
    }

    def __init__(self, ciphertext: str, language: str = 'EN'):
        self.ciphertext = ciphertext.upper()
        self.alphabet = string.ascii_uppercase
        self.target_freq = self.ID_FREQ if language.upper() == 'ID' else self.EN_FREQ
        self.language = "Indonesia" if language.upper() == 'ID' else "Inggris"

    def get_character_frequencies(self, text: str) -> Dict[str, float]:
        letters_only = [char for char in text if char in self.alphabet]
        total_letters = len(letters_only)
        if total_letters == 0:
            return {char: 0.0 for char in self.alphabet}
        counts = Counter(letters_only)
        return {char: (counts.get(char, 0) / total_letters) * 100 for char in self.alphabet}

    def decrypt_shift(self, shift: int) -> str:
        """Melakukan dekripsi teks dengan pergeseran KE DEPAN (+)."""
        decrypted_text = []
        for char in self.ciphertext:
            if char in self.alphabet:
                new_idx = (self.alphabet.index(char) + shift) % 26
                decrypted_text.append(self.alphabet[new_idx])
            else:
                decrypted_text.append(char)
        return "".join(decrypted_text)

    def calculate_chi_squared(self, decrypted_text: str) -> float:
        text_freq = self.get_character_frequencies(decrypted_text)
        chi_squared = 0.0
        for char in self.alphabet:
            expected = self.target_freq[char]
            observed = text_freq[char]
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected
        return chi_squared

    def print_all_and_get_results(self) -> List[Tuple[int, str, float]]:
        """Mencetak seluruh 26 kemungkinan dan menyimpannya untuk diurutkan nanti."""
        results = []
        print(f"\n--- HASIL BRUTE-FORCE (SELURUH 26 KEMUNGKINAN) ---")
        print(f"{'Key (+)':<7} | {'Plaintext (Hasil Dekripsi)':<30} | {'Score (Makin kecil makin akurat)':<35}")
        print("-" * 80)
        
        for shift in range(26):
            decrypted = self.decrypt_shift(shift)
            score = self.calculate_chi_squared(decrypted)
            results.append((shift, decrypted, score))
            
            # Print iterasi secara langsung agar semuanya muncul berurutan (0 sampai 25)
            print(f"{shift:<7} | {decrypted:<30} | {score:.2f}")
            
        return results

if __name__ == "__main__":
    print("=" * 80)
    print("SISTEM ANALISIS CAESAR CIPHER LENGKAP (100% HUMAN-VERIFIED MODEL)")
    print("=" * 80)
    
    user_input = input("Masukkan Ciphertext bebas: ").strip()
    
    if not user_input:
        print("\n[!] Ciphertext kosong.")
    else:
        lang_input = input("Pilih Bahasa target (EN untuk Inggris / ID untuk Indonesia): ").strip()
        
        analyzer = AdvancedCaesarAnalyzer(user_input, lang_input)
        
        print(f"\nMenganalisis menggunakan statistik Bahasa {analyzer.language}...")
        
        # 1. Tampilkan SELURUH 26 kemungkinan berurutan
        all_results = analyzer.print_all_and_get_results()
        
        # 2. Urutkan hasil berdasarkan skor terbaik untuk kesimpulan
        all_results.sort(key=lambda x: x[2])
        
        print("\n" + "=" * 80)
        print("KESIMPULAN: TOP 3 REKOMENDASI TERBAIK")
        print("=" * 80)
        print(f"{'Rank':<5} | {'Key (+)':<7} | {'Plaintext Terbaik':<30} | {'Score':<10}")
        print("-" * 80)
        
        # Tampilkan 3 teratas dari data yang sudah diurutkan
        for i in range(3):
            shift, text, score = all_results[i]
            print(f"#{i+1:<4} | {shift:<7} | {text:<30} | {score:.2f}")

        print("-" * 80)
        print("Program menampilkan seluruh tabel perhitungan, namun menyoroti 3 kandidat di atas.")
        print("Tugas Anda sekarang hanya perlu membaca tabel Top 3 untuk memastikan kata yang paling masuk akal!")
        print("=" * 80)