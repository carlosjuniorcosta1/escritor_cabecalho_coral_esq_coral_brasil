

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 21:33:29 2021

@author: carlo
"""

import pandas as pd 
import re

def limpa_coral(texto):
    import re 
    texto = re.sub(r'(\*\w{3}\:)?(\[\d+\])?|\[?\/\d+\]?|\+|/|/{2}|=?i?\s?\-?\w{3}_?r?s?n?=\s?\$?', '', texto)
    texto = texto.replace('hhh', '').replace('yyyy', '')\
    .replace('yyy', '').replace('xxx', '').replace('<', '')\
    .replace('>','').replace('?', '').replace('=', '').replace('[', '').replace(']', '')
    
    texto = re.sub(r'&\w+', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto   

regex_headers_tuples = r'(\w+|\w+’\w+’|\w+’\w+|\w+’)\s\((\w+.*?)\)'
          
regex_excep= r"([A-Za-z]+’)([A-Za-z]+)" #para separar \w+’\w+
regex_excep2 = r'(\w+’)\s(\w+’)' #para juntar palavras c dois apóstrofos
regex_excep3 = r'(\w+’)(\w+’)' #para separar as palavras c dois apóstrofos
regex_apostr = r"(\w+’(?!\n))\s(\w+(?!\n))" #para juntar \w’ com \w+
regex_remove_participants = r"(@.+,?(?=.\(.+\))\s+\(.+\)\n.+\n\s+.+\n.+\n\s+.+\n\s+.+(?!@))|(@.+,?(?=.\(.+\))\s+\(.+\)\n.+\n\s+.+\n.+\n\s+.+(?!@).+)|(@.+,?(?=.\(.+\))\s+\(.+\)\n.+\n\s+.+\n(?!@).+)|(@.+,?(?=.\(.+\))\s+\(.+\)\n.+\n\s+(?!@).+)|(@.+,?(?=.\(.+\))\s+\(.+\)\n.+s+(?!@).+)"

file_1 = str(input('Type the filename you want to extract from: '))
file_2 = str(input("Type the header's filename - txt - UTF-8: "))
file_3 = str(input("Patient/participant's name you want to count words - example: NAM ")) 

with open(file_1, 'r+', encoding='utf-8') as source:
    text_tr = source.read()
    text_tr = text_tr.replace("'", "’")
    text_tr_df = pd.DataFrame(text_tr.splitlines())
    text_tr_df = pd.DataFrame([text_tr_df[0].apply(limpa_coral).str.strip()]).transpose()
    text_tr = '\n'.join(text_tr_df[0].tolist())
    text_tr = re.sub(regex_apostr, r"\1\2", text_tr)

with open(file_1, 'r+', encoding='utf-8') as source:
    palavras_totais = source.read()
    palavras_totais = palavras_totais.replace("'", "’")
    palavras_totais = [x for x in palavras_totais.splitlines()]
    palavras_paciente = len(limpa_coral(('\n'.join([x for x in palavras_totais if x[1:4] == file_3]))).split())
    palavras_totais = len(limpa_coral(('\n'.join([x for x in palavras_totais ]))).split())
                     
formas_afereticas = """
babacar (embabacar), brigado (obrigado), brigada (obrigada), baixa (abaixa), credita (acredita), creditei (acreditei), creditou (acreditou) , baixar (abaixar), baixei (abaixei), baulado (abaulado), bora (embora), borrecido (aborrecido), brigada (obrigada), brigado (obrigado), caba (acaba), cabar (acabar), cabava (acabava), cabei (acabei), cabou (acabou), celera (acelera), celerando (acelerando), certar (acertar), chei (achei), cho (acho), contece (acontece), contecer (acontecer), conteceu (aconteceu), cordava (acordava), creditei (acreditei), dianta (adianta), doro (adoro), dotada (adotada), fessora (professora), final (afinal), fundar (afundar), garrado (agarrados), garrou (agarrou), gora (agora), gual (igual), gualzim (igualzinho), guenta (aguenta), guentando (aguentando), guentar (aguentar), guento (aguento), guentou (aguentou), inda (ainda), judar (ajudar), lambique (alambique), laranjado (alaranjado), lisou (alisou), magina (imagina), mamentar (amamentar), manhã (amanhã), marelo (amarelo), marrava (amarrava), migão (amigão aumentativo), mor (amor), ném (neném), panhava (apanhava), parece (aparece), pareceu (apareceu), partamento (apartamento), pelido (apelido),  perta (aperta), pertar (apertar), pertei (apertei), pesar (apesar), pinhada (apinhada), pois (depois), posa (raposa), proveita (aproveita), proveitei (aproveitei), proveitou (aproveitou),  proveitando (aproveitando), proveitei (aproveitei), purra (empurra), qui (daqui), rancaram (arrancaram), rancava (arrancava), rancou (arrancou), ranjar (arranjar), ranjasse (arranjasse), ranjou (arranjou), rebentando (arrebentando), rebentar (arrebentar), regaço (arregaços), rorosa (horrorosa), roz (arroz), rumaram (arrumaram), sobiando (assobiando),té (até), té (até), teirinho (inteirinho), teja (esteja), tendeu (entendeu), tendi (entendi), testino (intestino), tradinha (entradinha), trapalha (atrapalha), trapalhado (atrapalhado), trapalhou (atrapalhou), travessa (atravessa), travessadinho (atravessadinho), trevida (atrevida), trevido (atrevido), trevidão (atrevidão), vó (avó), vô (avô)""" 

formas_afereticas = formas_afereticas.replace("'", "’").replace(";", ",")
formas_afereticas = re.sub(regex_apostr, r"\1\2", formas_afereticas)
tuplas_afereticas = re.findall(regex_headers_tuples, formas_afereticas)
dict_afereticas1 = dict(tuplas_afereticas)
    
lista_compartilhada_af1 = []
for palavra_tr in text_tr.split():
    for chave, valor in dict_afereticas1.items():
        if palavra_tr == chave:
            lista_compartilhada_af1.append((chave, valor))
    
text_tr = re.sub(regex_excep, r"\1 \2", text_tr)
text_tr = re.sub(regex_excep2, r"\1\2", text_tr) 

formas_afereticas = re.sub(regex_excep, r"\1 \2", formas_afereticas)
formas_afereticas = re.sub(regex_excep2, r"\1\2", formas_afereticas)
tuplas_afereticas2 = re.findall(regex_headers_tuples, formas_afereticas)
dict_afereticas2 = dict(tuplas_afereticas2)            
                
lista_compartilhada_af2 = []
for palavra_tr in text_tr.split():
    for chave, valor in dict_afereticas2.items():
        if palavra_tr == chave:
            lista_compartilhada_af2.append((chave, valor))
                
formas_conv = """
a’ (olha), acabamo (acabamos), achamo (achamos), agradecemo (agradecemos), a’ lá (olha), a’ (olha), a’ (olha), aprendemo (aprendemos), arrumamo (arrumamos), assinávamo (assinávamos), atravessamo (atravessamos), avi (vi), avinha (vinha), bebemo (bebemos), beijamo (beijamos), botemo (botamos), chegamo (chegamos), cheguemo (chegamos), choramo (choramos), colocamo (colocamos), começamo (começamos), comemo (comemos), comemoramo (comemoramos), compramo (compramos), conhecemo (conhecemos), conseguimo (conseguimos), contamo (contamos), conversamo (conversamos), corremo (corremos), cortamo (cortamos), deixamo (deixamos), descansamo (descansamos), descemo (descemos), devemo (devemos), empurramo (empurramos), encontramo (encontramos), entramo (entramos), envem (vem), envinha (vinha), escolhemo (escolhemos), esquecemo (esquecemos), estamo (estamos), estudemo (estudamos), evem (vem), falamo (falamos), fazido (feito), ficamo (ficamos), fize (fiz), fizemo (fizemos), fomo (fomos), for (formos), fraga (flagra), fragando (flagrando), frago (flagro), fumo (fomos), ganhamo (ganhamos), levamo (levamos), levantamo (levantamos), levantemo (levantamos), mandamo (mandamos), manti (mantive), o’ (olha), o’(olha), paramo (paramos), passamo (passamos), pedimo (pedimos), peguemo (pegamos), perdemo (perdemos), pinchando (pichando), pintemo (pintemos), podemo (podemos), precisamo (precisamos), pusemo (pusemos), resolvemo (resolvemos), saímo (saímos), seje (seja), sentamo (sentamos), sentemo (sentamos), separamo (separamos), somo (somos), sufro (sofro), temo (temos), tiramo (tiramos), tivemo (tivemos), tomamo (tomamos), trabalhamo (trabalhamos), trago (trazido), vesse (visse), viemo (viemos), vimo (vimos), tó (toma), cê (você), cês (vocês), e’ (ele), ea (ela), eas (elas), es (eles), ocê (você), ocês (vocês), aque’ (aquele), aquea (aquela), aqueas (aquelas), aques (aqueles), ca (com a), co (com o), cos (com os), cum (com um), cuma (com uma), d’ (de) d’(de), d’(de), d’(de), dum (de um), duma (de uma), dumas (de umas), duns (de uns), n’ deerreí (na DRI), ni (em), n’ (onde), num (em um), numa (em uma), numas (em umas), pa (para), pas (para as), p’(para), p’(para), p’(para), p’(para), p’(para), p’(para), p’(para), po (para o), p’(para), pos (para os), p’(para), pra (para), pr’(para), pras (para as), pro (para o), pr’(para), pros (para os), prum (para um), pruma (para uma), pruns (para uns), p’(para), p’ (para), p’(para), pum (para um), puma (para uma), c’ aqueas (com aquelas), c’(com), c’ cê (com você), c’ e’ (com ele), c’ (com), c’(com essas), c’(com), c’ ocê (com você), c’ ocês (com vocês), daque’ (daquele), daquea (daquela), daqueas (daquelas), daques (daqueles), d’ cê (de você), de’ (dele), dea (dela), d’(de), d’(de), d’(de), des (deles), d’ es (de eles), d’(de), d’ ocê (de você), d’ ocês (de vocês), naque’ (naquele), naquea (naquela), naques (naqueles), ne’ (nele), n’ ocê (em você), n’ ocês (em vocês), p’ aque’ (para aquele), p’(para), p’ cê (para você), p’ cês (para vocês), p’ e’ (para ele), p’(para), p’ (para), p’(para), p’ es (para eles), p’ esse (para esse), p’ mim (para mim), p’ ocê (para você), p’ ocês (para vocês), pr’(para), pr’(para), pr’ ea (para ela), pr’(para), pr’(para), pr’ ocê (para você), pr’ ocês (para vocês), p’ sio’ (para a senhora), p’ siora (para a senhora), p’(para), armoçar (almoçar), artinho (altinho), arto (alto), arto (alto), comprica (complica), compricar (complicar), cravícula (clavícula), escardada (escaldada), prano (plano), pranta (planta), pray (play), prissado (plissado), probremas (problemas), sortando (soltando), sortar (soltar), sortei (soltei), sorto (solto), sortou (soltou), vorta (volta), vortar (voltar), vortava (voltava), vorto (volto), n’é (não é), n’(não), nũ (não), canarim (canarinho), espim (espinho), n’ é (não é), padrim (padrinho), passarim (passarinho), porco-espim (porco-espinho), sozim (sozinho), almoçozim (almoçozinho), amarelim (amarelinho), azulzim (azulzinho), bebezim (bebezinho), bichim (bichinho), bocadim (bocadinho), bonitim (bonitinho), cachorrim (cachorrinho), cantim (cantinho), capoeirim (capoeirinhas), carrim (carrinho), cedezinho (CD), certim (certinho), certins (certinhos), Chapeuzim Vermelho (Chapeuzinho Vermelho), chazim (chazinho), controladim (controladinha), desfiadim (desfiadinho), direitim (direitinho), direitim (direitinho), esquisitim (esquisitinho), fechadim (fechadinho), filhotim (filhotinho), formulariozim (formulariozinho), fundim (fundinho), Geraldim (Geraldinho), golezim (golezinho), igualzim (igualzinho), instantim (instantinho), jeitim (jeitinho), Joãozim (Joãozinho), joguim (joguinho), ladim (ladinho), maciim (maciinho), mansim (mansinho), Marquim (Marquinho), meninim (menininho), morenim (moreninho), murim (murinho), Paulim (Paulinho), pequeninim (pequenininha), pertim (pertinho), negocim (negocinhos), partidim (partidinho), porquim (porquinho), portim (portinha), potim (potinho), pouquim (pouquinho), pozim (pozinho), pretim (pretinho), prontim (prontinho), quadradim (quadradinha), quadradim (quadradinho), queimadim (queimadinho), rapidim (rapidinho), recheadim (recheadinho), rolim (rolinho), tamanim (tamaninho), tampadim (tampadinho), terrenim (terreninho), tiquim (tiquinho), todim (todinho), toquim (toquinho), trancadim (trancadinhos), trenzim (trenzinho), tudim (tudinho), sio’ (senhora), sior (senhor), siora (senhora), sô (senhor), mó (muito), po’ (pode) ,tá (está) ,tamo (estamos) ,tamos (estamos) ,tão (estão) ,tar (estar) ,taria (estaria) ,tás (estás) ,tava (estava) ,tavam (estavam) ,távamos (estávamos) ,tavas (estavas) ,teja (esteja) ,tem (tenho) ,teve (esteve) ,tive (estive) ,tiver (estiver) ,tiverem (estiverem) ,tivesse (estivesse) ,tô (estou) ,vamo (vamos) ,vão (vamos) ,vim (vir) ,xá (deixa), antiguim (antiguinho), banhozim (banhozinho), branquim (branquinho), certim (certinho), 
devagarzim (devagarzinho), direitim (direitinho), direitim (direitinho), gostosim (gostosinho), limãozim (limãozinho), minutim (minutinho), pertim (pertinho), pulim (pulinho), pouquim (pouquinho), rapidim (rapidinho), recibim (recibinho), verdim (verdinho), xixizim (xixizinho), zerim (zerinho)
"""
text_tr = re.sub(regex_excep3, r'\1 \2', text_tr ) 
text_tr = re.sub(regex_apostr, r"\1\2", text_tr) 
#onomatopeias = """
#tanana, bla bla bla 
formas_conv = formas_conv.replace("'", "’").replace(";", ",")
formas_conv = re.sub(regex_apostr, r"\1\2", formas_conv)
tuplas_conv = re.findall(regex_headers_tuples, formas_conv)
dict_conv1 = dict(tuplas_conv)
    
lista_compartilhada_conv1 = []
for palavra_tr in text_tr.split():
    for chave, valor in dict_conv1.items():
        if palavra_tr == chave:
            lista_compartilhada_conv1.append((chave, valor))
    
text_tr = re.sub(regex_excep, r"\1 \2", text_tr)
text_tr = re.sub(regex_excep3, r'\1\2', text_tr)
text_tr = re.sub(regex_apostr, r'\1\2', text_tr)

formas_conv = re.sub(regex_excep, r"\1 \2", formas_conv)
formas_conv = re.sub(regex_excep2, r'\1\2', formas_conv)
formas_conv = re.sub(regex_apostr, r'\1\2', formas_conv)
tuplas_conv2 = re.findall(regex_headers_tuples, formas_conv)
dict_conv2 = dict(tuplas_conv2)            
               
lista_compartilhada_conv2 = []
for palavra_tr in text_tr.split():
    for chave, valor in dict_conv2.items():
        if palavra_tr == chave:
            lista_compartilhada_conv2.append((chave, valor))


with open(file_2, 'r+', encoding='utf-8' ) as source:
    header = source.read()
    text_h = header.replace("'", "’")
    text_h = re.sub(r'\w+\s(?=\(vocativo\)).\w+..', '', text_h)
    text_h = re.sub(r'\w+\s(?=\(interjeição\)).\w+..', '', text_h)
    text_h = re.sub(regex_remove_participants, '', text_h)
    text_h = re.sub(r'(@.+(?!\n.+@))', '', text_h)
    text_tr = re.sub(regex_excep, r'\1 \2', text_tr) 
    text_h = re.sub(regex_apostr, r"\1\2", text_h)
    text_tr = re.sub(regex_apostr, r"\1\2", text_tr)
    tuplas_h1 = re.findall(regex_headers_tuples, text_h)
    
  
    dict_h1 = dict(tuplas_h1)

    lista_compartilhada_h1 = []
    for palavra_tr in text_tr.split():
        for chave, valor in dict_h1.items():
            if palavra_tr == chave:
                lista_compartilhada_h1.append((chave, valor))    
    
    text_tr = re.sub(regex_excep3, r'\1 \2', text_tr) #\w+’\w+’ > \w+’\s\w+’
    text_tr = re.sub(regex_excep, r"\1 \2", text_tr) #\w+’\w+ > \w’\s\w+ #espaçamento original aqui
    text_h = re.sub(regex_excep3, r'\1 \2', text_h)
    text_h = re.sub(regex_excep, r"\1 \2", text_h)
    tuplas_h2 = re.findall(regex_headers_tuples, text_h)

    dict_h2 = dict(tuplas_h2)
    
    lista_compartilhada_h2 = []
    for palavra_tr in text_tr.split():
        for chave, valor in dict_h2.items():
            if palavra_tr == chave:
                lista_compartilhada_h2.append((chave, valor)) 
   
    for x in lista_compartilhada_af2:
        lista_compartilhada_af1.append(x)
        
    for x in lista_compartilhada_conv2:
        lista_compartilhada_conv1.append(x)
   
    for x in lista_compartilhada_h2:
        lista_compartilhada_h1.append(x)

text_h = re.sub(r'Formas\s+?aferéticas:.+|Formas\s+?convencionalizadas:.+|Apheretic\s+?forms:.+|Apheretic\s+?Forms:.+|Conventionalized\s+?forms:.+|Standardized\s+?forms:.+|Standardized\s+?Forms:.+', '', text_h)
text_h_restante = re.sub(r'\d\)\s', '', text_h)
text_h_restante = '\n'.join(re.findall(r'.+', text_h_restante))

dict_afereticas_total = dict(lista_compartilhada_af1)
dict_conv_total = dict(lista_compartilhada_conv1)
dict_h_total = dict(lista_compartilhada_h1)
  
chaves_conv = set(dict_conv_total.items())
chaves_af = set(dict_afereticas_total.items())
chaves_h = set(dict_h_total.items())

conjunto1 = chaves_af.difference(chaves_h)
conjunto2 = chaves_h.difference(chaves_af)
conjunto3= chaves_af.intersection(chaves_h)
conjunto_f = chaves_h - conjunto2
formas_af_totais = dict(conjunto1.union(conjunto_f))

conjunto4 = chaves_conv.difference(chaves_h)
conjunto5 = conjunto2.difference(chaves_conv)
conjunto6 = chaves_conv.intersection(conjunto2)

formas_conv_totais = dict(conjunto4.union(conjunto5).union(conjunto6))
                
with open(file_2, 'r+', encoding='utf-8' ) as source:
    
    header = source.read()
    header = header.replace("'", "’")
    
    header_df = pd.DataFrame()
    header_df['Title'] = ["@Title:" + ' '.join(re.findall(r'(?<=@Title:).+', header))]
    header_df['File'] = "@File:" + ' '.join(re.findall(r'(?<=@File:).+', header))
    header_df['Participants'] = ''.join(str(re.findall(r'(?<=Participants:)(@.+,?(?=.\(.+\))\s+\(.+\)\n.+\n\s+.+\n.+\n\s+.+\n\s+.+(?!@))|(@.+,?(?=.\(.+\))\s+\(.+\)\n.+\n\s+.+\n.+\n\s+.+(?!@).+)|(@.+,?(?=.\(.+\))\s+\(.+\)\n.+\n\s+.+\n(?!@).+)|(@.+,?(?=.\(.+\))\s+\(.+\)\n.+\n\s+(?!@).+)|(@.+,?(?=.\(.+\))\s+\(.+\)\n.+s+(?!@).+)', header)))
    header_tratamento = '\n'.join(header_df['Participants'].tolist())
    header_tratamento = re.sub("\'',\s+|\[\(|,\s\''\)\]|'", '', header_tratamento)
    header_tratamento = re.sub(r'\\n', '\n', header_tratamento)
    header_tratamento = re.sub(r'\\t', '\t', header_tratamento)
    header_df['Participants'] = header_tratamento
    header_df['Participants'] = header_df['Participants'].apply(lambda x: re.sub(r'\)\](?=$)', '', x))
    header_df['Date'] = "@Date:" + ' '.join(re.findall(r'(?<=@Date:).+', header))
    header_df['Place'] = "@Place:" + ' '.join(re.findall(r'(?<=@Place:).+', header))
    header_df['Situation'] = "@Situation:" + ' '.join(re.findall(r'(?<=@Situation:).+', header))
    header_df['Topic'] = "@Topic:" + ' '.join(re.findall(r'(?<=@Topic:).+', header))
    header_df['Source'] = "@Source:" + ' '.join(re.findall(r'(?<=@Source:).+', header))
    header_df['Class'] = "@Class:" + ' '.join(re.findall(r'(?<=@Class:).+', header))
    header_df['Length'] = "@Length:" + ' '.join(re.findall(r'(?<=@Length:).+', header))
    header_df['Words'] = "@Words:" + ' ' + str(palavras_totais)
    header_df['Patient_words'] = "@Patient_words:" + ' ' + str(palavras_paciente)
    header_df['Acoustic_quality'] = "Acoustic_quality: " 
    header_df['Transcriber'] = "@Transcriber:" + ' '.join(re.findall(r'(?<=@Transcriber:).+', header))
    header_df['Revisor'] = "@Revisor:" + ' '.join(re.findall(r'(?<=@Revisor:).+', header))
    header_df['Comments'] = "@Comments:"
    
    header_df.transpose()
    lista_af_final = []
    for k, v in formas_af_totais.items():
        lista_af_final.append(f'{k} ({v}),')
    header_df['Apheretic_forms'] = "Apheretic forms: " + ' '.join(sorted(lista_af_final))
    
    lista_conv_final = []
    for k, v in formas_conv_totais.items():
        lista_conv_final.append(f'{k} ({v}),')

    header_df['Conventionalized_forms'] = "Conventionalized forms: " + ' '.join(sorted(lista_conv_final))
    header_df['Conventionalized_forms'] = header_df['Conventionalized_forms'].apply(lambda x: re.sub(r',(?=$)', ';', x))
    header_df['Conventionalized_forms'] = header_df['Conventionalized_forms'].apply(lambda x: re.sub(regex_excep, r'\1 \2', x))
    header_df['Apheretic_forms'] = header_df['Apheretic_forms'].apply(lambda x: re.sub(r',(?=$)', ';', x))
        
    header_df_derretido = header_df.melt()
    texto_rest_df = pd.DataFrame([text_h_restante.splitlines()]).transpose()
    texto_rest_df.reset_index(inplace = True)
    texto_rest_df.columns = ['variable', 'value']
    texto_rest_df['variable'] = texto_rest_df['variable'].astype('str')
    header_df_derretido = pd.concat([header_df_derretido, texto_rest_df], ignore_index = True)
    header_txt = '\n'.join(header_df_derretido['value'].tolist())
    

    with open(f"{file_2[:-4]}_novo.txt", 'w+', encoding = 'utf-8') as writer:
        file = writer.write(header_txt)
        print('By: Carlos - LEEL \n Let me know if I can help you with something :) \n whatsapp: +55 31 98924 1307 \n email: carlosjuniorcosta1@gmail.com')
