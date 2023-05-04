from PySide6.QtCore import QRegularExpression

re = QRegularExpression('0-9')
print(re.pattern())
