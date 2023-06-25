# Quantum Simulation and Quantum Computation produce different results
Below circuit is used:
```python
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
qc = QuantumCircuit(qr, cr)

k=1
h=1.5
alpha=-np.arcsin((1/np.sqrt(2))*(np.sqrt(1+h/np.sqrt(h**2+k**2))))
def sin(k,h):
    return (h*k)/np.sqrt((h**2+2*k**2)**2+(h*k)**2)
phi=0.5*np.arcsin(sin(k,h))

qc.ry(2*alpha,qr[0])
qc.x(qr[0])
qc.ry(2*phi,qr[0])
qc.h(qr[0])

qc.ry(2*alpha,qr[1])
qc.x(qr[1])
qc.ry(-2*phi,qr[1])
qc.h(qr[1])

qc.measure(qr,cr)
```
It is the receiver half of an energy transmission circuit. The original circuit can be found in the links section down below.

# Results
To produce data sets with simulation use command:
```sh
python3 shot.py -sim
```

To produce data sets with a quantum computer place your IBM key in key.py and use command:
```sh
python3 shot.py
```

Results will be placed in `data.bits`.

## simulation
```sh
./contact -bits data/data.bits.simulation.gz
...
0 0.037640
1 0.061990
2 0.337310
3 0.563060
```

## ibmq_quito during the day
```sh
./contact -bits data/data.q3.day.ibmq_quito.bits.gz
...
0 0.074950
1 0.065450
2 0.457500
3 0.402100
```

## ibmq_jakarta during the night
```sh
./contact -bits data/data.q5.night.ibmq_jakarta.bits.gz
...
0 0.053100
1 0.080750
2 0.348900
3 0.517250
```

# Links
* [Realization of Quantum Energy Teleportation on Superconducting Quantum Hardware](https://arxiv.org/abs/2301.02666)
* [Quantum-Energy-Teleportation](https://github.com/IKEDAKAZUKI/Quantum-Energy-Teleportation)