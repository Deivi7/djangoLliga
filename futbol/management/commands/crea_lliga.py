from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint
 
from futbol.models import *
 
faker = Faker(["es_CA","es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
        
        data_inici = faker.date_between(start_date='-1y', end_date='today')
        data_fi = data_inici + timedelta(days=randint(90, 180))  # 3 a 6 meses de duración
 
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga( nom=titol_lliga, temporada="temporada", data_inici=data_inici, data_fi=data_fi )
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            fundacio = randint(1880, 2020)
            equip = Equip(ciutat=ciutat,nom=nom, fundacio=fundacio)
            #print(equip)
            equip.save()
            lliga.equips.add(equip)
 
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.name()
                posicio = "jugador"
                dorsal = randint(1, 99)
                data_naixement = faker.date_between(start_date='-40y', end_date='-16y')
                jugador = Jugador(nom=nom,posicio=posicio,
                    data_naixement=data_naixement,equip=equip,dorsal=dorsal)
                #print(jugador)
                jugador.save()
 
        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local!=visitant:
                    partit = Partit(local=local,visitant=visitant)
                    partit.local = local
                    partit.data = faker.date_between(start_date='-1y', end_date='today')
                    partit.visitant = visitant
                    partit.lliga = lliga
                    partit.save()