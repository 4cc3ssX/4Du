import hashlib,os,sys,re,time

r = '\033[031m'
g = '\033[032m'
b = '\033[036m'
y = '\033[033m'
n = '\033[00m'

FILES = {}
DUPLICATED = {}

def main(PATH):
	global FILES,DUPLICATED
	content = os.listdir(PATH)
	if content:
		for j in content:
			if os.path.isfile(PATH+j):
				f_original = open(PATH+j, 'rb')
				FILES[hashlib.md5(f_original.read()).hexdigest()] = j
				f_original.close()
		for i in content:
			if os.path.isfile(PATH+i):
				f = open(PATH+i, 'rb')
				md5 = hashlib.md5(f.read()).hexdigest()
				f.close()
				if md5 in FILES.keys() and FILES[md5] != i:
					DUPLICATED[md5] = FILES[md5]+">"+ i
		return True
	else:
		return False
def result(PATH):
	file = time.strftime("%H%M%S")+".out"
	f = open(file, 'w+')
	for d in DUPLICATED:
		f.write(PATH+DUPLICATED[d].split('>')[0]+"\n")
	return file
if __name__ == '__main__':
	p = input("[!] Enter path to scan ~> ")
	if os.path.isdir(p):
		if not re.match(r"^.*\/$", p):
			p+='/'
		if main(p):
			if DUPLICATED:
				print("-"*os.get_terminal_size()[0])
				for h in DUPLICATED:
					du = DUPLICATED[h].split('>')
					print(f"{h} @ {b}{du[0]}{n} -> {r}{du[1]}{n}")
				print("-"*os.get_terminal_size()[0])
				print(f"[{r}!{n}] {y}{len(DUPLICATED)}{n} duplicated file(s) are detected!")
				out_f = result(p)
				print(f"[{g}+{n}] Output saved to {g}{out_f}{n}")
				con = input(f"[{r}!{n}] Duplicated file(s) will be {y}DELETED{n}. {r}Yes{n} (or) {g}No{n} [Y/n]? ")
				if con.lower() == 'y' or con.lower() == 'yes':
					f = open(out_f, 'r')
					for l in f.readlines():
						os.remove(l.strip())
					f.close()
					print(f"[{g}*{n}] All have been deleted!")
				else:
					sys.exit(0)
			else:
				print(f"[{r}!{n}] No duplicated file(s) found!")
		else:
			print(f'[{r}!{n}] Empty directory!')
			sys.exit(0)
	else:
		print(f"[{r}!{n}] Not Found or Trying to access file.")
		sys.exit(0)