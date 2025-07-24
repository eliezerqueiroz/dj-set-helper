# test_spotify.py (Versão de Depuração Avançada com a biblioteca 'requests')

import os
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pprint

# --- PASSO 0: CONFIGURAÇÃO ---
load_dotenv()
print("--- INICIANDO PROCESSO DE DEPURAÇÃO AVANÇADA ---")
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ ERRO CRÍTICO: Credenciais não encontradas.")
    exit()

# --- ETAPA 1: OBTER O TOKEN DE ACESSO DIRETAMENTE ---
print("\n--- ETAPA 1: OBTENDO ACCESS TOKEN ---")
access_token = None
try:
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    access_token = client_credentials_manager.get_access_token(as_dict=False)
    if not access_token:
        raise Exception("Token de acesso retornado é nulo.")
    print("✅ Access Token obtido com sucesso!")
except Exception as e:
    print(f"❌ ERRO CRÍTICO ao obter token: {e}")
    exit()

# --- ETAPA 2: BUSCAR A MÚSICA USANDO REQUESTS ---
print("\n--- ETAPA 2: BUSCANDO A MÚSICA (MANUALMENTE) ---")
track_name_to_search = "Lose Yourself"
artist_name_to_search = "Eminem"
track_id = None
try:
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"track:{track_name_to_search} artist:{artist_name_to_search}", "type": "track", "limit": 1}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status() # Lança um erro se a requisição falhar (não for 2xx)
    
    results = response.json()
    track_info = results['tracks']['items'][0]
    track_id = track_info['id']
    print(f"✅ Música encontrada: '{track_info['name']}' | ID: {track_id}")

except Exception as e:
    print(f"❌ ERRO durante a busca manual: {e}")

# --- ETAPA 3: BUSCAR AUDIO FEATURES USANDO REQUESTS (O ENDPOINT NOVO E CORRETO) ---
print("\n--- ETAPA 3: BUSCANDO AUDIO FEATURES (MANUALMENTE) ---")
if track_id:
    try:
        # Usando o endpoint NOVO, que aceita múltiplos IDs
        features_url = f"https://api.spotify.com/v1/audio-features"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"ids": track_id} # Passando o ID como um parâmetro de busca

        print(f"Fazendo requisição GET para: {features_url} com params: {params}")
        response = requests.get(features_url, headers=headers, params=params)

        if response.status_code == 200:
            # O resultado para este endpoint é uma lista dentro de uma chave 'audio_features'
            features = response.json()['audio_features'][0]
            print("✅🎉 SUCESSO! Audio features recebidas diretamente!")
            pprint.pprint(features)
        else:
            print("--- INFORMAÇÕES DO ERRO DA API ---")
            print(f"   URL da Requisição: {response.url}")
            print(f"   Status Code: {response.status_code}")
            print(f"   Resposta da API: {response.text}")
            print("------------------------------------")
    except Exception as e:
        print(f"❌ ERRO durante a busca de features manual: {e}")