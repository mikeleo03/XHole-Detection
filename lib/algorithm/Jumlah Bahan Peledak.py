import math

def massa_bahan_peledak(r, H, T, J, rho1, B):
  """
  Menentukan massa bahan peledak yang dibutuhkan.

  Args:
    r: Jari-jari lubang ledak (m)
    H: Kedalaman jenjang (m)
    T: Tebal batuan yang akan dihancurkan (m)
    J: Kedalaman stemming (m)
    rho1: Massa jenis bahan peledak (kg/m^3)
    B: Burden (m)
    subdrill: Kedalaman subdrill (m)
    stemming: Kedalaman stemming (m)

  Returns:
    Massa bahan peledak (kg)
  """

  # Menghitung volume batuan yang akan dihancurkan
  massa_bahan_peledak = math.pi * r ** 2 * (H - T + J)

  return massa_bahan_peledak


def main():
  # Input
  r = float(input("Masukkan nilai jari-jari lubang ledak (m): "))
  rho1 = float(input("Masukkan nilai massa jenis bahan peledak (kg/m^3): "))
  H = float(input("Masukkan nilai tinggi jenjang (m): "))
  B = float(input("Masukkan nilai burden (m): "))
  J = 0.2 * B #subdrill
  T = 0.7 * B #stemming

  # Menghitung massa bahan peledak
  massa_bahan_peledak = massa_bahan_peledak(r, H, T, J, rho1, B)

  # Menampilkan hasil
  print("Massa bahan peledak yang dibutuhkan:", massa_bahan_peledak, "kg")


if __name__ == "__main__":
  main()
