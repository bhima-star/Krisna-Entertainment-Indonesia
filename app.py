from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# =======================
# 1. Konfigurasi App
# =======================
app = Flask(__name__)

# 🔐 SECRET KEY — WAJIB untuk session & flash()
app.secret_key = 'krisna_secret_key_123'  # kamu boleh ganti isinya bebas (misal string acak)

# Konfigurasi Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'krisna_entertainment'

mysql = MySQL(app)

# =======================
# Helper Template Checker
# =======================
def pick_template(*names):
    for name in names:
        if name in app.jinja_env.list_templates():
            return name
    return names[0]


# =======================
# ROUTE: Home
# =======================
@app.route('/')
def index():
    layanan_data = []
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nama_layanan FROM layanan")
        layanan_data = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"Gagal memuat data layanan: {e}", "error")
        
    return render_template(pick_template('index.html', 'home.html'), layanan=layanan_data)


# =======================
# ROUTE: Layanan
# =======================
@app.route('/layanan')
def layanan():
    layanan_data = []
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nama_layanan, deskripsi, harga FROM layanan")
        layanan_data = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"Gagal memuat daftar layanan: {e}", "error")
        
    return render_template(pick_template('layanan.html'), layanan=layanan_data)


# =======================
# ROUTE: Galeri
# =======================
@app.route('/galeri')
def galeri():
    return render_template(pick_template('galeri.html'))


# =======================
# ROUTE: Kontak
# =======================
@app.route('/kontak', methods=['GET', 'POST'])
def kontak():
    if request.method == 'POST':
        nama = request.form.get('nama')
        email = request.form.get('email')
        pesan = request.form.get('pesan')
        
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO kontak (nama, email, pesan) VALUES (%s, %s, %s)",
                (nama, email, pesan)
            )
            mysql.connection.commit()
            cur.close()
            flash('Pesan kamu sudah terkirim! Terima kasih 😊', 'success')
        except Exception as e:
            flash(f'Gagal mengirim pesan: {e}', 'error')

        return redirect(url_for('kontak')) 

    return render_template(pick_template('kontak.html'))


# =======================
# ROUTE: Booking
# =======================
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    layanan_data = []
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nama_layanan FROM layanan")
        layanan_data = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"Gagal memuat daftar layanan: {e}", "error")

    if request.method == 'POST':
        nama = request.form.get('nama')
        email = request.form.get('email')
        layanan_id = request.form.get('layanan')
        tanggal = request.form.get('tanggal')
        pesan = request.form.get('pesan')

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO pemesanan (nama, email, layanan, tanggal, pesan)
                VALUES (%s, %s, %s, %s, %s)
            """, (nama, email, layanan_id, tanggal, pesan))
            mysql.connection.commit()
            cur.close()
            
            flash('Pemesanan berhasil dikirim! Kami akan segera menghubungi kamu 💙', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Gagal melakukan pemesanan: {e}', 'error')

    return render_template(pick_template('booking.html'), layanan=layanan_data)


# =======================
# ROUTE: Admin
# =======================
@app.route('/admin')
def admin():
    pemesanan_data = []
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                p.id, p.nama, p.email, l.nama_layanan, p.tanggal, p.pesan, p.tanggal_pesan
            FROM pemesanan p
            LEFT JOIN layanan l ON p.layanan = l.id
            ORDER BY p.tanggal_pesan DESC
        """)
        pemesanan_data = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"Gagal memuat data pemesanan (Admin): {e}", "error")
        
    return render_template(pick_template('admin.html'), pemesanan=pemesanan_data)


# =======================
# Jalankan Server Flask
# =======================
if __name__ == '__main__':
    app.run(debug=True)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     