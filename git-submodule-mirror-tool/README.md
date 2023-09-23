# git-submodule-mirror-tool

## 介绍

开发项目时引用github等需要代理访问的仓库，但数量一多就难管理，尤其是子模块自身有子模块的情况。
该脚本可以方便管理子模块的镜像，能一键推送子模块到镜像站、将镜像URL应用到``.gitmodules`文件中。

脚本设计初衷是为了解决CI环境中不方便使用代理的问题。

## 使用方法

1. 开启目标镜像站的`push-to-create`特性，push即创建仓库

以gitea为例，详见[gitea文档](https://docs.gitea.com/administration/config-cheat-sheet#repository-repository)，修改配置文件:

```
[repository]
ENABLE_PUSH_CREATE_ORG=true
ENABLE_PUSH_CREATE_USER=true
DEFAULT_PUSH_CREATE_PRIVATE=false
```

2. 编辑`git-mirror.py`，修改镜像站地址

```
MIRROR_SITE_SSH = "ssh://git@example.com/%s.git"
MIRROR_SITE_HTTP = "http://example.com/%s"
```

3. 生成子模块列表至`submodule-mirrors.txt`

```
$ ./git-mirror.py show > submodule-mirrors.txt
lib/CGame++/lib/ccronexpr|https://github.com/staticlibs/ccronexpr.git
lib/CGame++/lib/rapidyaml|https://github.com/noodlefighter/rapidyaml.git
lib/CGame++/lib/rapidyaml/ext/c4core|https://github.com/biojppm/c4core
lib/CGame++/lib/rapidyaml/ext/c4core/cmake|https://github.com/biojppm/cmake
lib/CGame++/lib/rapidyaml/ext/c4core/src/c4/ext/debugbreak|https://github.com/biojppm/debugbreak
lib/CGame++/lib/rapidyaml/ext/c4core/src/c4/ext/fast_float|https://github.com/fastfloat/fast_float

```

4. 编辑`submodule-mirrors.txt`

根据需要选择保留需要镜像的子模块，并填写镜像的提交路径，如：

```
lib/CGame++/lib/rapidyaml|https://github.com/noodlefighter/rapidyaml.git|mirror/rapidyaml
lib/CGame++/lib/rapidyaml/ext/c4core|https://github.com/biojppm/c4core
lib/CGame++/lib/rapidyaml/ext/c4core/cmake|https://github.com/biojppm/cmake
```

5. 运行脚本push镜像到指定的镜像站

```
$ ./git-mirror.py push
```

6. 通过镜像拉取子模块

脚本会逐层写入镜像站地址，并执行`git submodule update`

```
$ ./git-mirror.py update-submodules
```

## 配置文件格式说明

```
<submodule_path>|<source_url>|<mirror_name>[|<submodule_name>]
```

### submodule_path

子模块相对于当前git仓库的路径

### source_url

子模块的原始URL

### mirror_name

镜象名，用于生成镜像url，如设置为abc，对应镜像url为"http://example.com/abc"

### submodule_name

（可选）子模块名

当.gitmodules文件中的子模块名和路径不同时使用，下面一例子模块名是`extern/c4core`，与路径`ext/c4core`不同：

```
[submodule "extern/c4core"]
	path = ext/c4core
	url = http://abc.com/c4core
```


