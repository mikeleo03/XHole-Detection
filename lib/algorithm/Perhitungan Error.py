import math

def distribusi_fragmentasi(Vo, Qe, E):
  """
  Menghitung distribusi fragmentasi batuan hasil peledakan menggunakan metode Kuznetsov.

  Args:
    B: Burden (m)
    S: Spasi (m)
    Hjenjang: Tinggi jenjang (m)
    Qe: Daya ledak (kg)
    E: Energi peledakan (kJ)

  Returns:
    List of fragmentasi batuan (mm)
  """

  # Konstanta
  A = 50

  # Menghitung volume lubang ledak
  Vo = B * S * L

  # Perhitungan
  X = A * (Vo / Qe) ** 0.8 * Qe ** (1 / 6) / (E / 115) ** (-19 / 30)

  # Mengubah unit X ke mm
  X *= 100

  # Mengembalikan hasil sebagai list dengan satu elemen
  return [int(X)]


def main():
  Rho1 = float(input("Masukkan nilai Massa Jenis Bahan Peledak (gr/cc): "))
  VoD = float(input("Masukkan nilai Kecepatan Detonasi Batuan (feet per second): "))
  AF1 = (Rho1*VoD**2/1.2*1200**2)**(1/3) #Adjustment Bahan Peledak

  Rho2 = float(input("Masukkan nilai Massa Jenis Batuan (pound cubic feet): "))
  AF2 = (160/Rho2)**(1/3) #Adjustment Batuan

  Kbstd = 30 
  B = D*Kbstd*AF1*AF2 #R.L.Ash
  L = float(input("Masukkan nilai tinggi jenjang (m): "))

def hitung_s(L, B, metode_penyalaan):
  """ 
  Menghitung nilai S berdasarkan stiffness ratio dan metode penyalaan.

  Args:
    L: Panjang lubang ledak (m)
    B: Burden (m)
    metode_penyalaan: Metode penyalaan, bisa "serentak" atau "tunda"

  Returns:
    Nilai S (m)
  """

  # Menghitung stiffness ratio
  L_B = L / B
  metode_penyalaan = str(input("Masukkan metode penyalaan (serentak/tunda): "))

  # Menghitung nilai S
  if L_B < 4:
    if metode_penyalaan == "serentak":
      S = (L + 2 * B) / 3
    elif metode_penyalaan == "tunda":
      S = (L + 7 * B) / 8
  else:
    if metode_penyalaan == "serentak":
      S = 2 * B
    elif metode_penyalaan == "tunda":
      S = 1.4 * B

  return S

def corrected_burden(B, rock_deposition, geologic_structure, number_of_rows):
 """
 Menghitung corrected burden (Bc) dengan mempertimbangkan faktor koreksi.

 Args:
   B: Burden (ft)
   rock_deposition: Kondisi sedimentasi batuan ('steeply dipping into cut', 'steeply dipping into face', atau lainnya)
   geologic_structure: Struktur geologi batuan ('heavily cracked', 'thin well cemented layers', atau 'massive intact rock')
   number_of_rows: Jumlah baris lubang ledak (1, 2, atau lebih)

 Returns:
   Corrected burden (Bc) (ft)
 """

rock_deposition = str(input("Koreksi Bedding ( steeply dipping into cut atau  steeply dipping into face): "))
geologic_structure = str(input("Koreksi Struktur Geologi ( steeply dipping into cut atau  steeply dipping into face): "))
number_of_rows = int(input("Jumlah baris peledakan: "))# Menentukan faktor koreksi Kd

 if rock_deposition == "steeply dipping into cut":
   Kd = 1.18
 elif rock_deposition == "steeply dipping into face":
   Kd = 0.95
 else:
   Kd = 1.0

 # Menentukan faktor koreksi Ks
 if geologic_structure == "heavily cracked":
   Ks = 1.30
 elif geologic_structure == "thin well cemented layers":
   Ks = 1.1
 else:
   Ks = 0.95

 # Menentukan faktor koreksi Kr
 if number_of_rows <= 2:
   Kr = 1.0
 else:
   Kr = 0.95

 # Menghitung corrected burden
 Bc = Kd * Ks * Kr * B

 return Bc

Bc = corrected_burden(B, rock_deposition, geologic_structure, number_of_rows)
print("Corrected burden:", Bc, "m")


# Menghitung fragmentasi
fragmentasi = distribusi_fragmentasi(Vo, 100, 100000)

  # Menampilkan hasil
print("Distribusi fragmentasi batuan hasil peledakan:")
print(fragmentasi[0], "mm")


if __name__ == "__main__":
  main()


