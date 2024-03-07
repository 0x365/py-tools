package main

import (
   "C"
)

//export func_name
func func_name(in_num_as_c C.int) C.int {
	in_num := int(in_num_as_c)
	
	// Execute stuff
	
	return C.int(in_num)
}


func main() {}