# OO_hw5 评测机源码仓库

## 使用说明

### 参数和启动

使用 `python main.py [OPTION]...` 启动评测机

可选的参数：

- `-h` 或 `--help`   
  输出帮助信息

- `-m` 或 `--multiprocess`
  使用多线程进行评测

- `-s` 或 `--single`
  使用单线程进行评测

- `-n` 或 `--nointeract`
  关闭交互（缺省默认开启），关闭后将不会在控制台进行输出，但错误信息依旧会保存在 ./errors 目录下。
  同时会在运行目录下生成 matcher.log 文件提供运行状态的说明。

默认的参数是：`-s`

### 输出说明

生成的运行状态将会形如 `---->   epoch <test_case>   ---   wrong: <wrong>   ---   tle: <tle>   <----`

其中 test_case 是当前评测的数据数量；wrong 是评测出错的输出数量，包括 RTLE；tle 是输出检查程序出错的次数，也就是 checker 错误的次数，正常情况下应该是 0。

生成的错误数据将会存放在 ./errors 文件夹下，文件名格式为 `<date>@<time>@<name>.log`，其中 date 是生成日期，time 是生成时刻，name 是被测用户的 jar 包名字。

### 注意事项

下载好之后，请注意在本地新建 errors 文件夹，否则无法保存错误数据。

## 代码说明

### <p>main.py</p>

读取目录下的 jar 包并分配控制台参数，控制使用多线程、单线程评测和交互控制参数的传递。请不要改动。

### <p>jar_files_search.py</p>

搜索目录下的 jar 包并返回文件名列表。interact 参数负责控制输出。请不要改动。

### <p>multiprocess.py</p>

多线程评测的文件，入口函数为 `multi_process(jar_files, interact)`。interact 参数负责控制输出。

### <p>singleprocess.py</p>

单线程评测的文件，入口函数为 `single_process(jar_files, interact)`。interact 参数负责控制输出。

### <p>generate.py</p>

生成数据。

### <p>evaluate.py</p>

评测数据。入口函数 `evaluate(origin, name)`，将会调用 run_java.py 下的 `execute_java_with_program(name, input_program)` 获取返回值。

其中 origin 是输入的测试数据（str 类型），name 是待测用户的名字（不含 .jar 后缀），input_program 是输入程序的地址，通过下面这段代码控制。

```python
if (os.name == 'nt'):
    program_path = '.\\tools\\datainput_student_win64.exe'
else:
    program_path = './tools/datainput_student_linux_x86_64'
```

然后调用 checker() 并返回。

### <p>error.py</p>

负责输出错误。其中函数 `error_output(name, error_type, input, output, error_info)` 负责输出错误到 ./errors 文件夹下的对应文件。

参数解释：

- name：待测用户的名字
- error_type：错误类型，将会在文件头显示，如 `Format Error`
- input：输入数据，str 类型
- output：用户输出，str 类型，无法获取请设置为空
- error_info：详细评测输出

输出的文件名格式为 `<date>@<time>@<name>.log`。

### <p>run_java.py</p>

执行 jar 包。有两个函数 `execute_java(stdin, name)` 和 `execute_java_with_program(name, input_program)`。

- `execute_java(stdin, name)`
  不会通过程序喂入数据。输入的数据为 stdin（str 类型），执行命令 `java -jar ./<name>.jar`。
- `execute_java_with_program(name, input_program)`
  通过程序 `<input_program>` 喂入数据，等价于执行命令 `<input_program> | java -jar ./<name>.jar`

### 其他说明

编写输出代码时必须使用 interact 参数控制是否允许输出到控制台（True 为允许输出）。

设置输出字体的颜色、背景和样式必须使用 `from colorama import Fore, Back, Style`。

请使用 error&#x200B;.py 输出错误信息到文件，使用 run_java.py 运行 jar 包。也可以考虑使用 .bat 或者 .sh 文件运行 jar 包。（请在 run_java.py 种编写对应代码）。

请在 README&#x200B;.md（或者代码中）编写代码说明。