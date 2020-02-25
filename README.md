# zdock 批处理脚本

本脚本是 zdock 的批处理脚本(Linux)，通过对应的参数去执行 zdock 的程序。

1. Python3 开发

2. zdock3.0.2_linux_x64

3. 测试环境

   操作系统：Linux Mint 19.3 Cinnamon

   Linux 内核：5.0.0-32-generic

   处理器：Intel© Core™ i3-3120M CPU @ 2.50GHz × 2

## 说明

### 参数选项：

-help 帮助信息

-version 脚本版本

-mode 0 默认值，对 pdb 执行 mark_sur, zdock, create.pl 三步。                

​				1 只对 pdb 执行 mark_sur 这一步。

​				2 只对 pdb 执行 zdock 这一步，但需要指定输入文件是 mark_sur 处理后的文件

​				3 只对 pdb 执行 create.pl 这一步，但需要指定输入文件是 zdock 处理后的文件。

-input filepath file 是可以是单个 pdb 文件的路径，若只有文件名默认为当前目录，也可以是 pdb 的文件夹（多个 pdb 批处理）。

-output path 输出文件指定路径，在不指定输出路径的情况下默认当前路径。

-multiProcessMode n 开启n个进程的多线程池，n=0为默认值不开启多线程

-ligand filepath 指定配体，可以是单个文件的路径，也可以是多个文件的文件夹路径，有几个 ligand 输出多个结果。

### 项目结构：

--zdock_script

 --command/ zdock 软件原来的程序

 --zdock.py 批处理脚本

 --README.md 脚本说明

### 针对脚本的一些说明：

1. 当 mode=0 时，中间文件会默认输出到指定输出的路径下的 mark_sur_pdb、zdock_pdb 下。

2. output 的几种情况：

   eg1: /home/mcn

   eg2: /home/mcn/dd/

   首先判断路径是否存在。若存在，则为输出文件的输出路径(eg1)。若不存在，在那个路径新建文件夹作为输出文件的路径(eg2)

3. 脚本支持分步执行 zdock 的三个步骤，但要注意现阶段脚本的的第二步 zdock 只能接受第一步输出的文件夹结构，第三步 create_pl 也接受第二步输出的文件夹结构。如果想把其他不是这个脚本生成的文件用这个脚本运行，请将输入文件夹的格式改成这个样子。

   mark_sur 的输出：

   -outputdir 输出文件夹

   --pdbfile 输出的 pdb 文件

   zdock 的输出：

   -outputdir 输出文件夹

   --pdbnamedir 一个 pdb 的不同 ligand 都装入这个文件夹

   ---pdb-ligand-file 以 pdb 名称加 ligand 为输出文件的名称

4. 在 pdb 只有一个，ligand 也只有一个的情况，就算是指定了参数多进程是不会开启的。

### 实例：

#### 1.我有一个 pdb 和一个配体，想直接三步全执行生成最后结果。【已测试】

```python
python3 zdock.py  -input  ./example/H25N7.29.pdb  -ligand  ./ligand/Ag74_m.pdb  -output ./result
```

#### 2.我有多个 pdb，但只有一个配体的情况下，想直接三步全执行生成最后结果。

开多进程模式【已测试】

```python
python3 zdock.py  -input  ./example  -ligand  ./ligand/Ag74_m.pdb  -output ./result   -multiProcessMode 5
```

不开多进程模式【已测试】

```python
python3 zdock.py  -input  ./example  -ligand  ./ligand/Ag74_m.pdb  -output ./result
```

#### 3.我有一个 pdb，有多个配体，直接三步全执行生成最后结果。

开多进程模式【已测试】

```python
python3 zdock.py  -input  ./example/H25N7.29.pdb  -ligand  ./ligand  -output ./result  -multiProcessMode 5
```

不开多进程模式【已测试】

```python
python3 zdock.py  -input  ./example/H25N7.29.pdb  -ligand  ./ligand  -output ./result
```

#### 4.我有一个或一堆 pdb,只想执行 mark_sur

一个 pdb【已测试】

```python
python3 zdock.py -mode 1  -input ./example/H25N7.29.pdb -output ./mark_sur
```

多个 pdb【已测试】

```python
python3 zdock.py -mode 1  -input ./example/ -output ./mark_sur
```

多个 pdb，多进程模式【已测试】

```python
python3 zdock.py -mode 1  -input ./example/ -output ./mark_sur -multiProcessMode 5
```

#### 5.我有一个或一堆 pdb_m, 只想执行 zdock

一个 pdb_m，一个配体【已测试】

```python
python3 zdock.py -mode 2  -input ./mark_sur/H25N7.29_m.pdb -output ./zdock_pdb -ligand ./ligand/Ag74_m.pdb
```

一个 pdb_m，多个配体【已测试】

```python
python3 zdock.py -mode 2  -input ./mark_sur/H25N7.29_m.pdb -output ./zdock_pdb -ligand ./ligand
```

一个 pdb_m，多个配体，多进程模式【已测试】

```python
python3 zdock.py -mode 2  -input ./mark_sur/H25N7.29_m.pdb -output ./zdock_pdb -ligand ./ligand -multiProcessMode 5
```

多个 pdb_m，一个配体【已测试】

```python
python3 zdock.py -mode 2  -input ./mark_sur -output ./zdock_pdb -ligand ./ligand/Ag74_m.pdb
```

多个 pdb_m，一个配体，多进程模式【已测试】

```python
python3 zdock.py -mode 2  -input ./mark_sur -output ./zdock_pdb -ligand ./ligand/Ag74_m.pdb -multiProcessMode 5
```

多个 pdb_m，多个配体 【已测试】

```python
python3 zdock.py -mode 2  -input ./mark_sur -output ./zdock_pdb -ligand ./ligand
```

多个 pdb_m，多个配体 ,多进程模式【已测试】

```python
python3 zdock.py -mode 2  -input ./mark_sur -output ./zdock_pdb -ligand ./ligand -multiProcessMode 5
```

#### 6.我有一个或一堆 pdb_m.out, 只想执行 create_pl

一个 pdb_m.out【已测试】

```python
python3 zdock.py -mode 3  -input ./zdock_pdb/H25N7.29/H25N7.29_m_Ag74.out -output ./create_pl_pdb
```

多个 pdb_m.out【已测试】

```python
python3 zdock.py -mode 3  -input ./zdock_pdb/ -output ./create_pl_pdb
```

多个 pdb_m.out，多进程模式【已测试】

```python
python3 zdock.py -mode 3  -input ./zdock_pdb/ -output ./create_pl_pdb -multiProcessMode 5
```