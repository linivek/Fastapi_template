# 定义一个变量，方便后续修改 Poetry 命令
POETRY = poetry run

# 定义一个格式化代码的目标
# 这个目标会运行 Black 和 Isort 来格式化和排序代码
format:
	@echo "Running Black to format code..."
	$(POETRY) black .
	@echo "Running Isort to sort imports..."
	$(POETRY) isort .
	@echo "Code formatting and import sorting complete."

# .PHONY 声明 'format' 是一个伪目标，即使存在同名文件也会执行
.PHONY: format
