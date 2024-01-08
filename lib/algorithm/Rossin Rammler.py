import math

def distribusi_fragmentasi(X, Xc, n):
  """
  Menentukan distribusi fragmentasi batuan hasil peledakan.

  Args:
    X: Ukuran ayakan (cm)
    Yc: Ukuran karateristik
    n: Indeks keseragaman

  Returns:
    Persentase material yang tertahan pada ayakan (%)
  """

  Rx = math.exp(-(X / Xc) ** n) * 100

  return Rx


def main():
  # Input
  X = float(input("Masukkan nilai ukuran ayakan (cm): "))
  Xc = (X/0.683)**n
  W = float(input("Masukkan nilai standar deviasi dari keakuratan pemboran (m): "))
  Bc = float(input("Masukkan nilai burden (m): "))
  d = float(input("Masukkan nilai diameter lubang ledak (m): "))
  L = float(input("Masukkan nilai tinggi jenjang (m): "))
  CC = float(input("Masukkan nilai tinggi jenjang (m): "))
  A = Bc / d

  # Menghitung indeks keseragaman
  n = (2.2 - 14 * (Bc / d)) * (1 - (W / Bc)) * (1 + (A - 1) / 1) * (CC / L)
    

  # Menghitung distribusi fragmentasi
  Rx = distribusi_fragmentasi(X, Xc, n)

  # Menampilkan hasil
  print("Persentase material yang tertahan pada ayakan:", Rx, "%")


if __name__ == "__main__":
  main()
