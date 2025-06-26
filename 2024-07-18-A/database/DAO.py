from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def getArchi(ch_min, ch_max):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select DISTINCTROW g1.GeneID as g1id, g1.`Function` as fun1 , g2.GeneID as g2id, c1.Localization, c2.Localization , g2.`Function` as fun2 , g1.Chromosome as ch1, g2.Chromosome as ch2, g1.Essential as es1, g2.Essential as es2, i.Expression_Corr as peso 
                        from genes g1, genes g2, classification c1, classification c2, interactions i 
                        where g2.GeneID <>g1.GeneID
                        and g1.Chromosome >= %s and g1.Chromosome <=%s
                        and g2.Chromosome >= %s and g2.Chromosome <=%s
                        and c1.GeneID = g1.GeneID and c2.GeneID = g2.GeneID
                        and c2.Localization = c1.Localization
                        and ((i.GeneID1 = c1.GeneID AND i.GeneID2 = c2.GeneID) or (i.GeneID1 = c2.GeneID and i.GeneID2 = c1.GeneID))
                        having g1.Chromosome <= g2.Chromosome
                    """
            cursor.execute(query, (ch_min, ch_max, ch_min, ch_max))
            for row in cursor:
                result.append((Gene(row["g1id"], row['fun1'], row['es1'], row['ch1']),
                               Gene(row["g2id"], row['fun2'], row['es2'], row['ch2']) , row["peso"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(ch_min, ch_max):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select *
                        from genes g
                        where g.Chromosome >= %s
                        and g.Chromosome <= %s"""
            cursor.execute(query, (ch_min, ch_max))

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getCromosomi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select distinct g.Chromosome 
                        from genes g """
            cursor.execute(query)

            for row in cursor:
                result.append(row[0])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                       FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result