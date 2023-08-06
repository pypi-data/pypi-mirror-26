from hashlib import sha256
import hashlib
import random
import base58
from gec.groups import EllipticCurveGroup, CyclicGroup, JacobianGroup
from gec.fields import FiniteField

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
ripemd160 = hashlib.new('ripemd160')


class FiniteFieldBTC(FiniteField):
    P = 2**256 - 2**32 - 977


class EllipticCurveGroupBTC(EllipticCurveGroup):
    A = 0
    B = 7


class JacobianGroupBTC(JacobianGroup):
    A = 0
    B = 7


Gx = FiniteFieldBTC(
    0X79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798)
Gy = FiniteFieldBTC(
    0X483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
G = EllipticCurveGroupBTC((Gx, Gy))


class EllipticCurveCyclicSubgroupBTC(CyclicGroup):
    G = G
    N = N


def gen_random_number():
    return random.randint(1, N)


def gen_priv_key(key, version=128, compress=1):
    private_key = bytes([version]) + key.to_bytes(
        32, byteorder='big') + bytes([compress])
    auth = sha256(sha256(private_key).digest()).digest()[:4]
    res = private_key + auth
    assert len(res) == 1 + 32 + 1 + 4
    return base58.b58encode(res)


def gen_pub_key(key):
    pub = G @ EllipticCurveCyclicSubgroupBTC(key)
    n = hex(pub.value[0].value).replace('0x', '')
    return '0' + str(2 + (pub.value[1].value % 2)) + ((64 - len(n)) * '0' + n)


def gen_key_pair(key=gen_random_number()):
    return gen_priv_key(key), gen_pub_key(key)


def gen_address(key):
    pub = G @ EllipticCurveCyclicSubgroupBTC(key)
    x, y = pub.value[0].value, pub.value[1].value
    if y % 2 == 0:
        prefix = bytes([0x02])
    else:
        prefix = bytes([0x03])
    networkid = bytes([0x00])
    ripemd160.update(
        sha256(
            prefix + x.to_bytes(32, byteorder='big')
        ).digest()
    )
    hashed = ripemd160.digest()
    assert len(hashed) == 20
    with_network = networkid + hashed
    auth = sha256(sha256(with_network).digest()).digest()[:4]
    res = with_network + auth
    assert len(res) == 25
    return base58.b58encode(res)
