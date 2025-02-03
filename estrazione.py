import os
import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    """Estrae tutto il testo da un PDF e lo suddivide in sezioni."""
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    
    with open('test.txt', 'w') as file:
        file.write(text)

    # Identifica le sezioni basandosi sulle intestazioni principali (con ricerca esatta)
    headers = [
        "DATI ANAGRAFICI",
        "ATTIVITA'",
        "L'IMPRESA IN CIFRE",
        "DOCUMENTI CONSULTABILI",
        "AMMINISTRATORI",
        "SOCIALI",
        "CERTIFICAZIONE D'IMPRESA",
        "DOCUMENTI CONSULTABILI",
        "1 - Sede",
        "2 - Informazioni da statuto/atto costitutivo",
        "3 - Capitale e strumenti finanziari",
        "4 - Soci e titolari di diritti su azioni e quote",
        "5 - Amministratori",
        "6 - Sindaci, membri organi di controllo",
        "7 - Attivita', albi, ruoli e licenze",
        "8 - Sedi secondarie ed unita' locali",
        "9 - Aggiornamento Impresa"
    ]
    
    sections = {}
    current_header = None
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line in headers:  # Cerca una corrispondenza esatta
            current_header = line
            sections[current_header] = []
        elif current_header:
            sections[current_header].append(line)
    
    # Rimuovi il testo tra "REVOCA" e "carica" nella sezione "AMMINISTRATORI"
    if "5 - Amministratori" in sections:
        sections["5 - Amministratori"] = remove_revoke_to_carica(sections["5 - Amministratori"])
    
    # Combina le righe di ciascuna sezione in stringhe uniche
    for header in sections:
        sections[header] = "\n".join(sections[header])  # Unisce le righe senza newline extra
    
    return sections

def remove_revoke_to_carica(section_lines):
    """Rimuove tutte le porzioni di testo tra 'REVOCA' e 'Carica' nella sezione 'AMMINISTRATORI'."""
    section_text = "\n".join(section_lines)
    
    # Usa espressioni regolari per trovare e rimuovere tutte le occorrenze di testo tra "REVOCA" e "carica"
    # Il pattern ora cattura anche il testo tra righe diverse
    pattern = r'REVOCA[\s\S]*?Carica'  # Correlazione non avida tra "REVOCA" e "carica" su più righe
    modified_text = re.sub(pattern, '', section_text, flags=re.DOTALL)
    
    # Ritorna il testo modificato come lista di righe
    return modified_text.split("\n")

def print_selected_sections(sections, selected_sections):
    """Stampa le sezioni selezionate."""
    for section_name in selected_sections:
        if section_name in sections:
            print(f"\n--- Sezione: {section_name} ---\n")
            print(sections[section_name])
        else:
            print(f"Sezione '{section_name}' non trovata.")

# File PDF da processare
pdf_path = input("Inserisci il percorso del file PDF: ")
sections = extract_text_from_pdf(pdf_path)

# Visualizza le intestazioni delle sezioni
print("\nSezioni disponibili:")
section_keys = list(sections.keys())
for i, section_name in enumerate(section_keys, 1):
    print(f"{i}: {section_name}")

# Chiedi all'utente di scegliere più sezioni separando i numeri con una virgola
selected_input = input("\nInserisci i numeri delle sezioni da visualizzare, separati da virgola (ad esempio: 1, 3, 5): ")
selected_indices = [int(i.strip()) - 1 for i in selected_input.split(',')]  # Converte gli input in indici validi

# Ottieni le sezioni selezionate
selected_sections = [section_keys[i] for i in selected_indices if 0 <= i < len(sections)]

# Stampa le sezioni selezionate
print_selected_sections(sections, selected_sections)
