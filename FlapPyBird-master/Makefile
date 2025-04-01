# 默认目标，运行主程序
default:
	@make run

# 运行主程序
run:
	python main.py

# 使用pygbag构建Web版本
web:
	pygbag main.py

# 构建Web版本
web-build:
	pygbag --build main.py

# 初始化项目，安装依赖
init:
	@pip install -U pip; \
	pip install -e ".[dev]"; \
	pre-commit install; \

# 安装pre-commit钩子
pre-commit:
	pre-commit install

# 对所有文件运行pre-commit检查
pre-commit-all:
	pre-commit run --all-files

# 格式化代码
format:
	black .

# 运行代码检查
lint:
	flake8 --config=../.flake8 --output-file=./coverage/flake8-report --format=default
