from flask import Flask
from config.database import engine, Base
from routes.web import menu_bp, order_bp
from flask_cors import CORS

app = Flask(__name__)

# Setup CORS secara global, izinkan semua origin
CORS(app)

# Buat tabel otomatis (kalau belum ada di DB)
Base.metadata.create_all(bind=engine)

# Daftarkan blueprint route utama
app.register_blueprint(menu_bp, url_prefix="/menus")
app.register_blueprint(order_bp, url_prefix="/orders")

if __name__ == "__main__":
    # Jalankan di host 0.0.0.0 supaya bisa diakses dari device lain (Flutter mobile/web)
    app.run(debug=True, host="0.0.0.0", port=5000)
