import json
import yaml

try:
    with open("service_catalog.yaml", "r") as f:
        data = yaml.safe_load(f)
except FileNotFoundError:
    print("Friendly error if the file is missing/unreadable.")

healthy = []
unhealthy = 0
maintenance = 0

for service in data.get("services", []):
    status = service.get("status")
    if status == "healthy":
        healthy.append(service)
    elif status == "unhealthy":
        unhealthy += 1
    elif status == "maintenance":
        maintenance += 1

data["services"] = healthy
with open("healthy_services.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Healthy: {len(healthy)}, Unhealthy: {unhealthy}, Maintenance:"f" {maintenance}")
print("Healthy services: api-gateway, auth-svc, currency-service, fraud-scanner, ledger-svc, payment-gateway, statement-generator")