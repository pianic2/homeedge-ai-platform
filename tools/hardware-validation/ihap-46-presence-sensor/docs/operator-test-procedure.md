# Procedura operativa riproducibile — IHAP-46

## Obiettivo

Questa procedura permette a una persona diversa dall'autore del test di ripetere la stessa prova sullo stesso sensore o su un esemplare equivalente.

Una prova è riproducibile quando conserva sia i dati del dispositivo sia il contesto necessario per interpretarli: posizione del sensore, configurazione della stanza, azione umana, durata, ripetizione e anomalie.

## 1. Identificare gli oggetti fisici

Prima del flash assegnare un identificativo stabile a:

- modulo di presenza, ad esempio `LD2410C-OWNED-01`;
- board, ad esempio `ESP32C3-SM-01`;
- stanza, ad esempio `ROOM-STUDIO-01`;
- eventuale PIR di confronto.

Fotografare separatamente fronte e retro del sensore e della board quando l'esemplare non è già documentato. Non includere persone, indirizzi, schermate private o identificativi radio nei file pubblicabili.

## 2. Documentare il montaggio

Il sensore deve rimanere fermo durante l'intera run. Registrare:

- altezza dal pavimento in centimetri;
- parete o supporto utilizzato;
- direzione verso cui è orientato;
- distanza approssimativa da porta e punto di prova;
- posizione della porta durante ogni scenario;
- presenza di pareti adiacenti, tende, ventilatori o oggetti mobili.

Quando si confrontano due sensori, ripetere per quanto possibile la stessa geometria. Se il montaggio cambia, usare una nuova run ID.

## 3. Verificare il collegamento

Per la prima acquisizione LD2410C usare soltanto la ricezione UART:

```text
LD2410C VCC -> 5 V della board
LD2410C GND -> GND della board
LD2410C TX  -> ESP32-C3 GPIO5
```

Non collegare LD2410C RX, LD2410C OUT o PIR OUT finché pinout e livelli logici dell'esemplare non sono verificati.

Dopo il flash, il pre-flight deve confermare:

- avvio del firmware di test;
- ricezione di campioni;
- almeno un frame UART LD2410C valido, quando il canale UART è selezionato.

## 4. Usare sempre il runtime guidato

Il percorso operativo principale è:

```bash
python host/guided_run.py \
  --port /dev/ttyACM0 \
  --run-id <ID-UNIVOCO> \
  --sensor ld2410c_uart
```

Il runtime:

1. acquisisce i dati di contesto;
2. salva una copia immutabile del piano effettivo;
3. esegue il pre-flight;
4. stampa la preparazione dello scenario;
5. attende la conferma dell'operatore;
6. mostra un conto alla rovescia;
7. registra automaticamente inizio e fine;
8. ricorda a monitor l'azione durante il test;
9. consente di annotare anomalie;
10. genera risultati e report.

Non avviare manualmente il cronometro e non creare marker da un secondo terminale, salvo attività di debug del tool.

## 5. Regole durante le prove

- Eseguire una sola azione controllata per scenario.
- Non cambiare montaggio, sensibilità, cablaggio o disposizione della stanza durante una run.
- Mantenere uguali percorso, velocità e punto finale tra le ripetizioni.
- Evitare persone non coinvolte nell'area di test.
- Annotare movimenti involontari, porte aperte per errore, perdita di alimentazione o spostamenti del sensore.
- Interrompere e ripetere lo scenario quando una condizione d'invalidazione si verifica.
- Usare un nuovo `run-id` quando cambia un elemento della configurazione.

## 6. Azioni richieste per scenario

| Scenario | Azione principale dell'operatore | Stato reale della stanza |
|---|---|---|
| `ROOM_EMPTY_BASELINE` | Lasciare la stanza vuota e non passare nelle aree adiacenti immediate | Vuota |
| `ENTER_ROOM` | Entrare a passo normale e raggiungere il punto interno definito | Da vuota a occupata |
| `MOVING_LATERAL` | Camminare lateralmente tra due punti fissi | Persona in movimento |
| `MOVING_APPROACH` | Avvicinarsi e allontanarsi lungo lo stesso percorso | Persona in movimento |
| `SEATED_STILL` | Restare seduti senza movimenti volontari ampi | Persona sostanzialmente immobile |
| `MICRO_MOVEMENT` | Restare seduti digitando o voltando pagine | Persona con piccoli movimenti |
| `EXIT_CLEAR` | Uscire, chiudere la porta e restare lontani | Da occupata a vuota |
| `ADJACENT_DOOR_CLOSED` | Camminare fuori dalla stanza con porta chiusa | Stanza vuota, attività adiacente |
| `ADJACENT_DOOR_OPEN` | Camminare fuori senza oltrepassare la soglia | Stanza vuota, porta aperta |
| `WALL_MOVEMENT` | Muoversi dietro la parete adiacente | Stanza vuota, attività oltre parete |
| `NON_HUMAN_INTERFERENCE` | Attivare un solo oggetto mobile documentato | Stanza vuota |
| `REBOOT_PERSISTENCE` | Eseguire un reset dichiarato e continuare il movimento previsto | Dipende dal tentativo |
| `DIGITAL_UART_CONSISTENCY` | Alternare periodi chiaramente occupati e vuoti | Stato alternato |

Le istruzioni dettagliate e le condizioni d'invalidazione vengono lette da `config/operator-actions.json` e mostrate dal runtime prima di ogni ripetizione.

## 7. Sequenza consigliata

La prima sessione sul LD2410C dovrebbe procedere per gradi:

### Fase A — collegamento e risposta

- `ROOM_EMPTY_BASELINE`;
- `ENTER_ROOM`;
- `EXIT_CLEAR`.

### Fase B — requisito di presenza

- `MOVING_LATERAL`;
- `MOVING_APPROACH`;
- `SEATED_STILL`;
- `MICRO_MOVEMENT`.

### Fase C — confini della stanza

- `ADJACENT_DOOR_CLOSED`;
- `ADJACENT_DOOR_OPEN`;
- `WALL_MOVEMENT`, quando applicabile.

### Fase D — robustezza e interfacce

- `NON_HUMAN_INTERFERENCE`, quando applicabile;
- `REBOOT_PERSISTENCE`;
- `DIGITAL_UART_CONSISTENCY`, soltanto dopo la verifica elettrica dell'uscita digitale.

## 8. Quando una run è utilizzabile come evidence

Una run è utilizzabile quando:

- il pre-flight è passato;
- gli identificativi fisici sono presenti;
- montaggio e stanza sono documentati;
- ogni intervallo ha marker automatici di inizio e fine;
- le anomalie sono annotate;
- il piano effettivo è salvato;
- `results.json` e `report.html` vengono generati senza correzioni manuali dei dati.

Una run non dimostra da sola che il sensore sia adatto all'MVP. Le conclusioni richiedono confronto tra scenari, ripetizioni, alternative e confini definiti da IHAP-46.

## 9. Conservazione delle evidence

I dati grezzi restano in `runs/<RUN-ID>/` e non vengono pubblicati automaticamente.

Dopo la revisione si prepara un pacchetto sanitizzato che può contenere:

- manifest della run;
- configurazione del test;
- foto tecniche prive di metadati sensibili;
- risultati aggregati;
- grafici;
- limiti osservati;
- collegamento alla commit del firmware e del piano di test.

Non pubblicare identificativi radio, dati personali, percorsi domestici dettagliati o log non necessari alla riproduzione tecnica.
