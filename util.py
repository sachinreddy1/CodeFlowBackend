import base64

class Util:
    def decodeBase64(encodedString):
        decoded_bytes = base64.b64decode(encodedString)
        decoded_string = decoded_bytes.decode('iso-8859-1')
        return decoded_string
    
    def isValidFileType(path):
        validFileTypes = ["py", "js", "kt", "java", "yml", ".production"]

        if ('.' in path):
            s = path.split('.')
            if s[-1] in validFileTypes:
                return True
        return False