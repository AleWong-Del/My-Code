from PIL import Image
import streamlit as st

try:
  import pytesseract

  OCR_DISPONIVEL = True
except ImportError:
  OCR_DISPONIVEL = False

st.set_page_config(
    page_title="ChipLens - Bancada", page_icon="🔍", layout="centered"
)

# Catálogo Validado de Armazenamento
CATALOGO_ARMAZENAMENTO = {
    "8 GB": [
        "KMFN10012M-B214",
        "KMFN10012M",
        "KMFNX0012M-B214",
        "KMFNX0012M",
        "H9TQ64A8GTMCUR-KUM",
        "H9TQ64A8GTMCUR",
        "JZ005",
        "MT29TZZZ8D5BKFAH",
        "08EMCP08-NL3DT227",
        "08EMCP08",
    ],
    "16 GB": [
        "KMDD60018M-B320",
        "KMDD60018M",
        "KMFE60012M-B214",
        "KMFE60012M",
        "KMQE60013M-B318",
        "KMQE60013M",
        "KMQN10006B-B318",
        "KMQN10006B",
        "THGBMFG7C1LBAIL",
        "H9HP53ACPMMDARKMM",
        "H9TQ17ABJTBCUR-KUM",
        "H9TQ17ABJTBCUR",
        "JZ033",
        "JZ064",
        "KLMAG1JETD",
        "KLMAG1JENB-B031",
        "KLMAG1JENB",
        "KMOE10013M",
    ],
    "32 GB": [
        "KMRX1000BM-B614",
        "KMRX1000BM",
        "KMRX100BN-B614",
        "KMRX100BN",
        "KMDH6001DA-B422",
        "KMDH6001DA",
        "KLMAG1JETD-B041",
        "THGBMBG7C2KBAIL",
        "THGBMFG8C2LBAIL",
        "H9TQ26ADFTBCUR-KUM",
        "H9TQ26ADFTBCUR",
        "H9TQ27ADFTMC",
        "JZ028",
        "JZ109",
        "SPA7DMVE8-S",
        "KMGX6001BM-B514",
        "KMGX6001BM",
        "KM4X6001KM-B321",
        "KM4X6001KM",
        "SPDV6NN1PX4K9B",
        "KMQX10013M-B419",
        "KMQX10013M",
        "KMQD60013M-B318",
        "KMQD60013M",
    ],
    "64 GB": [
        "KLUFG8RHDA-B2D1",
        "KLUFG8RHDA",
        "KLUCG4J1ED-B0C1",
        "KLUCG4J1ED",
        "KMDP6001DA-B425",
        "KMDP6001DA",
        "KMDP6001DB-B425",
        "KMDP6001DB",
        "JZ128",
        "JZ185",
        "JY941",
        "KMRC10014M",
        "KLMCG4JENB-B043",
        "KLMCG4JENB",
        "KMGP6001BA-B514",
        "KMGP6001BA",
    ],
    "128 GB": [
        "KLUDG4U1EA-B0C1",
        "KLUDG4U1EA",
        "KM8V7001JM-B813",
        "KM8V7001JM",
        "KM2V7001CM-B706",
        "KM2V7001CM",
        "KMDV6001DM-B620",
        "KMDV6001DM",
        "H9HQ15ACPMBD-AR",
        "H9HQ15ACPMBD",
        "H28S8Q302CMR",
        "MT29VZZZAD8GQFSM-046",
        "MT29VZZZAD8GQFSM",
        "JZ151",
        "KM5L9001DM-B424",
        "KM5L9001DM",
        "H9QT0G6CN6",
    ],
    "256 GB": [
        "KLUEG8U1EA-B0C1",
        "KLUEG8U1EA",
        "KM8V8001JM-B813",
        "KM8V8001JM",
        "KM2V8001CM-B707",
        "KM2V8001CM",
        "KM8F8001JM-B813",
        "KM8F8001JM",
        "H9HQ21AECMMD-AR",
        "H9HQ21AECMMD",
        "H28S9O302BMR",
        "MT29VZZZBD9GQFSM-046",
        "MT29VZZZBD9GQFSM",
        "JZ205",
    ],
    "512 GB": [
        "KLUFG8U1EM-B0C1",
        "KLUFG8U1EM",
        "KM8F9001JM-B813",
        "KM8F9001JM",
        "H9HQ22AFAMMD-AR",
        "H9HQ22AFAMMD",
        "H28U9Q302CMR",
        "THGJFJT2T84BATP",
    ],
}

# Catálogo Validado de CPUs
CATALOGO_CPUS = {
    "CPU 2A": ["MSM8210", "0VV"],
    "CPU (Modelo Padrão)": [
        "SM6115",
        "200-AA",
        "SDM450",
        "01-AA",
        "MSM8953",
        "3AB",
        "D01-AC",
        "MT6762V",
        "UMS9230",
        "UNISOC UMS9230",
        "MT6765V",
        "SM6225",
        "000-AD",
        "MSM8916",
        "MSM8917",
        "EXYNOS 7570",
        "7570",
    ],
}


def analisar_codigo(texto_entrada):
  texto = texto_entrada.upper().strip()
  # Remove espaços ou quebras de linha para facilitar leitura do OCR
  texto_limpo = texto.replace(" ", "").replace("\n", "")

  armazenamento_encontrado = "Não identificado"
  codigo_arm_matched = ""

  # Prioriza códigos mais longos primeiro para evitar falsos positivos (ex: KLMAG1JETD-B041 vs KLMAG1JETD)
  todos_arm = []
  for cap, codigos in CATALOGO_ARMAZENAMENTO.items():
    for cod in codigos:
      todos_arm.append((len(cod), cap, cod))
  todos_arm.sort(reverse=True)

  for _, cap, cod in todos_arm:
    if cod in texto or cod.replace("-", "") in texto_limpo:
      armazenamento_encontrado = cap
      codigo_arm_matched = cod
      break

  cpu_encontrada = "Não identificada"
  codigo_cpu_matched = ""

  for tipo_cpu, codigos in CATALOGO_CPUS.items():
    for cod in codigos:
      if cod in texto or cod.replace("-", "") in texto_limpo:
        cpu_encontrada = tipo_cpu
        codigo_cpu_matched = cod
        break
    if codigo_cpu_matched:
      break

  return (
      armazenamento_encontrado,
      codigo_arm_matched,
      cpu_encontrada,
      codigo_cpu_matched,
  )


# Interface Mobile
st.title("🔍 ChipLens - Bancada")
st.caption("Aponte a câmara para o chip ou digite o código abaixo")

# 1. Câmara do Telemóvel
imagem_capturada = st.camera_input("Capturar chip com a câmara")

texto_ocr = ""
if imagem_capturada is not None:
  imagem = Image.open(imagem_capturada)
  with st.spinner("A ler código na imagem..."):
    if OCR_DISPONIVEL:
      try:
        texto_ocr = pytesseract.image_to_string(imagem)
      except Exception:
        pass

# 2. Campo Manual / Correção Rápida (caso o reflexo atrapalhe a câmara)
codigo_manual = st.text_input(
    "Ou digite/cole o código do chip (ex: KMQD60013M, MSM8210):",
    value=texto_ocr.strip(),
)

texto_para_analisar = codigo_manual if codigo_manual else texto_ocr

if texto_para_analisar:
  arm, cod_arm, cpu, cod_cpu = analisar_codigo(texto_para_analisar)

  st.divider()
  st.subheader("📋 Diagnóstico da Placa:")

  if arm != "Não identificado":
    st.success(f"💾 **Armazenamento:** {arm}  *(Ref: {cod_arm})*")
  else:
    st.warning("💾 **Armazenamento:** Não identificado na lista")

  if cpu != "Não identificada":
    if cpu == "CPU 2A":
      st.error(f"⚙️ **Processador:** {cpu}  *(Ref: {cod_cpu})*")
    else:
      st.info(f"⚙️ **Processador:** {cpu}  *(Ref: {cod_cpu})*")
  else:
    st.warning("⚙️ **Processador:** Não identificado na lista")