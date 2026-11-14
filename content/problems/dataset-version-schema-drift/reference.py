import re

def dataset_contract_drift(expected, observed):
    def ident(value,physical=False):
        return type(value) is str and re.fullmatch(r"[a-z][a-z0-9_/-]{0,63}" if physical else r"[a-z][a-z0-9_-]{0,63}",value) is not None
    def validate(snapshot):
        if type(snapshot) is not dict or len(snapshot)>128:raise ValueError("snapshot")
        for dataset,entry in snapshot.items():
            if not ident(dataset) or type(entry) is not dict or set(entry)!={'version','features'} or not ident(entry['version']):raise ValueError("dataset descriptor")
            features=entry['features']
            if type(features) is not dict or not 1<=len(features)<=128:raise ValueError("features")
            for name,desc in features.items():
                if not ident(name) or type(desc) is not tuple or len(desc)!=4:raise ValueError("feature descriptor")
                dtype,shape,unit,frame=desc
                if type(dtype) is not str or dtype not in ('float32','float64','int64','bool'):raise ValueError("dtype")
                if type(shape) is not tuple or len(shape)>4 or any(type(d) is not int or not 1<=d<=10000 for d in shape):raise ValueError("shape")
                if not ident(unit,True) or not ident(frame,True):raise ValueError("unit/frame")
    validate(expected);validate(observed)
    out=[]
    for dataset in expected.keys()|observed.keys():
        if dataset not in expected:out.append((dataset,'','unexpected_dataset'));continue
        if dataset not in observed:out.append((dataset,'','missing_dataset'));continue
        a,b=expected[dataset],observed[dataset]
        if a['version']!=b['version']:out.append((dataset,'','version'))
        af,bf=a['features'],b['features']
        for name in af.keys()|bf.keys():
            if name not in af:out.append((dataset,name,'unexpected_feature'));continue
            if name not in bf:out.append((dataset,name,'missing_feature'));continue
            for index,reason in enumerate(('dtype','shape','unit','frame')):
                if af[name][index]!=bf[name][index]:out.append((dataset,name,reason))
    return sorted(out)
