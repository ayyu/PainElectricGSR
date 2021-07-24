# Pain/Electric GSR E-Prime 3.0 Experiment

## Equipment

- Computer with script and 2+ USB ports
- Digitimer Train Generator DG2A
    - MODE = GATED
    - REPETITION = 100 Hz
    - DELAY = 0
    - POWER = ON
    - OUTPUT = 2nd setting
- Digitimer Stimulator DS7A
- NI DAQmx compatible device (e.g. NI USB-6343)
- QSTLab TCS II
- BNC to BNC cables
- 2x USB A to B cables
- 2x BNC to Ethernet cables (for Biopac)

### Connections

- Computer | USB > USB A to B > QSTLab TCS | COMPUTER IN/OUT
- Computer | USB > USB A to B cable > National Instruments
- National Instruments | AO 0 > BNC to Ethernet > Biopac Channel Input (GSR recording TTL for **pain**)
- National Instruments | AO 1 > BNC to BNC > DG2A | IN
- DG2A | OUTPUT (bottom) > BNC to BNC > DG7A | in
- DS7A | out > Biopac Channel Input (GSR recording TTL for **electric**)

## Experiment settings

The `.startupInfo3` file contains variables that need to be set any time you run the experiment.
Open the file, then enter the temperatures as calibrated for each subject.
Note that you will need to enter the serial port number assigned by the computer after plugging in the TCS II.
This port number is inconsistent and may change every time you restart the computer or plug in the TCS II.

To check what the current assigned port is, you can use [CoolTerm](https://freeware.the-meiers.org/):
1. Connect the TCS II using the USB cable
2. Open CoolTerm
3. Click on `Options`
4. Set the Baudrate to 115200
5. Choose a Port from the ones available (prefixed with COM)
6. Click `OK`
7. Click `Connect`
8. If you see the expected outputs (e.g. temperatures listed as the thermode updates), note the COM port you selected
9. If you don't see the expected output, go to step 3 again and choose the next available port
10. Close CoolTerm
11. Enter the noted port (number only) into the `.startupInfo3` file for `Serial.CommPort`

## Conditions

- 2 modalities:
    1. Pain (heat)
    2. Electric
- 6 intensity levels for each modality
- 2 x 6 = 12 conditions
- 5 trials per condition
- 5 x 12 = 60 trials total

## Run list requirements 
- pseudorandom preset lists
- 10 runs of 6 trials each
- rules:
    - first trial of run can't be two highest intensities (can't be 5/6)
    - one consecutive repetition is ok, but not more than twice (AAB, but not AAA)
    - any 2 consecutive trials must not be more than 3 levels apart

## Run structure
- 6 trials
    - pre-fixation (5 seconds)
    - stimulus (8 seconds)
    - post-fixation (1.5 seconds)
    - 4 rating screens
        - painful yes/no (10 seconds)
        - intensity 0-100 (10 seconds)
        - salience 0-100 (10 seconds)
        - unpleasantness 0-100 (10 seconds)
    - ITI with jitter (2-3 seconds)