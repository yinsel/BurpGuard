import argparse
import subprocess
import time
# 启动客户端代理
def start_client_proxy_handler(port: str, verbose: bool, burp: str) -> subprocess.Popen:
    command = f"""mitmdump -s ProxyHandler/ClientProxyHandler.py --mode upstream:http://127.0.0.1:{burp}@{port}  {'' if verbose else '-q'} -k"""
    return subprocess.Popen(command, shell=True)

# 启动 Burp 上游代理
def start_burp_proxy_handler(port: str, verbose: bool,proxy: str) -> subprocess.Popen:
    command = f"""mitmdump -s ProxyHandler/BurpProxyHandler.py {f"-p {port}" if proxy == "" else f"{f'--mode upstream:{proxy}@{port}'}"} {'' if verbose else '-q'} -k"""
    return subprocess.Popen(command, shell=True)

def main():
    parser = argparse.ArgumentParser(description="BurpGuard")
    parser.add_argument("-p1", "--port1", help="客户端代理端口, 默认8081", default="8081")
    parser.add_argument("-p2", "--port2", help="Burp上游代理端口, 默认8082", default="8082")
    parser.add_argument("-burp", "--burp", help="burp端口, 默认8080" ,default="8080")
    parser.add_argument("-proxy", "--proxy", help="最终请求代理", required=False, default="")
    parser.add_argument("-v", "--verbose", action="store_true", help="输出详细请求日志, 默认关闭", required=False, default=False)

    args = parser.parse_args()

    client_proxy_process = start_client_proxy_handler(args.port1, args.verbose, args.burp)
    time.sleep(0.1)
    burp_proxy_process = start_burp_proxy_handler(args.port2, args.verbose, args.proxy)

    print("[*] BurpGuard 启动成功")
    print(f"[*] 客户端代理端口: {args.port1}")
    print(f"[*] Burp端口: {args.burp}")
    print(f"[*] Burp上游代理端口: {args.port2}")
    if args.proxy:
        print(f"[*] 最终请求代理: {args.proxy}")
    print("[*] 最终代理链: " + f"客户端->{args.port1}->Burp({args.burp})->{args.port2}" + (f"->{args.proxy}" if args.proxy else ""))

    client_proxy_process.wait()
    burp_proxy_process.wait()

if __name__ == "__main__":
    main()
