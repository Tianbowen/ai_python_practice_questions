# ai_python_practice_questions

# python初始化项目

```bush
# 安装 uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# cd到项目目录 创建项目
uv init quetions
cd quetions
# 安装核心依赖 (ipykernel 让 vscode 能识别环境， notebook)
uv add --dev ipykernel notebook

# 为当前目录注册一个永久的 jupyter 内核(关键一步)
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=quetions-kernel

# vscode 打开目录，右上角选择内核，jupyter kernel，选择 quetions-kernel


```

