# nonebot-plugin-fhl

适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的 飞花令 插件

### 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_fhl
```

- 使用 pip

```
pip install nonebot_plugin_fhl
```

### 配置项

> 以下配置项可在 `.env.*` 文件中设置，具体参考 [NoneBot 配置方式](https://nonebot.dev/docs/appendices/config)

#### `feihualing_api`
 - 类型：`str`
 - 默认：`http://106.54.63.95:8080`
 - 说明：飞花令 API

### 使用

**以下命令需要加[命令前缀](https://nonebot.dev/docs/appendices/config#command-start-和-command-separator) (默认为`/`)，可自行设置为空**

```
@机器人 + /梦笔生花
```

### API 搭建

- 安装 golang

- Clone 源代码

```
git clone https://github.com/lianhong2758/fhlAPI
```

- 编译

  下面两种均可，二选一
```
go build mian.go
```
```
make build
```

- 数据文件

   飞花令需要的数据文件需要存放在`data/`下，提供两张获取方法：

   - 前往 [huggingface](https://huggingface.co/qwerdvd/FeiHuaLing) 下载

   - 自己 `build dataset`，将 `2b-dedup.txt` 放在 `data/` 下，第一次启动的时候会自动 `build dataset`

   **此操作需要的内存大约在10G左右，请自行准备大内存**
   **第一次`build`完成之后请重新启动程序释放内存**

- 启动

```
./main.go
```

- 在 `.env.*` 文件中设置 `api` 地址

### 特别感谢

- [lianhong2758](https://github.com/lianhong2758/fhlAPI) 提供了内置的飞花令api

- [MeetWq](https://github.com/MeetWq) 大佬的 [nonebot-plugin-wordle](https://github.com/noneplugin/nonebot-plugin-wordle) 本插件参考了很多实现

