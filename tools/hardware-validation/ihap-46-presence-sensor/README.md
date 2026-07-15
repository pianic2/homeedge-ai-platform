# IHAP-46 — Test reale del sensore di presenza

Questo pacchetto serve a eseguire prove fisiche riproducibili sul sensore LD2410C e, quando disponibile, su un sensore PIR di confronto.

L'obiettivo non è osservare semplicemente se il sensore "sembra funzionare". Ogni prova deve dichiarare:

- quale sensore e quale board sono stati usati;
- dove e come è stato montato il sensore;
- quale azione ha eseguito la persona;
- per quanto tempo è stata eseguita;
- quale stato reale della stanza era atteso;
- quali dati sono stati ricevuti;
- quali anomalie hanno reso il tentativo non valido.

Il runtime guida l'operatore a monitor, registra automaticamente l'inizio e la fine di ogni scenario e genera le evidence della run.

<!--
AI_AGENT_METADATA:
  issue: IHAP-46
  artifact_role: reproducible_physical_test_harness
  human_entrypoint: README.md
  detailed_human_procedure: docs/operator-test-procedure.md
  runtime_entrypoint: host/guided_run.py
  numerical_test_plan: config/test-plan.json
  operator_action_source: config/operator-actions.json
  raw_runs_default_location: runs/
  production_event_boundary: presence_detected_boolean_only
  detailed_radar_fields: laboratory_evidence_only
  decisions_allowed_here: none

HIDDEN_AGENT_RULES:
  - Do not treat harness creation or a successful run as sensor acceptance.
  - Do not create or accept an ADR from raw observations without Project Owner decision.
  - Do not move detailed radar telemetry into the MVP event contract.
  - Do not commit raw runs by default; prepare sanitized summaries and evidence manifests separately.
  - IHAP-49 owns quantitative power evidence.
  - IHAP-50 owns final wiring.
  - IHAP-51 owns enclosure and placement constraints.
-->

## Come si svolge una prova

Una run completa segue questo ordine:

1. identificazione del sensore, della board e della stanza;
2. montaggio del sensore in una posizione misurata e documentata;
3. compilazione e flash del firmware di test;
4. anteprima delle azioni che verranno richieste;
5. pre-flight automatico della connessione e dei dati;
6. esecuzione guidata degli scenari;
7. generazione di log, risultati JSON e report HTML;
8. revisione delle evidence prima di trarre conclusioni.

La procedura completa e le regole per rendere la prova ripetibile sono descritte in [`docs/operator-test-procedure.md`](docs/operator-test-procedure.md).

## Cosa serve

- una board ESP32-C3 compatibile con la baseline IHAP-44;
- il modulo LD2410C da testare;
- un computer con ESP-IDF 6.x e Python 3;
- alimentazione della board tramite USB del computer;
- una posizione di montaggio stabile;
- una stanza in cui sia possibile controllare ingresso, uscita e movimento nelle aree adiacenti;
- un PIR identificato, solo per le prove comparative che lo richiedono.

Prima di collegare un'uscita del sensore alla board, verificare il pinout e i livelli logici del modulo fisico.

La prima prova LD2410C può usare il collegamento UART già sperimentato:

```text
LD2410C VCC -> 5 V della board
LD2410C GND -> GND della board
LD2410C TX  -> ESP32-C3 GPIO5
```

Questo collegamento permette alla board di ricevere i dati del radar. L'ingresso RX del radar, l'uscita digitale LD2410C e il PIR restano disabilitati finché non vengono verificati e configurati esplicitamente.

## Preparazione del software

Dalla directory `firmware/`:

```bash
idf.py set-target esp32c3
idf.py menuconfig
idf.py build
idf.py -p /dev/ttyACM0 flash
```

Dalla directory principale di questo pacchetto:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r host/requirements.txt
```

## Leggere le istruzioni prima della prova

Prima di collegarsi al dispositivo, eseguire l'anteprima:

```bash
python host/guided_run.py --dry-run
```

Il comando stampa, per ogni scenario:

- scopo della prova;
- preparazione della stanza;
- azione che la persona deve eseguire;
- durata;
- numero di ripetizioni;
- condizioni che invalidano il tentativo.

Per visualizzare un solo scenario:

```bash
python host/guided_run.py \
  --dry-run \
  --scenario SEATED_STILL
```

## Eseguire una run reale

Per testare inizialmente il canale UART del LD2410C:

```bash
python host/guided_run.py \
  --port /dev/ttyACM0 \
  --run-id IHAP46-LD2410C-01 \
  --sensor ld2410c_uart
```

Il programma chiede e registra:

- nome dell'operatore;
- identificativo del sensore;
- identificativo della board;
- identificativo della stanza;
- altezza di montaggio;
- orientamento e posizione;
- note su pareti, porte e oggetti mobili.

Successivamente esegue un pre-flight. Se firmware, campioni o frame UART non sono disponibili, la prova si ferma senza iniziare gli scenari.

Per ogni scenario il monitor mostra una schermata simile:

```text
TEST: SEATED_STILL — Seated substantially still
Ripetizione: 1/3
Durata registrata: 10:00

Preparazione prima di iniziare
  1. Posiziona una sedia nel punto di prova.
  2. Siediti con porta chiusa e postura normale.

Azioni durante la registrazione
  1. Rimani seduto senza movimenti volontari ampi.
  2. Respira normalmente e mantieni la postura più stabile possibile.
```

La registrazione inizia solo quando l'operatore conferma che la preparazione è completa. Durante il test il runtime ristampa periodicamente l'azione da eseguire e il tempo rimanente.

L'inizio e la fine dello scenario vengono marcati automaticamente: non è necessario usare un secondo terminale.

## Eseguire solo alcuni scenari

Per una prima verifica breve:

```bash
python host/guided_run.py \
  --port /dev/ttyACM0 \
  --run-id IHAP46-LD2410C-SMOKE-01 \
  --sensor ld2410c_uart \
  --scenario ROOM_EMPTY_BASELINE \
  --scenario ENTER_ROOM \
  --scenario SEATED_STILL \
  --scenario EXIT_CLEAR
```

Le prove opzionali, come movimento dietro una parete o interferenze non umane, vengono incluse solo con:

```bash
--include-optional
```

## Testare altri canali

Dopo aver verificato cablaggio e livelli logici, è possibile aggiungere:

```bash
--sensor ld2410c_out
--sensor pir_out
```

Il report valuta soltanto i canali dichiarati nella run. Un PIR non collegato non deve essere incluso tra i canali selezionati.

## Evidence prodotte

Ogni run viene salvata in `runs/<RUN-ID>/`:

```text
run.json                    configurazione, operatore, stanza e montaggio
effective-test-plan.json    scenari e soglie realmente usati
serial.log                  output completo ricevuto dalla board
records.jsonl               record JSON con timestamp del computer
marks.jsonl                 inizio, fine e annotazioni degli scenari
capture-events.jsonl        connessioni, reset e riconnessioni seriali
results.json                valutazione leggibile dalle macchine
report.html                 report interattivo leggibile dagli umani
```

Non modificare i file di una run completata. Se una configurazione, un'azione o un'annotazione è errata, eseguire una nuova run con un nuovo identificativo.

I log grezzi restano locali per impostazione predefinita. Nel repository verranno pubblicati soltanto manifest, risultati riassunti ed evidence sanitizzate dopo la revisione.

## Verificare gli strumenti senza sensore

```bash
python host/ihap46.py selftest \
  --output runs/IHAP46-SELFTEST

python -m unittest discover -s tests -v
```

Questi comandi verificano il software di raccolta e analisi. Non sostituiscono le prove fisiche del dispositivo.
