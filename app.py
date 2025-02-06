import pandas as pd
import streamlit as st
import ast

# Load dataset hasil clustering
@st.cache
def load_data():
    file_path = "clustered_data.csv"  # Ganti dengan path file Anda
    data = pd.read_csv(file_path)
    return data

# Load data
data = load_data()

# Pastikan kolom 'genres' ada
if 'genres' not in data.columns:
    st.write("Kolom 'genres' tidak ada dalam dataset. Mohon tambahkan kolom genre.")
    st.stop()  # Hentikan eksekusi lebih lanjut jika kolom tidak ada

# Membersihkan kolom 'genres' untuk memastikan data berupa list
def clean_genres(genres_str):
    try:
        # Mengubah string menjadi list menggunakan ast.literal_eval
        genres_list = ast.literal_eval(genres_str)
        # Menghilangkan spasi dan mengubah ke lowercase
        return [genre.strip().lower() for genre in genres_list]
    except Exception as e:
        # Jika ada kesalahan, kembalikan list kosong
        return []

# Terapkan pembersihan ke kolom 'genres'
data['genres'] = data['genres'].apply(clean_genres)

# Streamlit App
st.title("Game Recommendation System")
st.write("Rekomendasi game berdasarkan genre pilihan Anda.")

# Pilihan Genre
genre_columns = ['Tutorial', 'Gore', 'Photo Editing', 'Adventure', 'Accounting', 
                 'Massively Multiplayer', 'Racing', 'RPG', 'Web Publishing', 'Casual',
                 'Early Access', 'Sexual Content', 'Utilities', 'Sports', 'Violent', 
                 'Game Development', 'Action', 'Animation & Modeling', 'Free to Play',
                 'Strategy', 'Design & Illustration', 'Video Production', 'Documentary',
                 'Indie', 'Education', 'Software Training', 'Simulation', 'Nudity',
                 'Audio Production']

selected_genre = st.multiselect("Pilih genre game:", genre_columns)

# # Debugging genre yang dipilih oleh pengguna
# st.write("Genre yang dipilih oleh pengguna:", selected_genre)
selected_genre_clean = [genre.strip().lower() for genre in selected_genre]
# st.write("Genre yang dipilih setelah dibersihkan:", selected_genre_clean)

# Memverifikasi genre yang valid dalam dataset
valid_genres = set([genre for sublist in data['genres'] for genre in sublist])
st.write("Daftar genre yang valid:", valid_genres)

# Filter data berdasarkan genre
if selected_genre:
    # Filter data untuk game yang memiliki setidaknya satu genre yang dipilih
    filtered_data = data[data['genres'].apply(lambda genres: any(genre in genres for genre in selected_genre_clean))]

    # # Debugging: Menampilkan jumlah data yang terfilter
    # st.write(f"Jumlah game yang terfilter: {len(filtered_data)}")
    
    # Menampilkan beberapa game yang terfilter
    st.write("Beberapa game yang terfilter:", filtered_data[['name', 'genres']].head())

    recommended_games = filtered_data.sort_values(by='positive_ratings', ascending=False).head(5)

    # Menampilkan hasil
    if not recommended_games.empty:
        st.write(f"Menampilkan 5 game terbaik untuk genre yang dipilih:")
        st.dataframe(recommended_games[['name', 'positive_ratings', 'average_playtime', 'price']].head(5))
    else:
        st.write("Tidak ada game yang cocok dengan genre yang dipilih.")
else:
    st.write("Pilih setidaknya satu genre untuk melihat rekomendasi.")
