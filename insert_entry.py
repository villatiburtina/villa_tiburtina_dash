import pandas as pd
import logging
import streamlit as st # type: ignore
from datalake.dbconnector import PostGresConnector
from utils.variables import (connection_str, sex_list, access_list, know_list,
                             access_problem_list, ente_list, status_list)
from utils.utils import (check_mandatory_fields_new_entry, check_consistency_altro_fields,
                         generate_insert_statement_anagrafica_sportello)

with st.form("Aggiungi Utente Sportello"):
    st.write("**Inserisci i dati dell'utente**")
    # NOME
    name = st.text_input('**Nome (Obbligatorio)**', value="", 
                         help="Nome dell'utente (obbligatorio)")
    st.write(f'Nome: {name}')
    # COGNOME
    surname = st.text_input("**Cognome (Obbligatorio)**", value="",
                            help="Cognome dell'utente (obbligatorio)")
    st.write(f'Cognome: {surname}')
    # ETA'
    age = st.slider("**Età (Obbligatorio)**", value=0,
                    help="""Età dell'utente (obbligatorio), nel caso non venga dichiarata
                            inserirne un spannometrica""")
    st.write(f'Età: {age}')
    # SESSO
    sex = st.selectbox("**Sesso**", options=sex_list, 
                       help="Sesso dell'utente")
    st.write(f'Sesso: {sex}')
    # GENERE
    gender = st.text_input("**Genere**",  value="",
                            help="Genere dell'utente, testo libero per descrivere il genere")
    st.write(f'Genere: {gender}')
    # INDIRIZZO
    address = st.text_input("**Indirizzo (Obbligatorio)**", value="",
                            help="Indirizzo dell'utente (obbligatorio), possibilmente specificare la via")
    st.write(f'Indirizzo: {address}')
    # CITTA'
    city = st.text_input("**Città**", value="", help="Città dell'utente")
    st.write(f'Città: {city}')
    # CONTATTO
    contact = st.text_input("**Contatto (Obbligatorio)**", value="",
                            help="""Contatto dell'utente (obbligatorio), può essere un numero di telefono
                                    o una mail""")
    st.write(f'Contatto: {contact}')
    # MODALITA' DI ACCESSO
    access_modality = st.selectbox("**Modalità di accesso**", options=access_list,
                                    help="Modalità di accesso allo sportello")
    st.write(f'Modalità di accesso: {access_modality}')
    # CONOSCENZA SPORTLLO
    know_how = st.selectbox("**Conoscenza Sportello**", options=know_list,
                                help="Come è venuto a conoscienza dello sportello")
    st.write(f'Conoscenza Sportello: {know_how}')
    # DESCRIZIONE PROBLEMA DI ACCESSO
    summary = st.text_input("**Descrizione del problema di accesso (Obbligatorio)**", value="",
                            help="Descrizione del problema di accesso (obbligatorio)")
    st.write(f'Descrizione del problema di accesso: {summary}')
    # PROBLEMA DI ACCESSO
    access_problem = st.selectbox("**Problema di accesso (Obbligatorio)**", options=access_problem_list,
                                    help="Seleziona una categoria di problema di accesso")
    st.write(f'Problema di accesso: {access_problem}')
    # PROBLEMA DI ACCESSO ALTRO
    if access_problem == "Altro":
        access_problem_altro = st.text_input("**Specificare il problema**", value="", 
                                        help="Specificare il problema di accesso se non presente in lista")
        st.write(f'Problema di accesso (altro): {access_problem_altro}')
    else:
        access_problem_altro = None
    # AZIONI INTRAPRESE
    actions = st.text_input("**Azioni intraprese**", value="", 
                            help="Specificare le azioni intraprese")
    st.write(f'Azioni intraprese: {actions}')
    # ENTE COINVOLTO
    involved_entity = st.selectbox("**Ente coinvolto**", options=ente_list,
                                    help="Specificare l'ente coinvolto")
    st.write(f'Ente coinvolto: {involved_entity}')
    # ENTE COINVOLTO ALTRO
    if involved_entity == "Altro":
        involved_entity_altro = st.text_input("**Specificare l'ente coinvolto**", value="", 
                                              help="Specificare l'ente coinvolto se non presente in lista")
        st.write(f'Ente coinvolto (altro): {involved_entity_altro}')
    else:
        involved_entity_altro = None
    # STRUTTURA COINVOLTA
    involved_structure = st.text_input("**Struttura coinvolta**", value="", 
                                        help="Specificare la struttura coinvolta")
    st.write(f'Struttura coinvolta: {involved_structure}')
    # DOCUMENTAZIONE
    documentation = st.text_input("**Documentazione**", value="", 
                                  help="Documentazione presentata dall'utente")
    st.write(f'Documentazione: {documentation}')
    # RISCONTRO
    status = st.selectbox("**Riscontro**", options=status_list,
                          help="Stato del riscontro")
    st.write(f'Riscontro: {status}')
    # DESCRIZIONE RISCONTRO
    notes = st.text_input("**Note Riscontro**", value="", 
                          help="Note aggiuntive sul riscontro")
    st.write(f'Note Riscontro: {notes}')
    # DATA RISCONTRO
    if status != "In corso":
        status_date = st.date_input("**Data Riscontro**", value=pd.Timestamp.now().date(),
                                    max_value=pd.Timestamp.now().date())
        st.write(f'Data Riscontro: {status_date}')
    else:
        status_date = None

    button_check = st.form_submit_button("Controlla Utente")
    button_save = st.form_submit_button("Salva Utente")

    new_entry= {
        'data_inserimento': pd.Timestamp.now().date().strftime("%Y-%m-%d"),
        'nome': name,
        'cognome': surname,
        'età': age,
        'sesso': sex if sex != "" else None,
        'genere': gender if gender != "" else None,
        'indirizzo': address,
        'città': city if city != "" else None,
        'contatto': contact,
        'modalità_accesso': access_modality if access_modality != "" else None,
        'conoscenza_sportello': know_how if know_how != "" else None,
        'descrizione_problema_accesso': summary,
        'problema_accesso': access_problem,
        'problema_di_accesso_altro': access_problem_altro if access_problem_altro != "" else None,
        'azioni_intraprese': actions if actions != "" else None,
        'ente_coinvolto': involved_entity if involved_entity != "" else None,
        'ente_coinvolto_altro': involved_entity_altro if involved_entity_altro != "" else None,
        'struttura_coinvolta': involved_structure if involved_structure != "" else None,
        'documentazione': documentation if documentation != "" else None,
        'riscontro': status,
        'note_riscontro': notes if notes != "" else None,
        'data_riscontro': status_date}


if button_check:
    
    if not check_mandatory_fields_new_entry(new_entry):
        st.error("""Compilare tutti i campi obbligatori: 
                 Nome, Cognome, Età, Indirizzo, Contatto, Descrizione Problema Accesso""")

    if not check_consistency_altro_fields(new_entry):
        st.error("""Se hai selezionato altro per i campi Problema di Accesso o Ente Coinvolto,
                 specificare il campo Altro corrispondente""")

    st.write("Il nuovo utente avrà i seguenti dati:")
    st.dataframe(pd.DataFrame(new_entry, index=[0]))

if button_save:
    sql_query = generate_insert_statement_anagrafica_sportello(new_entry)
    connector = PostGresConnector(connection_str=connection_str)
    try:
        logging.info(f"Inserting new user: {new_entry}")
        connector.run_query(sql_query)
        logging.error(f"User inserted: {new_entry}")
    except Exception as e:
        st.error(f"Errore durante il salvataggio dell'utente: {e}")
    st.write("Utente Salvato")