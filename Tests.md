# Tests

Je donne ci-dessous des exemples d'entrées sorties, pour tester le système, dans différents langages.

Je veux montrer à chaque fois des exemples :

- numériques (pour montrer que l'on peut s'en servir comme d'une petite calculatrice) ;
- montrant un élément de syntaxe spécifique au langage (`dict`/`set`/`list`/`tuple` en compréhension en Python, `type`/`match with`/`let rec` en OCaml, `fonction`/`pointeur` en C) ;
- montrer que l'on peut importer un module ou une bibliothèque.

Bonus :

- montrer que le système gère bien les stderr et les exceptions ?
- TODO: montrer que l'on peut afficher proprement le code de retour 0 / 1 / autre ?
- montrer que le système exécute bien le code en isolement de la machine : pas capable de lire (ou écrire) quoique ce soit, de supprimer un fichier, et d'utiliser Internet.

## Lancer ou automatiser ces tests ?

Les tests sont définis dans le dossier [json_tests](./json_tests/).

Ces tests sont automatisés avec le super [Makefile](./Makefile) intégré :
```bash
$ make test_python
$ make test_ocaml
$ make test_c
```

TODO: automatically build the `fileNUM.ext` and `fileNUM.json` from this file?

## En Python

> Les tests sont définis dans le dossier [json_tests](./json_tests/python/).

- numériques (pour montrer que l'on peut s'en servir comme d'une petite calculatrice) ;

```python
In[1]: print(0.1+0.1+0.1)
Out[1]: 0.30000000000000004
```

- montrant un élément de syntaxe spécifique au langage (`dict`/`set`/`list`/`tuple` en compréhension en Python, `type`/`match with`/`let rec` en OCaml, `fonction`/`pointeur` en C) ;

```python
In[2]: sum(max(i**k-j**(k+1) for i in range(2**k) for j in range(3**k)) for k in [3,4,5,6,7,8])
Out[2]: 17878636286225238456
```

- montrer que l'on peut importer un module ou une bibliothèque :

```python
In[3]: import math; print(math.exp(math.pi)**3 + math.cos(math.sin(1)))
Out[3]: 12392.314174662086
```

```python
In[4]: import os; print(f"os.getcwd()={os.getcwd()}")
Out[4]: os.getcwd()=/home/lilian/publis/Peut-on-coder-avec-OCaml-Python-and-C-par-SMS.git
```

- montrer que le système gère bien les stderr et les exceptions ?

```python
In[5]: print(f"2021/0 = {2021/0}")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```

```python
In[6]: print("This is fine."); assert(0.1+0.1+0.1 == 0.3)
This is fine.
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

- montrer que le système exécute bien le code en isolement de la machine : pas capable de lire (ou écrire) quoique ce soit, de supprimer un fichier, et d'utiliser Internet.

```python
In[7]: file=open("/etc/passwd", "r"); print("".join(file.readlines()))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '/etc/passwd'
```

```python
In[8]: path="test.txt"; file=open(path, "w"); print("Test to write to a file from Python: succeed, now file is gone", file=file, flush=True); file=open(path, "r"); print("".join(file.readlines())); import os; os.remove(path)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: 'test.txt'
```

```python
In[9]: import re; from urllib.request import urlopen; html="".join(l.decode() for l in urlopen("http://monip.org/").readlines()); ip=re.search("[0-9]+.[0-9]+.[0-9]+.[0-9]+", html).group(0); print(f"Your IP address is: {ip}")
Out[9]: 1.2.3.4
```

## En OCaml

> Les tests sont définis dans le dossier [json_tests](./json_tests/ocaml/).

TODO: WARNING: camisole uses `ocamlopt` and not `ocaml` toplevel!

- numériques (pour montrer que l'on peut s'en servir comme d'une petite calculatrice) ;

```ocaml
# print_endline (string_of_bool ((0.1 +. 0.1 +. 0.1) = 0.3));;
false
- : unit = ()
```

- montrant un élément de syntaxe spécifique au langage (`dict`/`set`/`list`/`tuple` en compréhension en Python, `type`/`match with`/`let rec` en OCaml, `fonction`/`pointeur` en C) ;

```ocaml
# type 'a btree = Leaf of 'a | Node of ('a btree * 'a btree);; let rec sum (tree : int btree) = match tree with | Leaf i -> i | Node(left, right) -> (sum left) + (sum right);; sum( Node(Leaf 10, Node(Leaf 20, Leaf 30)) );;
- : int = 60
```

```ocaml
# let rec fibo n = match n with | 0 -> 0 | 1 -> 1 | n -> (fibo (n-1)) + (fibo (n-2)) in fibo 30;;
- : int = 832040
```

- montrer que l'on peut importer un module ou une bibliothèque :

```ocaml
# let range n = Array.init n (fun i -> i) in List.fold_left (+) 0 (Array.to_list (range 100));;
- : int = 4950
```

- montrer que le système gère bien les stderr et les exceptions ?

```ocaml
# 1 / 0;;
Exception: Division_by_zero.
```

```ocaml
# print_endline "This is fine."; 1 / 0;;
This is fine.
Exception: Division_by_zero.
```

- montrer que le système exécute bien le code en isolement de la machine : pas capable de lire (ou écrire) quoique ce soit, de supprimer un fichier, et d'utiliser Internet.

```ocaml
# Sys.command("cat /etc/passwd");;
cat: /etc/passwd: No such file or directory
- : int = 1
```

TODO: convert these code to *not* use `Sys.command` but pure OCaml API.

```ocaml
# Sys.command("echo 'Test to write to a file from OCaml: succeed, now file is gone' > test.txt ; cat test.txt ; rm -vf test.txt");;
Test to write to a file from OCaml: succeed, now file is gone
removed 'test.txt'
- : int = 0
```

```ocaml
# Sys.command("wget --quiet http://monip.org/ -O - | html2text | grep -o 'IP : .*'")
IP : 1.2.3.4
- : int = 0
```

## En C

> Les tests sont définis dans le dossier [json_tests](./json_tests/c/).

TODO:

---

## Et autres ?

Comme ce système utilise [Camisole](https://camisole.prologin.org/), je pourrais tester tous les langages supportés :

> Ada, C, C#, C++, D, Go, Haskell, Java, Javascript, Lua, OCaml, PHP, Pascal, Perl, Prolog, Python, Ruby, Rust, Scheme.

Sur ma machine, je pourrai tester Lua, Java, Javascript et Rust.
