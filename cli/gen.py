# os.makedirs('folder/subfolder/')

# import io
#
# with io.FileIO("foobar.txt", "w") as file:
#     file.write("Hello!")

class Generator():
    def __init__(self):
        raise NotImplemented

    def gen_service(self):
        return NotImplemented


# f= open("guru99.txt","w+")
# f=open("guru99.txt", "a+")



class ServiceSpec():
    def __init__(self):
        self.content = {}

class SpecInput():
    def __init__(self, name, default_value=None, choices=None, help=''):
        raise NotImplemented

# Templates
# =====================================================================================================================>

interface_template = "@interface\ndef %s_%s(info):\n    raise NotImplementedError"