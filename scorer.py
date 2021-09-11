import argparse
import json

def run_evaluation(args):
    verbose = args.v
    with open(args.g) as file:
        gold = dict([(d['ID'], {'acronyms':d['acronyms'],'long-forms':d['long-forms']}) for d in json.load(file)])
    with open(args.p) as file:
        pred = dict([(d['ID'], {'acronyms':d['acronyms'],'long-forms':d['long-forms']}) for d in json.load(file)])
        pred = [pred[k] for k,v in gold.items()]
        gold = [gold[k] for k,v in gold.items()]
    p, r, f1 = score_phrase_level(gold, pred, verbos=verbose)
    return p, r, f1

def score_phrase_level(key, predictions, verbos=False):
    gold_shorts = set()
    gold_longs = set()
    pred_shorts = set()
    pred_longs = set()

    def find_phrase(seq, shorts, longs):
        for i, data in enumerate(seq):
            for sh in data['acronyms']:
                shorts.add(str(i)+'#'+str(sh[0])+'-'+str(sh[1]))
            for lf in data['long-forms']:
                longs.add(str(i)+'#'+str(lf[0])+'-'+str(lf[1]))

    find_phrase(key, gold_shorts, gold_longs)
    find_phrase(predictions, pred_shorts, pred_longs)

    def find_prec_recall_f1(pred, gold):
        correct = 0
        for phrase in pred:
            if phrase in gold:
                correct += 1
        # print(correct)
        prec = correct / len(pred) if len(pred) > 0 else 1
        recall = correct / len(gold) if len(gold) > 0 else 1
        f1 = 2 * prec * recall / (prec + recall) if prec+recall > 0 else 0
        return prec, recall, f1

    prec_short, recall_short, f1_short = find_prec_recall_f1(pred_shorts, gold_shorts)
    prec_long, recall_long, f1_long = find_prec_recall_f1(pred_longs, gold_longs)
    precision_micro, recall_micro, f1_micro = find_prec_recall_f1(pred_shorts.union(pred_longs), gold_shorts.union(gold_longs))

    precision_macro = (prec_short + prec_long) / 2
    recall_macro = (recall_short + recall_long) / 2
    f1_macro = 2*precision_macro*recall_macro/(precision_macro+recall_macro) if precision_macro+recall_macro > 0 else 0

    if verbos:
        print('Shorts: P: {:.2%}, R: {:.2%}, F1: {:.2%}'.format(prec_short, recall_short, f1_short))
        print('Longs: P: {:.2%}, R: {:.2%}, F1: {:.2%}'.format(prec_long, recall_long, f1_long))
        print('micro scores: P: {:.2%}, R: {:.2%}, F1: {:.2%}'.format(precision_micro, recall_micro, f1_micro))
        print('macro scores: P: {:.2%}, R: {:.2%}, F1: {:.2%}'.format(precision_macro, recall_macro, f1_macro))

    return precision_macro, recall_macro, f1_macro


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', type=str,
                        help='Gold file path')
    parser.add_argument('-p', type=str,
                        help='Prediction file path')
    parser.add_argument('-v', dest='v',
                        default=False, action='store_true',
                        help="Verbose Evaluation")


    args = parser.parse_args()
    p, r, f1 = run_evaluation(args)
    print('Official Scores:')
    print('P: {:.2%}, R: {:.2%}, F1: {:.2%}'.format(p,r,f1))