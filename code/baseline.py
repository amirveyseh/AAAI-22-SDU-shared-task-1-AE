import argparse
import json

def predict(data):
    predictions = []
    for d in data:
        pred = {
            'ID': d['ID'],
            'acronyms': [],
            'long-forms': []
        }
        tokens = d['text'].split()
        for i, t in enumerate(tokens):
            t2 = t.replace('(','').replace(')','')
            if len(t2) > 0:
                if t2[0].isupper() and len([c for c in t2 if c.isupper()])/len(t2) > 0.6 and 2 <= len(t2) <= 10:
                    pred['acronyms'].append([sum([len(w)+1 for w in tokens[:i]]),sum([len(w)+1 for w in tokens[:i]])+len(t)])
                    if t.startswith('(') and t.endswith(')'):
                        uppers = []
                        for c in t:
                            if c.isupper():
                                uppers.append(c)
                        candids = tokens[i-len(uppers):i]
                        match = True
                        for j, candid in enumerate(candids):
                            if candid[0].lower() != uppers[j].lower():
                                match = False
                        if match:
                            pred['long-forms'].append([sum([len(w)+1 for w in tokens[:i-len(uppers)]]),sum([len(w)+1 for w in tokens[:i-1]])+len(tokens[i-1])])
        predictions.append(pred)
    return predictions

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', type=str,
                        help='Path the the input file (e.g., dev.json)')
    parser.add_argument('-output', type=str,
                        help='Prediction file path')
    args = parser.parse_args()

    ## READ data
    with open(args.input) as file:
        data = json.load(file)

    ## Predict
    predictions = predict(data)

    ## Save
    with open(args.output, 'w') as file:
        json.dump(predictions, file)