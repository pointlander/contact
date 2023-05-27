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

qr = QuantumRegister(2)
cr = ClassicalRegister(2)

qc = QuantumCircuit(qr, cr)

# Define the parameters
k=1
h=1.5

#Prepare the ground state
alpha=-np.arcsin((1/np.sqrt(2))*(np.sqrt(1+h/np.sqrt(h**2+k**2))))

qc.ry(2*alpha,qr[0])
qc.x(qr[0])

def sin(k,h):
    return (h*k)/np.sqrt((h**2+2*k**2)**2+(h*k)**2)

phi=0.5*np.arcsin(sin(k,h))

qc.ry(2*phi,qr[0])

qc.h(qr[0])
qc.measure(qr[0],cr[0])


qc.ry(2*alpha,qr[1])
qc.x(qr[1])
qc.ry(-2*phi,qr[1])
qc.h(qr[1])
qc.measure(qr[1],cr[1])

qc.draw()

# Enable your account on Qiskit, replace 'My_API_Token' with your newly generated token
IBMQ.save_account(key.KEY, overwrite=True)
IBMQ.load_account()
# After loading credentials we query the backends
# IBMQ.backends()

#IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')

from qiskit.providers.ibmq import least_busy

small_devices = provider.backends(filters=lambda x: x.configuration().n_qubits >= 0
                                   and not x.configuration().simulator)
backend=least_busy(small_devices)

print("Name", backend.name())
print("Status", backend.status())
print("Limit",backend.job_limit())
print("Remaining Jobs",backend.remaining_jobs_count())
print("Number of Active Jobs",backend.active_jobs())

n_shots=2000
qc_total = transpile(qc, backend)

job = execute(qc_total, backend=backend, shots=n_shots, memory=True)
job.status()

results = job.result()
lines = results.get_memory(qc_total)
with open('data.bits', 'w') as f:
    for line in lines:
        f.write(f"{line}\n")

