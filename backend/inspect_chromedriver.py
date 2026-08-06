from webdriver_manager.chrome import ChromeDriverManager
path = ChromeDriverManager().install()
print(path)
import os
print('exists:', os.path.exists(path))
print('isfile:', os.path.isfile(path))
print('size:', os.path.getsize(path))
print('ext:', os.path.splitext(path)[1])
