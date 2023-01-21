operation_table = {
	
	'add' : {'type':'Rtype','opcode':'0x00','funct':'0x20'},
	'addu': {'type':'Rtype','opcode':'0x00','funct':'0x21'},
	'and' : {'type':'Rtype','opcode':'0x00','funct':'0x24'},
	'or'  : {'type':'Rtype','opcode':'0x00','funct':'0x25'},
	'sub' : {'type':'Rtype','opcode':'0x00','funct':'0x22'},
	'subu': {'type':'Rtype','opcode':'0x00','funct':'0x23'},
	'sll' : {'type':'Rtype','opcode':'0x00','funct':'0x00'},
	'srl' : {'type':'Rtype','opcode':'0x00','funct':'0x02'},
	'sra' : {'type':'Rtype','opcode':'0x00','funct':'0x03'},
	'slt' : {'type':'Rtype','opcode':'0x00','funct':'0x2a'},
	'xor' : {'type':'Rtype','opcode':'0x00','funct':'0x26'},
	'jr'  : {'type':'Rtype','opcode':'0x00','funct':'0x08'},
	'addi':	{'type':'Itype','opcode':'0x08'},
	'andi': {'type':'Itype','opcode':'0x0c'},
	'slti': {'type':'Itype','opcode':'0x0a'},
	'beq' : {'type':'Itype','opcode':'0x04'},
	'bgez': {'type':'Itype','opcode':'0x01'},
	'bne' : {'type':'Itype','opcode':'0x05'},
	'lw'  : {'type':'Itype','opcode':'0x23'},
	'sw'  : {'type':'Itype','opcode':'0x2b'},
	'j'	  : {'type':'Jtype','opcode':'0x02'},
	'jal' : {'type':'Jtype','opcode':'0x03'}

}

register_table = {
	'0'	: '0x0',
	'zero' : '0x0',
	'at'   : '0x1',
	'v0'   : '0x2',
	'v1'   : '0x3',
	'a0'   : '0x4',
	'a1'   : '0x5',
	'a2'   : '0x6',
	'a3'   : '0x7',
	't0'   : '0x8',
	't1'   : '0x9',
	't2'   : '0xA',
	't3'   : '0xB',
	't4'   : '0xC',
	't5'   : '0xD',
	't6'   : '0xE',
	't7'   : '0xF',
	's0'   : '0x10',
	's1'   : '0x11',
	's2'   : '0x12',
	's3'   : '0x13',
	's4'   : '0x14',
    's5'   : '0x15',
	's6'   : '0x16',
	's7'   : '0x17',
	't8'   : '0x18',
	't9'   : '0x19',
	'k0'   : '0x1A',
	'k1'   : '0x1B',
    'gp'   : '0x1C',
	'sp'   : '0x1D',
	'fp'   : '0x1E',
    'ra'   : '0x1F'
	}


def sign_extend(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

def check_labels(instruction,mode,pc,line,label,btable):
	 # GUI needs these 
  #  values to be defined here as well
	x = instruction.replace(","," ")
	sep = '#'
	x = x.rsplit(sep,1)[0]
#	print(x)
	x = x.replace("$"," ")
	x = x.replace("("," ")
	x = x.replace(")"," ")
	x = x.replace(":"," ")
	x = x.replace("–","-")
	x = x.split()

	a = 2
	if x == []:
		line = int(line) - 1
		return line
	#print (x)
	#if mode == '2':
		#print(line)
	if x[0] in operation_table:
		op = x[0]
		if op in ['beq','bgez','bne']:
			tnp = []
			tnp.append(x[0])
			tnp.append(hex(int(pc,16) + int(line)*4))
			btable.append(tnp)
			#print(btable)
		return line
	elif x[1] in operation_table:
		#print('FOUND label')
		if x[1] in ['move']:
			x[1] = 'add'
			op = x[1]
			x.append('zero')
		op = x[1]
		x[0] = x[0].replace(":","")
		x[1] = x[2]
		x[2] = x[3]
		x[3] = x[4]
		if mode == '2':
			tmp = []
			tmp.append(x[0])
			#print(line)
			t = hex(int(pc,16) + int(line)*4)
			tmp.append(t)
			label.append(tmp)
			#print(label)
			#print(line)
			#print(x[0])
		return line
	elif x[0] == 'move':
		x[0] = 'add'
		op = x[0]
		x.append('zero')
		return line
	else:
		print("Invalid operation.")
		exit()
def assemble_input(instruction, mode,line,label,btable):
	global imm
	x = instruction.replace(","," ")
	sep = '#'
	x = x.rsplit(sep,1)[0]
#	print(x)
	x = x.replace("$"," ")
	x = x.replace("("," ")
	x = x.replace(")"," ")
	x = x.replace(":"," ")
	x = x.replace("–","-")
	x = x.split()
	
	if x == []:
		line = int(line) - 1
		return 'None'
	
	if len(x) < 2:
		print("Enter a valid instruction")
		return 'None'

	if x[0] in operation_table:
		op = x[0]
	elif x[1] in operation_table:
		if x[1] in ['move']:
			x[1] = 'add'
			op = x[1]
			x.append('zero')
		op = x[1]
		x[0] = x[0].replace(":","")
		x[1] = x[2]
		x[2] = x[3]
		x[3] = x[4]

	elif x[0] == 'move':
		x[0] = 'add'
		op = x[0]
		x.append('zero')

	else:
		print("Invalid operation.")
		exit()

	opcod = format(int(operation_table[op]['opcode'],16),'06b')

	if operation_table[op]['type'] == 'Rtype':
		if op in ['sll','srl','sra']:
			#print ('Shift function')
			rs = format(0,'05b')
			rt = format(int(register_table[x[2]],16),'05b')
			rd = format(int(register_table[x[1]],16),'05b')
			#print(int(x[3]))
			shamt = format(int(x[3]),'05b')
		elif op == 'jr':
			rs = format(int(register_table[x[1]],16),'05b')
			rd = format(0,'05b')
			rt = format(0,'05b')
			shamt = format(0,'05b')

		else:
			rd = format(int(register_table[x[1]],16),'05b')
			rs = format(int(register_table[x[2]],16),'05b')
			rt = format(int(register_table[x[3]],16),'05b')
			shamt = format(0,'05b')
		funct = format(int(operation_table[op]['funct'],16),'06b')
		final_string = opcod + rs + rt + rd + shamt + funct
		return format(int(final_string,2),'08x')
		

	elif operation_table[op]['type'] == 'Itype':
		
		if op not in ['lw','sw','beq','bgez','bne']:

			#print('Itype instruction')
			imm = int(x[3])
			#print(imm)
			imm = sign_extend(imm,16)
			#print (imm)
			rs = format(int(register_table[x[2]],16),'05b')
			rt = format(int(register_table[x[1]],16),'05b')
		elif op not in ['beq','bgez','bne']:
			#print("Lw or Sw operation")
			imm = int(x[2])
			imm = sign_extend(imm,16)
			rt = format(int(register_table[x[1]],16),'05b')
			rs = format(int(register_table[x[3]],16),'05b')
		else:
			#print("Branch operation")
			if mode == '2':
				for i in label:
					if x[3] == i[0]:
						imm = int(i[1],16)
				brloc = int(btable.pop(0)[1],16)
				#print(btable)
				imm = imm - brloc
				imm = imm // 4
				imm = sign_extend(imm,16)

			else:
				imm = int(x[3])
				imm = sign_extend(imm,16)
			rs = format(int(register_table[x[1]],16),'05b')
			rt = format(int(register_table[x[2]],16),'05b')
		final_string = opcod + rs + rt + imm
		return format(int(final_string,2),'08x')
		
	else:
		#print('Jtype instruction')
		if mode == '1':
			imm = int(x[1])
			imm = sign_extend(imm,26)
		else:
			for i in label:
					if x[1] == i[0]:
						imm = int(i[1],16)
						imm = sign_extend(imm,32)
						imm = (imm[4:])
						imm = (imm[:26])
					#	imm = format(int((bin(imm)[2:]),2),'26b')
		final_string = opcod + imm
		return format(int(final_string,2),'08x')
		
def main():
	global line
	print("\n			-=-=-=-=-=MIPS ASSEMBLER=-=-=-=-=-\n")
	#print(operation_table['add']['opcode'])
	print("If you want to use Graphical User Interface, use: 'python Gui.py'\n\n")
	print("[1]Interactive Mode")
	print("[2]Batch Mode")
	mode = input("Please Choose a Mode: ")
	while mode not in ['1','2']:
		if mode in ['quit','Quit']:
			exit()
		mode = input("Invalid Input. Choose '1' or '2': ")
	if mode == '1':
		string = input('Please enter an instruction: ')
		while string not in ['quit','Quit']:
			result = assemble_input(string,mode,'0',[],[])
			if result not in ['None']:
				print (result)
			string = input('Please enter an instruction: ')
	elif mode == '2':
		line = '0'
		label = []
		btable = []
		print('Assembling from file\n')
		f1 = open('final.obj','a+')
		pc = '0x80001000'
		fname = input("Specify file name: ")
		f = open(fname,'r')
		#f2 = open('final.obj')
		fl = f.readlines()
		for string in fl:
			line = check_labels(string,mode,pc,line,label,btable)
			#assemble_input(string)
			line = int(line) + 1
		for string in fl:
			result = (assemble_input(string,mode,line,label,btable))
			#print(result)
			if result not in ['None']:
				f1.write(result)
				f1.write('\n')


		f.close()
		f1.close()
		print("File Successfuly assembled into: 'final.obj'")
if __name__ == "__main__":
    main()
