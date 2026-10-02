import argparse
import requests
from registry_client import RegistryClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("service_id", type=int)
    args = parser.parse_args()
    client = RegistryClient()
    try:
        service = client.get_service(args.service_id)
        print(f"Status before: {service['status']}")
        client.patch_service(args.service_id,{"status": "maintenance"})
        print("Status after: maintenance")
        confirmed = client.get_service(args.service_id)
        if confirmed["status"] == "maintenance":
            print("Confirmed: status change stuck.")
        else:
            print(f"Confirmed status: {confirmed['status']}")
        client.delete_service(args.service_id)
        print(f"Deregistered {confirmed['name']} "f"(id {confirmed['id']}).")
    except requests.exceptions.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            print(f"Service with id {args.service_id} "f"not found, nothing to do.")
        else:
            print(f"[ERROR] HTTP error: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Registry error: {exc}")

if __name__ == "__main__":
    main()