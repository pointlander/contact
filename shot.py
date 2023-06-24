# Copyright 2023 The Contact Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import key
import numpy as np 
from qiskit import * #qiskit
from qiskit.visualization import plot_histogram, plot_bloch_multivector, array_to_latex
from qiskit import Aer
from qiskit.extensions import Initialize
from qiskit import QuantumCircuit, QuantumRegister, transpile, execute
from qiskit.quantum_info import random_statevector
from qiskit.quantum_info import partial_trace, entropy
import qiskit.quantum_info as qi
import sys
from qiskit_ibm_provider import IBMProvider

sim = False
cnot = False
printBackends = False
for option in sys.argv:
    if option == "-sim":
        sim = True
    if option == "-cnot":
        cnot = True
    if option == "-print":
        printBackends = True

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

if cnot:
    qc.cnot(qr[0], qr[1])

qc.measure(qr,cr)

qc.draw()

if sim:
    simulator = Aer.get_backend('qasm_simulator')
    n_shots=100000
    qc_meas = QuantumCircuit(qr,cr)
    qc_meas.measure(qr,cr)
    qc_total = qc.compose(qc_meas)  
    job = execute(qc_total, backend=simulator, shots=n_shots, memory=True)

    results = job.result()
    lines = results.get_memory(qc_total)
    with open('data.bits', 'w') as f:
        for line in lines:
            f.write(f"{line}\n")
    quit()

IBMProvider.save_account(key.KEY, overwrite=True)
provider = IBMProvider(instance="ibm-q/open/main")
if printBackends:
    for b in provider.backends():
        status = b.status()
        print(b.name + ' ' + str(status.operational) + ' ' + str(status.pending_jobs))
    quit()
#backend = provider.get_backend("ibmq_quito")
backend = provider.get_backend("ibmq_jakarta")

#print("Name", backend.name())
#print("Status", backend.status())
#print("Limit",backend.job_limit())
#print("Remaining Jobs",backend.remaining_jobs_count())
#print("Number of Active Jobs",backend.active_jobs())

n_shots=20000
qc_total = transpile(qc, backend=backend)
job = backend.run(qc_total, shots=n_shots, memory=True)
job.status()

results = job.result()
lines = results.get_memory(qc_total)
with open('data.bits', 'w') as f:
    for line in lines:
        f.write(f"{line}\n")

