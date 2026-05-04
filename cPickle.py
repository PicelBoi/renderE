import pickle as p

def load(f, *args, **kwargs):
    if f.mode == "r":
        f2 = open(f.name, "rb")
        data = p.load(f2, *args, **kwargs)
        f2.close()
        return data
    else:
        return p.load(f, *args, **kwargs)

dump = p.dump