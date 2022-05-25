from modelos import Pagina
from app import db

import datetime as dt

paginaFavoritaUm = Pagina(nome='paginaFavoritaUm',
            caminho='',
            favorito=True,
            id_usuario=2, 
            data_criacao=dt.datetime.today(),
            # excluir_em,
            )

paginaComumUm = Pagina(nome='paginaComumUm',
            caminho='',
            favorito=False,
            id_usuario=2, 
            data_criacao=dt.datetime.today(),
            # excluir_em,
            )

paginaComumDois = Pagina(nome='paginaComumDois',
            caminho='',
            favorito=False,
            id_usuario=2, 
            data_criacao=dt.datetime.today(),
            # excluir_em,
            )

db.session.add(paginaFavoritaUm)
db.session.add(paginaComumUm)
db.session.add(paginaComumDois)
db.session.commit()