import time

def log(message, module='backend'):
    print(time.strftime("%Y%m%d %H:%M:%S", time.gmtime()), f"[{module}]", message )
