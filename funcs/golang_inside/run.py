import ctypes
import os

os.system("go build -buildmode=c-shared -o library.so library.go")

library = ctypes.cdll.LoadLibrary('./library.so')

func_name = library.func_name
func_name.argtypes = [ctypes.c_int64]
func_name.restype = ctypes.c_void_p

out = func_name(543534)

print(out)