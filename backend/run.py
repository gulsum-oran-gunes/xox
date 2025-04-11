# /backend/run.py

from app import create_app  # app/__init__.py'deki create_app fonksiyonunu içe aktar

app = create_app()  # Flask uygulamasını oluştur
if __name__ == '__main__':
    print("Flask uygulaması başlatılıyor...")
    app.run(debug=True)  # Uygulamayı çalıştır
