import requests
ngrok = requests.get("http://127.0.0.1:4040/api/tunnels")
url = [t['public_url'] for t in ngrok.json()['tunnels'] if t['proto'] == 'https'][0]
with open('.env', 'r') as f:
    lines = f.readlines()
with open('.env', 'w') as f:
    for line in lines:
        if line.startswith("NGROK_URL="):
            f.write(f"NGROK_URL={url}\n")
        elif line.startswith("WEBHOOK_URL="):
            f.write(f"WEBHOOK_URL={url}/webhook\n")
        else:
            f.write(line)
print("Updated .env with current ngrok URL:", url)
