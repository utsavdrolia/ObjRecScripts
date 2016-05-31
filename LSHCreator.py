from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections


def hash(vals, labels):
    proj = 'rbp'
    engine = Engine(len(vals[0]), lshashes=[RandomBinaryProjections(proj, 64)])
    for val, label in zip(vals, labels):
        val = [int(a*255) for a in val]
        print val
        engine.store_vector(val, data=label)
    dic = engine.storage.get_all_buckets(proj)