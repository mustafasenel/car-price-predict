import joblib
import pandas as pd
import streamlit as st

# Kaydedilmiş modeli yükleme
model = joblib.load("model_kaydi.pkl")

# Tahmin fonksiyonunu tanımla
def predict_price(input_df):
    # Tahmin yapılacak işlemleri buraya yazın
    # model.predict() kullanarak tahmin yapabilirsiniz
    predicted_prices = model.predict(input_df)
    return predicted_prices[0]

# Streamlit uygulamasını oluştur
def main():

    st.set_page_config(
    page_title="Araç Fiyatları Tahmin Uygulaması",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
    )

    st.header("ARAÇ FİYATLARI TAHMİN UYGULAMASI")
    # Giriş özelliklerini seçmek için selectboxları oluştur
    markalar = {
    'Audi': ('A1', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'R8', 'S', 'TT' 'Q3', 'Q5', 'Q7'),
    'BMW': ('1 Serisi', '2 Serisi', '3 Serisi', '4 Serisi', '5 Serisi', '6 Serisi', '7 Serisi', 'X3', 'X5', 'i3', 'i8'),
    'Chevrolet': ('Aveo', 'Cruze', 'Lacetti', 'Spark', 'Malibu', 'Camaro', 'Equinox', 'Tahoe', 'Silverado'),
    'Citroen': ('C-Elysee', 'C1', 'C2', 'C3', 'C4', 'C5', 'Berlingo', 'Jumper', 'SpaceTourer'),
    'Dacia': ('Sandero', 'Logan', 'Duster', 'Lodgy', 'Dokker', 'Spring'),
    'Fiat': ('Egea', 'Linea', 'Fiorino', 'Tipo', 'Doblo', '500', 'Palio', 'Punto', ),
    'Ford': ('Focus', 'Mondeo', 'Fiesta', 'Kuga', 'Mustang', 'Ranger'),
    'Honda': ('Civic', 'City', 'Accord', 'CR-V', 'HR-V', 'Jazz'),
    'Hyundai': ('i10', 'i20', 'i30', 'Accent', 'Accent Blue', 'Accent Era', 'Tucson', 'Santa Fe', 'Kona'),
    'Kia': ('Rio', 'Picanto', 'Ceed', 'Cerato', 'Stinger', 'Sportage', 'Sorento', 'Telluride'),
    'Mercedes - Benz': ('A', 'B', 'C', 'E', 'S'),
    'Nissan': ('Micra', 'Almera', 'Note', 'Primera', 'Qashqai', 'Juke', 'X-Trail', 'Navara', 'Leaf'),
    'Opel': ('Corsa', 'Astra', 'Vectra', 'Meriva', 'Insignia', 'Mokka', 'Grandland', 'Crossland'),
    'Peugeot': ('206', '207', '208', '301', '307', '308', '407', '508', '2008', '3008', '5008'),
    'Renault': ('Clio', 'Megane', 'Symbol', 'Fluence', 'Talisman', 'Captur', 'Kadjar', 'Koleos'),
    'Seat': ('Ibiza', 'Leon', 'Toledo', 'Ateca', 'Tarraco', 'Alhambra'),
    'Skoda': ('Fabia', 'Rapid', 'Octavia', 'SuperB', 'Kamiq', 'Karoq', 'Kodiaq'),
    'Tofas': ('Sahin', 'Dogan', 'Kartal', 'Serce'),
    'Toyota': ('Corolla', 'Yaris', 'Auris' 'Camry', 'C-HR', 'RAV4', 'Land Cruiser'),
    'Volkswagen': ('Golf', 'Passat', 'Scirocco', 'Bora', 'Jetta', 'Tiguan', 'Polo', 'T-Roc', 'Touareg'),
    'Volvo': ('S40', 'S60', 'S90', 'V40', 'V50', 'V60', 'XC40', 'XC60')
    }

    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        marka = st.selectbox('Aracınızın Markasını Seçin', sorted(markalar.keys()))

        if marka:
            modeller = sorted(markalar[marka])
            arac_model = st.selectbox('Aracınızın Modelini Seçin', modeller)

    
        years = list(range(2023, 1989, -1))  # 1990'dan 2023'e kadar olan yılları içeren bir liste oluşturuyoruz
        yil = st.selectbox('Yıl Seçin', years)
        km = st.number_input('Aracın KM Bilgisini Girin', format="%.0f")
        vites = st.selectbox('Aracınızın Vites Tipini Seçin', ('Manuel', 'Otomatik', 'Yari Otomatik'))
        yakit = st.selectbox('Aracınızın Yakıt Tipini Seçin', ('Benzin', 'Dizel', 'LPG')) 
        kasa = st.selectbox('Aracınızın Kasa Tipini Seçin', ('Sedan', 'Hatchback/3', 'Hatchback/5', 'Coupe', 'Station wagon', 'MPV'))

    with col2: 
        hacim = st.number_input('Aracın Motor Hacmini Girin', format="%.0f")
        guc = st.number_input('Aracın Motor Gücünü Girin', format="%.0f")
        cekis = st.selectbox('Aracınızın Çekiş Tipini Seçin', ('Onden Cekis', 'Arkadan Itis', '4WD (Surekli)'))
        tuketim = st.number_input('Aracın Ortalama Yakıt Tüketimini Girin')
        degisen = st.number_input('Aracın Değişen Parça Sayısını Girin', format="%.0f")
        boyali = st.number_input('Aracın Boyalı Parça Sayısını Girin', format="%.0f")
        kimden = st.selectbox('Aracınızın Satıcısını Seçin', ('Sahibinden', 'Galeriden', 'Yetkili Bayiden'))

    with col3:
        # Girdi özelliklerini tanımla
        input_features = {
            "Marka": [marka],
            "Model": [arac_model],
            "Yil": [int(yil)],
            "KM": [int(km)],
            "Vites": [vites],
            "Yakit": [yakit],
            "Kasa": [kasa],
            "Hacim": [float(hacim)],
            "Guc": [int(guc)],
            "Cekis": [cekis],
            "Tuketim": [float(tuketim)],
            "Degisen": [int(degisen)],
            "Boyali": [int(boyali)],
            "Kimden": [kimden]
        }

    
        # Girdi özelliklerini DataFrame'e dönüştür
        input_df = pd.DataFrame(input_features)

        if st.button('Tahmin Et'):
            predicted_price = predict_price(input_df)

            # Tahmin edilen fiyatı ekrana yazdır
            st.markdown("<h1 style='text-align: center;'>{}₺</h1>".format(format(round(predicted_price, -3), ".0f")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
