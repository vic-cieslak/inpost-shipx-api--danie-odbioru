
# Skrypt integracji z API InPost ShipX

Te repozytorium zawiera skrypt, który integruje się z API InPost ShipX w celu tworzenia przesyłek i zamawiania odbiorów. Skrypt obsługuje interakcje z API, w tym wysyłanie szczegółów przesyłek, zarządzanie (niektórymi) błędami i pobieranie etykiet wysyłkowych (wysyłanie ich do klienta w celu natychmiastowego pobrania). Skrypt jest używany na produkcji. Jest mało optymalny ale działa. 

## Funkcje

- Tworzenie przesyłki z danymi nadawcy i odbiorcy
- Obsługa różnych wymiarów i wag paczek
- Pobieranie etykiet wysyłkowych w formacie PDF
- Obsługa błędów dotyczących nadmiernych rozmiarów lub wagi paczek
- Łatwo konfigurowalne dane uwierzytelniające API

## Wymagania

- Python 3.x
- Biblioteka `requests`
- Biblioteka `Flask` (tylko do jsonify, bo jest używany jako część apki flaskowej)

## Instalacja

1. Sklonuj to repozytorium:

   ```bash
   git clone https://github.com/yourusername/inpost-shipx-api.git
   cd inpost-shipx-api
   ```

2. Zainstaluj wymagane pakiety Pythona:

   ```bash
   pip install requests Flask
   ```

## Konfiguracja

1. Otwórz plik skryptu i dodaj swój URL API oraz token Bearer na początku pliku:

   ```python
   # Dodaj swoje sekrety tutaj
   API_URL = 'https://api-shipx-pl.easypack24.net/v1/organizations/<TWOJE_ID>'
   BEARER_TOKEN = 'YOUR_BEARER_TOKEN'
   ```

2. Zastąp wartości zastępcze w sekcji przykładowego użycia na końcu skryptu rzeczywistymi wartościami:

   ```python
   if __name__ == '__main__':
       # Przykładowe użycie (zastąp te wartości rzeczywistymi)
       client_contact = {
           'imie': 'Jan',
           'nazwisko': 'Kowalski',
           'emailAddress': 'jan.kowalski@example.com',
           'phoneNumber': '123-456-789',
           'companyName': None  # lub 'Jakakolwiek Firma'
       }
       client_address = {
           'street': 'Główna',
           'houseNumber': '123',
           'apartmentNumber': '',
           'city': 'Przykładowe Miasto',
           'postalCode': '12345'
       }
       package = {
           'length': 100,
           'width': 50,
           'height': 30,
           'weight': 2,
           'uwagi': 'Ostrożnie'
       }
       response = create_shipment(client_contact, client_address, package)
       print(response)
   ```

## Użycie

Uruchom skrypt:

```bash
python script.py
```

To spowoduje wykonanie funkcji `create_shipment` z podanymi przykładowymi wartościami. Zmodyfikuj słowniki `client_contact`, `client_address` i `package`, aby przetestować z różnymi danymi.

## Licencja

Ten projekt jest licencjonowany na licencji MIT. Zobacz plik [LICENSE](LICENSE) po więcej szczegółów.

## Wkład

Wkłady są mile widziane! Prosimy o forkowanie repozytorium i przesyłanie pull requestów z twoimi zmianami.

## Kontakt

W przypadku pytań lub wsparcia prosimy o kontakt. 
