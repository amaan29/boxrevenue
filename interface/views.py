from django.shortcuts import render
from BORevenuePred import *
# Create your views here.

def base(request):
    return render(request, 'base.html')

def response(request):
    mname = request.GET.get('mname')
    dist = request.GET.get('dist')
    theatres = request.GET.get('theatres')
    rating = request.GET.get('mpaa')
    rel = request.GET.get('rel')
    action = request.GET.get('Action')
    adv = request.GET.get('Adventure')
    anim = request.GET.get('Animation')
    bio = request.GET.get('Biography')
    com = request.GET.get('Comedy')
    crim = request.GET.get('Crime')
    doc = request.GET.get('Documentary')
    drama = request.GET.get('Drama')
    fam = request.GET.get('Family')
    fantasy = request.GET.get('Fantasy')
    fic = request.GET.get('Fiction')
    hist = request.GET.get('History')
    horror = request.GET.get('Horror')
    music = request.GET.get('Music')
    mystery = request.GET.get('Mystery')
    rom = request.GET.get('Romance')
    scifi = request.GET.get('Sci-Fi')
    thrill = request.GET.get('Thriller')
    
    gens = [action, adv, anim, bio, com, crim, doc, drama, fam,
            fantasy, fic, hist, horror, music, mystery, rom, scifi, thrill]

    theatres = np.log10(int(theatres))
    rel = np.log10(int(rel))

    flag = 0
    for i in range(18):
        if gens[i] == None:
            gens[i] = 0
        else:
            gens[i] = 1
            flag = 1

    if flag == 0:
        return render(request, 'base.html', {'genre' : 0})

    distTr = le1.inverse_transform(df['distributor'])
    np.append(distTr, dist)
    distTr = le1.fit_transform(distTr)
    dist = distTr[-1]

    rTr = le2.inverse_transform(df['MPAA'])
    np.append(rTr, rating)
    rTr = le2.fit_transform(rTr)
    rating = rTr[-1]

    predVals = [[dist, theatres, rating, rel, gens[0], gens[1], gens[2], gens[3], gens[4], gens[5], gens[6], gens[7], gens[8],
                 gens[9], gens[10], gens[11], gens[12], gens[13], gens[14], gens[15], gens[16], gens[17]]]

    revenue = int(model.predict(predVals)[0] * (10**8))


    return render(request,'response.html', {'revenue' : revenue, 'mname' : mname.capitalize})
