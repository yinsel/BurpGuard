import argparse
from pathlib import Path
from multiprocessing import Process
from mitmproxy.tools.main import mitmdump

BASE_DIR = Path(__file__).parent

def addon(config, file):
    return BASE_DIR / config / file

def validate_config(config):
    required = [
        "ClientProxyHandler.py",
        "BurpProxyHandler.py"
    ]

    missing = []

    for file in required:
        path = addon(config, file)

        if not path.exists():
            missing.append(path)

    if missing:
        for path in missing:
            print(f"[!] Missing addon: {path}")

        raise SystemExit(1)


def run_proxy(script, port, verbose, mode=None):
    args = [
        "-s", str(script),
        "-p", str(port),
        "-k",
        "--http2"
    ]

    if mode:
        args += ["--mode", mode]

    if not verbose:
        args.insert(0, "-q")

    mitmdump(args=args)


def client_proxy(port, verbose, burp, config):
    run_proxy(
        addon(config, "ClientProxyHandler.py"),
        port,
        verbose,
        f"upstream:http://127.0.0.1:{burp}"
    )


def burp_proxy(port, verbose, proxy, config):
    run_proxy(
        addon(config, "BurpProxyHandler.py"),
        port,
        verbose,
        f"upstream:{proxy}" if proxy else None
    )


def main():
    parser = argparse.ArgumentParser(description="BurpGuard")

    parser.add_argument("-c", "--config", required=True)
    parser.add_argument("-p1", default=8081)
    parser.add_argument("-p2", default=8082)
    parser.add_argument("-burp", default=8080)
    parser.add_argument("-proxy", default="")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    validate_config(args.config)

    processes = [
        Process(
            target=client_proxy,
            args=(args.p1, args.verbose, args.burp, args.config),
            daemon=True
        ),
        Process(
            target=burp_proxy,
            args=(args.p2, args.verbose, args.proxy, args.config),
            daemon=True
        )
    ]

    for p in processes:
        p.start()

    print("[*] BurpGuard 启动成功")
    print(f"[*] 加载配置名称: {args.config}")
    print(f"[*] 客户端代理端口: {args.p1}")
    print(f"[*] Burp端口: {args.burp}")
    print(f"[*] Burp上游代理端口: {args.p2}")

    if args.proxy:
        print(f"[*] 最终请求代理: {args.proxy}")

    chain = f"客户端->{args.p1}->Burp({args.burp})->{args.p2}"

    if args.proxy:
        chain += f"->{args.proxy}"

    print(f"[*] 最终代理链: {chain}")

    for p in processes:
        p.join()


if __name__ == "__main__":
    main()