from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Daftar bagian wajah dan koordinat targetnya (misalnya, untuk wajah standar)
# Anda perlu menyesuaikan koordinat ini dengan gambar wajah polos Anda.
bagian_wajah = [
    {'nama': 'mata_kiri', 'gambar': 'mata.png', 'target_x': 100, 'target_y': 150},
    {'nama': 'mata_kanan', 'gambar': 'mata.png', 'target_x': 250, 'target_y': 150},
    {'nama': 'hidung', 'gambar': 'hidung.png', 'target_x': 175, 'target_y': 200},
    {'nama': 'mulut', 'gambar': 'mulut.png', 'target_x': 175, 'target_y': 250},
    {'nama': 'telinga_kiri', 'gambar': 'telinga.png', 'target_x': 50, 'target_y': 175},
    {'nama': 'telinga_kanan', 'gambar': 'telinga.png', 'target_x': 300, 'target_y': 175},
]

@app.route('/')
def index():
    # Acak urutan bagian wajah yang ditampilkan
    bagian_wajah_acak = random.sample(bagian_wajah, len(bagian_wajah))
    return render_template('index.html', bagian_wajah=bagian_wajah_acak)

@app.route('/cek_posisi', methods=['POST'])
def cek_posisi():
    data = request.get_json()
    nama_bagian = data['nama']
    x = data['x']
    y = data['y']

    # Cari data bagian wajah berdasarkan nama
    bagian = next((b for b in bagian_wajah if b['nama'] == nama_bagian), None)

    if bagian:
        # Cek apakah posisi drop cukup dekat dengan target (toleransi misalnya 20 piksel)
        toleransi = 20
        if abs(x - bagian['target_x']) <= toleransi and abs(y - bagian['target_y']) <= toleransi:
            return jsonify({'status': 'benar', 'pesan': f'Hebat! {bagian["nama"].replace("_", " ").title()} di tempat yang benar!'})
        else:
            return jsonify({'status': 'salah', 'pesan': 'Coba lagi, ya!'})
    else:
        return jsonify({'status': 'error', 'pesan': 'Bagian wajah tidak ditemukan.'})

if __name__ == '__main__':
    app.run(debug=True)
