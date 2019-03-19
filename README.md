# RK chat server + client
## Zagon
### chat server
- zaženi server
  - `./chatServer.py` ali `python3 chatServer.py`),
### chat client
- zaženi klient(e)
  - `./chatClient.py` ali `python3 chatClient.py`).

## Uporaba
- če hočeš poslati javno sporočilo, ga vtipkaj v konzolo,
- če hočeš poslati zasebno sporočilo, predenj vtipkaj `@<ime uporabnika>`,
  če hočeš npr. pozdraviti Janeza, vtipkaj `@Janez pozdravljen`,

### primer uporabe
- Profesor:
>  $ ./chatClient.py  
>  Uporabniško ime: profesor  
>  [system] connecting to chat server ...  
>  [system] connected!  
>  [19:44 | RKchat]: Pridružil se nam je uporabnik ŠTUDENT  
>  pozdravljen, študent  
>  [19:44 | ŠTUDENT]: POZDRAVLJENI, GOSPOD PROFESOR (private)  
>  @študent ste pripravljeni na jutrišnji kolokvij?  
>  [19:45 | ŠTUDENT]: SEVEDA SEM (private)  
>  @študent no, vso srečo  
>  [19:46 | ŠTUDENT]: HVALA (private)  
>  [19:46 | ŠTUDENT]: NASVIDENJE (public)  
>  [19:46 | RKchat]: Uporabnik ŠTUDENT je odšel  
>  ^C  

- Študent:
>  $ ./chatClient.py  
>  Uporabniško ime: študent  
>  [system] connecting to chat server ...  
>  [system] connected!  
>  [19:44 | PROFESOR]: POZDRAVLJEN, ŠTUDENT (public)  
>  @profesor pozdravljeni, gospod profesor  
>  [19:45 | PROFESOR]: STE PRIPRAVLJENI NA JUTRIŠNJI KOLOKVIJ? (private)  
>  @profesor seveda sem  
>  [19:46 | PROFESOR]: NO, VSO SREČO (private)  
>  @profesor hvala  
>  nasvidenje  
>  ^C  

## Lastnosti
  - Znak "|" ni dovoljen,
  - vedno se izpiše čas pošiljanja sporočila.

  
