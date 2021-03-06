import plac
from wrappedfst import WrappedFst
from loguru import logger


def readsym(f):
    dct = {}
    for line in open(f):
        w, i = line.split()
        i = int(i)
        dct[w] = i
        dct[i] = w
    return dct


def main(inlex, isym_f, osym_f, outf):
    logger.info('Not including words with phone count <= 1 or duplicate prons!')
    isym = readsym(isym_f)
    osym = readsym(osym_f)
    fst = WrappedFst()
    start = fst.add_state()
    end = fst.add_state()
    set_prons = set()
    words_skipped = []
    with open(inlex) as fh:
        for line in fh:
            word, *phones = line.split()
            if len(phones) <= 1:
                words_skipped.append(word)
                continue
            if tuple(phones) not in set_prons:
                set_prons.add(tuple(phones))
            else:
                words_skipped.append(word)
                continue
            
            state = start
            for i, phone in enumerate(phones):
                olabel = 0
                if i == 0:
                    olabel = osym[word]
                    new_state = fst.add_state()
                    fst.add_arc(start, new_state, isym[phone + '_B'], olabel, 0.)
                    state = new_state
                elif i == len(phones) - 1:
                    fst.add_arc(state, end, isym[phone + '_E'], 0, 0.)
                else:
                    new_state = fst.add_state()
                    fst.add_arc(state, new_state, isym[phone + '_I'], 0, 0.) 
                    state = new_state
    fst.set_start(start)
    fst.set_final(end)
    fst.write(outf)
    print(words_skipped)
            

plac.call(main)
