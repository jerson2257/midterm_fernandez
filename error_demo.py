import requests
from registry_client import RegistryClient

def main():
    print("Testing 401 error...")
    wrong_client = RegistryClient(
        api_key="wrong-key")
    try:
        wrong_client.get_services()
    except requests.exceptions.HTTPError as exc:
        print("What happened: 401 Unauthorized")
        print("Probable cause: wrong or missing API key.")
    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Request failed: {exc}")

    print()
    print("Testing 404 error...")
    client = RegistryClient()
    try:
        client.get_service(9999)
    except requests.exceptions.HTTPError as exc:
        print("What happened: 404 Not Found")
        print("Probable cause: service with id 9999 does not exist.")
    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Request failed: {exc}")

if __name__ == "__main__":
    main()