import tvm
from tvm import te
import numpy as np
import os

# Define the compute
n = 1024
A = te.placeholder((n,), name="A", dtype="float32")
B = te.placeholder((n,), name="B", dtype="float32")
C = te.compute((n,), lambda i: A[i] + B[i], name="C")

# Create schedule and vectorize
s = te.create_schedule(C.op)
i = C.op.axis[0]
xo, xi = s[C].split(i, factor=4)
s[C].vectorize(xi)

# Target: ARM with NEON
target = tvm.target.Target("llvm -mtriple=armv7l-linux-gnueabihf -mcpu=cortex-a53 -mattr=+neon")

# Build the lowered function
mod = tvm.build(s, [A, B, C], target=target, name="vec_add")

# Export to object file
path_o = "vec_add.o"
path_so = "vec_add.so"
mod.save(path_o)  # object file
mod.export_library(path_so)  # shared library

print("Exported object and shared library.")

# Generate a main C program that uses this
main_c = """
#include <tvm/runtime/c_runtime_api.h>
#include <tvm/runtime/module.h>
#include <tvm/runtime/registry.h>
#include <dlpack/dlpack.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Load module
    TVMModuleHandle mod;
    TVMModLoadFromFile("vec_add.so", "so", &mod);

    // Prepare input arrays
    int n = 1024;
    float* a = (float*) malloc(n * sizeof(float));
    float* b = (float*) malloc(n * sizeof(float));
    float* c = (float*) malloc(n * sizeof(float));
    for (int i = 0; i < n; ++i) {
        a[i] = i * 1.0f;
        b[i] = i * 2.0f;
    }

    // Wrap inputs as DLTensor
    DLTensor da, db, dc;
    TVMArrayAlloc((int64_t[]){n}, 1, kDLFloat, 32, 1, kDLCPU, 0, &da);
    TVMArrayAlloc((int64_t[]){n}, 1, kDLFloat, 32, 1, kDLCPU, 0, &db);
    TVMArrayAlloc((int64_t[]){n}, 1, kDLFloat, 32, 1, kDLCPU, 0, &dc);

    memcpy(da.data, a, n * sizeof(float));
    memcpy(db.data, b, n * sizeof(float));

    // Get function and call
    TVMFunctionHandle fadd;
    TVMModGetFunction(mod, "vec_add", 0, &fadd);
    TVMValue args[3];
    int type_codes[3] = {kTVMDLTensorHandle, kTVMDLTensorHandle, kTVMDLTensorHandle};
    args[0].v_handle = &da;
    args[1].v_handle = &db;
    args[2].v_handle = &dc;
    TVMFuncCall(fadd, args, type_codes, 3, NULL);

    memcpy(c, dc.data, n * sizeof(float));

    for (int i = 0; i < 10; ++i) {
        printf("c[%d] = %f\\n", i, c[i]);
    }

    // Cleanup
    free(a); free(b); free(c);
    TVMArrayFree(&da);
    TVMArrayFree(&db);
    TVMArrayFree(&dc);
    return 0;
}
"""

# Write main C file
with open("main_vec_add.c", "w") as f:
    f.write(main_c)

print("Generated main_vec_add.c")

# Optional: Compile into executable for ARM using cross compiler
# Example command (run outside Python):
# arm-linux-gnueabihf-gcc -o vec_add_exec main_vec_add.c vec_add.o -ltvm_runtime -ldl -pthread

