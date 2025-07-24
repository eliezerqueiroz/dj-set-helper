import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pprint

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

print("Tentando carregar as credenciais...")

# Pega as credenciais das variáveis de ambiente
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Verificação crucial: garante que as credenciais foram carregadas
if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ ERRO: Credenciais do Spotify não encontradas.")
    print("Certifique-se de que você criou um arquivo .env com SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET.")
else:
    print("✅ Credenciais carregadas com sucesso.")
    
    try:
        # Autenticação
        client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        print("✅ Autenticação com o Spotify bem-sucedida!")

        # Vamos fazer uma busca de teste para ver se tudo funciona!
        track_name_to_search = "Lose Yourself"
        artist_name_to_search = "Eminem"
        
        print(f"\nBuscando por '{track_name_to_search}' por '{artist_name_to_search}'...")

        query = f"track:{track_name_to_search} artist:{artist_name_to_search}"
        results = sp.search(q=query, type='track', limit=1)
        
        if results['tracks']['items']:
            track_info = results['tracks']['items'][0]
            track_id = track_info['id']
            
            print("🎶 Música encontrada! Buscando detalhes de áudio...")
            
            audio_features = sp.audio_features(track_id)[0]
            
            print("\n--- DETALHES ---")
            pprint.pprint({
                'name': track_info['name'],
                'artist': track_info['artists'][0]['name'],
                'bpm': audio_features['tempo'],
                'energy': audio_features['energy']
            })
            print("----------------\n")
            print("🎉 Teste concluído com sucesso!")
            
        else:
            print(f"\n🤷‍♀️ Nenhuma música encontrada.")

    except Exception as e:
        print(f"❌ Ocorreu um erro durante a comunicação com o Spotify: {e}")