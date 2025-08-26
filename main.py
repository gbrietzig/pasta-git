import json
import os
import sys
import urllib.request
import urllib.error


GITHUB_API = "https://api.github.com/rate_limit"


def build_request(url: str) -> urllib.request.Request:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-conn-test-script"
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, headers=headers, method="GET")


def main() -> int:
    try:
        request = build_request(GITHUB_API)
        with urllib.request.urlopen(request, timeout=15) as response:
            status_code = response.getcode()
            raw = response.read()
            payload = json.loads(raw.decode("utf-8"))

        rate = payload.get("resources", {}).get("core", {})
        remaining = rate.get("remaining")
        limit = rate.get("limit")
        reset_ts = rate.get("reset")

        print("Conexão com GitHub API: OK")
        print(f"HTTP {status_code}")
        print(f"Limite core: {remaining}/{limit} (reset epoch: {reset_ts})")
        if os.getenv("GITHUB_TOKEN"):
            print("Autenticação: utilizando GITHUB_TOKEN")
        else:
            print("Autenticação: não utilizada (modo anônimo)")
        return 0
    except urllib.error.HTTPError as err:
        try:
            detail = err.read().decode("utf-8")
        except Exception:
            detail = str(err)
        print("Falha ao acessar GitHub API (HTTPError)")
        print(f"Status: {err.code}")
        print(detail)
        return 1
    except urllib.error.URLError as err:
        print("Falha de rede ao acessar GitHub API (URLError)")
        print(str(err))
        return 1
    except Exception as err:
        print("Erro inesperado ao acessar GitHub API")
        print(str(err))
        return 1


if __name__ == "__main__":
    sys.exit(main())