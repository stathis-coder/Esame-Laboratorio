class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    #funzione che istanzia l'oggetto sul nome 
    def __init__(self,name):
        self.name=name

    #funzione che permette di prendere i dati del file
    def get_data(self):
        #creo una lista vuota che conterrà le liste annidate
        data_list= []
        #controllo che esista veramente un file che si possa aprire
        try:
            my_file=open(self.name,'r')

        except:
            raise ExamException('Error: No such file was found, please try again')
            
        #ciclo su tutto il file    
        for i, line in enumerate(my_file):

            #separo gli elementi del fie sulla virgola (separo gli epoch dalle temperature)
            elements = line.split(',')

            #escludo la prima riga(escludo i titoli delle colonne)
            if elements[0] != 'epoch':
                
                
                #controllo che l'input di epoch sia convertibile in interi
                try: 
                    #converto gli epoch in interi
                    elements[0]=int(elements[0])
                except:
                    #salto la riga
                    continue
            

                #controllo che l'input di temperature sia convertibile in float
                try:
                    #converto le temperature in floating point
                    elements[1]=float(elements[1])
                except:
                    #salto la riga
                    continue
               
                
                #appendo le epoch e le temperature in un lista che a sua volta verra appesa alla super lista "data_list"
                data_list.append([elements[0], elements[1]])

        #prima di ritornare la data_list ciclo su tutta la lista per confermare che le epoch siano ordinate
        for i, line in enumerate(data_list):
            #se sono al primo elemento
            if i==0:
                #passo al successivo
                continue
            #se non sono al primo elemento
            if i>0:
                #se una epoch e minore della sua precedente
                if data_list[i][0]<=data_list[i-1][0]:
                    #alzo l'eccezzione (utilizzo "i" e "i+1" invece che "i-1" e "i" per segnare la posizione perche l'utente vede solo il file data e non la lista data_list cosi facendo salto i titoli delle colonne e l'utente puo trovare l'eccezione piu facilmente)
                    raise ExamException('Error: all epochs must be ordered cronologically, epoch',data_list[i][0],' in position',i,' is greater then epoch',data_list[i][0],' in position',i+1,'please try again with a file with cronoligcally ordered epochs')    

        #ritorno la super lista
        return data_list
#funzione che analizza i dati e ritorna media, minimo e massimo delle temperture di un giorno
def daily_stats(data_list):
    #creo una lista vuota dove salvero le stesse temperature ma con epoch calibrati sull'inizio della giornata
    day_start_list=[]
    
    #creo la lista risultato dove salvero il minimo, massimo, e media di temperature giornaliere
    result_list=[]

    #ciclo su tutta data_list
    for i, line in enumerate(data_list):
        #se sono all'ultimo elemento della lista
        if i==len(data_list)-1:
            #ne aggiungo uno in piu per interrompere corettamente il ciclo nella riga 83
            day_start_list.append([data_list[0][0],data_list[0][1]])
        #utilizzando l'operazione di modulo riesco a calcolare l'inizio di ogni giorno in epoch e lo salvo insieme alla temperatura corrispondente
        day_start_list.append([(data_list[i][0]-(data_list[i][0]%86400)),data_list[i][1]])
   
    
    #creo una lista dove salvero le temperature con lo stesso epoch
    same_day_list=[]

    #ciclo su tutto
    for i, line in enumerate(day_start_list):
        #se sono al primo elemento della lista
        if i==0:
            #appendo la temperatura alla lista delle temperature giornaliere
            same_day_list.append(day_start_list[i][1])
        if i > 0 and i<len(day_start_list)-1:
            
            #se l'epoch è uguale al suo precedente
            if day_start_list[i][0]==day_start_list[i-1][0]:
                #appendo la temperatura che corrisponde all'epoch precedente alla lista sam_day_list
                same_day_list.append(day_start_list[i][1])

            #se l'epoch è diverso dal suo precedente 
            if day_start_list[i][0]!=day_start_list[i-1][0]:

                #appendo alla lista "result" il minimo, e il massimo calcolato sulla lista di temperature e anche la media calcolata facendo la somma di tutta la lista / la lunghezza della lista
                result_list.append([min(same_day_list),max(same_day_list),(sum(same_day_list)/len(same_day_list))])

                #svuoto la lista in modo da poter passare al prossimo giorno
                same_day_list=[]
    
    #ritorno la lista risultato
    return result_list

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
lista=daily_stats(time_series)
print(len(lista))
print(lista)


