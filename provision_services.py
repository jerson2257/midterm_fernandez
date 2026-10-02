from registry_client import RegistryClient
import requests

NEW_SERVICES = [
    {
        "name": "rewards-svc",
        "version": "0.1.0",
        "owner": "engagement@aeropay.io",
        "environment": "staging",
        "status": "healthy",
        "health_url": "/health/rewards",
        "dependencies": ["notification-svc"],
    },
    {
        "name": "audit-trail-svc",
        "version": "1.0.0",
        "owner": "compliance@aeropay.io",
        "environment": "production",
        "status": "healthy",
        "health_url": "/health/audit-trail",
        "dependencies": [],
    },
    {
        "name": "rate-limiter",
        "version": "0.9.0",
        "owner": "platform@aeropay.io",
        "environment": "production",
        "status": "healthy",
        "health_url": "/health/rate-limiter",
        "dependencies": ["api-gateway", "auth-svc"],
    },
]

def fetch_all_services(client):
    collected = []
    offset = 0
    limit = 10
    while True:
        page = client.get_services(limit=limit, offset=offset)
        collected.extend(page["results"])
        offset += limit
        if offset >= page["count"]:
            break
    return collected

def main():
    client = RegistryClient()
    try:
        services = fetch_all_services(client)
        existing = {service["name"]: service for service in services}
        for payload in NEW_SERVICES:
            name = payload["name"]
            if name in existing:
                print(f"Already registered: {name}")
                continue
            created = client.create_service(payload)
            service_id = created["id"]
            verified = client.get_service(service_id)
            print(f"Registered {verified['name']} "f"with id {verified['id']}.")
    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Could not reach registry: {exc}")

if __name__ == "__main__":
    main()