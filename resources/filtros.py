def normalize_path_params(estado=None,
                     ranking_min=0,
                     ranking_max=5,
                     diaria_min=0,
                     diaria_max=1000,
                     limit=50,
                     offset=0, **dados):
    if estado:
        return {
            "ranking_min": ranking_min,
            "ranking_max": ranking_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "estado": estado,
            "limit": limit,
            "offset": offset}
    return {
        "ranking_min": ranking_min,
        "ranking_max": ranking_max,
        "diaria_min": diaria_min,
        "diaria_max": diaria_max,
        "limit": limit,
        "offset": offset}

# path /hoteis?estado=São Paulo&ranking_min=4.0&diaria_max=600


consulta_sem_cidade = "SELECT * FROM hoteis \
                        WHERE (ranking >= ? and ranking <= ?) \
                        and (diaria >= ? and diaria <= ?) \
                        LIMIT ? OFFSET ?"

consulta_com_cidade = "SELECT * FROM hoteis \
                        WHERE (ranking >= ? and ranking <= ?) \
                        and (diaria >= ? and diaria <= ?) \
                        and (estado = ?) LIMIT ? OFFSET ?"

consulta_media_site = "SELECT sites.site_id, sites.url, COUNT(hoteis.hotel_id) as qntdd_hoteis,ROUND((SUM(hoteis.ranking) * 1.0 / COUNT(hoteis.hotel_id)), 2) AS media_ranking FROM sites \
                        INNER JOIN hoteis ON hoteis.site_id = sites.site_id \
                        GROUP BY sites.site_id"