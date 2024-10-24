create_sesso_enum = """
    CREATE TYPE sesso_enum AS ENUM ('M', 'F', 'Non Binario', 'Altro');
"""

create_modalità_accesso_enum = """
    CREATE TYPE modalità_accesso_enum AS ENUM ('Chiamata', 'Sportello');
"""

create_conoscenza_sportello_enum = """
    CREATE TYPE conoscenza_sportello_enum AS ENUM ('Iniziative', 'Volantinaggio', 'Passaparola', 'Altro');
"""

create_problem_accesso_enum = """
    CREATE TYPE problema_accesso_enum AS ENUM ('Agende Chiuse', 'Mancata presa in carico',
        'Mancato rispetto priorità', 'Mediazione/Stranier*', 'Servizi Sociali',
        'Servizi Consultoriali', 'Altro');
"""

create_ente_coinvolto_enum = """
    CREATE TYPE ente_coinvolto_enum AS ENUM ('Regione', 'Municipio', 'Comune', 'Altro');
"""

create_riscontro_enum = """
    CREATE TYPE riscontro_enum AS ENUM ('In corso', 'Positivo', 'Negativo', 'Parziale');
"""

create_anagrafica_table = """
    CREATE TABLE anagrafica_sportello (
        sq_id SERIAL PRIMARY KEY,
        data_inserimento DATE NOT NULL,
        nome VARCHAR NOT NULL,
        cognome VARCHAR NOT NULL,
        età INTEGER NOT NULL,
        sesso_genere sesso_enum,
        indirizzo VARCHAR NOT NULL,
        città VARCHAR,
        contatto VARCHAR NOT NULL,
        modalità_accesso modalità_accesso_enum,
        conoscenza_sportello conoscenza_sportello_enum,
        conoscenza_sportello_altro TEXT,
        descrizione_problema_accesso TEXT NOT NULL,
        problema_accesso TEXT NOT NULL,
        problema_di_accesso_altro VARCHAR,
        prestazione_richiesta VARCHAR NOT NULL,
        codice_prestazione VARCHAR,
        azioni_intraprese VARCHAR,
        ente_coinvolto ente_coinvolto_enum,
        ente_coinvolto_altro VARCHAR,
        struttura_coinvolta VARCHAR,
        documentazione VARCHAR,
        riscontro riscontro_enum,
        note_riscontro TEXT,
        data_riscontro DATE
    );
"""

create_role_enum = """
    CREATE TYPE role_enum AS ENUM ('admin', 'user');
"""

create_user_table = """
    CREATE TABLE users_login (
        username VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        role role_enum NOT NULL
    );
"""

select_user_table = """
    SELECT * FROM users_login;
"""

select_user_table_no_password = """
    SELECT username, role FROM users_login;
"""